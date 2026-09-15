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
| 💰 **Total Net Asset Value (NAV)** | **₹147,507.55** |
| 🏦 **Cash Balance** | **₹134.25** |
| 📊 **Total Return (ROI)** | **-1.6616%** |
| 📅 **Last Synchronization** | **2026-09-15** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹32,800.00 | ₹32,710.00 | ₹32,710.00 | -0.27% | 22.2% |
| **GESHIP** | logistics | 21.0000 | ₹1,400.20 | ₹1,412.20 | ₹29,656.20 | +0.86% | 20.1% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,831.10 | ₹1,831.10 | ₹27,466.50 | +0.00% | 18.6% |
| **TATACOMM** | telecommunications | 16.0000 | ₹1,761.60 | ₹1,761.60 | ₹28,185.60 | +0.00% | 19.1% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,545.00 | ₹1,545.00 | ₹29,355.00 | +0.00% | 19.9% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-15 | **GESHIP** | `BUY` | 1.0000 | ₹1,412.20 | ₹1.41 | ₹-1,413.61 |
| 2026-09-15 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,545.00 | ₹29.36 | ₹-29,384.35 |
| 2026-09-15 | **TATACOMM** | `BUY` | 16.0000 | ₹1,761.60 | ₹28.19 | ₹-28,213.79 |
| 2026-09-15 | **BHARTIARTL** | `SELL` | 1.0000 | ₹1,831.10 | ₹1.83 | +₹1,829.27 |
| 2026-09-15 | **HBLENGINE** | `SELL` | 42.0000 | ₹722.20 | ₹30.33 | +₹30,302.07 |
| 2026-09-15 | **MCX** | `SELL` | 8.0000 | ₹3,276.00 | ₹26.21 | +₹26,181.79 |
| 2026-09-11 | **HBLENGINE** | `BUY` | 1.0000 | ₹722.20 | ₹0.72 | ₹-722.92 |
| 2026-09-11 | **GESHIP** | `SELL` | 1.0000 | ₹1,412.20 | ₹1.41 | +₹1,410.79 |
| 2026-09-11 | **HBLENGINE** | `BUY` | 41.0000 | ₹722.20 | ₹29.61 | ₹-29,639.81 |
| 2026-09-11 | **BHARTIARTL** | `BUY` | 16.0000 | ₹1,831.10 | ₹29.30 | ₹-29,326.90 |

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
