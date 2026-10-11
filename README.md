# COEP Quantitative Finance Club - HMM Sector Rotation Strategy

An institutional-grade quantitative equity trading system leveraging **Hidden Markov Models (Gaussian HMM)** to detect macro regime transitions across Indian NSE sectors, coupled with an automated high-efficiency execution engine with turnover dampeners and statutory tax modeling.

---

## Live Portfolio Dashboard (Paper Trading)

| Metric | Value |
| :--- | ---: |
| **Initial Capital** | ₹150,000.00 |
| **Current NAV** | ₹142,016.78 |
| **Return Since Inception** | -5.32% |
| **Cash Balance** | ₹574.59 (0.4%) |
| **Active Bullish Sector** | Automobiles |
| **Latest Valuation Date** | 2026-10-11 |
| **Rebalance Order Queue** | Next Market Open |

### Current Active Holdings

| Symbol | Shares | Average Cost | Latest Price | Market Value | Unrealized P&L |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **BHARTIARTL** | 15 | ₹1,810.50 | ₹1,805.10 | ₹27,076.50 | -0.30% |
| **BHARTIHEXA** | 19 | ₹1,386.80 | ₹1,532.00 | ₹29,108.00 | **+10.47%** |
| **TATACOMM** | 17 | ₹1,659.60 | ₹1,656.70 | ₹28,163.90 | -0.17% |
| **GESHIP** | 18 | ₹1,567.90 | ₹1,533.70 | ₹27,606.60 | -2.18% |
| **HBLENGINE** | 41 | ₹762.45 | ₹719.20 | ₹29,487.20 | -5.67% |

---

## 2022–2026 Walk-Forward Benchmark (Net of All Indian Taxes & Slippage)

A comprehensive out-of-sample backtest was conducted over **2022 to 2026** comparing naive daily rebalancing against the newly implemented turnover-dampened architecture, incorporating full statutory Indian cash delivery friction (STT 0.1% on sell, Stamp Duty 0.015% on buy, Exchange Turnover, SEBI Fees, 18% GST, DP charges, and 10 bps slippage):

| Metric | Naive Daily (No Caps) | Enhanced Architecture (Turnover Dampeners) | Monthly Benchmark |
| :--- | :---: | :---: | :---: |
| **Initial Capital** | ₹1,50,000 | ₹1,50,000 | ₹1,50,000 |
| **Ending NAV** | ₹4,40,496 | **₹5,23,290** | ₹5,77,073 |
| **Total Net Return** | +193.66% | **+248.86%** | +284.72% |
| **Annualized CAGR** | 26.94% | **31.88%** | 34.76% |
| **Sharpe Ratio (Rf=6.5%)** | 0.95 | **1.08** | 1.25 |
| **Max Drawdown** | -25.17% | **-23.96%** | -21.30% |
| **Total Trades Executed** | 796 | **454 (-43%)** | 222 |
| **Taxes & Friction Paid** | ₹53,233 | **₹31,816 (-40%)** | ₹18,558 |
| **Exit Win Rate** | 51.6% | 45.1% | 57.0% |

> **Key Quantitative Takeaway**: The **Enhanced Architecture** eliminates 342 wasteful churn trades and saves **₹21,417** in statutory tax bleed, boosting overall net CAGR by **+4.94% annualized** with lower maximum drawdown.

---

## Continuous Automated Execution Architecture

The system supports two continuous execution modes that run **without requiring your personal laptop to stay on**:

### 1. GitHub Actions Cloud Automation (100% Free, Built-In)
- Configured in [`.github/workflows/daily_sync.yml`](.github/workflows/daily_sync.yml).
- Automatically triggers across Indian trading hours (09:15 AM to 03:30 PM IST Monday–Friday) every 30 minutes.
- Updates live portfolio valuations, processes queued orders, enforces stop-losses, and commits updated records back to GitHub with `[skip ci]`.

### 2. Dedicated Cloud VPS Daemon (24/7 Real-Time Polling)
- Uses [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/) or AWS EC2.
- 1-Click setup via [`deploy/setup_vps.sh`](deploy/setup_vps.sh).
- Configures a Linux `systemd` daemon ([`deploy/hmm_bot.service`](deploy/hmm_bot.service)) that polls ticks every 60 seconds, enforces sub-minute stop-loss exits, and auto-pushes state to GitHub every 15 minutes.

---

## Local Execution Commands

- **Interactive Dashboard Runner**: Double-click [`run_trading_bot.bat`](run_trading_bot.bat)
- **Silent Background Process**: Double-click [`start_bot_background.vbs`](start_bot_background.vbs)
- **Stop Running Bot**: Double-click [`stop_bot.bat`](stop_bot.bat)
- **Run Benchmark Simulation**:
  ```bash
  python scratch/run_walkforward_turnover_benchmark.py
  ```

