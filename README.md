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
| 💰 **Total Net Asset Value (NAV)** | **₹148,617.34** |
| 🏦 **Cash Balance** | **₹87.09** |
| 📊 **Total Return (ROI)** | **-0.9218%** |
| 📅 **Last Synchronization** | **2026-09-24** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹34,220.00 | ₹34,615.00 | ₹34,615.00 | +1.15% | 23.3% |
| **POLYCAB** | power_and_utilities | 3.0000 | ₹8,417.00 | ₹8,417.00 | ₹25,251.00 | +0.00% | 17.0% |
| **GESHIP** | logistics | 19.0000 | ₹1,483.80 | ₹1,483.80 | ₹28,192.20 | +0.00% | 19.0% |
| **HBLENGINE** | automobiles | 39.0000 | ₹764.35 | ₹764.35 | ₹29,809.65 | +0.00% | 20.1% |
| **GIPCL** | power_and_utilities | 160.0000 | ₹191.64 | ₹191.64 | ₹30,662.40 | +0.00% | 20.6% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-24 | **GIPCL** | `BUY` | 160.0000 | ₹191.64 | ₹30.66 | ₹-30,693.06 |
| 2026-09-24 | **HBLENGINE** | `BUY` | 39.0000 | ₹764.35 | ₹29.81 | ₹-29,839.46 |
| 2026-09-24 | **GESHIP** | `BUY` | 19.0000 | ₹1,483.80 | ₹28.19 | ₹-28,220.39 |
| 2026-09-24 | **POLYCAB** | `BUY` | 3.0000 | ₹8,417.00 | ₹25.25 | ₹-25,276.25 |
| 2026-09-24 | **SYRMA** | `SELL` | 16.0000 | ₹1,719.40 | ₹27.51 | +₹27,482.89 |
| 2026-09-24 | **DIXON** | `SELL` | 2.0000 | ₹13,200.00 | ₹26.40 | +₹26,373.60 |
| 2026-09-24 | **BHARTIHEXA** | `SELL` | 20.0000 | ₹1,525.20 | ₹30.50 | +₹30,473.50 |
| 2026-09-24 | **BHARTIARTL** | `SELL` | 16.0000 | ₹1,833.20 | ₹29.33 | +₹29,301.87 |
| 2026-09-23 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,534.30 | ₹1.53 | ₹-1,535.83 |
| 2026-09-23 | **SYRMA** | `BUY` | 16.0000 | ₹1,741.80 | ₹27.87 | ₹-27,896.67 |

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
