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
| 💰 **Total Net Asset Value (NAV)** | **₹142,189.05** |
| 🏦 **Cash Balance** | **₹33.15** |
| 📊 **Total Return (ROI)** | **-5.2073%** |
| 📅 **Last Synchronization** | **2026-10-07** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹33,415.00 | ₹30,840.00 | ₹30,840.00 | -7.71% | 21.7% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,810.50 | ₹1,810.50 | ₹27,157.50 | +0.00% | 19.1% |
| **BHARTIHEXA** | telecommunications | 20.0000 | ₹1,386.80 | ₹1,386.80 | ₹27,736.00 | +0.00% | 19.5% |
| **HINDZINC** | metals_and_mining | 50.0000 | ₹557.65 | ₹557.65 | ₹27,882.50 | +0.00% | 19.6% |
| **SARDAEN** | metals_and_mining | 57.0000 | ₹500.70 | ₹500.70 | ₹28,539.90 | +0.00% | 20.1% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-10-07 | **SARDAEN** | `BUY` | 57.0000 | ₹500.70 | ₹28.54 | ₹-28,568.44 |
| 2026-10-07 | **HINDZINC** | `BUY` | 50.0000 | ₹557.65 | ₹27.88 | ₹-27,910.38 |
| 2026-10-07 | **BHARTIHEXA** | `BUY` | 20.0000 | ₹1,386.80 | ₹27.74 | ₹-27,763.74 |
| 2026-10-07 | **BHARTIARTL** | `BUY` | 15.0000 | ₹1,810.50 | ₹27.16 | ₹-27,184.66 |
| 2026-10-07 | **HBLENGINE** | `SELL` | 40.0000 | ₹764.30 | ₹30.57 | +₹30,541.43 |
| 2026-10-07 | **GVT&D** | `SELL` | 6.0000 | ₹4,245.10 | ₹25.47 | +₹25,445.13 |
| 2026-10-07 | **DIXON** | `SELL` | 2.0000 | ₹13,015.00 | ₹26.03 | +₹26,003.97 |
| 2026-10-07 | **GESHIP** | `SELL` | 19.0000 | ₹1,532.60 | ₹29.12 | +₹29,090.28 |
| 2026-10-06 | **HBLENGINE** | `BUY` | 40.0000 | ₹763.60 | ₹30.54 | ₹-30,574.54 |
| 2026-10-06 | **GESHIP** | `BUY` | 1.0000 | ₹1,559.30 | ₹1.56 | ₹-1,560.86 |

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
