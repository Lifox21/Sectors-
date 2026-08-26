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
| 💰 **Total Net Asset Value (NAV)** | **₹153,196.21** |
| 🏦 **Cash Balance** | **₹312.31** |
| 📊 **Total Return (ROI)** | **+2.1308%** |
| 📅 **Last Synchronization** | **2026-08-26** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,947.00 | ₹1,902.10 | ₹28,531.50 | -2.31% | 18.6% |
| **HINDZINC** | metals_and_mining | 49.0000 | ₹592.60 | ₹626.50 | ₹30,698.50 | +5.72% | 20.0% |
| **3MINDIA** | diversified | 1.0000 | ₹33,570.00 | ₹33,570.00 | ₹33,570.00 | +0.00% | 21.9% |
| **GESHIP** | logistics | 22.0000 | ₹1,332.20 | ₹1,332.20 | ₹29,308.40 | +0.00% | 19.1% |
| **HBLENGINE** | automobiles | 45.0000 | ₹683.90 | ₹683.90 | ₹30,775.50 | +0.00% | 20.1% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-26 | **HINDZINC** | `SELL` | 3.0000 | ₹626.50 | ₹1.88 | +₹1,877.62 |
| 2026-08-26 | **HBLENGINE** | `BUY` | 45.0000 | ₹683.90 | ₹30.78 | ₹-30,806.28 |
| 2026-08-26 | **GESHIP** | `BUY` | 22.0000 | ₹1,332.20 | ₹29.31 | ₹-29,337.71 |
| 2026-08-26 | **3MINDIA** | `BUY` | 1.0000 | ₹33,570.00 | ₹33.57 | ₹-33,603.57 |
| 2026-08-26 | **SARDAEN** | `SELL` | 61.0000 | ₹514.40 | ₹31.38 | +₹31,347.02 |
| 2026-08-26 | **BHARTIHEXA** | `SELL` | 19.0000 | ₹1,579.80 | ₹30.02 | +₹29,986.18 |
| 2026-08-26 | **GVT&D** | `SELL` | 7.0000 | ₹4,340.00 | ₹30.38 | +₹30,349.62 |
| 2026-08-25 | **SARDAEN** | `BUY` | 61.0000 | ₹506.50 | ₹30.90 | ₹-30,927.40 |
| 2026-08-25 | **HINDZINC** | `BUY` | 52.0000 | ₹592.60 | ₹30.82 | ₹-30,846.01 |
| 2026-08-25 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,592.90 | ₹30.27 | ₹-30,295.37 |

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
