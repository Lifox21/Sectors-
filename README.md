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
| 💰 **Total Net Asset Value (NAV)** | **₹149,749.98** |
| 🏦 **Cash Balance** | **₹187.68** |
| 📊 **Total Return (ROI)** | **-0.1667%** |
| 📅 **Last Synchronization** | **2026-09-21** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,835.00 | ₹1,893.30 | ₹30,292.80 | +3.18% | 20.2% |
| **MCX** | financial_infrastructure | 9.0000 | ₹3,260.00 | ₹3,260.00 | ₹29,340.00 | +0.00% | 19.6% |
| **HBLENGINE** | automobiles | 42.0000 | ₹760.00 | ₹760.00 | ₹31,920.00 | +0.00% | 21.3% |
| **DIXON** | electronics_ems | 2.0000 | ₹12,995.00 | ₹12,995.00 | ₹25,990.00 | +0.00% | 17.4% |
| **GIPCL** | power_and_utilities | 170.0000 | ₹188.35 | ₹188.35 | ₹32,019.50 | +0.00% | 21.4% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-21 | **GIPCL** | `BUY` | 170.0000 | ₹188.35 | ₹32.02 | ₹-32,051.52 |
| 2026-09-21 | **HBLENGINE** | `SELL` | 1.0000 | ₹760.00 | ₹0.76 | +₹759.24 |
| 2026-09-21 | **DIXON** | `BUY` | 2.0000 | ₹12,995.00 | ₹25.99 | ₹-26,015.99 |
| 2026-09-21 | **BHARTIHEXA** | `SELL` | 20.0000 | ₹1,540.10 | ₹30.80 | +₹30,771.20 |
| 2026-09-21 | **GVT&D** | `SELL` | 6.0000 | ₹4,385.00 | ₹26.31 | +₹26,283.69 |
| 2026-09-18 | **HBLENGINE** | `BUY` | 43.0000 | ₹760.00 | ₹32.68 | ₹-32,712.68 |
| 2026-09-18 | **BHARTIHEXA** | `BUY` | 20.0000 | ₹1,540.10 | ₹30.80 | ₹-30,832.80 |
| 2026-09-18 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,893.30 | ₹1.89 | ₹-1,895.19 |
| 2026-09-18 | **MCX** | `BUY` | 9.0000 | ₹3,260.00 | ₹29.34 | ₹-29,369.34 |
| 2026-09-18 | **GVT&D** | `BUY` | 6.0000 | ₹4,385.00 | ₹26.31 | ₹-26,336.31 |

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
