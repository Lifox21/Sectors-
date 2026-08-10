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
| 💰 **Total Net Asset Value (NAV)** | **₹149,790.76** |
| 🏦 **Cash Balance** | **₹248.21** |
| 📊 **Total Return (ROI)** | **-0.1395%** |
| 📅 **Last Synchronization** | **2026-08-10** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹35,900.00 | ₹35,900.00 | ₹35,900.00 | +0.00% | 24.0% |
| **MCX** | financial_infrastructure | 10.0000 | ₹2,759.30 | ₹2,759.30 | ₹27,593.00 | +0.00% | 18.4% |
| **GESHIP** | logistics | 21.0000 | ₹1,329.60 | ₹1,329.60 | ₹27,921.60 | +0.00% | 18.6% |
| **HBLENGINE** | automobiles | 41.0000 | ₹694.55 | ₹694.55 | ₹28,476.55 | +0.00% | 19.0% |
| **GIPCL** | power_and_utilities | 180.0000 | ₹164.73 | ₹164.73 | ₹29,651.40 | +0.00% | 19.8% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-10 | **GIPCL** | `BUY` | 180.0000 | ₹164.73 | ₹29.65 | ₹-29,681.05 |
| 2026-08-10 | **HBLENGINE** | `SELL` | 1.0000 | ₹694.55 | ₹0.69 | +₹693.86 |
| 2026-08-10 | **GESHIP** | `SELL` | 1.0000 | ₹1,329.60 | ₹1.33 | +₹1,328.27 |
| 2026-08-10 | **POLYCAB** | `SELL` | 3.0000 | ₹9,275.00 | ₹27.82 | +₹27,797.17 |
| 2026-08-10 | **HBLENGINE** | `BUY` | 42.0000 | ₹694.55 | ₹29.17 | ₹-29,200.27 |
| 2026-08-10 | **GESHIP** | `BUY` | 22.0000 | ₹1,329.60 | ₹29.25 | ₹-29,280.45 |
| 2026-08-10 | **MCX** | `BUY` | 10.0000 | ₹2,759.30 | ₹27.59 | ₹-27,620.59 |
| 2026-08-10 | **POLYCAB** | `BUY` | 3.0000 | ₹9,275.00 | ₹27.82 | ₹-27,852.83 |
| 2026-08-10 | **3MINDIA** | `BUY` | 1.0000 | ₹35,900.00 | ₹35.90 | ₹-35,935.90 |

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
