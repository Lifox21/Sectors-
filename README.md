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
| 💰 **Total Net Asset Value (NAV)** | **₹147,191.79** |
| 🏦 **Cash Balance** | **₹393.34** |
| 📊 **Total Return (ROI)** | **-1.8721%** |
| 📅 **Last Synchronization** | **2026-09-03** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MCX** | financial_infrastructure | 9.0000 | ₹3,286.00 | ₹3,170.20 | ₹28,531.80 | -3.52% | 19.4% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,862.80 | ₹1,869.00 | ₹28,035.00 | +0.33% | 19.0% |
| **BHARTIHEXA** | telecommunications | 20.0000 | ₹1,531.10 | ₹1,505.60 | ₹30,112.00 | -1.67% | 20.5% |
| **TATACOMM** | telecommunications | 17.0000 | ₹1,696.40 | ₹1,696.40 | ₹28,838.80 | +0.00% | 19.6% |
| **HBLENGINE** | automobiles | 47.0000 | ₹665.55 | ₹665.55 | ₹31,280.85 | +0.00% | 21.3% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-03 | **HBLENGINE** | `BUY` | 47.0000 | ₹665.55 | ₹31.28 | ₹-31,312.13 |
| 2026-09-03 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,505.60 | ₹1.51 | ₹-1,507.11 |
| 2026-09-03 | **TATACOMM** | `BUY` | 17.0000 | ₹1,696.40 | ₹28.84 | ₹-28,867.64 |
| 2026-09-03 | **BHARTIARTL** | `SELL` | 1.0000 | ₹1,869.00 | ₹1.87 | +₹1,867.13 |
| 2026-09-03 | **MCX** | `BUY` | 1.0000 | ₹3,170.20 | ₹3.17 | ₹-3,173.37 |
| 2026-09-03 | **HINDZINC** | `SELL` | 54.0000 | ₹587.95 | ₹31.75 | +₹31,717.55 |
| 2026-09-03 | **GESHIP** | `SELL` | 23.0000 | ₹1,353.60 | ₹31.13 | +₹31,101.67 |
| 2026-09-02 | **HINDZINC** | `SELL` | 3.0000 | ₹588.40 | ₹1.77 | +₹1,763.43 |
| 2026-09-02 | **GESHIP** | `SELL` | 2.0000 | ₹1,305.60 | ₹2.61 | +₹2,608.59 |
| 2026-09-02 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,531.10 | ₹29.09 | ₹-29,119.99 |

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
