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
| 💰 **Total Net Asset Value (NAV)** | **₹148,873.00** |
| 🏦 **Cash Balance** | **₹118.77** |
| 📊 **Total Return (ROI)** | **-0.7513%** |
| 📅 **Last Synchronization** | **2026-08-14** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HBLENGINE** | automobiles | 44.0000 | ₹694.55 | ₹678.50 | ₹29,854.00 | -2.31% | 20.1% |
| **DIXON** | electronics_ems | 2.0000 | ₹14,035.00 | ₹14,130.00 | ₹28,260.00 | +0.68% | 19.0% |
| **HINDZINC** | metals_and_mining | 53.0000 | ₹578.35 | ₹561.90 | ₹29,780.70 | -2.84% | 20.0% |
| **SARDAEN** | metals_and_mining | 57.0000 | ₹531.15 | ₹531.15 | ₹30,275.55 | +0.00% | 20.3% |
| **GIPCL** | power_and_utilities | 174.0000 | ₹175.77 | ₹175.77 | ₹30,583.98 | +0.00% | 20.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-14 | **GIPCL** | `BUY` | 174.0000 | ₹175.77 | ₹30.58 | ₹-30,614.56 |
| 2026-08-14 | **SARDAEN** | `BUY` | 57.0000 | ₹531.15 | ₹30.28 | ₹-30,305.83 |
| 2026-08-14 | **HINDZINC** | `BUY` | 2.0000 | ₹561.90 | ₹1.12 | ₹-1,124.92 |
| 2026-08-14 | **HBLENGINE** | `BUY` | 2.0000 | ₹678.50 | ₹1.36 | ₹-1,358.36 |
| 2026-08-14 | **BHARTIARTL** | `SELL` | 14.0000 | ₹1,992.10 | ₹27.89 | +₹27,861.51 |
| 2026-08-14 | **3MINDIA** | `SELL` | 1.0000 | ₹35,340.00 | ₹35.34 | +₹35,304.66 |
| 2026-08-13 | **HINDZINC** | `BUY` | 51.0000 | ₹578.35 | ₹29.50 | ₹-29,525.34 |
| 2026-08-13 | **HBLENGINE** | `SELL` | 6.0000 | ₹693.05 | ₹4.16 | +₹4,154.14 |
| 2026-08-13 | **BHARTIARTL** | `BUY` | 14.0000 | ₹1,939.10 | ₹27.15 | ₹-27,174.55 |
| 2026-08-13 | **DIXON** | `BUY` | 2.0000 | ₹14,035.00 | ₹28.07 | ₹-28,098.07 |

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
