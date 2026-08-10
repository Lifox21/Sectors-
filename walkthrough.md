# Walkthrough: HMM Paper Trading & Automated Daily Pipelines

This walkthrough guide covers the paper trading system and the automated daily pipelines created for the **COEP Quantitative Finance Club HMM strategy**.

---

## 1. Local Paper Trading Environment

The local paper trading files are stored in the workspace:
1. **[live_paper_trading.py](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/live_paper_trading.py)**: The main execution module providing an interactive command-line interface (CLI) to track your portfolio, perform walk-forward HMM calculations, evaluate stock scores, and log trades.
2. **[paper_portfolio_state.json](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scratch/paper_portfolio_state.json)**: The JSON state ledger containing your current virtual cash balance, active equity holdings, average buy prices, current prices, and the daily Net Asset Value (NAV) history.
3. **[paper_trade_log.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scratch/paper_trade_log.csv)**: A CSV transaction ledger listing Date, Ticker, Action (BUY/SELL), Shares, Price, Commission (10 bps), and total cash impact.

### How to Run:
Launch the interactive CLI:
```bash
python live_paper_trading.py
```

---

## 2. Automated Daily Market Sync Pipelines

We have built two automated sync engines to ensure your database is updated daily with live market closes and the HMM models are evaluated automatically:

### A. GitHub Actions Remote Sync Workflow
We created a GitHub Action configuration file:
* **File path**: [`.github/workflows/daily_sync.yml`](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/.github/workflows/daily_sync.yml)
* **Trigger Schedule**: Mon-Fri at **11:30 AM UTC (5:00 PM IST)**. Can also be triggered manually using the "Run workflow" button in your GitHub repository's Actions tab.
* **Function**: 
  1. Installs dependencies (`pandas`, `numpy`, `hmmlearn`, `yfinance`).
  2. Runs `python scratch/sync_live_and_get_signals.py` to sync today's closes and check if there are signal changes (sectors or top 5 stocks) compared to yesterday.
  3. **Automated Issue Notifications**: If a change in signals is detected, it automatically creates a new GitHub Issue in your repository titled `ACTION REQUIRED: HMM Portfolio Rebalance - [DATE]` containing the exact buy, sell, and hold action plan.
  4. Commits the updated daily CSV price files and pushes them back to your repository.

> [!IMPORTANT]
> **Workflow Permission**: Ensure that you have enabled write permissions in your GitHub Repository settings. 
> Under `Settings -> Actions -> General -> Workflow permissions`, select **"Read and write permissions"** so the runner can create issues and push commits back.

### B. Local Runner & Scheduler
* **File path**: [`run_daily_local.bat`](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/run_daily_local.bat)
* **Local Log**: [`scratch/daily_run_log.txt`](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scratch/daily_run_log.txt)
* **Function**: Executes the sync script locally and appends stdout/stderr to a text log.
* **Local Cron Job**: Set up in the IDE background to trigger every Mon-Fri at **4:30 PM IST** to wake up the agent, run the sync, and print today's stock recommendations.

---

## 3. Git Repository Remote Setup

The workspace is now initialized as a Git repository and mapped to your private repository:
* **Remote origin**: `https://github.com/Ved-2107/Sectors.git`
* **Staged & Committed files**: Includes all Python code files, `.gitignore`, `.github/workflows/daily_sync.yml`, custom index database files under `Indices/Daily/`, and scoring sheets.
* **Ignored files**: Large HTML templates (`quant_club_sector_terminal.html`), large raw JSON files (`regime_analysis_data.json`), and temporary database state ledgers are ignored to keep the repository history clean.

### Finalizing the Code Push:
To push any local changes to GitHub, run the following in your terminal:
```bash
git push
```
