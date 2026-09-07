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
| 💰 **Total Net Asset Value (NAV)** | **₹149,561.55** |
| 🏦 **Cash Balance** | **₹258.99** |
| 📊 **Total Return (ROI)** | **-0.2923%** |
| 📅 **Last Synchronization** | **2026-09-07** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 17.0000 | ₹1,862.80 | ₹1,840.00 | ₹31,280.00 | -1.22% | 20.9% |
| **DIXON** | electronics_ems | 2.0000 | ₹14,240.00 | ₹14,240.00 | ₹28,480.00 | +0.00% | 19.0% |
| **POLYCAB** | power_and_utilities | 3.0000 | ₹8,300.00 | ₹8,300.00 | ₹24,900.00 | +0.00% | 16.6% |
| **BHARTIHEXA** | telecommunications | 21.0000 | ₹1,495.40 | ₹1,495.40 | ₹31,403.40 | +0.00% | 21.0% |
| **GIPCL** | power_and_utilities | 162.0000 | ₹205.18 | ₹205.18 | ₹33,239.16 | +0.00% | 22.2% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-07 | **GIPCL** | `BUY` | 162.0000 | ₹205.18 | ₹33.24 | ₹-33,272.40 |
| 2026-09-07 | **BHARTIHEXA** | `BUY` | 21.0000 | ₹1,495.40 | ₹31.40 | ₹-31,434.80 |
| 2026-09-07 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,840.00 | ₹1.84 | ₹-1,841.84 |
| 2026-09-07 | **POLYCAB** | `BUY` | 3.0000 | ₹8,300.00 | ₹24.90 | ₹-24,924.90 |
| 2026-09-07 | **GESHIP** | `SELL` | 23.0000 | ₹1,369.70 | ₹31.50 | +₹31,471.60 |
| 2026-09-07 | **3MINDIA** | `SELL` | 1.0000 | ₹32,845.00 | ₹32.84 | +₹32,812.15 |
| 2026-09-07 | **MCX** | `SELL` | 8.0000 | ₹3,275.40 | ₹26.20 | +₹26,177.00 |
| 2026-09-04 | **GESHIP** | `BUY` | 23.0000 | ₹1,369.70 | ₹31.50 | ₹-31,534.60 |
| 2026-09-04 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,840.00 | ₹1.84 | ₹-1,841.84 |
| 2026-09-04 | **MCX** | `SELL` | 1.0000 | ₹3,275.40 | ₹3.28 | +₹3,272.12 |

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
