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
| 💰 **Total Net Asset Value (NAV)** | **₹147,443.25** |
| 🏦 **Cash Balance** | **₹137.85** |
| 📊 **Total Return (ROI)** | **-1.7045%** |
| 📅 **Last Synchronization** | **2026-09-10** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MCX** | financial_infrastructure | 8.0000 | ₹3,342.00 | ₹3,300.00 | ₹26,400.00 | -1.26% | 17.9% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,673.00 | ₹4,545.00 | ₹27,270.00 | -2.74% | 18.5% |
| **3MINDIA** | diversified | 1.0000 | ₹32,800.00 | ₹32,800.00 | ₹32,800.00 | +0.00% | 22.2% |
| **GESHIP** | logistics | 21.0000 | ₹1,400.20 | ₹1,400.20 | ₹29,404.20 | +0.00% | 19.9% |
| **IGIL** | miscellaneous | 101.0000 | ₹311.20 | ₹311.20 | ₹31,431.20 | +0.00% | 21.3% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-10 | **IGIL** | `BUY` | 101.0000 | ₹311.20 | ₹31.43 | ₹-31,462.63 |
| 2026-09-10 | **GESHIP** | `BUY` | 21.0000 | ₹1,400.20 | ₹29.40 | ₹-29,433.60 |
| 2026-09-10 | **MCX** | `SELL` | 1.0000 | ₹3,300.00 | ₹3.30 | +₹3,296.70 |
| 2026-09-10 | **3MINDIA** | `BUY` | 1.0000 | ₹32,800.00 | ₹32.80 | ₹-32,832.80 |
| 2026-09-10 | **BHARTIHEXA** | `SELL` | 21.0000 | ₹1,539.20 | ₹32.32 | +₹32,290.88 |
| 2026-09-10 | **DIXON** | `SELL` | 2.0000 | ₹13,500.00 | ₹27.00 | +₹26,973.00 |
| 2026-09-10 | **BHARTIARTL** | `SELL` | 17.0000 | ₹1,839.00 | ₹31.26 | +₹31,231.74 |
| 2026-09-09 | **BHARTIHEXA** | `BUY` | 21.0000 | ₹1,544.80 | ₹32.44 | ₹-32,473.24 |
| 2026-09-09 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,814.70 | ₹1.81 | ₹-1,816.51 |
| 2026-09-09 | **MCX** | `BUY` | 1.0000 | ₹3,350.00 | ₹3.35 | ₹-3,353.35 |

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
