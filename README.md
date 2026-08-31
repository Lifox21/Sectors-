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
| 💰 **Total Net Asset Value (NAV)** | **₹152,043.89** |
| 🏦 **Cash Balance** | **₹265.00** |
| 📊 **Total Return (ROI)** | **+1.3626%** |
| 📅 **Last Synchronization** | **2026-08-31** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,947.00 | ₹1,882.40 | ₹30,118.40 | -3.32% | 19.8% |
| **HBLENGINE** | automobiles | 48.0000 | ₹683.90 | ₹674.10 | ₹32,356.80 | -1.43% | 21.3% |
| **DIXON** | electronics_ems | 2.0000 | ₹14,711.00 | ₹14,650.00 | ₹29,300.00 | -0.41% | 19.3% |
| **POLYCAB** | power_and_utilities | 3.0000 | ₹9,088.00 | ₹9,088.00 | ₹27,264.00 | +0.00% | 17.9% |
| **GIPCL** | power_and_utilities | 159.0000 | ₹205.91 | ₹205.91 | ₹32,739.69 | +0.00% | 21.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-31 | **GIPCL** | `BUY` | 159.0000 | ₹205.91 | ₹32.74 | ₹-32,772.43 |
| 2026-08-31 | **POLYCAB** | `BUY` | 3.0000 | ₹9,088.00 | ₹27.26 | ₹-27,291.26 |
| 2026-08-31 | **GESHIP** | `SELL` | 23.0000 | ₹1,339.60 | ₹30.81 | +₹30,779.99 |
| 2026-08-31 | **BHARTIHEXA** | `SELL` | 19.0000 | ₹1,550.10 | ₹29.45 | +₹29,422.45 |
| 2026-08-28 | **HBLENGINE** | `BUY` | 3.0000 | ₹665.75 | ₹2.00 | ₹-1,999.25 |
| 2026-08-28 | **GESHIP** | `BUY` | 23.0000 | ₹1,317.20 | ₹30.30 | ₹-30,325.89 |
| 2026-08-28 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,551.10 | ₹29.47 | ₹-29,500.37 |
| 2026-08-28 | **DIXON** | `BUY` | 2.0000 | ₹14,711.00 | ₹29.42 | ₹-29,451.42 |
| 2026-08-28 | **GVT&D** | `SELL` | 6.0000 | ₹4,407.80 | ₹26.45 | +₹26,420.35 |
| 2026-08-28 | **3MINDIA** | `SELL` | 1.0000 | ₹34,245.00 | ₹34.24 | +₹34,210.75 |

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
