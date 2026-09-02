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
| 💰 **Total Net Asset Value (NAV)** | **₹147,553.33** |
| 🏦 **Cash Balance** | **₹567.23** |
| 📊 **Total Return (ROI)** | **-1.6311%** |
| 📅 **Last Synchronization** | **2026-09-02** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GESHIP** | logistics | 23.0000 | ₹1,325.60 | ₹1,305.60 | ₹30,028.80 | -1.51% | 20.4% |
| **HINDZINC** | metals_and_mining | 54.0000 | ₹597.00 | ₹588.40 | ₹31,773.60 | -1.44% | 21.5% |
| **MCX** | financial_infrastructure | 8.0000 | ₹3,286.00 | ₹3,286.00 | ₹26,288.00 | +0.00% | 17.8% |
| **BHARTIARTL** | telecommunications | 16.0000 | ₹1,862.80 | ₹1,862.80 | ₹29,804.80 | +0.00% | 20.2% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,531.10 | ₹1,531.10 | ₹29,090.90 | +0.00% | 19.7% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-02 | **HINDZINC** | `SELL` | 3.0000 | ₹588.40 | ₹1.77 | +₹1,763.43 |
| 2026-09-02 | **GESHIP** | `SELL` | 2.0000 | ₹1,305.60 | ₹2.61 | +₹2,608.59 |
| 2026-09-02 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,531.10 | ₹29.09 | ₹-29,119.99 |
| 2026-09-02 | **BHARTIARTL** | `BUY` | 16.0000 | ₹1,862.80 | ₹29.80 | ₹-29,834.61 |
| 2026-09-02 | **MCX** | `BUY` | 8.0000 | ₹3,286.00 | ₹26.29 | ₹-26,314.29 |
| 2026-09-02 | **3MINDIA** | `SELL` | 1.0000 | ₹32,895.00 | ₹32.90 | +₹32,862.11 |
| 2026-09-02 | **DIXON** | `SELL` | 1.0000 | ₹14,590.00 | ₹14.59 | +₹14,575.41 |
| 2026-09-02 | **HBLENGINE** | `SELL` | 51.0000 | ₹660.20 | ₹33.67 | +₹33,636.53 |
| 2026-09-01 | **HINDZINC** | `BUY` | 57.0000 | ₹597.00 | ₹34.03 | ₹-34,063.03 |
| 2026-09-01 | **HBLENGINE** | `BUY` | 3.0000 | ₹659.20 | ₹1.98 | ₹-1,979.58 |

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
