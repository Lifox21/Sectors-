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
| 💰 **Total Net Asset Value (NAV)** | **₹150,040.24** |
| 🏦 **Cash Balance** | **₹638.14** |
| 📊 **Total Return (ROI)** | **+0.0268%** |
| 📅 **Last Synchronization** | **2026-08-20** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HBLENGINE** | automobiles | 48.0000 | ₹694.55 | ₹712.90 | ₹34,219.20 | +2.64% | 22.8% |
| **DIXON** | electronics_ems | 1.0000 | ₹14,035.00 | ₹14,850.00 | ₹14,850.00 | +5.81% | 9.9% |
| **3MINDIA** | diversified | 1.0000 | ₹33,550.00 | ₹33,550.00 | ₹33,550.00 | +0.00% | 22.4% |
| **BHARTIARTL** | telecommunications | 17.0000 | ₹1,941.70 | ₹1,941.70 | ₹33,008.90 | +0.00% | 22.0% |
| **GESHIP** | logistics | 26.0000 | ₹1,299.00 | ₹1,299.00 | ₹33,774.00 | +0.00% | 22.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-20 | **HBLENGINE** | `BUY` | 4.0000 | ₹712.90 | ₹2.85 | ₹-2,854.45 |
| 2026-08-20 | **GESHIP** | `BUY` | 26.0000 | ₹1,299.00 | ₹33.77 | ₹-33,807.77 |
| 2026-08-20 | **BHARTIARTL** | `BUY` | 17.0000 | ₹1,941.70 | ₹33.01 | ₹-33,041.91 |
| 2026-08-20 | **DIXON** | `SELL` | 1.0000 | ₹14,850.00 | ₹14.85 | +₹14,835.15 |
| 2026-08-20 | **3MINDIA** | `BUY` | 1.0000 | ₹33,550.00 | ₹33.55 | ₹-33,583.55 |
| 2026-08-20 | **GIPCL** | `SELL` | 174.0000 | ₹170.18 | ₹29.61 | +₹29,581.71 |
| 2026-08-20 | **SARDAEN** | `SELL` | 57.0000 | ₹509.35 | ₹29.03 | +₹29,003.92 |
| 2026-08-20 | **HINDZINC** | `SELL` | 53.0000 | ₹573.90 | ₹30.42 | +₹30,386.28 |
| 2026-08-14 | **GIPCL** | `BUY` | 174.0000 | ₹175.77 | ₹30.58 | ₹-30,614.56 |
| 2026-08-14 | **SARDAEN** | `BUY` | 57.0000 | ₹531.15 | ₹30.28 | ₹-30,305.83 |

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
