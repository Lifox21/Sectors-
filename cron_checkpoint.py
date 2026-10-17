"""Dedicated Cron Checkpoint & Watchdog Runner for HMM Sector Trading System.

Designed to be invoked by Linux crontab or Windows Task Scheduler to guarantee
zero-delay execution at exact Indian market timings (IST).
Pushes updates directly to the 'lifox' repository.
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

IST = ZoneInfo("Asia/Kolkata")
ROOT_DIR = Path(__file__).resolve().parent
LOG_DIR = ROOT_DIR / "scratch"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "cron_run.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [CRON] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
    ],
)
logger = logging.getLogger("CronRunner")


def is_process_running(process_name_pattern: str) -> bool:
    """Check if a process matching pattern is currently running."""
    try:
        if sys.platform == "win32":
            cmd = f'powershell "Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like \'*{process_name_pattern}*\' }} | Select-Object -ExpandProperty ProcessId"'
            out = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
            # If any line contains a PID other than current process
            pids = [p for p in out.splitlines() if p.strip() and p.strip() != str(os.getpid())]
            return len(pids) > 0
        else:
            res = subprocess.run(["pgrep", "-f", process_name_pattern], capture_output=True, text=True)
            pids = [p for p in res.stdout.strip().split() if p and p != str(os.getpid())]
            return len(pids) > 0
    except Exception as exc:
        logger.warning(f"Process check failed: {exc}")
        return False


def run_bot_once(remote: str = "lifox", branch: str = "master", force_active: bool = False) -> int:
    """Execute a single complete trading bot evaluation cycle."""
    cmd = [
        sys.executable,
        str(ROOT_DIR / "trading_bot.py"),
        "--once",
        "--auto-push",
        "--remote",
        remote,
        "--branch",
        branch,
    ]
    if force_active:
        cmd.append("--force-active")

    logger.info(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(ROOT_DIR), text=True)
    return result.returncode


def run_watchdog(remote: str = "lifox") -> None:
    """Ensure continuous trading bot daemon is running during market hours."""
    now = datetime.now(IST)
    is_weekday = now.weekday() < 5
    market_open = now.time() >= datetime.strptime("09:10", "%H:%M").time()
    market_close = now.time() <= datetime.strptime("15:35", "%H:%M").time()

    if not (is_weekday and market_open and market_close):
        logger.info(f"Watchdog: Outside market hours ({now.strftime('%H:%M:%S')} IST). Continuous bot is in standby or stopped.")
        return

    pattern = "trading_bot.py --loop"
    running = is_process_running(pattern)
    if running:
        logger.info("Watchdog: Continuous bot daemon is healthy and running.")
    else:
        logger.warning("Watchdog: Continuous bot daemon is NOT running during market hours! Auto-starting...")
        if sys.platform == "win32":
            vbs_script = ROOT_DIR / "start_bot_background.vbs"
            if vbs_script.exists():
                subprocess.Popen(["wscript.exe", str(vbs_script)], cwd=str(ROOT_DIR))
            else:
                subprocess.Popen(
                    [sys.executable, str(ROOT_DIR / "trading_bot.py"), "--loop", "--interval", "60", "--remote", remote],
                    cwd=str(ROOT_DIR),
                    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                )
        else:
            # Check if systemd service exists
            res = subprocess.run(["systemctl", "is-active", "hmm_bot"], capture_output=True, text=True)
            if "active" in res.stdout:
                logger.info("Watchdog: systemd hmm_bot service is active.")
            else:
                logger.warning("Watchdog: Restarting systemd service hmm_bot...")
                subprocess.run(["sudo", "systemctl", "restart", "hmm_bot"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Zero-Delay Scheduled Cron Runner for HMM Trading Bot")
    parser.add_argument(
        "--action",
        choices=["run-once", "market-open", "hourly-check", "rebalance", "market-close", "eod-sync", "watchdog"],
        default="run-once",
        help="Action to execute at this scheduled interval",
    )
    parser.add_argument("--remote", default="lifox", help="Git remote to sync with (default: lifox)")
    parser.add_argument("--branch", default="master", help="Git branch to sync with (default: master)")
    parser.add_argument("--force", action="store_true", help="Force execution even outside market hours")

    args = parser.parse_args()
    now_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"=== Scheduled Cron Trigger: [{args.action.upper()}] at {now_ist} IST ===")

    if args.action == "watchdog":
        run_watchdog(remote=args.remote)
        return

    # Checkpoint executions
    force = args.force or (args.action in ["market-close", "eod-sync"])
    rc = run_bot_once(remote=args.remote, branch=args.branch, force_active=force)
    if rc == 0:
        logger.info(f"=== Cron Action [{args.action.upper()}] Completed Successfully ===")
    else:
        logger.error(f"=== Cron Action [{args.action.upper()}] Failed with exit code {rc} ===")
        sys.exit(rc)


if __name__ == "__main__":
    main()
