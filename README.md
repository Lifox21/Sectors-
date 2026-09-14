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
| 💰 **Total Net Asset Value (NAV)** | **₹147,624.87** |
| 🏦 **Cash Balance** | **₹832.87** |
| 📊 **Total Return (ROI)** | **-1.5834%** |
| 📅 **Last Synchronization** | **2026-09-11** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MCX** | financial_infrastructure | 8.0000 | ₹3,342.00 | ₹3,276.00 | ₹26,208.00 | -1.97% | 17.8% |
| **3MINDIA** | diversified | 1.0000 | ₹32,800.00 | ₹32,710.00 | ₹32,710.00 | -0.27% | 22.2% |
| **GESHIP** | logistics | 20.0000 | ₹1,400.20 | ₹1,412.20 | ₹28,244.00 | +0.86% | 19.1% |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,831.10 | ₹1,831.10 | ₹29,297.60 | +0.00% | 19.8% |
| **HBLENGINE** | automobiles | 42.0000 | ₹722.20 | ₹722.20 | ₹30,332.40 | +0.00% | 20.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-11 | **HBLENGINE** | `BUY` | 1.0000 | ₹722.20 | ₹0.72 | ₹-722.92 |
| 2026-09-11 | **GESHIP** | `SELL` | 1.0000 | ₹1,412.20 | ₹1.41 | +₹1,410.79 |
| 2026-09-11 | **HBLENGINE** | `BUY` | 41.0000 | ₹722.20 | ₹29.61 | ₹-29,639.81 |
| 2026-09-11 | **BHARTIARTL** | `BUY` | 16.0000 | ₹1,831.10 | ₹29.30 | ₹-29,326.90 |
| 2026-09-11 | **IGIL** | `SELL` | 101.0000 | ₹314.30 | ₹31.74 | +₹31,712.55 |
| 2026-09-11 | **GVT&D** | `SELL` | 6.0000 | ₹4,548.10 | ₹27.29 | +₹27,261.31 |
| 2026-09-10 | **IGIL** | `BUY` | 101.0000 | ₹311.20 | ₹31.43 | ₹-31,462.63 |
| 2026-09-10 | **GESHIP** | `BUY` | 21.0000 | ₹1,400.20 | ₹29.40 | ₹-29,433.60 |
| 2026-09-10 | **MCX** | `SELL` | 1.0000 | ₹3,300.00 | ₹3.30 | +₹3,296.70 |
| 2026-09-10 | **3MINDIA** | `BUY` | 1.0000 | ₹32,800.00 | ₹32.80 | ₹-32,832.80 |

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
