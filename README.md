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
| 💰 **Total Net Asset Value (NAV)** | **₹146,630.26** |
| 🏦 **Cash Balance** | **₹694.06** |
| 📊 **Total Return (ROI)** | **-2.2465%** |
| 📅 **Last Synchronization** | **2026-09-28** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GESHIP** | logistics | 20.0000 | ₹1,483.80 | ₹1,497.20 | ₹29,944.00 | +0.90% | 20.4% |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,795.80 | ₹1,785.40 | ₹28,566.40 | -0.58% | 19.5% |
| **BHARTIHEXA** | telecommunications | 21.0000 | ₹1,507.20 | ₹1,481.80 | ₹31,117.80 | -1.69% | 21.2% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,280.00 | ₹4,280.00 | ₹25,680.00 | +0.00% | 17.5% |
| **HBLENGINE** | automobiles | 38.0000 | ₹806.00 | ₹806.00 | ₹30,628.00 | +0.00% | 20.9% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-28 | **HBLENGINE** | `BUY` | 38.0000 | ₹806.00 | ₹30.63 | ₹-30,658.63 |
| 2026-09-28 | **BHARTIHEXA** | `BUY` | 2.0000 | ₹1,481.80 | ₹2.96 | ₹-2,966.56 |
| 2026-09-28 | **GESHIP** | `BUY` | 1.0000 | ₹1,497.20 | ₹1.50 | ₹-1,498.70 |
| 2026-09-28 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,785.40 | ₹1.79 | ₹-1,787.19 |
| 2026-09-28 | **GVT&D** | `BUY` | 6.0000 | ₹4,280.00 | ₹25.68 | ₹-25,705.68 |
| 2026-09-28 | **TATACOMM** | `SELL` | 17.0000 | ₹1,666.50 | ₹28.33 | +₹28,302.17 |
| 2026-09-28 | **3MINDIA** | `SELL` | 1.0000 | ₹33,925.00 | ₹33.92 | +₹33,891.07 |
| 2026-09-25 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,507.20 | ₹28.64 | ₹-28,665.44 |
| 2026-09-25 | **TATACOMM** | `BUY` | 17.0000 | ₹1,670.00 | ₹28.39 | ₹-28,418.39 |
| 2026-09-25 | **BHARTIARTL** | `BUY` | 15.0000 | ₹1,795.80 | ₹26.94 | ₹-26,963.94 |

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
