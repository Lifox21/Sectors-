# Workspace Analysis Report: COEP Quantitative Finance Club - HHM Portfolio Project

This report provides a detailed breakdown of the folder structure, data assets, and quantitative pipeline architecture in the workspace directory `c:\Users\Ved Bajaj\Desktop\Lifox\QF Club\HHM`. It is designed to be comprehensive and structured so that you can easily copy/paste or share this information directly with Claude or other LLMs to continue work on the codebase.

---

## 1. Project Context & Objectives
Based on the documentation found in [Project  Quantitative Portfolio Construction & Risk Management Architecture.md](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/Project%20%20Quantitative%20Portfolio%20Construction%20&%20Risk%20Management%20Architecture.md), this workspace contains the codebase and data files for the **COEP Quantitative Finance Club (QFC) Alpha Portfolio Project**. 

The goal of this project is to build a sequential quantitative pipeline that filters a universe of ~2,000 Indian equities (Market Cap > ₹500 Cr) down to a highly optimized, alpha-generating **Top 20 Portfolio**.

### Sequential Filtering Engine Architecture:
1. **Phase 1: Macro State Detection (Sector Filter):**
   * Uses **ARIMA-HMM** (Adaptive Trend Mapping) and **MS-GARCH** (Volatility Clustering) on sector indices (e.g., Nifty Bank, Nifty IT) to identify structural bullish trends (State 0) or volatile/unpredictable states (State 1).
   * Stocks in volatile/bearish (State 1) sectors are completely ignored.
2. **Phase 2: Micro Breakout Detection (Technical Filter):**
   * Applies **CUSUM (Cumulative Sum) Filters** to mathematically identify momentum breakouts.
   * Uses **Relative Strength HMM (RS-HMM)** on stock-to-sector ratio lines to confirm individual outperformance.
3. **Phase 3: Factor Scoring (Fundamental Filter):**
   * Evaluates the fundamental health of companies passing the technical filter.
   * Calculates **Sector-Neutral Cross-Sectional Z-Scores** for metrics like P/E, P/B, ROE, ROCE, EPS growth, debt-to-equity, etc.
   * Applies **Regime-Conditioned Weighting** to adjust factor weights based on the broader market regime (e.g., Growth vs. Quality).
4. **Phase 4: Dynamic Optimizer (Portfolio Management):**
   * Manages a concentrated 20-stock portfolio.
   * Implements **Swap Logic** (new candidates compete against the weakest holding in the Top 20) and a **Monitoring Loop** (exits triggered by RS-HMM bearish transitions or CUSUM breaks).

---

## 2. Directory Tree Structure

```text
c:\Users\Ved Bajaj\Desktop\Lifox\QF Club\HHM
├── Project  Quantitative Portfolio Construction & Risk Management Architecture.md  # Kickoff Roadmap & Specs
├── Project  Quantitative Portfolio Construction & Risk Management Architecture.pdf  # PDF copy of the specs
├── Data_Enhanced.csv                                                               # Master stock financial data
├── quant_club_sector_terminal.html                                                 # Interactive dashboard
├── Indices/
│   └── Daily/
│       ├── agriculture_daily.csv                                                   # Historical daily sector prices
│       ├── airlines_daily.csv
│       ├── ... (32 sectoral daily CSVs)
│       └── textiles_apparel_daily.csv
├── Stocks/
│   └── Daily/
│       ├── 360ONE_daily.csv                                                        # Historical daily stock prices
│       ├── 3MINDIA_daily.csv
│       ├── ... (Hundreds of individual equity CSVs)
│       └── ZYDUSWELL_daily.csv
└── scored_csv/
    ├── scoring_manifest.csv                                                        # Overview of sector scoring
    ├── global_ranking.csv                                                          # Aggregated rating of 1,426 equities
    ├── top_bottom_20.csv                                                           # Final portfolio candidate lists
    ├── agriculture_scored.csv                                                      # Sector-specific scored tables
    ├── automobiles_scored.csv
    └── ... (32 sector scored CSVs)
```

---

## 3. Comprehensive File-by-File Analysis

### 3.1. Root Files

#### 1. [Project  Quantitative Portfolio Construction & Risk Management Architecture.md](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/Project%20%20Quantitative%20Portfolio%20Construction%20&%20Risk%20Management%20Architecture.md) (and `.pdf` version)
* **Description:** The project charter, design specification, and roadmap detailing domain responsibilities, mathematical algorithms (ARIMA-HMM, MS-GARCH, CUSUM, Z-Scores), and business logic rules (Swap Logic).

#### 2. [Data_Enhanced.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/Data_Enhanced.csv)
* **Size:** ~9.04 MB
* **Contents:** The fundamental database for 1,426 listed Indian equities. It is a wide-format CSV containing comprehensive corporate financial statements, including:
  * **Quarterly Results (Mar 2023 - Mar 2026):** Sales, Expenses, Operating Profit, OPM %, Interest, Depreciation, PBT, Tax %, Net Profit, EPS.
  * **Profit & Loss Statements (Mar 2014 - Mar 2026, plus TTM):** Sales, Expenses, OPM %, Other Income, Interest, Depreciation, PBT, Net Profit, EPS, Dividend Payout %, and Compounded Growth metrics.
  * **Balance Sheets (Mar 2014 - Mar 2026):** Equity Capital, Reserves, Borrowings, Other Liabilities, Fixed Assets, CWIP, Investments, Other Assets, Total Assets/Liabilities.
  * **Cash Flows (Mar 2014 - Mar 2026):** Cash from Operating, Investing, and Financing activities, Net Cash Flow, Free Cash Flow, CFO/OP.
  * **Financial Ratios:** Debtor Days, Inventory Days, Days Payable, Cash Conversion Cycle, Working Capital Days, ROCE %.
  * **Shareholding Patterns (Quarterly & Yearly):** Holdings of Promoters, FIIs, DIIs, Public, Government, and number of shareholders.

#### 3. [quant_club_sector_terminal.html](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/quant_club_sector_terminal.html)
* **Size:** ~39.9 MB
* **Description:** An offline-capable, interactive sector dashboard/terminal styled with dark UI aesthetics. It features typography from Google Fonts (`Inter` and `JetBrains Mono`) and uses CSS variables for a premium neon-accented appearance. Because it is 39.9MB, it contains the entire project's pricing, indexing, and scoring datasets preloaded inside the HTML file in JSON format. This allows users to search, filter, and visualize sector states, technical metrics, and stock scores dynamically.

---

### 3.2. Subdirectories

#### 📂 `Indices/Daily`
* **Contents:** Contains **32 CSV files** of sectoral indices representing different industries in the Indian market (e.g., `banking_daily.csv`, `media_and_entertainment_daily.csv`, `oil_gas_utilities_daily.csv`).
* **Purpose:** Serves as the source data for Phase 1 (Macro HMM & GARCH models) to determine bullish and bearish sectors.
* **Schema:**
  | Date (YYYY-MM-DD) | Open (Float) | High (Float) | Low (Float) | Close (Float) | Volume (Float) |
  | :--- | :--- | :--- | :--- | :--- | :--- |

---

#### 📂 `Stocks/Daily`
* **Contents:** Contains **hundreds of individual stock CSV files** matching the ticker symbols in the dataset (e.g., `3MINDIA_daily.csv`, `DIXON_daily.csv`).
* **Purpose:** Serves as source data for Phase 2 (Micro CUSUM breakouts and RS-HMM relative strength relative to sector benchmarks).
* **Schema:** Same daily OHLCV structure as the sectoral indices, starting from `2015-01-01`.

---

#### 📂 `scored_csv`
Contains output tables generated by the fundamental factor and LLM review pipeline:

#### 1. [scoring_manifest.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scored_csv/scoring_manifest.csv)
* **Contents:** A high-level manifest summarizing the scoring runs for each sector.
* **Columns:** `source`, `output`, `sector`, `stocks` (count of companies), `mean_score`, `llm_reviewed`.

#### 2. [global_ranking.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scored_csv/global_ranking.csv)
* **Contents:** A consolidated list ranking 1,426 equities based on combined quantitative and qualitative criteria.
* **Columns:**
  * `Global Rank` / `Global Percentile`
  * `Stock Name` / `Symbol` / `Sector` / `industry`
  * `market_cap` (Market Capitalization)
  * `Hedge Fund Score` (Quantitative factor score)
  * `LLM Score` (Qualitative analysis rating)
  * `Combined Score` (Aggregated total score)
  * `Pros` / `Cons` (Detailed qualitative insights, e.g., cash flows, inventory cycles, depreciation spikes, valuation concerns).

#### 3. [top_bottom_20.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scored_csv/top_bottom_20.csv)
* **Contents:** The subset of `global_ranking.csv` listing the final **Top 20** recommended portfolio candidates (e.g., DIXON, 3MINDIA, MCX, GESHIP, HINDZINC) and **Bottom 20** lowest-ranking stocks to avoid or short (e.g., TEJASNET, OLAELEC, ABFRL, HIMATSEIDE).

#### 4. **Sector-specific Scored Files (32 Files)**
* **Contents:** Individual CSV files for each sector (e.g., `banking_scored.csv`, `chemicals_scored.csv`) containing the breakdown of scores, pros, and cons specifically relative to their sector peers.

---

## 4. Integration Guide for Claude

If you want to feed this structure to Claude, you can use the following guide:

1. **Architecture Planning:** Ask Claude to review [Project  Quantitative Portfolio Construction & Risk Management Architecture.md](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/Project%20%20Quantitative%20Portfolio%20Construction%20&%20Risk%20Management%20Architecture.md) to generate the math and Python code for ARIMA-HMM and MS-GARCH.
2. **Backtesting Price Engines:** The historical data in `Indices/Daily` (for macro trends) and `Stocks/Daily` (for micro breakouts) are aligned by date and OHLCV formats, making it easy to run vectorised backtests.
3. **Fundamental Scoring Validation:** Ask Claude to write script functions parsing [Data_Enhanced.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/Data_Enhanced.csv) to calculate sector-neutral Z-scores for custom metrics and compare them with the results in `scored_csv/global_ranking.csv`.
4. **Optimizing Portfolio Swaps:** Feed the swap logic rules from the spec and [top_bottom_20.csv](file:///c:/Users/Ved%20Bajaj/Desktop/Lifox/QF%20Club/HHM/scored_csv/top_bottom_20.csv) to Claude to model a mock portfolio rebalancing loop based on rolling weekly/monthly data.
