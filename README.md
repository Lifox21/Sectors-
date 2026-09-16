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
| 💰 **Total Net Asset Value (NAV)** | **₹144,728.38** |
| 🏦 **Cash Balance** | **₹397.70** |
| 📊 **Total Return (ROI)** | **-3.5144%** |
| 📅 **Last Synchronization** | **2026-09-16** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹32,800.00 | ₹31,590.00 | ₹31,590.00 | -3.69% | 21.8% |
| **LODHA** | real_estate | 26.0000 | ₹1,064.80 | ₹1,064.80 | ₹27,684.80 | +0.00% | 19.1% |
| **HINDZINC** | metals_and_mining | 50.0000 | ₹560.90 | ₹560.90 | ₹28,045.00 | +0.00% | 19.4% |
| **SARDAEN** | metals_and_mining | 57.0000 | ₹501.35 | ₹501.35 | ₹28,576.95 | +0.00% | 19.7% |
| **HINDCOPPER** | metals_and_mining | 58.0000 | ₹490.24 | ₹490.24 | ₹28,433.92 | +0.00% | 19.6% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-16 | **HINDCOPPER** | `BUY` | 58.0000 | ₹490.24 | ₹28.43 | ₹-28,462.36 |
| 2026-09-16 | **SARDAEN** | `BUY` | 57.0000 | ₹501.35 | ₹28.58 | ₹-28,605.53 |
| 2026-09-16 | **HINDZINC** | `BUY` | 50.0000 | ₹560.90 | ₹28.05 | ₹-28,073.05 |
| 2026-09-16 | **LODHA** | `BUY` | 26.0000 | ₹1,064.80 | ₹27.68 | ₹-27,712.49 |
| 2026-09-16 | **BHARTIHEXA** | `SELL` | 19.0000 | ₹1,505.50 | ₹28.60 | +₹28,575.90 |
| 2026-09-16 | **TATACOMM** | `SELL` | 16.0000 | ₹1,748.20 | ₹27.97 | +₹27,943.23 |
| 2026-09-16 | **BHARTIARTL** | `SELL` | 15.0000 | ₹1,830.40 | ₹27.46 | +₹27,428.54 |
| 2026-09-16 | **GESHIP** | `SELL` | 21.0000 | ₹1,390.40 | ₹29.20 | +₹29,169.20 |
| 2026-09-15 | **GESHIP** | `BUY` | 1.0000 | ₹1,412.20 | ₹1.41 | ₹-1,413.61 |
| 2026-09-15 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,545.00 | ₹29.36 | ₹-29,384.35 |

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
