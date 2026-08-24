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
| 💰 **Total Net Asset Value (NAV)** | **₹151,609.93** |
| 🏦 **Cash Balance** | **₹423.33** |
| 📊 **Total Return (ROI)** | **+1.0733%** |
| 📅 **Last Synchronization** | **2026-08-24** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HBLENGINE** | automobiles | 45.0000 | ₹694.55 | ₹690.50 | ₹31,072.50 | -0.58% | 20.5% |
| **3MINDIA** | diversified | 1.0000 | ₹33,800.00 | ₹33,875.00 | ₹33,875.00 | +0.22% | 22.3% |
| **RADICO** | consumer_staples | 6.0000 | ₹4,606.90 | ₹4,578.40 | ₹27,470.40 | -0.62% | 18.1% |
| **LODHA** | real_estate | 23.0000 | ₹1,260.40 | ₹1,257.60 | ₹28,924.80 | -0.22% | 19.1% |
| **SIKA** | capital_goods | 29.0000 | ₹1,040.00 | ₹1,029.10 | ₹29,843.90 | -1.05% | 19.7% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-24 | **HBLENGINE** | `SELL` | 3.0000 | ₹692.85 | ₹2.08 | +₹2,076.47 |
| 2026-08-24 | **SIKA** | `BUY` | 29.0000 | ₹1,040.00 | ₹30.16 | ₹-30,190.16 |
| 2026-08-24 | **LODHA** | `BUY` | 23.0000 | ₹1,260.40 | ₹28.99 | ₹-29,018.19 |
| 2026-08-24 | **RADICO** | `BUY` | 6.0000 | ₹4,606.90 | ₹27.64 | ₹-27,669.04 |
| 2026-08-24 | **3MINDIA** | `BUY` | 1.0000 | ₹33,800.00 | ₹33.80 | ₹-33,833.80 |
| 2026-08-24 | **GIPCL** | `SELL` | 192.0000 | ₹178.80 | ₹34.33 | +₹34,295.27 |
| 2026-08-24 | **GVT&D** | `SELL` | 6.0000 | ₹4,173.50 | ₹25.04 | +₹25,015.96 |
| 2026-08-24 | **MCX** | `SELL` | 10.0000 | ₹3,261.40 | ₹32.61 | +₹32,581.39 |
| 2026-08-24 | **POLYCAB** | `SELL` | 3.0000 | ₹9,026.50 | ₹27.08 | +₹27,052.42 |
| 2026-08-12 | **GIPCL** | `BUY` | 192.0000 | ₹174.05 | ₹33.42 | ₹-33,451.02 |

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
