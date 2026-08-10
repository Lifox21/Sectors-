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
| 💰 **Total Net Asset Value (NAV)** | **₹99,900.10** |
| 🏦 **Cash Balance** | **₹0.00** |
| 📊 **Total Return (ROI)** | **-0.0999%** |
| 📅 **Last Synchronization** | **2026-08-10** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 0.5565 | ₹35,900.00 | ₹35,900.00 | ₹19,980.02 | +0.00% | 20.0% |
| **GESHIP** | logistics | 15.0226 | ₹1,330.00 | ₹1,330.00 | ₹19,980.02 | +0.00% | 20.0% |
| **MCX** | financial_infrastructure | 7.1948 | ₹2,777.00 | ₹2,777.00 | ₹19,980.02 | +0.00% | 20.0% |
| **HBLENGINE** | automobiles | 28.7834 | ₹694.15 | ₹694.15 | ₹19,980.02 | +0.00% | 20.0% |
| **POLYCAB** | power_and_utilities | 2.1506 | ₹9,290.50 | ₹9,290.50 | ₹19,980.02 | +0.00% | 20.0% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-10 | **POLYCAB** | `BUY` | 2.1506 | ₹9,290.50 | ₹19.98 | ₹-20,000.00 |
| 2026-08-10 | **HBLENGINE** | `BUY` | 28.7834 | ₹694.15 | ₹19.98 | ₹-20,000.00 |
| 2026-08-10 | **MCX** | `BUY` | 7.1948 | ₹2,777.00 | ₹19.98 | ₹-20,000.00 |
| 2026-08-10 | **GESHIP** | `BUY` | 15.0226 | ₹1,330.00 | ₹19.98 | ₹-20,000.00 |
| 2026-08-10 | **3MINDIA** | `BUY` | 0.5565 | ₹35,900.00 | ₹19.98 | ₹-20,000.00 |

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
