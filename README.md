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
| 💰 **Total Net Asset Value (NAV)** | **₹150,342.62** |
| 🏦 **Cash Balance** | **₹356.27** |
| 📊 **Total Return (ROI)** | **+0.2284%** |
| 📅 **Last Synchronization** | **2026-08-13** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HBLENGINE** | automobiles | 42.0000 | ₹694.55 | ₹693.05 | ₹29,108.10 | -0.22% | 19.4% |
| **3MINDIA** | diversified | 1.0000 | ₹36,165.00 | ₹36,165.00 | ₹36,165.00 | +0.00% | 24.1% |
| **DIXON** | electronics_ems | 2.0000 | ₹14,035.00 | ₹14,035.00 | ₹28,070.00 | +0.00% | 18.7% |
| **BHARTIARTL** | telecommunications | 14.0000 | ₹1,939.10 | ₹1,939.10 | ₹27,147.40 | +0.00% | 18.1% |
| **HINDZINC** | metals_and_mining | 51.0000 | ₹578.35 | ₹578.35 | ₹29,495.85 | +0.00% | 19.6% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-08-13 | **HINDZINC** | `BUY` | 51.0000 | ₹578.35 | ₹29.50 | ₹-29,525.34 |
| 2026-08-13 | **HBLENGINE** | `SELL` | 6.0000 | ₹693.05 | ₹4.16 | +₹4,154.14 |
| 2026-08-13 | **BHARTIARTL** | `BUY` | 14.0000 | ₹1,939.10 | ₹27.15 | ₹-27,174.55 |
| 2026-08-13 | **DIXON** | `BUY` | 2.0000 | ₹14,035.00 | ₹28.07 | ₹-28,098.07 |
| 2026-08-13 | **3MINDIA** | `BUY` | 1.0000 | ₹36,165.00 | ₹36.16 | ₹-36,201.17 |
| 2026-08-13 | **GIPCL** | `SELL` | 192.0000 | ₹175.97 | ₹33.79 | +₹33,752.45 |
| 2026-08-13 | **GVT&D** | `SELL` | 6.0000 | ₹4,304.70 | ₹25.83 | +₹25,802.37 |
| 2026-08-13 | **MCX** | `SELL` | 10.0000 | ₹2,970.00 | ₹29.70 | +₹29,670.30 |
| 2026-08-13 | **POLYCAB** | `SELL` | 3.0000 | ₹9,297.00 | ₹27.89 | +₹27,863.11 |
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
