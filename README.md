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
| 💰 **Total Net Asset Value (NAV)** | **₹141,009.47** |
| 🏦 **Cash Balance** | **₹100.57** |
| 📊 **Total Return (ROI)** | **-5.9937%** |
| 📅 **Last Synchronization** | **2026-10-05** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,795.80 | ₹1,741.10 | ₹26,116.50 | -3.05% | 18.5% |
| **BHARTIHEXA** | telecommunications | 20.0000 | ₹1,507.20 | ₹1,379.20 | ₹27,584.00 | -8.49% | 19.6% |
| **3MINDIA** | diversified | 1.0000 | ₹33,415.00 | ₹30,795.00 | ₹30,795.00 | -7.84% | 21.8% |
| **GESHIP** | logistics | 18.0000 | ₹1,530.60 | ₹1,530.60 | ₹27,550.80 | +0.00% | 19.5% |
| **HINDZINC** | metals_and_mining | 52.0000 | ₹555.05 | ₹555.05 | ₹28,862.60 | +0.00% | 20.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-10-05 | **HINDZINC** | `BUY` | 52.0000 | ₹555.05 | ₹28.86 | ₹-28,891.46 |
| 2026-10-05 | **GESHIP** | `BUY` | 18.0000 | ₹1,530.60 | ₹27.55 | ₹-27,578.35 |
| 2026-10-05 | **HBLENGINE** | `SELL` | 37.0000 | ₹779.35 | ₹28.84 | +₹28,807.11 |
| 2026-10-05 | **TATACOMM** | `SELL` | 16.0000 | ₹1,683.00 | ₹26.93 | +₹26,901.07 |
| 2026-10-01 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,379.20 | ₹1.38 | ₹-1,380.58 |
| 2026-10-01 | **TATACOMM** | `SELL` | 1.0000 | ₹1,683.00 | ₹1.68 | +₹1,681.32 |
| 2026-10-01 | **HBLENGINE** | `BUY` | 37.0000 | ₹794.50 | ₹29.40 | ₹-29,425.90 |
| 2026-10-01 | **BHARTIHEXA** | `SELL` | 1.0000 | ₹1,424.50 | ₹1.42 | +₹1,423.08 |
| 2026-10-01 | **ASTRAMICRO** | `SELL` | 17.0000 | ₹1,636.70 | ₹27.82 | +₹27,796.08 |
| 2026-09-30 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,409.40 | ₹1.41 | ₹-1,410.81 |

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
