# COEP Quantitative Finance Club HMM Sector Trading System

This repository implements a Gaussian Hidden Markov Model sector-switching and ranking trading pipeline. The strategy uses sector regime shifts to dynamically reallocate capital away from bearish sectors into equal-weighted positions in top-performing stocks from bullish sectors.

---

## Live Paper Portfolio Dashboard

> [!NOTE]
> This paper portfolio starts on **August 10, 2026** with **INR 150,000.00**.
> No live/paper stock positions are assumed before the first 9:30 AM IST execution.

### Portfolio Summary

| Metric | Value |
| :--- | :--- |
| **Total Net Asset Value (NAV)** | **INR 150,000.00** |
| **Cash Balance** | **INR 150,000.00** |
| **Total Return (ROI)** | **+0.0000%** |
| **Last Synchronization** | **2026-08-10** |
| **Portfolio Start Date** | **2026-08-10** |
| **Execution Rule** | **Trades are recorded only during the 9:30 AM IST execution window** |

---

### Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| No active holdings. Currently 100% in cash. | | | | | | | |

---

### Recent Transactions Log

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| No transactions logged yet. | | | | | | |

---

## Running the Local Platform

### 1. Requirements

```bash
pip install numpy pandas hmmlearn yfinance
```

### 2. Launch the Interactive Trading Terminal

```bash
python live_paper_trading.py
```

### 3. Trigger Manual Update

```bash
python scratch/sync_portfolio_and_readme.py
```
