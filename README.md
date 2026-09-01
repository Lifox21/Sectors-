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
| 💰 **Total Net Asset Value (NAV)** | **₹148,954.25** |
| 🏦 **Cash Balance** | **₹390.05** |
| 📊 **Total Return (ROI)** | **-0.6972%** |
| 📅 **Last Synchronization** | **2026-09-01** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HBLENGINE** | automobiles | 51.0000 | ₹683.90 | ₹659.20 | ₹33,619.20 | -3.61% | 22.6% |
| **DIXON** | electronics_ems | 1.0000 | ₹14,711.00 | ₹14,461.00 | ₹14,461.00 | -1.70% | 9.7% |
| **3MINDIA** | diversified | 1.0000 | ₹33,315.00 | ₹33,315.00 | ₹33,315.00 | +0.00% | 22.4% |
| **GESHIP** | logistics | 25.0000 | ₹1,325.60 | ₹1,325.60 | ₹33,140.00 | +0.00% | 22.2% |
| **HINDZINC** | metals_and_mining | 57.0000 | ₹597.00 | ₹597.00 | ₹34,029.00 | +0.00% | 22.8% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-01 | **HINDZINC** | `BUY` | 57.0000 | ₹597.00 | ₹34.03 | ₹-34,063.03 |
| 2026-09-01 | **HBLENGINE** | `BUY` | 3.0000 | ₹659.20 | ₹1.98 | ₹-1,979.58 |
| 2026-09-01 | **GESHIP** | `BUY` | 25.0000 | ₹1,325.60 | ₹33.14 | ₹-33,173.14 |
| 2026-09-01 | **DIXON** | `SELL` | 1.0000 | ₹14,461.00 | ₹14.46 | +₹14,446.54 |
| 2026-09-01 | **3MINDIA** | `BUY` | 1.0000 | ₹33,315.00 | ₹33.31 | ₹-33,348.32 |
| 2026-09-01 | **GIPCL** | `SELL` | 159.0000 | ₹198.80 | ₹31.61 | +₹31,577.59 |
| 2026-09-01 | **POLYCAB** | `SELL` | 3.0000 | ₹8,895.50 | ₹26.69 | +₹26,659.81 |
| 2026-09-01 | **BHARTIARTL** | `SELL` | 16.0000 | ₹1,877.20 | ₹30.04 | +₹30,005.16 |
| 2026-08-31 | **GIPCL** | `BUY` | 159.0000 | ₹205.91 | ₹32.74 | ₹-32,772.43 |
| 2026-08-31 | **POLYCAB** | `BUY` | 3.0000 | ₹9,088.00 | ₹27.26 | ₹-27,291.26 |

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
