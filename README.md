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
| 💰 **Total Net Asset Value (NAV)** | **₹149,243.27** |
| 🏦 **Cash Balance** | **₹74.57** |
| 📊 **Total Return (ROI)** | **-0.5045%** |
| 📅 **Last Synchronization** | **2026-09-09** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 17.0000 | ₹1,862.80 | ₹1,814.70 | ₹30,849.90 | -2.58% | 20.7% |
| **MCX** | financial_infrastructure | 9.0000 | ₹3,342.00 | ₹3,350.00 | ₹30,150.00 | +0.24% | 20.2% |
| **DIXON** | electronics_ems | 2.0000 | ₹13,845.00 | ₹13,845.00 | ₹27,690.00 | +0.00% | 18.6% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,673.00 | ₹4,673.00 | ₹28,038.00 | +0.00% | 18.8% |
| **BHARTIHEXA** | telecommunications | 21.0000 | ₹1,544.80 | ₹1,544.80 | ₹32,440.80 | +0.00% | 21.7% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-09 | **BHARTIHEXA** | `BUY` | 21.0000 | ₹1,544.80 | ₹32.44 | ₹-32,473.24 |
| 2026-09-09 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,814.70 | ₹1.81 | ₹-1,816.51 |
| 2026-09-09 | **MCX** | `BUY` | 1.0000 | ₹3,350.00 | ₹3.35 | ₹-3,353.35 |
| 2026-09-09 | **GVT&D** | `BUY` | 6.0000 | ₹4,673.00 | ₹28.04 | ₹-28,066.04 |
| 2026-09-09 | **DIXON** | `BUY` | 2.0000 | ₹13,845.00 | ₹27.69 | ₹-27,717.69 |
| 2026-09-09 | **HBLENGINE** | `SELL` | 42.0000 | ₹730.10 | ₹30.66 | +₹30,633.53 |
| 2026-09-09 | **GESHIP** | `SELL` | 21.0000 | ₹1,393.40 | ₹29.26 | +₹29,232.14 |
| 2026-09-09 | **3MINDIA** | `SELL` | 1.0000 | ₹33,025.00 | ₹33.02 | +₹32,991.97 |
| 2026-09-08 | **HBLENGINE** | `BUY` | 42.0000 | ₹731.25 | ₹30.71 | ₹-30,743.21 |
| 2026-09-08 | **GESHIP** | `BUY` | 21.0000 | ₹1,383.80 | ₹29.06 | ₹-29,088.86 |

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
