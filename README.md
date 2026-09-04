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
| 💰 **Total Net Asset Value (NAV)** | **₹149,743.48** |
| 🏦 **Cash Balance** | **₹1,272.18** |
| 📊 **Total Return (ROI)** | **-0.1710%** |
| 📅 **Last Synchronization** | **2026-09-04** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MCX** | financial_infrastructure | 8.0000 | ₹3,286.00 | ₹3,275.40 | ₹26,203.20 | -0.32% | 17.5% |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,862.80 | ₹1,840.00 | ₹29,440.00 | -1.22% | 19.7% |
| **3MINDIA** | diversified | 1.0000 | ₹32,845.00 | ₹32,845.00 | ₹32,845.00 | +0.00% | 21.9% |
| **DIXON** | electronics_ems | 2.0000 | ₹14,240.00 | ₹14,240.00 | ₹28,480.00 | +0.00% | 19.0% |
| **GESHIP** | logistics | 23.0000 | ₹1,369.70 | ₹1,369.70 | ₹31,503.10 | +0.00% | 21.0% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-04 | **GESHIP** | `BUY` | 23.0000 | ₹1,369.70 | ₹31.50 | ₹-31,534.60 |
| 2026-09-04 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,840.00 | ₹1.84 | ₹-1,841.84 |
| 2026-09-04 | **MCX** | `SELL` | 1.0000 | ₹3,275.40 | ₹3.28 | +₹3,272.12 |
| 2026-09-04 | **DIXON** | `BUY` | 2.0000 | ₹14,240.00 | ₹28.48 | ₹-28,508.48 |
| 2026-09-04 | **3MINDIA** | `BUY` | 1.0000 | ₹32,845.00 | ₹32.84 | ₹-32,877.85 |
| 2026-09-04 | **HBLENGINE** | `SELL` | 47.0000 | ₹695.75 | ₹32.70 | +₹32,667.55 |
| 2026-09-04 | **TATACOMM** | `SELL` | 17.0000 | ₹1,756.10 | ₹29.85 | +₹29,823.85 |
| 2026-09-04 | **BHARTIHEXA** | `SELL` | 20.0000 | ₹1,495.40 | ₹29.91 | +₹29,878.09 |
| 2026-09-03 | **HBLENGINE** | `BUY` | 47.0000 | ₹665.55 | ₹31.28 | ₹-31,312.13 |
| 2026-09-03 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,505.60 | ₹1.51 | ₹-1,507.11 |

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
