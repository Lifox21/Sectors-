"""Shared causal regime detection and ranking helpers for the trading system."""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM


HMM_FEATURE_COLUMNS = ["Smoothed_Returns", "Log_Vol", "AR1_Residual"]
RANKING_REQUIRED_COLUMNS = {"Global Rank", "Symbol", "Combined Score", "Sector"}


def causal_smoothing(series: pd.Series, window: int = 2) -> pd.Series:
    """Return a trailing mean; no observation uses a future price."""
    if window <= 1:
        return series.astype(float)
    return series.astype(float).rolling(window=window, min_periods=window).mean()


def ar1_residuals(values: np.ndarray) -> np.ndarray:
    """Fit AR(1) on returns available at each observation and return residuals."""
    returns = np.diff(values)
    residuals = np.zeros(len(values), dtype=float)
    if len(returns) < 3:
        residuals[1:] = returns
        return residuals

    y = returns[1:]
    x = returns[:-1]
    design = np.column_stack([np.ones_like(x), x])
    intercept, coefficient = np.linalg.lstsq(design, y, rcond=None)[0]
    residuals[1] = returns[0] - intercept
    residuals[2:] = returns[1:] - (intercept + coefficient * returns[:-1])
    return residuals


def build_hmm_features(df_sector: pd.DataFrame, smoothing_window: int = 2) -> pd.DataFrame:
    """Build clean, chronologically sorted features from a sector close-price series."""
    required = {"Date", "Close"}
    missing = required.difference(df_sector.columns)
    if missing:
        raise ValueError(f"Sector data is missing required columns: {sorted(missing)}")

    df = df_sector[["Date", "Close"]].copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna().sort_values("Date").drop_duplicates("Date", keep="last")
    df = df[df["Close"] > 0].reset_index(drop=True)

    df["Close_smoothed"] = causal_smoothing(df["Close"], smoothing_window)
    df["Smoothed_Returns"] = np.log(df["Close_smoothed"] / df["Close_smoothed"].shift(1))
    volatility = df["Smoothed_Returns"].rolling(window=10, min_periods=10).std()
    df["Log_Vol"] = np.log(volatility + 1e-8)
    df = df.dropna().reset_index(drop=True)
    df["AR1_Residual"] = ar1_residuals(df["Close_smoothed"].to_numpy())
    return df


def _fit_hmm(features: np.ndarray, max_iter: int = 200) -> GaussianHMM:
    model = GaussianHMM(
        n_components=3,
        covariance_type="diag",
        n_iter=max_iter,
        tol=1e-4,
        min_covar=1e-4,
        random_state=42,
    )
    model.fit(features)
    return model


def _state_mapping(model: GaussianHMM, scaled_features: np.ndarray, returns: np.ndarray) -> dict[int, int]:
    """Map raw HMM labels to bullish=0, neutral=1, bearish=2 by expected return."""
    posterior = model.predict_proba(scaled_features)
    weights = posterior.sum(axis=0)
    state_returns = np.divide(
        posterior.T @ returns,
        weights,
        out=np.full(3, -np.inf),
        where=weights > 1e-8,
    )
    ordered_raw_states = np.argsort(state_returns)
    return {
        int(ordered_raw_states[2]): 0,
        int(ordered_raw_states[1]): 1,
        int(ordered_raw_states[0]): 2,
    }


def evaluate_hmm_regime(
    df_sector: pd.DataFrame,
    target_idx: int | None = None,
    target_date: str | pd.Timestamp | None = None,
    smoothing_window: int = 2,
    min_history: int = 252,
    training_window: int = 756,
    min_bullish_probability: float = 0.55,
    return_details: bool = False,
):
    """Evaluate the latest available causal HMM regime at a date or row index.

    The last posterior is a filtering result: it uses data through the target only.
    A finite rolling training window lets the regime parameters adapt to market changes.
    """
    raw = df_sector.copy()
    raw["Date"] = pd.to_datetime(raw["Date"], errors="coerce")
    raw = raw.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    if target_date is not None:
        cutoff = pd.Timestamp(target_date)
        raw = raw[raw["Date"] <= cutoff]
    elif target_idx is not None:
        if target_idx < 0:
            raise ValueError("target_idx must be non-negative")
        raw = raw.iloc[: target_idx + 1]

    features = build_hmm_features(raw, smoothing_window)
    if len(features) < min_history:
        details = {"state": 1, "probabilities": [0.0, 1.0, 0.0], "reason": "insufficient_history"}
        return details if return_details else details["state"]

    train = features.tail(training_window).reset_index(drop=True)
    values = train[HMM_FEATURE_COLUMNS].to_numpy(dtype=float)
    mean = values.mean(axis=0)
    std = values.std(axis=0)
    scaled = (values - mean) / np.maximum(std, 1e-8)

    try:
        model = _fit_hmm(scaled)
        mapping = _state_mapping(model, scaled, train["Smoothed_Returns"].to_numpy())
        raw_probabilities = model.predict_proba(scaled)[-1]
    except (ValueError, FloatingPointError):
        details = {"state": 1, "probabilities": [0.0, 1.0, 0.0], "reason": "model_fit_failed"}
        return details if return_details else details["state"]

    probabilities = np.zeros(3, dtype=float)
    for raw_state, regime_state in mapping.items():
        probabilities[regime_state] = raw_probabilities[raw_state]

    state = int(np.argmax(probabilities))
    if state == 0 and probabilities[0] < min_bullish_probability:
        state = 1

    details = {
        "state": state,
        "probabilities": probabilities.tolist(),
        "as_of_date": train["Date"].iloc[-1].strftime("%Y-%m-%d"),
        "reason": "ok",
    }
    return details if return_details else details["state"]


def fit_hmm_for_walk_forward(scaled_features: np.ndarray, returns: np.ndarray):
    """Fit a model and return its raw-to-regime mapping for causal backtests."""
    model = _fit_hmm(scaled_features, max_iter=30)
    return model, _state_mapping(model, scaled_features, returns)


def filter_hmm_observations(
    model: GaussianHMM,
    prior_posterior: np.ndarray,
    observations: np.ndarray,
    mapping: dict[int, int],
) -> tuple[list[int], list[list[float]]]:
    """Filter observations sequentially, without Viterbi smoothing over future rows."""
    log_likelihoods = model._compute_log_likelihood(observations)
    posterior = prior_posterior.copy()
    regimes: list[int] = []
    probabilities: list[list[float]] = []

    for log_likelihood in log_likelihoods:
        prior = posterior @ model.transmat_
        stable_likelihood = np.exp(log_likelihood - np.max(log_likelihood))
        posterior = prior * stable_likelihood
        posterior /= posterior.sum()

        ordered = np.zeros(3, dtype=float)
        for raw_state, regime_state in mapping.items():
            ordered[regime_state] = posterior[raw_state]
        regimes.append(int(np.argmax(ordered)))
        probabilities.append(ordered.tolist())

    return regimes, probabilities


def load_rankings(ranking_path: str) -> pd.DataFrame:
    """Load and validate the fundamental ranking source before it drives trades."""
    ranking = pd.read_csv(ranking_path)
    missing = RANKING_REQUIRED_COLUMNS.difference(ranking.columns)
    if missing:
        raise ValueError(f"Ranking file is missing required columns: {sorted(missing)}")

    ranking = ranking.copy()
    ranking["Symbol"] = ranking["Symbol"].astype(str).str.strip()
    ranking["Sector"] = ranking["Sector"].astype(str).str.strip()
    ranking["Global Rank"] = pd.to_numeric(ranking["Global Rank"], errors="coerce")
    ranking["Combined Score"] = pd.to_numeric(ranking["Combined Score"], errors="coerce")
    ranking = ranking.dropna(subset=["Symbol", "Sector", "Global Rank", "Combined Score"])
    ranking = ranking[ranking["Symbol"] != ""]

    if ranking["Symbol"].duplicated().any():
        duplicates = ranking.loc[ranking["Symbol"].duplicated(), "Symbol"].tolist()
        raise ValueError(f"Ranking file has duplicate symbols: {duplicates[:5]}")
    if ranking["Global Rank"].duplicated().any():
        raise ValueError("Ranking file has duplicate Global Rank values")
    return ranking


def _stock_metrics(file_path: str, as_of_date: pd.Timestamp) -> tuple[float, float, float, float, str] | None:
    if not os.path.exists(file_path):
        return None
    prices = pd.read_csv(file_path, usecols=["Date", "Close"])
    prices["Date"] = pd.to_datetime(prices["Date"], errors="coerce")
    prices["Close"] = pd.to_numeric(prices["Close"], errors="coerce")
    prices = prices.dropna().sort_values("Date")
    prices = prices[(prices["Date"] <= as_of_date) & (prices["Close"] > 0)]
    if len(prices) < 64:
        return None

    close = prices["Close"].to_numpy(dtype=float)

    def return_over(days: int) -> float:
        if len(close) <= days:
            return np.nan
        return close[-1] / close[-days - 1] - 1.0

    daily_returns = np.diff(np.log(close[-64:]))
    return (
        return_over(21),
        return_over(63),
        return_over(252),
        float(np.std(daily_returns, ddof=1) * np.sqrt(252)),
        prices["Date"].iloc[-1].strftime("%Y-%m-%d"),
    )


def ranked_candidates(
    ranking: pd.DataFrame,
    active_sectors: list[str],
    stocks_dir: str,
    as_of_date: str | pd.Timestamp,
    max_price_age_days: int = 7,
) -> pd.DataFrame:
    """Combine the static fundamental score with causal local-price momentum."""
    as_of = pd.Timestamp(as_of_date)
    candidates = ranking[ranking["Sector"].isin(active_sectors)].copy()
    rows = []
    for index, row in candidates.iterrows():
        metrics = _stock_metrics(os.path.join(stocks_dir, f"{row['Symbol']}_daily.csv"), as_of)
        if metrics is None:
            continue
        ret_21, ret_63, ret_252, volatility, price_date = metrics
        rows.append((index, ret_21, ret_63, ret_252, volatility, price_date))

    if not rows:
        return candidates.iloc[0:0].copy()

    metrics_df = pd.DataFrame(
        rows,
        columns=["_index", "Return 21D", "Return 63D", "Return 252D", "Volatility 63D", "Price Date"],
    ).set_index("_index")
    candidates = candidates.join(metrics_df, how="inner")
    momentum = candidates[["Return 21D", "Return 63D", "Return 252D"]].rank(pct=True).mean(axis=1) * 100.0
    low_volatility = (1.0 - candidates["Volatility 63D"].rank(pct=True)) * 100.0
    candidates["Technical Score"] = 0.8 * momentum + 0.2 * low_volatility
    candidates["Rank Score"] = 0.7 * candidates["Combined Score"] + 0.3 * candidates["Technical Score"]
    candidates["Ranking As Of"] = as_of.strftime("%Y-%m-%d")
    candidates["Price Age Days"] = (
        as_of.normalize() - pd.to_datetime(candidates["Price Date"])
    ).dt.days
    # Never issue a trade from a stale price history. The daily synchronizer
    # refreshes stock files before calling this function.
    candidates = candidates[candidates["Price Age Days"] <= max_price_age_days]
    return candidates.sort_values(
        ["Rank Score", "Combined Score", "Global Rank", "Symbol"],
        ascending=[False, False, True, True],
    ).reset_index(drop=True)


def apply_sector_caps(
    candidates: pd.DataFrame,
    max_per_sector: int = 1,
    max_positions: int = 5,
) -> pd.DataFrame:
    """Filter top ranked candidates enforcing maximum positions per sector."""
    if candidates.empty:
        return candidates
    selected_indices = []
    sector_counts: dict[str, int] = {}
    for idx, row in candidates.iterrows():
        sec = str(row["Sector"])
        current_count = sector_counts.get(sec, 0)
        if current_count < max_per_sector:
            selected_indices.append(idx)
            sector_counts[sec] = current_count + 1
            if len(selected_indices) >= max_positions:
                break
    return candidates.loc[selected_indices].reset_index(drop=True)


class SwapPolicy:
    """Turnover-damping policy that prevents daily whipsaws and portfolio churn."""

    def __init__(
        self,
        swap_margin: float = 0.15,
        min_holding_days: int = 5,
        stop_loss_pct: float = 0.08,
    ):
        self.swap_margin = swap_margin
        self.min_holding_days = min_holding_days
        self.stop_loss_pct = stop_loss_pct

    def evaluate_portfolio(
        self,
        holdings: dict[str, dict],
        active_sectors: list[str],
        candidate_df: pd.DataFrame,
        current_date_str: str,
        max_positions: int = 5,
        max_per_sector: int = 1,
        live_prices: dict[str, float] | None = None,
    ) -> tuple[list[str], list[str], dict[str, str]]:
        """Determine exits, retentions, and new entries.

        Returns:
            (target_symbols, exits_to_sell, exit_reasons)
        """
        exits: list[str] = []
        exit_reasons: dict[str, str] = {}
        kept_symbols: list[str] = []

        # Map candidate scores and sectors
        candidate_lookup = {}
        for _, row in candidate_df.iterrows():
            sym = str(row["Symbol"])
            candidate_lookup[sym] = {
                "score": float(row.get("Rank Score", row.get("Combined Score", 0.0))),
                "sector": str(row["Sector"]),
            }

        # 1. Evaluate current holdings for mandatory or risk-based exits
        curr_date = pd.to_datetime(current_date_str)
        for sym, data in holdings.items():
            sector = data.get("sector")
            if not sector and sym in candidate_lookup:
                sector = candidate_lookup[sym]["sector"]

            # Trigger 1: Stop-loss breach (if live prices supplied)
            if live_prices and sym in live_prices:
                cur_price = live_prices[sym]
                buy_price = data.get("buy_price", cur_price)
                if buy_price > 0 and (cur_price / buy_price - 1.0) <= -self.stop_loss_pct:
                    exits.append(sym)
                    exit_reasons[sym] = f"stop_loss_triggered (loss <= -{self.stop_loss_pct*100:.1f}%)"
                    continue

            # Trigger 2: Sector dropped out of Bullish HMM state (mandatory exit)
            if sector and sector not in active_sectors:
                exits.append(sym)
                exit_reasons[sym] = f"sector_regime_exit ({sector} no longer Bullish)"
                continue

            # If passed, keep candidate
            kept_symbols.append(sym)

        # 2. Check if open slots or voluntary swaps are possible
        capped_candidates = apply_sector_caps(candidate_df, max_per_sector=max_per_sector, max_positions=max_positions * 2)
        target_symbols = list(kept_symbols)

        # Enforce sector caps on existing held symbols
        held_sector_counts: dict[str, int] = {}
        for sym in kept_symbols:
            sec = holdings[sym].get("sector") or (candidate_lookup.get(sym, {}).get("sector", "unknown"))
            held_sector_counts[sec] = held_sector_counts.get(sec, 0) + 1

        # Fill remaining empty slots up to max_positions
        for _, row in capped_candidates.iterrows():
            sym = str(row["Symbol"])
            sec = str(row["Sector"])
            if sym in target_symbols:
                continue
            if len(target_symbols) >= max_positions:
                break
            if held_sector_counts.get(sec, 0) < max_per_sector:
                target_symbols.append(sym)
                held_sector_counts[sec] = held_sector_counts.get(sec, 0) + 1

        # 3. Evaluate voluntary swaps for full portfolio:
        # A new candidate can only replace a held stock if:
        # - held stock has been held for >= min_holding_days
        # - candidate score > held stock score * (1 + swap_margin)
        for _, row in capped_candidates.iterrows():
            candidate_sym = str(row["Symbol"])
            candidate_sec = str(row["Sector"])
            candidate_score = float(row.get("Rank Score", row.get("Combined Score", 0.0)))
            if candidate_sym in target_symbols:
                continue

            # Find weakest replaceable holding
            worst_held = None
            worst_score = float("inf")
            for held_sym in list(target_symbols):
                entry_date_str = holdings.get(held_sym, {}).get("entry_date", current_date_str)
                days_held = (curr_date - pd.to_datetime(entry_date_str)).days
                if days_held < self.min_holding_days:
                    continue  # Locked holding - minimum dwell time

                held_score = candidate_lookup.get(held_sym, {}).get("score", 0.0)
                if held_score < worst_score:
                    worst_score = held_score
                    worst_held = held_sym

            if worst_held and candidate_score > worst_score * (1.0 + self.swap_margin):
                # Verify sector cap for candidate
                sec_after = held_sector_counts.get(candidate_sec, 0)
                worst_sec = holdings.get(worst_held, {}).get("sector")
                if candidate_sec != worst_sec and sec_after >= max_per_sector:
                    continue

                exits.append(worst_held)
                exit_reasons[worst_held] = f"swap_out (score {worst_score:.2f} < candidate {candidate_score:.2f} +{self.swap_margin*100:.0f}%)"
                target_symbols.remove(worst_held)
                target_symbols.append(candidate_sym)
                if worst_sec and worst_sec in held_sector_counts:
                    held_sector_counts[worst_sec] -= 1
                held_sector_counts[candidate_sec] = held_sector_counts.get(candidate_sec, 0) + 1

        return target_symbols, exits, exit_reasons

