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
| 💰 **Total Net Asset Value (NAV)** | **₹144,667.33** |
| 🏦 **Cash Balance** | **₹121.93** |
| 📊 **Total Return (ROI)** | **-3.5551%** |
| 📅 **Last Synchronization** | **2026-09-29** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GESHIP** | logistics | 18.0000 | ₹1,483.80 | ₹1,533.40 | ₹27,601.20 | +3.34% | 19.1% |
| **BHARTIARTL** | telecommunications | 15.0000 | ₹1,795.80 | ₹1,771.40 | ₹26,571.00 | -1.36% | 18.4% |
| **BHARTIHEXA** | telecommunications | 19.0000 | ₹1,507.20 | ₹1,426.50 | ₹27,103.50 | -5.35% | 18.7% |
| **HBLENGINE** | automobiles | 38.0000 | ₹806.00 | ₹785.65 | ₹29,854.70 | -2.52% | 20.6% |
| **3MINDIA** | diversified | 1.0000 | ₹33,415.00 | ₹33,415.00 | ₹33,415.00 | +0.00% | 23.1% |

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-29 | **BHARTIHEXA** | `SELL` | 2.0000 | ₹1,426.50 | ₹2.85 | +₹2,850.15 |
| 2026-09-29 | **GESHIP** | `SELL` | 2.0000 | ₹1,533.40 | ₹3.07 | +₹3,063.73 |
| 2026-09-29 | **BHARTIARTL** | `SELL` | 1.0000 | ₹1,771.40 | ₹1.77 | +₹1,769.63 |
| 2026-09-29 | **3MINDIA** | `BUY` | 1.0000 | ₹33,415.00 | ₹33.41 | ₹-33,448.42 |
| 2026-09-29 | **GVT&D** | `SELL` | 6.0000 | ₹4,203.00 | ₹25.22 | +₹25,192.78 |
| 2026-09-28 | **HBLENGINE** | `BUY` | 38.0000 | ₹806.00 | ₹30.63 | ₹-30,658.63 |
| 2026-09-28 | **BHARTIHEXA** | `BUY` | 2.0000 | ₹1,481.80 | ₹2.96 | ₹-2,966.56 |
| 2026-09-28 | **GESHIP** | `BUY` | 1.0000 | ₹1,497.20 | ₹1.50 | ₹-1,498.70 |
| 2026-09-28 | **BHARTIARTL** | `BUY` | 1.0000 | ₹1,785.40 | ₹1.79 | ₹-1,787.19 |
| 2026-09-28 | **GVT&D** | `BUY` | 6.0000 | ₹4,280.00 | ₹25.68 | ₹-25,705.68 |

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
