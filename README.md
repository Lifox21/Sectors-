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
| 💰 **Total Net Asset Value (NAV)** | **₹143,693.86** |
| 🏦 **Cash Balance** | **₹561.46** |
| 📊 **Total Return (ROI)** | **-4.2041%** |
| 📅 **Last Synchronization** | **2026-10-01** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,795.80 | ₹1,757.00 | ₹26,355.00 | -2.16% | 18.3% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,507.20 | ₹1,424.50 | ₹27,065.50 | -5.49% | 18.8% |
| **3MINDIA** | diversified | 1.0000 | ₹33,415.00 | ₹32,160.00 | ₹32,160.00 | -3.76% | 22.4% |
| **TATACOMM** | telecommunications | 17.0000 | ₹1,654.70 | ₹1,656.20 | ₹28,155.40 | +0.09% | 19.6% |
| **HBLENGINE** | automobiles | 37.0000 | ₹794.50 | ₹794.50 | ₹29,396.50 | +0.00% | 20.5% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-10-01 | **HBLENGINE** | `BUY` | 37.0000 | ₹794.50 | ₹29.40 | ₹-29,425.90 |
| 2026-10-01 | **BHARTIHEXA** | `SELL` | 1.0000 | ₹1,424.50 | ₹1.42 | +₹1,423.08 |
| 2026-10-01 | **ASTRAMICRO** | `SELL` | 17.0000 | ₹1,636.70 | ₹27.82 | +₹27,796.08 |
| 2026-09-30 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,409.40 | ₹1.41 | ₹-1,410.81 |
| 2026-09-30 | **ASTRAMICRO** | `BUY` | 17.0000 | ₹1,652.60 | ₹28.09 | ₹-28,122.29 |
| 2026-09-30 | **TATACOMM** | `BUY` | 17.0000 | ₹1,654.70 | ₹28.13 | ₹-28,158.03 |
| 2026-09-30 | **HBLENGINE** | `SELL` | 38.0000 | ₹808.30 | ₹30.72 | +₹30,684.68 |
| 2026-09-30 | **GESHIP** | `SELL` | 18.0000 | ₹1,537.80 | ₹27.68 | +₹27,652.72 |
| 2026-09-29 | **BHARTIHEXA** | `SELL` | 2.0000 | ₹1,426.50 | ₹2.85 | +₹2,850.15 |
| 2026-09-29 | **GESHIP** | `SELL` | 2.0000 | ₹1,533.40 | ₹3.07 | +₹3,063.73 |

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
