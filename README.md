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
| 💰 **Total Net Asset Value (NAV)** | **₹148,502.41** |
| 🏦 **Cash Balance** | **₹484.41** |
| 📊 **Total Return (ROI)** | **-0.9984%** |
| 📅 **Last Synchronization** | **2026-09-23** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,835.00 | ₹1,817.20 | ₹29,075.20 | -0.97% | 19.6% |
| **3MINDIA** | diversified | 1.0000 | ₹34,220.00 | ₹34,220.00 | ₹34,220.00 | +0.00% | 23.0% |
| **BHARTIHEXA** | telecommunications | 20.0000 | ₹1,534.30 | ₹1,534.30 | ₹30,686.00 | +0.00% | 20.7% |
| **DIXON** | electronics_ems | 2.0000 | ₹13,084.00 | ₹13,084.00 | ₹26,168.00 | +0.00% | 17.6% |
| **SYRMA** | electronics_ems | 16.0000 | ₹1,741.80 | ₹1,741.80 | ₹27,868.80 | +0.00% | 18.8% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-23 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,534.30 | ₹1.53 | ₹-1,535.83 |
| 2026-09-23 | **SYRMA** | `BUY` | 16.0000 | ₹1,741.80 | ₹27.87 | ₹-27,896.67 |
| 2026-09-23 | **DIXON** | `BUY` | 2.0000 | ₹13,084.00 | ₹26.17 | ₹-26,194.17 |
| 2026-09-23 | **POLYCAB** | `SELL` | 3.0000 | ₹8,350.00 | ₹25.05 | +₹25,024.95 |
| 2026-09-23 | **GIPCL** | `SELL` | 166.0000 | ₹186.92 | ₹31.03 | +₹30,997.69 |
| 2026-09-22 | **GIPCL** | `SELL` | 4.0000 | ₹186.92 | ₹0.75 | +₹746.93 |
| 2026-09-22 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,534.30 | ₹29.15 | ₹-29,180.85 |
| 2026-09-22 | **POLYCAB** | `BUY` | 3.0000 | ₹8,350.00 | ₹25.05 | ₹-25,075.05 |
| 2026-09-22 | **3MINDIA** | `BUY` | 1.0000 | ₹34,220.00 | ₹34.22 | ₹-34,254.22 |
| 2026-09-22 | **DIXON** | `SELL` | 2.0000 | ₹13,084.00 | ₹26.17 | +₹26,141.83 |

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
