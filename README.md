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
| 💰 **Total Net Asset Value (NAV)** | **₹150,729.62** |
| 🏦 **Cash Balance** | **₹113.02** |
| 📊 **Total Return (ROI)** | **+0.4864%** |
| 📅 **Last Synchronization** | **2026-08-12** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **POLYCAB** | power_and_utilities | 3.0000 | ₹9,275.00 | ₹9,289.00 | ₹27,867.00 | +0.15% | 18.5% |
| **MCX** | financial_infrastructure | 10.0000 | ₹2,759.30 | ₹2,970.10 | ₹29,701.00 | +7.64% | 19.7% |
| **HBLENGINE** | automobiles | 48.0000 | ₹694.55 | ₹691.50 | ₹33,192.00 | -0.44% | 22.0% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,406.50 | ₹4,406.50 | ₹26,439.00 | +0.00% | 17.5% |
| **GIPCL** | power_and_utilities | 192.0000 | ₹174.05 | ₹174.05 | ₹33,417.60 | +0.00% | 22.2% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-12 | **GIPCL** | `BUY` | 192.0000 | ₹174.05 | ₹33.42 | ₹-33,451.02 |
| 2026-08-12 | **HBLENGINE** | `BUY` | 6.0000 | ₹691.50 | ₹4.15 | ₹-4,153.15 |
| 2026-08-12 | **GVT&D** | `BUY` | 6.0000 | ₹4,406.50 | ₹26.44 | ₹-26,465.44 |
| 2026-08-12 | **GESHIP** | `SELL` | 22.0000 | ₹1,281.90 | ₹28.20 | +₹28,173.60 |
| 2026-08-12 | **3MINDIA** | `SELL` | 1.0000 | ₹35,935.00 | ₹35.94 | +₹35,899.07 |
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
