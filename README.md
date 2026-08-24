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
| 💰 **Total Net Asset Value (NAV)** | **₹151,942.79** |
| 🏦 **Cash Balance** | **₹371.69** |
| 📊 **Total Return (ROI)** | **+1.2952%** |
| 📅 **Last Synchronization** | **2026-08-24** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HBLENGINE** | automobiles | 43.0000 | ₹694.55 | ₹690.90 | ₹29,708.70 | -0.53% | 19.6% |
| **3MINDIA** | diversified | 1.0000 | ₹33,800.00 | ₹33,885.00 | ₹33,885.00 | +0.25% | 22.3% |
| **RADICO** | consumer_staples | 6.0000 | ₹4,606.90 | ₹4,600.00 | ₹27,600.00 | -0.15% | 18.2% |
| **SIKA** | capital_goods | 29.0000 | ₹1,040.00 | ₹1,036.60 | ₹30,061.40 | -0.33% | 19.8% |
| **DLF** | real_estate | 44.0000 | ₹689.00 | ₹689.00 | ₹30,316.00 | +0.00% | 20.0% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-24 | **DLF** | `BUY` | 44.0000 | ₹689.00 | ₹30.32 | ₹-30,346.32 |
| 2026-08-24 | **HBLENGINE** | `SELL` | 2.0000 | ₹690.90 | ₹1.38 | +₹1,380.42 |
| 2026-08-24 | **LODHA** | `SELL` | 23.0000 | ₹1,258.40 | ₹28.94 | +₹28,914.26 |
| 2026-08-24 | **HBLENGINE** | `SELL` | 3.0000 | ₹692.85 | ₹2.08 | +₹2,076.47 |
| 2026-08-24 | **SIKA** | `BUY` | 29.0000 | ₹1,040.00 | ₹30.16 | ₹-30,190.16 |
| 2026-08-24 | **LODHA** | `BUY` | 23.0000 | ₹1,260.40 | ₹28.99 | ₹-29,018.19 |
| 2026-08-24 | **RADICO** | `BUY` | 6.0000 | ₹4,606.90 | ₹27.64 | ₹-27,669.04 |
| 2026-08-24 | **3MINDIA** | `BUY` | 1.0000 | ₹33,800.00 | ₹33.80 | ₹-33,833.80 |
| 2026-08-24 | **GIPCL** | `SELL` | 192.0000 | ₹178.80 | ₹34.33 | +₹34,295.27 |
| 2026-08-24 | **GVT&D** | `SELL` | 6.0000 | ₹4,173.50 | ₹25.04 | +₹25,015.96 |

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
