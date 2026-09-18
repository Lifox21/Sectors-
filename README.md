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
| 💰 **Total Net Asset Value (NAV)** | **₹149,865.86** |
| 🏦 **Cash Balance** | **₹441.06** |
| 📊 **Total Return (ROI)** | **-0.0894%** |
| 📅 **Last Synchronization** | **2026-09-18** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,835.00 | ₹1,893.30 | ₹30,292.80 | +3.18% | 20.2% |
| **GVT&D** | miscellaneous | 6.0000 | ₹4,385.00 | ₹4,385.00 | ₹26,310.00 | +0.00% | 17.6% |
| **MCX** | financial_infrastructure | 9.0000 | ₹3,260.00 | ₹3,260.00 | ₹29,340.00 | +0.00% | 19.6% |
| **BHARTIHEXA** | telecommunications | 20.0000 | ₹1,540.10 | ₹1,540.10 | ₹30,802.00 | +0.00% | 20.6% |
| **HBLENGINE** | automobiles | 43.0000 | ₹760.00 | ₹760.00 | ₹32,680.00 | +0.00% | 21.8% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-18 | **HBLENGINE** | `BUY` | 43.0000 | ₹760.00 | ₹32.68 | ₹-32,712.68 |
| 2026-09-18 | **BHARTIHEXA** | `BUY` | 20.0000 | ₹1,540.10 | ₹30.80 | ₹-30,832.80 |
| 2026-09-18 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,893.30 | ₹1.89 | ₹-1,895.19 |
| 2026-09-18 | **MCX** | `BUY` | 9.0000 | ₹3,260.00 | ₹29.34 | ₹-29,369.34 |
| 2026-09-18 | **GVT&D** | `BUY` | 6.0000 | ₹4,385.00 | ₹26.31 | ₹-26,336.31 |
| 2026-09-18 | **GESHIP** | `SELL` | 21.0000 | ₹1,432.10 | ₹30.07 | +₹30,044.03 |
| 2026-09-18 | **DIXON** | `SELL` | 2.0000 | ₹13,005.00 | ₹26.01 | +₹25,983.99 |
| 2026-09-18 | **HINDZINC** | `SELL` | 52.0000 | ₹596.00 | ₹30.99 | +₹30,961.01 |
| 2026-09-18 | **3MINDIA** | `SELL` | 1.0000 | ₹34,095.00 | ₹34.09 | +₹34,060.90 |
| 2026-09-17 | **HINDZINC** | `BUY` | 2.0000 | ₹567.50 | ₹1.14 | ₹-1,136.13 |

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
