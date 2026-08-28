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
| 💰 **Total Net Asset Value (NAV)** | **₹151,323.56** |
| 🏦 **Cash Balance** | **₹126.26** |
| 📊 **Total Return (ROI)** | **+0.8824%** |
| 📅 **Last Synchronization** | **2026-08-28** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,947.00 | ₹1,878.30 | ₹30,052.80 | -3.53% | 19.9% |
| **HBLENGINE** | automobiles | 48.0000 | ₹683.90 | ₹665.75 | ₹31,956.00 | -2.65% | 21.1% |
| **DIXON** | electronics_ems | 2.0000 | ₹14,711.00 | ₹14,711.00 | ₹29,422.00 | +0.00% | 19.4% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,551.10 | ₹1,551.10 | ₹29,470.90 | +0.00% | 19.5% |
| **GESHIP** | logistics | 23.0000 | ₹1,317.20 | ₹1,317.20 | ₹30,295.60 | +0.00% | 20.0% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-28 | **HBLENGINE** | `BUY` | 3.0000 | ₹665.75 | ₹2.00 | ₹-1,999.25 |
| 2026-08-28 | **GESHIP** | `BUY` | 23.0000 | ₹1,317.20 | ₹30.30 | ₹-30,325.89 |
| 2026-08-28 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,551.10 | ₹29.47 | ₹-29,500.37 |
| 2026-08-28 | **DIXON** | `BUY` | 2.0000 | ₹14,711.00 | ₹29.42 | ₹-29,451.42 |
| 2026-08-28 | **GVT&D** | `SELL` | 6.0000 | ₹4,407.80 | ₹26.45 | +₹26,420.35 |
| 2026-08-28 | **3MINDIA** | `SELL` | 1.0000 | ₹34,245.00 | ₹34.24 | +₹34,210.75 |
| 2026-08-28 | **HINDZINC** | `SELL` | 50.0000 | ₹610.10 | ₹30.50 | +₹30,474.49 |
| 2026-08-27 | **HINDZINC** | `BUY` | 1.0000 | ₹610.10 | ₹0.61 | ₹-610.71 |
| 2026-08-27 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,878.30 | ₹1.88 | ₹-1,880.18 |
| 2026-08-27 | **GVT&D** | `BUY` | 6.0000 | ₹4,407.80 | ₹26.45 | ₹-26,473.25 |

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
