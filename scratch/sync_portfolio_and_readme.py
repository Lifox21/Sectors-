"""Legacy entry point for the causal daily paper-trading workflow."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from paper_trading import run_daily_pipeline


if __name__ == "__main__":
    run_daily_pipeline()
