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
| 💰 **Total Net Asset Value (NAV)** | **₹141,938.43** |
| 🏦 **Cash Balance** | **₹574.59** |
| 📊 **Total Return (ROI)** | **-5.3744%** |
| 📅 **Last Synchronization** | **2026-10-09** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,810.50 | ₹1,804.60 | ₹27,069.00 | -0.33% | 19.1% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,386.80 | ₹1,500.70 | ₹28,513.30 | +8.21% | 20.1% |
| **TATACOMM** | telecommunications | 17.0000 | ₹1,659.60 | ₹1,677.40 | ₹28,515.80 | +1.07% | 20.1% |
| **GESHIP** | logistics | 18.0000 | ₹1,567.90 | ₹1,529.70 | ₹27,534.60 | -2.44% | 19.4% |
| **HBLENGINE** | automobiles | 41.0000 | ₹762.45 | ₹725.15 | ₹29,731.15 | -4.89% | 20.9% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-10-09 | **HBLENGINE** | `BUY` | 2.0000 | ₹725.15 | ₹1.45 | ₹-1,451.75 |
| 2026-10-09 | **BHARTIHEXA** | `SELL` | 1.0000 | ₹1,500.70 | ₹1.50 | +₹1,499.20 |
| 2026-10-08 | **HBLENGINE** | `BUY` | 39.0000 | ₹762.45 | ₹29.74 | ₹-29,765.29 |
| 2026-10-08 | **GESHIP** | `BUY` | 18.0000 | ₹1,567.90 | ₹28.22 | ₹-28,250.42 |
| 2026-10-08 | **TATACOMM** | `BUY` | 17.0000 | ₹1,659.60 | ₹28.21 | ₹-28,241.41 |
| 2026-10-08 | **SARDAEN** | `SELL` | 57.0000 | ₹499.35 | ₹28.46 | +₹28,434.49 |
| 2026-10-08 | **HINDZINC** | `SELL` | 50.0000 | ₹551.00 | ₹27.55 | +₹27,522.45 |
| 2026-10-08 | **3MINDIA** | `SELL` | 1.0000 | ₹30,825.00 | ₹30.82 | +₹30,794.17 |
| 2026-10-07 | **SARDAEN** | `BUY` | 57.0000 | ₹500.70 | ₹28.54 | ₹-28,568.44 |
| 2026-10-07 | **HINDZINC** | `BUY` | 50.0000 | ₹557.65 | ₹27.88 | ₹-27,910.38 |

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
