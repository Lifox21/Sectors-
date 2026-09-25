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
| 💰 **Total Net Asset Value (NAV)** | **₹147,840.77** |
| 🏦 **Cash Balance** | **₹1,117.57** |
| 📊 **Total Return (ROI)** | **-1.4395%** |
| 📅 **Last Synchronization** | **2026-09-25** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **3MINDIA** | diversified | 1.0000 | ₹34,220.00 | ₹34,590.00 | ₹34,590.00 | +1.08% | 23.4% |
| **GESHIP** | logistics | 19.0000 | ₹1,483.80 | ₹1,482.60 | ₹28,169.40 | -0.08% | 19.1% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,795.80 | ₹1,795.80 | ₹26,937.00 | +0.00% | 18.2% |
| **TATACOMM** | telecommunications | 17.0000 | ₹1,670.00 | ₹1,670.00 | ₹28,390.00 | +0.00% | 19.2% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,507.20 | ₹1,507.20 | ₹28,636.80 | +0.00% | 19.4% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-25 | **BHARTIHEXA** | `BUY` | 19.0000 | ₹1,507.20 | ₹28.64 | ₹-28,665.44 |
| 2026-09-25 | **TATACOMM** | `BUY` | 17.0000 | ₹1,670.00 | ₹28.39 | ₹-28,418.39 |
| 2026-09-25 | **BHARTIARTL** | `BUY` | 15.0000 | ₹1,795.80 | ₹26.94 | ₹-26,963.94 |
| 2026-09-25 | **GIPCL** | `SELL` | 160.0000 | ₹186.42 | ₹29.83 | +₹29,797.37 |
| 2026-09-25 | **HBLENGINE** | `SELL` | 39.0000 | ₹775.30 | ₹30.24 | +₹30,206.46 |
| 2026-09-25 | **POLYCAB** | `SELL` | 3.0000 | ₹8,366.50 | ₹25.10 | +₹25,074.40 |
| 2026-09-24 | **GIPCL** | `BUY` | 160.0000 | ₹191.64 | ₹30.66 | ₹-30,693.06 |
| 2026-09-24 | **HBLENGINE** | `BUY` | 39.0000 | ₹764.35 | ₹29.81 | ₹-29,839.46 |
| 2026-09-24 | **GESHIP** | `BUY` | 19.0000 | ₹1,483.80 | ₹28.19 | ₹-28,220.39 |
| 2026-09-24 | **POLYCAB** | `BUY` | 3.0000 | ₹8,417.00 | ₹25.25 | ₹-25,276.25 |

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
