"""Telegram Bot Notification Engine for HMM Quantitative Trading System.

Dispatches instant, real-time alerts to the user's Telegram whenever trading triggers
occur: Stop-Loss exits, Rebalance signals, Order fills, and EOD performance summaries.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Windows terminal UTF-8 encoding support
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_DIR / "paper_trading_config.json"
ENV_PATH = ROOT_DIR / ".env"
IST = ZoneInfo("Asia/Kolkata")

logger = logging.getLogger("TelegramNotifier")


def load_env_file(filepath: Path) -> dict[str, str]:
    """Parse simple KEY=VALUE pairs from a .env file."""
    env_vars: dict[str, str] = {}
    if not filepath.exists():
        return env_vars
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip("\"'")
    except Exception:
        pass
    return env_vars


class TelegramNotifier:
    """Manages Telegram bot credentials and dispatches formatted HTML alerts."""

    def __init__(self):
        self.bot_token: str = ""
        self.chat_id: str = ""
        self.enabled: bool = True
        self.notify_on_stop_loss: bool = True
        self.notify_on_trades: bool = True
        self.notify_on_rebalance: bool = True
        self.notify_on_eod: bool = True

        self._load_credentials()

    def _load_credentials(self) -> None:
        """Resolve credentials from environment, .env file, or config file."""
        # 1. Start with paper_trading_config.json
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    tg = cfg.get("telegram", {})
                    self.enabled = bool(tg.get("enabled", True))
                    self.bot_token = str(tg.get("bot_token", "")).strip()
                    self.chat_id = str(tg.get("chat_id", "")).strip()
                    self.notify_on_stop_loss = bool(tg.get("notify_on_stop_loss", True))
                    self.notify_on_trades = bool(tg.get("notify_on_trades", True))
                    self.notify_on_rebalance = bool(tg.get("notify_on_rebalance", True))
                    self.notify_on_eod = bool(tg.get("notify_on_eod", True))
            except Exception as exc:
                logger.warning(f"Failed to read telegram config from {CONFIG_PATH}: {exc}")

        # 2. Override with .env file if present
        env_vars = load_env_file(ENV_PATH)
        if "TELEGRAM_BOT_TOKEN" in env_vars and env_vars["TELEGRAM_BOT_TOKEN"]:
            self.bot_token = env_vars["TELEGRAM_BOT_TOKEN"]
        if "TELEGRAM_CHAT_ID" in env_vars and env_vars["TELEGRAM_CHAT_ID"]:
            self.chat_id = env_vars["TELEGRAM_CHAT_ID"]

        # 3. Override with system environment variables (highest priority)
        if os.getenv("TELEGRAM_BOT_TOKEN"):
            self.bot_token = os.environ["TELEGRAM_BOT_TOKEN"].strip()
        if os.getenv("TELEGRAM_CHAT_ID"):
            self.chat_id = os.environ["TELEGRAM_CHAT_ID"].strip()

    def is_configured(self) -> bool:
        """Check if bot token and chat ID are populated."""
        return bool(self.enabled and self.bot_token and self.chat_id)

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """Send a message to the configured Telegram chat."""
        if not self.is_configured():
            logger.debug("Telegram notifications skipped: bot_token or chat_id not configured.")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }

        try:
            import requests
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                logger.info("[TELEGRAM] Notification delivered successfully.")
                return True
            else:
                logger.warning(f"[TELEGRAM] Failed to send message: HTTP {resp.status_code} - {resp.text}")
                return False
        except Exception as exc:
            # Fallback to standard library urllib
            try:
                import urllib.parse
                import urllib.request
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        logger.info("[TELEGRAM] Notification delivered via fallback urllib.")
                        return True
            except Exception as e:
                logger.warning(f"[TELEGRAM] Delivery failed: {e}")
            return False

    def notify_stop_loss(
        self,
        symbol: str,
        buy_price: float,
        trigger_price: float,
        loss_pct: float,
        shares: int,
        cash_impact: float,
    ) -> bool:
        """Alert on stop-loss execution."""
        if not self.notify_on_stop_loss:
            return False

        now_str = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            f"🚨 <b>STOP-LOSS TRIGGERED & EXECUTED</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Symbol:</b> <code>{symbol}</code>\n"
            f"<b>Action:</b> Immediate SELL to protect capital\n"
            f"<b>Shares Sold:</b> {shares:,}\n"
            f"<b>Exit Price:</b> Rs. {trigger_price:,.2f}\n"
            f"<b>Buy Price:</b> Rs. {buy_price:,.2f}\n"
            f"<b>Loss Impact:</b> <b>{loss_pct:+.2f}%</b> (Threshold: -8.0%)\n"
            f"<b>Cash Recovered:</b> +Rs. {cash_impact:,.2f}\n"
            f"<b>Timestamp:</b> {now_str} IST\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>HMM Continuous Trading Bot • NSE</i>"
        )
        return self.send_message(msg)

    def notify_trade_fill(
        self,
        symbol: str,
        side: str,
        shares: int,
        price: float,
        remaining_cash: float,
        trade_reason: str = "Market-Open Rebalance Fill",
    ) -> bool:
        """Alert on trade execution fill."""
        if not self.notify_on_trades:
            return False

        emoji = "🟢" if side.upper() == "BUY" else "🔴"
        val = shares * price
        now_str = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

        msg = (
            f"{emoji} <b>ORDER EXECUTED: {side.upper()} {symbol}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Reason:</b> {trade_reason}\n"
            f"<b>Quantity:</b> {shares:,} shares\n"
            f"<b>Fill Price:</b> Rs. {price:,.2f}\n"
            f"<b>Trade Value:</b> Rs. {val:,.2f}\n"
            f"<b>Cash Remaining:</b> Rs. {remaining_cash:,.2f}\n"
            f"<b>Executed At:</b> {now_str} IST\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>COEP Quantitative Finance Club</i>"
        )
        return self.send_message(msg)

    def notify_rebalance_signal(
        self,
        active_sectors: list[str],
        target_symbols: list[str],
        exit_reasons: dict[str, str],
    ) -> bool:
        """Alert at 3:15 PM rebalance window when new signals are generated."""
        if not self.notify_on_rebalance:
            return False

        now_str = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
        sectors_str = ", ".join(active_sectors) if active_sectors else "None (Cash Protection Defended)"
        targets_str = ", ".join(target_symbols) if target_symbols else "100% Cash Buffer"

        exits_formatted = ""
        if exit_reasons:
            exits_formatted = "\n<b>Scheduled Swaps/Exits:</b>\n" + "\n".join(
                [f" • <code>{s}</code>: {r}" for s, r in exit_reasons.items()]
            )

        msg = (
            f"🔄 <b>STRATEGY REBALANCE SIGNAL (3:15 PM IST)</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Bullish Sectors (State 0):</b>\n{sectors_str}\n\n"
            f"<b>Target Portfolio Candidates:</b>\n<code>{targets_str}</code>"
            f"{exits_formatted}\n\n"
            f"<b>Window:</b> Orders queued for next session market-open fill.\n"
            f"<b>Timestamp:</b> {now_str} IST\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Zero-Delay HMM Regime Engine</i>"
        )
        return self.send_message(msg)

    def notify_eod_summary(
        self,
        nav: float,
        initial_capital: float,
        cash: float,
        holdings: dict,
        active_sectors: list[str],
    ) -> bool:
        """Daily market close summary report."""
        if not self.notify_on_eod:
            return False

        roi = ((nav / initial_capital) - 1.0) * 100.0 if initial_capital > 0 else 0.0
        now_str = datetime.now(IST).strftime("%Y-%m-%d")
        cash_pct = (cash / nav) * 100.0 if nav > 0 else 0.0

        pos_lines = []
        if not holdings:
            pos_lines.append("<i>(Portfolio 100% in cash — defensive mode)</i>")
        else:
            for sym, pos in holdings.items():
                sh = int(pos.get("shares", 0))
                bp = float(pos.get("buy_price", 0.0))
                cp = float(pos.get("current_price", bp))
                pnl = ((cp / bp) - 1.0) * 100.0 if bp > 0 else 0.0
                pnl_color = "+" if pnl >= 0 else ""
                pos_lines.append(f" • <b>{sym}</b>: {sh} sh | Buy: {bp:.1f} | Now: {cp:.1f} ({pnl_color}{pnl:.2f}%)")

        pos_str = "\n".join(pos_lines)
        sectors_str = ", ".join(active_sectors[:6]) if active_sectors else "None"

        msg = (
            f"📊 <b>DAILY EOD PORTFOLIO SUMMARY [{now_str}]</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Total NAV:</b> Rs. {nav:,.2f} (<b>{roi:+.2f}%</b>)\n"
            f"<b>Cash Balance:</b> Rs. {cash:,.2f} ({cash_pct:.1f}%)\n"
            f"<b>Active Sectors:</b> {sectors_str}\n\n"
            f"<b>Holdings Breakdown:</b>\n{pos_str}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Pushed to Lifox21/Sectors- [master]</i>"
        )
        return self.send_message(msg)

    def notify_system_alert(self, title: str, details: str) -> bool:
        """General system or watchdog alert."""
        now_str = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            f"⚠️ <b>SYSTEM ALERT: {title}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{details}\n\n"
            f"<b>Timestamp:</b> {now_str} IST"
        )
        return self.send_message(msg)


# Global singleton instance
notifier = TelegramNotifier()


def main():
    parser = argparse.ArgumentParser(description="Test and Configure Telegram Bot Notifications")
    parser.add_argument("--test", type=str, default=None, help="Send a test message to your Telegram chat")
    parser.add_argument("--status", action="store_true", help="Check if Telegram credentials are validly configured")
    parser.add_argument("--token", type=str, default=None, help="Set or test with a specific bot token")
    parser.add_argument("--chat-id", type=str, default=None, help="Set or test with a specific chat ID")

    args = parser.parse_args()
    bot = TelegramNotifier()
    if args.token:
        bot.bot_token = args.token
    if args.chat_id:
        bot.chat_id = args.chat_id

    if args.status or (not args.test):
        print("\n" + "=" * 60)
        print(" [TELEGRAM] BOT CONFIGURATION STATUS")
        print("=" * 60)
        print(f" Configured : {'YES' if bot.is_configured() else 'NO (Missing Token or Chat ID)'}")
        print(f" Enabled    : {bot.enabled}")
        print(f" Bot Token  : {'*' * 10 + bot.bot_token[-5:] if bot.bot_token else 'NOT SET'}")
        print(f" Chat ID    : {bot.chat_id if bot.chat_id else 'NOT SET'}")
        print("=" * 60)

    if args.test:
        print(f"\n[+] Sending test message to Chat ID: {bot.chat_id}...")
        success = bot.send_message(f"🧪 <b>TEST NOTIFICATION</b>\n\n{args.test}\n\n<i>Time: {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')} IST</i>")
        if success:
            print("[SUCCESS] Test message sent! Check your Telegram app.")
        else:
            print("[FAILED] Could not send message. Please verify your Bot Token and Chat ID.")


if __name__ == "__main__":
    main()
