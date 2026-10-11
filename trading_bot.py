"""Continuous HMM Sector Strategy Trading Bot for Indian Equities (NSE).

Continuously monitors live prices, evaluates HMM sector regimes,
tracks risk stop-losses, and executes portfolio rebalancing rules.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from paper_trading import (
    CONFIG_PATH,
    CostModel,
    INDICES_DIR,
    SCORED_DIR,
    SCRATCH_DIR,
    STATE_PATH,
    STOCKS_DIR,
    TRADE_LOG_PATH,
    _execute_trade,
    download_market_data,
    evaluate_sectors,
    generate_readme,
    load_config,
    load_state,
    portfolio_value,
    save_state,
    update_nav,
    update_sector_indices,
    update_stock_histories,
)
from strategy_core import SwapPolicy, load_rankings, ranked_candidates

# Ensure Windows terminal encoding compatibility
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Timezone
IST = ZoneInfo("Asia/Kolkata")


# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("TradingBot")


def git_sync_push(commit_msg: str = "Auto-update portfolio metrics and dashboard") -> bool:
    """Automatically commit and push portfolio state and README to GitHub."""
    try:
        workspace_dir = Path(__file__).resolve().parent
        tracked_files = [
            "README.md",
            "scratch/paper_portfolio_state.json",
            "scratch/paper_trade_log.csv",
            "scratch/paper_snapshots",
            "scored_csv/daily_ranking.csv",
        ]
        existing = [f for f in tracked_files if (workspace_dir / f).exists()]
        if not existing:
            return False

        # 1. Stage tracked files
        subprocess.run(["git", "add"] + existing, cwd=workspace_dir, check=True, capture_output=True, text=True)

        # 2. Check if there are cached diffs
        diff_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=workspace_dir, capture_output=True)
        if diff_res.returncode == 0:
            return False  # No new changes to push

        # 3. Pull rebase to avoid merge conflicts with remote
        subprocess.run(["git", "pull", "--rebase", "origin", "master"], cwd=workspace_dir, capture_output=True, text=True)

        # 4. Commit with [skip ci] to prevent infinite workflow loops
        full_msg = f"{commit_msg} [skip ci]"
        subprocess.run(["git", "commit", "-m", full_msg], cwd=workspace_dir, check=True, capture_output=True, text=True)

        # 5. Push to GitHub
        subprocess.run(["git", "push", "origin", "master"], cwd=workspace_dir, check=True, capture_output=True, text=True)
        logger.info(f"[GIT PUSH] Pushed updates to GitHub: {commit_msg}")
        return True
    except Exception as exc:
        logger.warning(f"[GIT PUSH] Auto-push to GitHub encountered: {exc}")
        return False


class MarketClock:
    """Manages Indian Standard Time (IST) market hours awareness."""

    MARKET_OPEN = dtime(9, 15)
    MARKET_CLOSE = dtime(15, 30)
    PRE_OPEN = dtime(9, 0)
    EOD_REBALANCE_START = dtime(15, 10)

    @classmethod
    def now_ist(cls) -> datetime:
        return datetime.now(IST)

    @classmethod
    def is_weekday(cls) -> bool:
        return cls.now_ist().weekday() < 5

    @classmethod
    def is_market_open(cls) -> bool:
        now = cls.now_ist()
        return cls.is_weekday() and (cls.MARKET_OPEN <= now.time() <= cls.MARKET_CLOSE)

    @classmethod
    def is_eod_rebalance_window(cls) -> bool:
        now = cls.now_ist()
        return cls.is_weekday() and (now.time() >= cls.EOD_REBALANCE_START)

    @classmethod
    def status_string(cls) -> str:
        now = cls.now_ist()
        if not cls.is_weekday():
            return "[CLOSED] (Weekend)"
        if now.time() < cls.PRE_OPEN:
            return f"[CLOSED] (Pre-market at {cls.PRE_OPEN.strftime('%H:%M')})"
        if now.time() < cls.MARKET_OPEN:
            return "[PRE-OPEN] (09:00 - 09:15 IST)"
        if now.time() <= cls.MARKET_CLOSE:
            return "[OPEN] (09:15 - 15:30 IST)"
        return "[CLOSED] (After Hours)"

    @classmethod
    def seconds_until_market_open(cls) -> int:
        now = cls.now_ist()
        today_open = now.replace(
            hour=cls.MARKET_OPEN.hour, minute=cls.MARKET_OPEN.minute, second=0, microsecond=0
        )
        if cls.is_weekday() and now < today_open:
            return max(0, int((today_open - now).total_seconds()))

        days_ahead = 1
        next_day = now + timedelta(days=days_ahead)
        while next_day.weekday() >= 5:
            days_ahead += 1
            next_day = now + timedelta(days=days_ahead)

        next_open = next_day.replace(
            hour=cls.MARKET_OPEN.hour, minute=cls.MARKET_OPEN.minute, second=0, microsecond=0
        )
        return max(0, int((next_open - now).total_seconds()))

    @classmethod
    def time_until_open_string(cls) -> str:
        sec = cls.seconds_until_market_open()
        hours = sec // 3600
        mins = (sec % 3600) // 60
        return f"{hours}h {mins}m"



def fetch_live_quotes(symbols: list[str]) -> dict[str, float]:
    """Fetch latest available prices for symbols using yfinance."""
    if not symbols:
        return {}

    try:
        import yfinance as yf
    except ImportError:
        logger.error("yfinance is not installed. Run 'pip install yfinance'")
        return {}

    quotes: dict[str, float] = {}
    clean_syms = [s.strip() for s in symbols if s.strip()]
    yf_tickers = [f"{sym}.NS" for sym in clean_syms]

    try:
        data = yf.download(
            yf_tickers,
            period="1d",
            interval="1m",
            progress=False,
            auto_adjust=False,
            threads=True,
        )
        if not data.empty and "Close" in data:
            close_data = data["Close"]
            for sym, yf_sym in zip(clean_syms, yf_tickers):
                try:
                    if isinstance(close_data, pd.DataFrame) and yf_sym in close_data.columns:
                        series = close_data[yf_sym].dropna()
                        if not series.empty:
                            quotes[sym] = float(series.iloc[-1])
                    elif isinstance(close_data, pd.Series) and not close_data.empty:
                        quotes[sym] = float(close_data.dropna().iloc[-1])
                except Exception:
                    pass
    except Exception as exc:
        logger.warning(f"Batch live price fetch failed ({exc}), falling back to cached prices.")

    # Fallback to local daily CSV files for any missing tickers
    for sym in clean_syms:
        if sym not in quotes:
            csv_path = STOCKS_DIR / f"{sym}_daily.csv"
            if csv_path.exists():
                try:
                    df = pd.read_csv(csv_path, usecols=["Close"])
                    if not df.empty:
                        quotes[sym] = float(df.iloc[-1]["Close"])
                except Exception:
                    pass

    return quotes


class HMMTradingBot:
    """Automated continuous trading bot executing the HMM sector strategy."""

    def __init__(self, dry_run: bool = False, auto_push: bool | None = None):
        self.dry_run = dry_run
        self.config = load_config()
        self.cost_model = CostModel(**self.config["cost_model"])
        self.state = load_state(float(self.config["initial_capital"]))
        self.running = False
        self.last_rebalance_date: str | None = None
        self.swap_policy = SwapPolicy(
            swap_margin=float(self.config.get("swap_margin", 0.15)),
            min_holding_days=int(self.config.get("min_holding_days", 5)),
            stop_loss_pct=float(self.config.get("stop_loss_pct", 0.08)),
        )
        self.auto_push = self.config.get("auto_git_push", True) if auto_push is None else auto_push
        self.last_git_push_time = 0.0
        self.git_sync_interval = float(self.config.get("git_sync_interval_seconds", 900))


    def print_dashboard(self, live_prices: dict[str, float], active_sectors: list[str]) -> None:
        """Render a clean CLI status dashboard."""
        now = MarketClock.now_ist()
        nav = portfolio_value(self.state, live_prices)
        initial = float(self.state.get("initial_capital", 150000.0))
        roi = ((nav / initial) - 1.0) * 100.0
        cash = float(self.state.get("cash", 0.0))

        print("\n" + "=" * 80)
        print(" [BOT] COEP QUANT FINANCE CLUB -- HMM STRATEGY TRADING BOT")
        print("=" * 80)
        print(f" [*] Current IST Time : {now.strftime('%Y-%m-%d %H:%M:%S')} IST")
        print(f" [*] Market Status    : {MarketClock.status_string()}")
        print(f" [*] Total NAV         : Rs. {nav:,.2f}  ({roi:+.2f}%)")
        print(f" [*] Cash Balance      : Rs. {cash:,.2f}  ({cash/nav*100:.1f}%)")
        print(f" [*] Active Bullish    : {', '.join(active_sectors[:6]) if active_sectors else 'None (Cash Defended)'}")
        print("-" * 80)
        print(f" {'SYMBOL':<12} {'SHARES':>8} {'BUY PRICE':>14} {'LIVE PRICE':>14} {'VALUE':>14} {'PNL (%)':>10}")
        print("-" * 80)

        holdings = self.state.get("holdings", {})
        if not holdings:
            print("  (No active holdings -- Capital 100% in cash)")
        else:
            for sym, pos in holdings.items():
                sh = pos["shares"]
                buy_p = pos["buy_price"]
                cur_p = live_prices.get(sym, pos.get("current_price", buy_p))
                mkt_val = sh * cur_p
                pnl_pct = ((cur_p / buy_p) - 1.0) * 100.0 if buy_p > 0 else 0.0
                color_pnl = f"{pnl_pct:+.2f}%"
                print(f" {sym:<12} {sh:>8.0f} Rs. {buy_p:>10.2f} Rs. {cur_p:>10.2f} Rs. {mkt_val:>10.2f} {color_pnl:>10}")

        print("=" * 80)

    def check_stop_losses(self, live_prices: dict[str, float]) -> list[str]:
        """Check all positions against the risk stop-loss threshold."""
        stop_loss_pct = float(self.config.get("stop_loss_pct", 0.08))
        now_date = MarketClock.now_ist().strftime("%Y-%m-%d")
        exits_triggered = []

        for sym, pos in list(self.state["holdings"].items()):
            cur_price = live_prices.get(sym)
            if not cur_price:
                continue
            buy_price = pos["buy_price"]
            loss = (cur_price / buy_price) - 1.0
            if loss <= -stop_loss_pct:
                logger.warning(
                    f"[STOP LOSS TRIGGERED] {sym}: Price Rs. {cur_price:.2f} "
                    f"vs Buy Rs. {buy_price:.2f} ({loss*100:.2f}% <= -{stop_loss_pct*100:.1f}%)"
                )
                if not self.dry_run:
                    trade = _execute_trade(
                        state=self.state,
                        date=now_date,
                        symbol=sym,
                        side="SELL",
                        shares=int(pos["shares"]),
                        reference_price=cur_price,
                        cost_model=self.cost_model,
                        signal_date=now_date,
                    )
                    if trade:
                        logger.info(f"[FILL] Stop-loss executed SELL for {sym}: Cash impact +Rs. {trade['Cash_Impact']:,.2f}")
                        save_state(self.state)
                        if self.auto_push:
                            git_sync_push(f"Execute stop-loss SELL for {sym} at Rs. {cur_price:.2f}")
                exits_triggered.append(sym)

        return exits_triggered


    def check_pending_orders(self, live_prices: dict[str, float]) -> None:
        """Execute any pending rebalance orders if market is open."""
        pending = self.state.get("pending_rebalance")
        if not pending:
            return

        now_date = MarketClock.now_ist().strftime("%Y-%m-%d")
        targets = pending.get("target_symbols", [])
        logger.info(f"Checking pending rebalance orders for targets: {targets}")

        if not MarketClock.is_market_open():
            logger.info("Market is closed. Pending orders will execute upon market open.")
            return

        if self.dry_run:
            logger.info(f"[Dry Run] Would execute pending rebalance for {targets}")
            return

        executed_any = False
        # Execute sells of existing holdings not in targets
        for sym in list(self.state["holdings"]):
            if sym not in targets:
                shares = int(self.state["holdings"][sym]["shares"])
                ref_price = live_prices.get(sym, self.state["holdings"][sym]["current_price"])
                trade = _execute_trade(
                    state=self.state,
                    date=now_date,
                    symbol=sym,
                    side="SELL",
                    shares=shares,
                    reference_price=ref_price,
                    cost_model=self.cost_model,
                    signal_date=pending.get("signal_date", now_date),
                )
                if trade:
                    executed_any = True
                    logger.info(f"[FILL] Rebalance exit SELL {sym} x {shares}")

        # Compute target allocations
        current_nav = portfolio_value(self.state, live_prices)
        target_allocation = current_nav / len(targets) if targets else 0.0

        for sym in targets:
            price = live_prices.get(sym)
            if not price:
                continue
            current_shares = int(self.state["holdings"].get(sym, {}).get("shares", 0))
            desired_shares = int(target_allocation / (price * 1.003))

            diff = desired_shares - current_shares
            if diff > 0:
                trade = _execute_trade(
                    state=self.state,
                    date=now_date,
                    symbol=sym,
                    side="BUY",
                    shares=diff,
                    reference_price=price,
                    cost_model=self.cost_model,
                    signal_date=pending.get("signal_date", now_date),
                )
                if trade:
                    executed_any = True
                    logger.info(f"[FILL] Rebalance entry BUY {sym} x {diff} @ Rs. {price:.2f}")

        self.state["pending_rebalance"] = None
        save_state(self.state)
        if executed_any and self.auto_push:
            git_sync_push(f"Execute market-open rebalance fills [{now_date}]")


    def evaluate_strategy_cycle(self) -> list[str]:
        """Run the HMM regime evaluation and test the SwapPolicy."""
        now_date = MarketClock.now_ist().strftime("%Y-%m-%d")
        sector_results = evaluate_sectors(now_date)
        active_sectors = [sec for sec, res in sector_results.items() if res.get("state") == 0]

        ranking_path = SCORED_DIR / "global_ranking.csv"
        if not ranking_path.exists():
            logger.error(f"Global ranking file not found at {ranking_path}")
            return active_sectors

        ranking = load_rankings(str(ranking_path))
        daily_ranking = ranked_candidates(ranking, active_sectors, str(STOCKS_DIR), now_date)

        # Evaluate Swaps and Exits with turnover damper & sector caps
        target_symbols, exits, exit_reasons = self.swap_policy.evaluate_portfolio(
            holdings=self.state["holdings"],
            active_sectors=active_sectors,
            candidate_df=daily_ranking,
            current_date_str=now_date,
            max_positions=int(self.config.get("max_positions", 5)),
            max_per_sector=int(self.config.get("max_stocks_per_sector", 1)),
        )

        for sym, reason in exit_reasons.items():
            logger.info(f"[STRATEGY] Trigger for {sym}: {reason}")

        # If targets differ from holdings, queue rebalance
        held_symbols = set(self.state["holdings"].keys())
        target_set = set(target_symbols)

        if held_symbols != target_set:
            logger.info(f"[SIGNAL] Portfolio Rebalance Generated! Target symbols: {target_symbols}")
            self.state["pending_rebalance"] = {
                "signal_date": now_date,
                "target_symbols": target_symbols,
                "target_weights": {s: 1.0 / len(target_symbols) for s in target_symbols},
            }
            save_state(self.state)

        return active_sectors

    def run_single_iteration(self) -> None:
        """Execute one complete polling cycle."""
        # 1. Gather watched universe
        ranking_path = SCORED_DIR / "global_ranking.csv"
        watched = list(self.state["holdings"].keys())
        if ranking_path.exists():
            try:
                top_syms = pd.read_csv(ranking_path, usecols=["Symbol"]).head(15)["Symbol"].tolist()
                watched = list(set(watched + top_syms))
            except Exception:
                pass

        # 2. Fetch live prices
        live_prices = fetch_live_quotes(watched)

        # 3. Check hard stop-losses
        self.check_stop_losses(live_prices)

        # 4. Check & execute pending orders
        self.check_pending_orders(live_prices)

        # 5. Evaluate HMM regimes & strategy
        now_date = MarketClock.now_ist().strftime("%Y-%m-%d")
        if self.last_rebalance_date != now_date:
            active_sectors = self.evaluate_strategy_cycle()
            self.last_rebalance_date = now_date
        else:
            sector_results = evaluate_sectors(now_date)
            active_sectors = [sec for sec, res in sector_results.items() if res.get("state") == 0]

        # 6. Update NAV, sync README, and print dashboard
        nav = update_nav(self.state, now_date, live_prices)
        save_state(self.state)
        generate_readme(self.state, now_date, nav)
        self.print_dashboard(live_prices, active_sectors)

        # 7. Periodic Git Push to GitHub
        current_time = time.time()
        if self.auto_push and (current_time - self.last_git_push_time >= self.git_sync_interval):
            pushed = git_sync_push(f"Auto-update portfolio metrics, README dashboard [{now_date}]")
            if pushed:
                self.last_git_push_time = current_time

    def run_continuous_loop(self, poll_interval: int = 60, force_active: bool = False) -> None:
        """Run continuous monitoring loop during trading hours."""
        self.running = True
        mode_str = "FORCE-ACTIVE (ignoring market hours)" if force_active else "TRADING-HOURS-ONLY (09:15 - 15:30 IST)"
        logger.info(f"[STARTED] Continuous HMM Trading Bot active (Interval: {poll_interval}s | Mode: {mode_str})")
        if self.auto_push:
            logger.info(f"[GIT SYNC] Auto-push enabled (Syncs every {int(self.git_sync_interval)}s + on trade fills)")
        logger.info("Press Ctrl+C to stop.")

        def handle_sigint(signum, frame):
            logger.info("\n[STOPPING] Received shutdown signal. Gracefully exiting bot...")
            self.running = False

        signal.signal(signal.SIGINT, handle_sigint)

        while self.running:
            try:
                is_open = MarketClock.is_market_open()
                if is_open or force_active:
                    # Market is OPEN: active polling and strategy execution
                    self.run_single_iteration()
                    for _ in range(poll_interval):
                        if not self.running:
                            break
                        time.sleep(1)
                else:
                    # Market is CLOSED: countdown to next session without API hammering
                    countdown = MarketClock.time_until_open_string()
                    status = MarketClock.status_string()
                    logger.info(f"[SESSION CLOSED] {status} | Next session opens in {countdown}. Bot standing by...")
                    
                    # Sleep 60 seconds (or wake up at exact market open)
                    sleep_sec = min(60, MarketClock.seconds_until_market_open())
                    sleep_sec = max(5, sleep_sec)
                    for _ in range(sleep_sec):
                        if not self.running:
                            break
                        time.sleep(1)
            except Exception as exc:
                logger.error(f"Error during bot iteration: {exc}", exc_info=True)
                time.sleep(10)

        logger.info("Bot stopped successfully. State preserved.")


def main():
    parser = argparse.ArgumentParser(description="HMM Sector Trading System -- Continuous Execution Bot")
    parser.add_argument("--loop", action="store_true", help="Run in continuous monitoring loop")
    parser.add_argument("--once", action="store_true", help="Run a single check iteration and exit")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds for loop mode")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without executing trades")
    parser.add_argument("--status", action="store_true", help="Show current portfolio status and exit")
    parser.add_argument("--force-active", action="store_true", help="Poll continuously even when market is closed (for testing/sim)")
    parser.add_argument("--auto-push", dest="auto_push", action="store_true", default=None, help="Force enable auto Git push to GitHub")
    parser.add_argument("--no-push", dest="auto_push", action="store_false", help="Disable auto Git push to GitHub")

    args = parser.parse_args()
    bot = HMMTradingBot(dry_run=args.dry_run, auto_push=args.auto_push)

    if args.status:
        watched = list(bot.state["holdings"].keys())
        prices = fetch_live_quotes(watched)
        now_date = MarketClock.now_ist().strftime("%Y-%m-%d")
        sectors = evaluate_sectors(now_date)
        active = [s for s, r in sectors.items() if r.get("state") == 0]
        bot.print_dashboard(prices, active)
        return

    if args.loop:
        bot.run_continuous_loop(poll_interval=args.interval, force_active=args.force_active)
    else:
        # Default to single iteration
        bot.run_single_iteration()


if __name__ == "__main__":
    main()

