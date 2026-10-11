"""Causal, auditable paper-trading workflow for the sector HMM strategy."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from strategy_core import (
    apply_sector_caps,
    evaluate_hmm_regime,
    load_rankings,
    ranked_candidates,
    SwapPolicy,
)


WORKSPACE_DIR = Path(__file__).resolve().parent
INDICES_DIR = WORKSPACE_DIR / "Indices" / "Daily"
STOCKS_DIR = WORKSPACE_DIR / "Stocks" / "Daily"
SCORED_DIR = WORKSPACE_DIR / "scored_csv"
SCRATCH_DIR = WORKSPACE_DIR / "scratch"
STATE_PATH = SCRATCH_DIR / "paper_portfolio_state.json"
TRADE_LOG_PATH = SCRATCH_DIR / "paper_trade_log.csv"
SNAPSHOT_DIR = SCRATCH_DIR / "paper_snapshots"
DAILY_RANKING_PATH = SCORED_DIR / "daily_ranking.csv"
MONTHLY_REPORT_PATH = SCRATCH_DIR / "monthly_paper_report.csv"
CONFIG_PATH = WORKSPACE_DIR / "paper_trading_config.json"


@dataclass(frozen=True)
class CostModel:
    """Conservative, configurable cash-equity paper-trading cost assumptions."""

    brokerage_bps: float = 0.0
    exchange_transaction_bps: float = 0.30
    sebi_turnover_bps: float = 0.01
    gst_rate: float = 0.18
    stamp_duty_buy_bps: float = 1.50
    stt_sell_bps: float = 10.0
    slippage_bps: float = 10.0

    def estimate_fees(self, side: str, notional: float) -> dict[str, float]:
        brokerage = notional * self.brokerage_bps / 10_000
        exchange = notional * self.exchange_transaction_bps / 10_000
        sebi = notional * self.sebi_turnover_bps / 10_000
        gst = (brokerage + exchange + sebi) * self.gst_rate
        stamp_duty = notional * self.stamp_duty_buy_bps / 10_000 if side == "BUY" else 0.0
        stt = notional * self.stt_sell_bps / 10_000 if side == "SELL" else 0.0
        total = brokerage + exchange + sebi + gst + stamp_duty + stt
        return {
            "brokerage": brokerage,
            "exchange": exchange,
            "sebi": sebi,
            "gst": gst,
            "stamp_duty": stamp_duty,
            "stt": stt,
            "total": total,
        }


DEFAULT_COST_MODEL = CostModel()


def load_config() -> dict:
    defaults = {
        "initial_capital": 150_000.0,
        "max_positions": 5,
        "max_stocks_per_sector": 1,
        "swap_margin": 0.15,
        "min_holding_days": 5,
        "stop_loss_pct": 0.08,
        "poll_interval_seconds": 60,
        "cost_model": asdict(DEFAULT_COST_MODEL),
    }
    if not CONFIG_PATH.exists():
        return defaults
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        configured = json.load(handle)
    defaults.update({key: value for key, value in configured.items() if key != "cost_model"})
    defaults["cost_model"].update(configured.get("cost_model", {}))
    return defaults


def _read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_state(initial_capital: float = 150_000.0) -> dict:
    state = _read_json(STATE_PATH, {})
    if not state:
        state = {
            "schema_version": 2,
            "initial_capital": initial_capital,
            "cash": initial_capital,
            "holdings": {},
            "last_updated_date": None,
            "nav_history": [],
            "pending_rebalance": None,
        }

    state["schema_version"] = 2
    state.setdefault("initial_capital", initial_capital)
    state.setdefault("cash", state["initial_capital"])
    state.setdefault("holdings", {})
    state.setdefault("nav_history", [])
    state.setdefault("pending_rebalance", None)
    state.pop("equity_history", None)
    return state


def save_state(state: dict) -> None:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = STATE_PATH.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
    temp_path.replace(STATE_PATH)


def download_market_data(symbols: list[str], days: int = 60) -> dict[str, pd.DataFrame]:
    """Download unadjusted OHLCV data. The result is used only after market close."""
    try:
        import yfinance as yf
    except ImportError as error:
        raise RuntimeError("Install yfinance before running the daily paper-trading pipeline.") from error

    now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    start = (now_ist - timedelta(days=days)).strftime("%Y-%m-%d")
    end = (now_ist + timedelta(days=1)).strftime("%Y-%m-%d")
    yahoo_symbols = [f"{symbol}.NS" for symbol in symbols]
    downloaded = yf.download(
        yahoo_symbols,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=False,
        progress=False,
        threads=True,
    )

    market_data: dict[str, pd.DataFrame] = {}
    for symbol, yahoo_symbol in zip(symbols, yahoo_symbols):
        try:
            frame = downloaded[yahoo_symbol][["Open", "High", "Low", "Close", "Volume"]].copy()
        except KeyError:
            continue
        frame = frame.dropna(subset=["Close"])
        if frame.empty:
            continue
        frame.index = pd.to_datetime(frame.index).tz_localize(None)
        frame.index.name = "Date"
        market_data[symbol] = frame
    return market_data


def update_stock_histories(market_data: dict[str, pd.DataFrame]) -> None:
    """Make local ranking and execution data match the post-close download."""
    for symbol, incoming in market_data.items():
        path = STOCKS_DIR / f"{symbol}_daily.csv"
        if not path.exists():
            continue
        historical = pd.read_csv(path)
        historical["Date"] = pd.to_datetime(historical["Date"], errors="coerce")
        incoming = incoming.reset_index()
        incoming["Date"] = pd.to_datetime(incoming["Date"]).dt.tz_localize(None)
        combined = pd.concat([historical, incoming], ignore_index=True)
        combined = combined.dropna(subset=["Date", "Close"])
        combined = combined.sort_values("Date").drop_duplicates("Date", keep="last")
        combined["Date"] = combined["Date"].dt.strftime("%Y-%m-%d")
        combined.to_csv(path, index=False)


def update_sector_indices(ranking: pd.DataFrame, market_data: dict[str, pd.DataFrame]) -> None:
    """Extend each synthetic sector index from the refreshed constituent closes."""
    closes = {
        symbol: frame["Close"].rename(symbol)
        for symbol, frame in market_data.items()
        if not frame.empty
    }
    if not closes:
        raise RuntimeError("No market data was downloaded; sector indices were not updated.")
    close_frame = pd.concat(closes.values(), axis=1).sort_index()

    for sector in ranking["Sector"].unique():
        index_path = INDICES_DIR / f"{sector}_daily.csv"
        if not index_path.exists():
            continue
        index_data = pd.read_csv(index_path)
        index_data["Date"] = pd.to_datetime(index_data["Date"])
        last_date = index_data["Date"].max()
        constituents = ranking.loc[ranking["Sector"] == sector, "Symbol"].tolist()
        available = [symbol for symbol in constituents if symbol in close_frame.columns]
        if not available:
            continue

        sector_closes = close_frame[available].sort_index().ffill()
        for date, prices in sector_closes.loc[sector_closes.index > last_date].iterrows():
            prior_prices = sector_closes.loc[sector_closes.index < date].tail(1)
            if prior_prices.empty:
                continue
            prior = prior_prices.iloc[0]
            returns = (prices / prior - 1.0).replace([np.inf, -np.inf], np.nan).dropna()
            if returns.empty:
                continue
            previous_close = float(index_data.iloc[-1]["Close"])
            close = previous_close * (1.0 + float(returns.mean()))
            index_data = pd.concat([
                index_data,
                pd.DataFrame([{
                    "Date": date,
                    "Open": close,
                    "High": close,
                    "Low": close,
                    "Close": close,
                    "Volume": 0.0,
                }]),
            ], ignore_index=True)

        index_data["Date"] = pd.to_datetime(index_data["Date"]).dt.strftime("%Y-%m-%d")
        index_data.to_csv(index_path, index=False)


def _latest_sector_date() -> str:
    banking = pd.read_csv(INDICES_DIR / "banking_daily.csv")
    return str(banking["Date"].iloc[-1])


def evaluate_sectors(as_of_date: str) -> dict[str, dict]:
    results = {}
    for path in sorted(INDICES_DIR.glob("*_daily.csv")):
        sector = path.name.removesuffix("_daily.csv")
        details = evaluate_hmm_regime(
            pd.read_csv(path),
            target_date=as_of_date,
            smoothing_window=2,
            return_details=True,
        )
        results[sector] = details
    return results


def prices_on_date(symbols: list[str], date: str, column: str) -> dict[str, float]:
    prices: dict[str, float] = {}
    for symbol in symbols:
        path = STOCKS_DIR / f"{symbol}_daily.csv"
        if not path.exists():
            continue
        data = pd.read_csv(path, usecols=["Date", column])
        rows = data[data["Date"].astype(str) == date]
        if not rows.empty and pd.notna(rows.iloc[-1][column]):
            prices[symbol] = float(rows.iloc[-1][column])
    return prices


def portfolio_value(state: dict, prices: dict[str, float]) -> float:
    holding_value = sum(
        position["shares"] * prices.get(symbol, position["current_price"])
        for symbol, position in state["holdings"].items()
    )
    return float(state["cash"] + holding_value)


def _append_trade(record: dict) -> None:
    TRADE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    expected_columns = list(record)
    if TRADE_LOG_PATH.exists():
        existing = pd.read_csv(TRADE_LOG_PATH)
        if list(existing.columns) != expected_columns:
            # Preserve the prior simplified ledger while moving it to the
            # detailed contract-note-style schema used from this version on.
            migrated = pd.DataFrame(columns=expected_columns)
            if not existing.empty:
                migrated["Date"] = existing.get("Date")
                migrated["Signal_Date"] = existing.get("Date")
                migrated["Ticker"] = existing.get("Ticker", existing.get("Symbol"))
                migrated["Action"] = existing.get("Action")
                migrated["Shares"] = existing.get("Shares")
                legacy_price = existing.get("Fill_Price", existing.get("Price"))
                migrated["Reference_Open"] = legacy_price
                migrated["Fill_Price"] = legacy_price
                migrated["Notional"] = pd.to_numeric(migrated["Shares"], errors="coerce") * pd.to_numeric(legacy_price, errors="coerce")
                migrated["Total_Fees"] = existing.get("Total_Fees", existing.get("Commission", 0.0))
                migrated["Cash_Impact"] = existing.get("Cash_Impact", existing.get("Total_Cash_Impact"))
                for column in expected_columns:
                    if column not in migrated:
                        migrated[column] = 0.0
            migrated[expected_columns].to_csv(TRADE_LOG_PATH, index=False)
    frame = pd.DataFrame([record])
    frame.to_csv(TRADE_LOG_PATH, mode="a", header=not TRADE_LOG_PATH.exists(), index=False)


def _execute_trade(
    state: dict,
    date: str,
    symbol: str,
    side: str,
    shares: int,
    reference_price: float,
    cost_model: CostModel,
    signal_date: str,
) -> dict | None:
    if shares <= 0 or reference_price <= 0:
        return None
    slip = cost_model.slippage_bps / 10_000
    fill_price = reference_price * (1.0 + slip if side == "BUY" else 1.0 - slip)

    if side == "SELL":
        held = state["holdings"].get(symbol)
        if held is None:
            return None
        shares = min(shares, int(held["shares"]))
        if shares <= 0:
            return None

    notional = shares * fill_price
    fees = cost_model.estimate_fees(side, notional)
    if side == "BUY":
        total_cost = notional + fees["total"]
        affordable = int(state["cash"] / (fill_price * (1.0 + 0.003)))
        shares = min(shares, affordable)
        if shares <= 0:
            return None
        notional = shares * fill_price
        fees = cost_model.estimate_fees(side, notional)
        total_cost = notional + fees["total"]
        state["cash"] -= total_cost
        holding = state["holdings"].get(symbol)
        if holding is None:
            state["holdings"][symbol] = {
                "shares": float(shares),
                "buy_price": fill_price,
                "current_price": fill_price,
                "entry_date": date,
                "peak_price": fill_price,
            }
        else:
            total_shares = holding["shares"] + shares
            holding["buy_price"] = (holding["buy_price"] * holding["shares"] + fill_price * shares) / total_shares
            holding["shares"] = float(total_shares)
            holding["current_price"] = fill_price
            holding.setdefault("entry_date", date)
            holding["peak_price"] = max(holding.get("peak_price", fill_price), fill_price)
        cash_impact = -total_cost
    else:
        proceeds = notional - fees["total"]
        state["cash"] += proceeds
        state["holdings"][symbol]["shares"] -= shares
        if state["holdings"][symbol]["shares"] <= 0:
            del state["holdings"][symbol]
        cash_impact = proceeds

    record = {
        "Date": date,
        "Signal_Date": signal_date,
        "Ticker": symbol,
        "Action": side,
        "Shares": shares,
        "Reference_Open": reference_price,
        "Fill_Price": fill_price,
        "Notional": notional,
        "Brokerage": fees["brokerage"],
        "Exchange_Charges": fees["exchange"],
        "SEBI_Fee": fees["sebi"],
        "GST": fees["gst"],
        "Stamp_Duty": fees["stamp_duty"],
        "STT": fees["stt"],
        "Total_Fees": fees["total"],
        "Cash_Impact": cash_impact,
    }
    _append_trade(record)
    return record


def execute_pending_rebalance(state: dict, execution_date: str, cost_model: CostModel) -> list[dict]:
    pending = state.get("pending_rebalance")
    if not pending or pending["signal_date"] >= execution_date:
        return []

    targets = pending["target_symbols"]
    needed = list(state["holdings"].keys()) + targets
    opening_prices = prices_on_date(needed, execution_date, "Open")
    if not targets or any(symbol not in opening_prices for symbol in targets):
        return []

    fills = []
    for symbol in list(state["holdings"]):
        if symbol not in targets:
            fill = _execute_trade(
                state, execution_date, symbol, "SELL", int(state["holdings"][symbol]["shares"]),
                opening_prices.get(symbol, 0.0), cost_model, pending["signal_date"],
            )
            if fill:
                fills.append(fill)

    open_nav = portfolio_value(state, opening_prices)
    target_value = open_nav / len(targets)
    desired_quantities = {}
    for symbol in targets:
        estimated_fill = opening_prices[symbol] * (1.0 + cost_model.slippage_bps / 10_000)
        desired_quantities[symbol] = int(target_value / (estimated_fill * 1.003))

    for symbol in targets:
        current = int(state["holdings"].get(symbol, {}).get("shares", 0))
        excess = current - desired_quantities[symbol]
        if excess > 0:
            fill = _execute_trade(
                state, execution_date, symbol, "SELL", excess, opening_prices[symbol],
                cost_model, pending["signal_date"],
            )
            if fill:
                fills.append(fill)

    for symbol in targets:
        current = int(state["holdings"].get(symbol, {}).get("shares", 0))
        shortfall = desired_quantities[symbol] - current
        if shortfall > 0:
            fill = _execute_trade(
                state, execution_date, symbol, "BUY", shortfall, opening_prices[symbol],
                cost_model, pending["signal_date"],
            )
            if fill:
                fills.append(fill)

    state["pending_rebalance"] = None
    return fills


def proposed_orders(state: dict, target_symbols: list[str], close_prices: dict[str, float]) -> list[dict]:
    orders = []
    for symbol in state["holdings"]:
        if symbol not in target_symbols:
            orders.append({"symbol": symbol, "action": "SELL", "reason": "not_in_next_target_set"})
    for symbol in target_symbols:
        orders.append({
            "symbol": symbol,
            "action": "TARGET_WEIGHT",
            "target_weight": 1.0 / len(target_symbols),
            "reference_close": close_prices.get(symbol),
        })
    return orders


def update_nav(state: dict, date: str, close_prices: dict[str, float]) -> float:
    for symbol, holding in state["holdings"].items():
        if symbol in close_prices:
            holding["current_price"] = close_prices[symbol]
    nav = portfolio_value(state, close_prices)
    state["last_updated_date"] = date
    state["nav_history"] = [row for row in state["nav_history"] if row["date"] != date]
    state["nav_history"].append({"date": date, "nav": nav})
    return nav


def write_snapshot(date: str, payload: dict) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H%M%S")
    path = SNAPSHOT_DIR / f"{date}_{timestamp}.json"
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return path


def create_monthly_report(state: dict) -> None:
    history = pd.DataFrame(state["nav_history"])
    if history.empty:
        return
    history["date"] = pd.to_datetime(history["date"])
    history = history.sort_values("date").set_index("date")
    monthly = history["nav"].resample("ME").last().to_frame("Portfolio_NAV")
    monthly["Portfolio_Return"] = monthly["Portfolio_NAV"].pct_change()

    if TRADE_LOG_PATH.exists():
        trades = pd.read_csv(TRADE_LOG_PATH)
        trades["Date"] = pd.to_datetime(trades["Date"])
        turnover = trades.groupby(trades["Date"].dt.to_period("M"))["Notional"].sum()
        costs = trades.groupby(trades["Date"].dt.to_period("M"))["Total_Fees"].sum()
        monthly["Turnover"] = [turnover.get(date.to_period("M"), 0.0) for date in monthly.index]
        monthly["Trading_Costs"] = [costs.get(date.to_period("M"), 0.0) for date in monthly.index]
    else:
        monthly["Turnover"] = 0.0
        monthly["Trading_Costs"] = 0.0

    daily_returns = history["nav"].pct_change()
    hit_rate = daily_returns.gt(0).resample("ME").mean()
    monthly["Daily_Hit_Rate"] = hit_rate

    benchmark_path = WORKSPACE_DIR / "capital_simulation_walkforward.csv"
    if benchmark_path.exists():
        benchmark = pd.read_csv(benchmark_path)
        benchmark["Date"] = pd.to_datetime(benchmark["Date"])
        benchmark = benchmark.set_index("Date")["Portfolio_Value"].resample("ME").last()
        benchmark_returns = benchmark.pct_change()
        monthly["Walk_Forward_Return"] = benchmark_returns.reindex(monthly.index)
        monthly["Excess_Return"] = monthly["Portfolio_Return"] - monthly["Walk_Forward_Return"]

    monthly.index.name = "Month"
    monthly.reset_index().to_csv(MONTHLY_REPORT_PATH, index=False)


def generate_readme(state: dict, as_of_date: str, nav: float) -> None:
    initial = state["initial_capital"]
    roi = (nav / initial - 1.0) * 100.0
    holdings = []
    for symbol, position in state["holdings"].items():
        value = position["shares"] * position["current_price"]
        holdings.append(
            f"| {symbol} | {position['shares']:.0f} | Rs. {position['buy_price']:,.2f} | "
            f"Rs. {position['current_price']:,.2f} | Rs. {value:,.2f} |"
        )
    holdings_table = "\n".join(holdings) or "| No positions | | | |"
    pending = state.get("pending_rebalance")
    pending_text = ", ".join(pending["target_symbols"]) if pending else "None"
    readme = f"""# COEP Quantitative Finance Club Paper Trading System

This is a paper-only sector HMM strategy. Signals use the close of day T and eligible orders are simulated at the open of the next available trading day.

## Portfolio Dashboard

| Metric | Value |
| :--- | ---: |
| Initial capital | Rs. {initial:,.2f} |
| NAV | Rs. {nav:,.2f} |
| Return | {roi:+.2f}% |
| Cash | Rs. {state['cash']:,.2f} |
| Latest close | {as_of_date} |
| Pending next-session targets | {pending_text} |

## Holdings

| Symbol | Shares | Average Cost | Latest Close | Market Value |
| :--- | ---: | ---: | ---: | ---: |
{holdings_table}

Daily immutable records are in `scratch/paper_snapshots/`; monthly performance is in `scratch/monthly_paper_report.csv`.
"""
    (WORKSPACE_DIR / "README.md").write_text(readme, encoding="utf-8")


def run_daily_pipeline() -> None:
    config = load_config()
    cost_model = CostModel(**config["cost_model"])
    ranking = load_rankings(SCORED_DIR / "global_ranking.csv")
    market_data = download_market_data(ranking["Symbol"].tolist())
    update_stock_histories(market_data)
    update_sector_indices(ranking, market_data)

    as_of_date = _latest_sector_date()
    state = load_state(float(config["initial_capital"]))
    fills = execute_pending_rebalance(state, as_of_date, cost_model)

    sector_results = evaluate_sectors(as_of_date)
    active_sectors = [sector for sector, result in sector_results.items() if result["state"] == 0]
    daily_ranking = ranked_candidates(ranking, active_sectors, str(STOCKS_DIR), as_of_date)
    daily_ranking.to_csv(DAILY_RANKING_PATH, index=False)

    swap_policy = SwapPolicy(
        swap_margin=float(config.get("swap_margin", 0.15)),
        min_holding_days=int(config.get("min_holding_days", 5)),
        stop_loss_pct=float(config.get("stop_loss_pct", 0.08)),
    )
    targets, exits, exit_reasons = swap_policy.evaluate_portfolio(
        holdings=state["holdings"],
        active_sectors=active_sectors,
        candidate_df=daily_ranking,
        current_date_str=as_of_date,
        max_positions=int(config.get("max_positions", 5)),
        max_per_sector=int(config.get("max_stocks_per_sector", 1)),
    )

    symbols = list(state["holdings"].keys()) + targets
    close_prices = prices_on_date(symbols, as_of_date, "Close")
    nav = update_nav(state, as_of_date, close_prices)
    orders = proposed_orders(state, targets, close_prices) if targets else []
    if targets:
        state["pending_rebalance"] = {
            "signal_date": as_of_date,
            "target_symbols": targets,
            "target_weights": {symbol: 1.0 / len(targets) for symbol in targets},
        }

    snapshot = {
        "schema_version": 1,
        "created_at_ist": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
        "price_cutoff_date": as_of_date,
        "cost_model": asdict(cost_model),
        "hmm_sector_results": sector_results,
        "active_sectors": active_sectors,
        "ranking_top_20": daily_ranking.head(20).to_dict(orient="records"),
        "proposed_orders": orders,
        "fills_at_open": fills,
        "portfolio_nav_at_close": nav,
        "portfolio_state": state,
    }
    snapshot_path = write_snapshot(as_of_date, snapshot)
    save_state(state)
    create_monthly_report(state)
    generate_readme(state, as_of_date, nav)
    print(f"Daily paper-trading run complete: {snapshot_path}")


if __name__ == "__main__":
    run_daily_pipeline()
