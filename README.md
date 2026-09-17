# COEP Quantitative Finance Club HMM Sector Trading System

This repository implements a **Gaussian Hidden Markov Model (HMM)** sector-switching and ranking trading pipeline. The strategy uses sector regime shifts to dynamically reallocate capital away from bearish sectors into equal-weighted positions in top-performing stocks of bullish sectors.

---

## 📈 Live Paper Portfolio Dashboard

> [!NOTE]
> This paper portfolio was initialized on **August 10, 2026** with a starting capital of **₹150,000.00**.
> The metrics below are automatically updated at daily market close.

### 📊 Portfolio Summary

| Metric | Value |
| :--- | :--- |
| 💰 **Total Net Asset Value (NAV)** | **₹145,093.06** |
| 🏦 **Cash Balance** | **₹537.46** |
| 📊 **Total Return (ROI)** | **-3.2713%** |
| 📅 **Last Synchronization** | **2026-09-17** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹32,800.00 | ₹31,935.00 | ₹31,935.00 | -2.64% | 22.0% |
| **HINDZINC** | metals_and_mining | 52.0000 | ₹560.90 | ₹567.50 | ₹29,510.00 | +1.18% | 20.3% |
| **DIXON** | electronics_ems | 2.0000 | ₹13,181.00 | ₹13,181.00 | ₹26,362.00 | +0.00% | 18.2% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,835.00 | ₹1,835.00 | ₹27,525.00 | +0.00% | 19.0% |
| **GESHIP** | logistics | 21.0000 | ₹1,391.60 | ₹1,391.60 | ₹29,223.60 | +0.00% | 20.1% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-17 | **HINDZINC** | `BUY` | 2.0000 | ₹567.50 | ₹1.14 | ₹-1,136.13 |
| 2026-09-17 | **GESHIP** | `BUY` | 21.0000 | ₹1,391.60 | ₹29.22 | ₹-29,252.82 |
| 2026-09-17 | **BHARTIARTL** | `BUY` | 15.0000 | ₹1,835.00 | ₹27.52 | ₹-27,552.53 |
| 2026-09-17 | **DIXON** | `BUY` | 2.0000 | ₹13,181.00 | ₹26.36 | ₹-26,388.36 |
| 2026-09-17 | **HINDCOPPER** | `SELL` | 58.0000 | ₹481.60 | ₹27.93 | +₹27,904.87 |
| 2026-09-17 | **SARDAEN** | `SELL` | 57.0000 | ₹497.35 | ₹28.35 | +₹28,320.60 |
| 2026-09-17 | **LODHA** | `SELL` | 26.0000 | ₹1,087.40 | ₹28.27 | +₹28,244.13 |
| 2026-09-16 | **HINDCOPPER** | `BUY` | 58.0000 | ₹490.24 | ₹28.43 | ₹-28,462.36 |
| 2026-09-16 | **SARDAEN** | `BUY` | 57.0000 | ₹501.35 | ₹28.58 | ₹-28,605.53 |
| 2026-09-16 | **HINDZINC** | `BUY` | 50.0000 | ₹560.90 | ₹28.05 | ₹-28,073.05 |

---

## 🚀 Running the Local Platform

### 1. Requirements
Install the dependencies:
```bash
pip install numpy pandas hmmlearn yfinance
```

### 2. Launch the Interactive Trading Terminal
Start the local CLI tool to review historical runs, check scores, or manage state:
```bash
python live_paper_trading.py
```

### 3. Trigger Manual Update
To trigger the synchronizer manually:
```bash
python scratch/sync_portfolio_and_readme.py
```
