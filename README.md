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
| 💰 **Total Net Asset Value (NAV)** | **₹143,638.30** |
| 🏦 **Cash Balance** | **₹768.20** |
| 📊 **Total Return (ROI)** | **-4.2411%** |
| 📅 **Last Synchronization** | **2026-09-30** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,795.80 | ₹1,771.20 | ₹26,568.00 | -1.37% | 18.5% |
| **BHARTIHEXA** | telecommunications | 20.0000 | ₹1,507.20 | ₹1,409.40 | ₹28,188.00 | -6.49% | 19.6% |
| **3MINDIA** | diversified | 1.0000 | ₹33,415.00 | ₹31,890.00 | ₹31,890.00 | -4.56% | 22.2% |
| **TATACOMM** | telecommunications | 17.0000 | ₹1,654.70 | ₹1,654.70 | ₹28,129.90 | +0.00% | 19.6% |
| **ASTRAMICRO** | telecommunications | 17.0000 | ₹1,652.60 | ₹1,652.60 | ₹28,094.20 | +0.00% | 19.6% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-30 | **BHARTIHEXA** | `BUY` | 1.0000 | ₹1,409.40 | ₹1.41 | ₹-1,410.81 |
| 2026-09-30 | **ASTRAMICRO** | `BUY` | 17.0000 | ₹1,652.60 | ₹28.09 | ₹-28,122.29 |
| 2026-09-30 | **TATACOMM** | `BUY` | 17.0000 | ₹1,654.70 | ₹28.13 | ₹-28,158.03 |
| 2026-09-30 | **HBLENGINE** | `SELL` | 38.0000 | ₹808.30 | ₹30.72 | +₹30,684.68 |
| 2026-09-30 | **GESHIP** | `SELL` | 18.0000 | ₹1,537.80 | ₹27.68 | +₹27,652.72 |
| 2026-09-29 | **BHARTIHEXA** | `SELL` | 2.0000 | ₹1,426.50 | ₹2.85 | +₹2,850.15 |
| 2026-09-29 | **GESHIP** | `SELL` | 2.0000 | ₹1,533.40 | ₹3.07 | +₹3,063.73 |
| 2026-09-29 | **BHARTIARTL** | `SELL` | 1.0000 | ₹1,771.40 | ₹1.77 | +₹1,769.63 |
| 2026-09-29 | **3MINDIA** | `BUY` | 1.0000 | ₹33,415.00 | ₹33.41 | ₹-33,448.42 |
| 2026-09-29 | **GVT&D** | `SELL` | 6.0000 | ₹4,203.00 | ₹25.22 | +₹25,192.78 |

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
