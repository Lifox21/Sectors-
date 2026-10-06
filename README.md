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
| 💰 **Total Net Asset Value (NAV)** | **₹141,931.26** |
| 🏦 **Cash Balance** | **₹379.56** |
| 📊 **Total Return (ROI)** | **-5.3792%** |
| 📅 **Last Synchronization** | **2026-10-06** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹33,415.00 | ₹30,400.00 | ₹30,400.00 | -9.02% | 21.4% |
| **GESHIP** | logistics | 19.0000 | ₹1,530.60 | ₹1,559.30 | ₹29,626.70 | +1.88% | 20.9% |
| **DIXON** | electronics_ems | 2.0000 | ₹12,748.00 | ₹12,748.00 | ₹25,496.00 | +0.00% | 18.0% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,247.50 | ₹4,247.50 | ₹25,485.00 | +0.00% | 18.0% |
| **HBLENGINE** | automobiles | 40.0000 | ₹763.60 | ₹763.60 | ₹30,544.00 | +0.00% | 21.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-10-06 | **HBLENGINE** | `BUY` | 40.0000 | ₹763.60 | ₹30.54 | ₹-30,574.54 |
| 2026-10-06 | **GESHIP** | `BUY` | 1.0000 | ₹1,559.30 | ₹1.56 | ₹-1,560.86 |
| 2026-10-06 | **GVT&D** | `BUY` | 6.0000 | ₹4,247.50 | ₹25.48 | ₹-25,510.49 |
| 2026-10-06 | **DIXON** | `BUY` | 2.0000 | ₹12,748.00 | ₹25.50 | ₹-25,521.50 |
| 2026-10-06 | **HINDZINC** | `SELL` | 52.0000 | ₹560.95 | ₹29.17 | +₹29,140.23 |
| 2026-10-06 | **BHARTIHEXA** | `SELL` | 20.0000 | ₹1,383.10 | ₹27.66 | +₹27,634.34 |
| 2026-10-06 | **BHARTIARTL** | `SELL` | 15.0000 | ₹1,779.90 | ₹26.70 | +₹26,671.80 |
| 2026-10-05 | **HINDZINC** | `BUY` | 52.0000 | ₹555.05 | ₹28.86 | ₹-28,891.46 |
| 2026-10-05 | **GESHIP** | `BUY` | 18.0000 | ₹1,530.60 | ₹27.55 | ₹-27,578.35 |
| 2026-10-05 | **HBLENGINE** | `SELL` | 37.0000 | ₹779.35 | ₹28.84 | +₹28,807.11 |

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
