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
| 💰 **Total Net Asset Value (NAV)** | **₹149,801.06** |
| 🏦 **Cash Balance** | **₹643.76** |
| 📊 **Total Return (ROI)** | **-0.1326%** |
| 📅 **Last Synchronization** | **2026-09-08** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,862.80 | ₹1,844.00 | ₹29,504.00 | -1.01% | 19.7% |
| **3MINDIA** | diversified | 1.0000 | ₹33,145.00 | ₹33,145.00 | ₹33,145.00 | +0.00% | 22.1% |
| **MCX** | financial_infrastructure | 8.0000 | ₹3,342.00 | ₹3,342.00 | ₹26,736.00 | +0.00% | 17.8% |
| **GESHIP** | logistics | 21.0000 | ₹1,383.80 | ₹1,383.80 | ₹29,059.80 | +0.00% | 19.4% |
| **HBLENGINE** | automobiles | 42.0000 | ₹731.25 | ₹731.25 | ₹30,712.50 | +0.00% | 20.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-08 | **HBLENGINE** | `BUY` | 42.0000 | ₹731.25 | ₹30.71 | ₹-30,743.21 |
| 2026-09-08 | **GESHIP** | `BUY` | 21.0000 | ₹1,383.80 | ₹29.06 | ₹-29,088.86 |
| 2026-09-08 | **BHARTIARTL** | `SELL` | 1.0000 | ₹1,844.00 | ₹1.84 | +₹1,842.16 |
| 2026-09-08 | **MCX** | `BUY` | 8.0000 | ₹3,342.00 | ₹26.74 | ₹-26,762.74 |
| 2026-09-08 | **3MINDIA** | `BUY` | 1.0000 | ₹33,145.00 | ₹33.15 | ₹-33,178.14 |
| 2026-09-08 | **GIPCL** | `SELL` | 162.0000 | ₹201.10 | ₹32.58 | +₹32,545.62 |
| 2026-09-08 | **BHARTIHEXA** | `SELL` | 21.0000 | ₹1,549.30 | ₹32.54 | +₹32,502.77 |
| 2026-09-08 | **POLYCAB** | `SELL` | 3.0000 | ₹8,373.50 | ₹25.12 | +₹25,095.38 |
| 2026-09-08 | **DIXON** | `SELL` | 2.0000 | ₹14,100.00 | ₹28.20 | +₹28,171.80 |
| 2026-09-07 | **GIPCL** | `BUY` | 162.0000 | ₹205.18 | ₹33.24 | ₹-33,272.40 |

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
