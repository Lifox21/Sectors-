# COEP Quantitative Finance Club HMM Sector Trading System

This repository implements a **Gaussian Hidden Markov Model (HMM)** sector-switching and ranking trading pipeline. The strategy uses sector regime shifts to dynamically reallocate capital away from bearish sectors into equal-weighted positions in top-performing stocks of bullish sectors.

---

## 📈 Live Paper Portfolio Dashboard

> [!NOTE]
> This paper portfolio was initialized on **August 10, 2026** with a starting capital of **₹100,000.00**.
> The metrics below are automatically updated at daily market close.

### 📊 Portfolio Summary

| Metric | Value |
| :--- | :--- |
| 💰 **Total Net Asset Value (NAV)** | **₹99,922.62** |
| 🏦 **Cash Balance** | **₹22,542.22** |
| 📊 **Total Return (ROI)** | **-0.0774%** |
| 📅 **Last Synchronization** | **2026-08-10** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GESHIP** | logistics | 15.0000 | ₹1,329.60 | ₹1,329.60 | ₹19,944.00 | +0.00% | 20.0% |
| **MCX** | financial_infrastructure | 7.0000 | ₹2,777.00 | ₹2,777.00 | ₹19,439.00 | +0.00% | 19.5% |
| **HBLENGINE** | automobiles | 28.0000 | ₹694.55 | ₹694.55 | ₹19,447.40 | +0.00% | 19.5% |
| **POLYCAB** | power_and_utilities | 2.0000 | ₹9,275.00 | ₹9,275.00 | ₹18,550.00 | +0.00% | 18.6% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-10 | **POLYCAB** | `BUY` | 2.0000 | ₹9,275.00 | ₹18.55 | ₹-18,568.55 |
| 2026-08-10 | **HBLENGINE** | `BUY` | 28.0000 | ₹694.55 | ₹19.45 | ₹-19,466.85 |
| 2026-08-10 | **MCX** | `BUY` | 7.0000 | ₹2,777.00 | ₹19.44 | ₹-19,458.44 |
| 2026-08-10 | **GESHIP** | `BUY` | 15.0000 | ₹1,329.60 | ₹19.94 | ₹-19,963.94 |

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
