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
| 💰 **Total Net Asset Value (NAV)** | **₹151,099.14** |
| 🏦 **Cash Balance** | **₹297.59** |
| 📊 **Total Return (ROI)** | **+0.7328%** |
| 📅 **Last Synchronization** | **2026-08-27** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,947.00 | ₹1,878.30 | ₹30,052.80 | -3.53% | 19.9% |
| **HINDZINC** | metals_and_mining | 50.0000 | ₹592.60 | ₹610.10 | ₹30,505.00 | +2.95% | 20.2% |
| **3MINDIA** | diversified | 1.0000 | ₹33,570.00 | ₹34,245.00 | ₹34,245.00 | +2.01% | 22.7% |
| **HBLENGINE** | automobiles | 45.0000 | ₹683.90 | ₹665.75 | ₹29,958.75 | -2.65% | 19.8% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,407.80 | ₹4,340.00 | ₹26,040.00 | -1.54% | 17.2% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-27 | **HINDZINC** | `BUY` | 1.0000 | ₹610.10 | ₹0.61 | ₹-610.71 |
| 2026-08-27 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,878.30 | ₹1.88 | ₹-1,880.18 |
| 2026-08-27 | **GVT&D** | `BUY` | 6.0000 | ₹4,407.80 | ₹26.45 | ₹-26,473.25 |
| 2026-08-27 | **GESHIP** | `SELL` | 22.0000 | ₹1,317.20 | ₹28.98 | +₹28,949.42 |
| 2026-08-26 | **HINDZINC** | `SELL` | 3.0000 | ₹626.50 | ₹1.88 | +₹1,877.62 |
| 2026-08-26 | **HBLENGINE** | `BUY` | 45.0000 | ₹683.90 | ₹30.78 | ₹-30,806.28 |
| 2026-08-26 | **GESHIP** | `BUY` | 22.0000 | ₹1,332.20 | ₹29.31 | ₹-29,337.71 |
| 2026-08-26 | **3MINDIA** | `BUY` | 1.0000 | ₹33,570.00 | ₹33.57 | ₹-33,603.57 |
| 2026-08-26 | **SARDAEN** | `SELL` | 61.0000 | ₹514.40 | ₹31.38 | +₹31,347.02 |
| 2026-08-26 | **BHARTIHEXA** | `SELL` | 19.0000 | ₹1,579.80 | ₹30.02 | +₹29,986.18 |

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
