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
| 💰 **Total Net Asset Value (NAV)** | **₹150,976.21** |
| 🏦 **Cash Balance** | **₹499.41** |
| 📊 **Total Return (ROI)** | **+0.6508%** |
| 📅 **Last Synchronization** | **2026-08-25** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GVT&D** | miscellaneous | 7.0000 | ₹4,185.00 | ₹4,185.00 | ₹29,295.00 | +0.00% | 19.4% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,947.00 | ₹1,947.00 | ₹29,205.00 | +0.00% | 19.3% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,592.90 | ₹1,592.90 | ₹30,265.10 | +0.00% | 20.0% |
| **HINDZINC** | metals_and_mining | 52.0000 | ₹592.60 | ₹592.60 | ₹30,815.20 | +0.00% | 20.4% |
| **SARDAEN** | metals_and_mining | 61.0000 | ₹506.50 | ₹506.50 | ₹30,896.50 | +0.00% | 20.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-25 | **SARDAEN** | `BUY` | 61.0000 | ₹506.50 | ₹30.90 | ₹-30,927.40 |
| 2026-08-25 | **HINDZINC** | `BUY` | 52.0000 | ₹592.60 | ₹30.82 | ₹-30,846.01 |
| 2026-08-25 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,592.90 | ₹30.27 | ₹-30,295.37 |
| 2026-08-25 | **BHARTIARTL** | `BUY` | 15.0000 | ₹1,947.00 | ₹29.20 | ₹-29,234.21 |
| 2026-08-25 | **GVT&D** | `BUY` | 7.0000 | ₹4,185.00 | ₹29.30 | ₹-29,324.29 |
| 2026-08-25 | **DLF** | `SELL` | 44.0000 | ₹682.95 | ₹30.05 | +₹30,019.75 |
| 2026-08-25 | **SIKA** | `SELL` | 29.0000 | ₹1,017.70 | ₹29.51 | +₹29,483.79 |
| 2026-08-25 | **RADICO** | `SELL` | 6.0000 | ₹4,630.00 | ₹27.78 | +₹27,752.22 |
| 2026-08-25 | **3MINDIA** | `SELL` | 1.0000 | ₹33,695.00 | ₹33.70 | +₹33,661.31 |
| 2026-08-25 | **HBLENGINE** | `SELL` | 43.0000 | ₹694.60 | ₹29.87 | +₹29,837.93 |

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
