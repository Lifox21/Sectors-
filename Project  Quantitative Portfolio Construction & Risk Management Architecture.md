# Project : Quantitative Portfolio Construction & Risk Management Architecture

**To:** All Domain Heads, COEP Quantitative Finance Club **Subject:** Official Kickoff & Master Roadmap - QFC Alpha Portfolio

Hi Heads,

I’m thrilled to announce that we are officially kicking off our first major research project of the academic year for the COEP Quantitative Finance Club!

**Project Title:** Portfolio Construction & Portfolio Risk Management

Our objective is highly ambitious: We are building a multi-layered quantitative pipeline to filter a universe of ~2,000 Indian equities (Market Cap > ₹500 Cr) down to an optimized, alpha-generating Top 20 portfolio.

To achieve this without falling prey to market noise or excessive transaction costs, we will use a **sequential filtering system**. We will not analyze 2,000 stocks simultaneously. Instead, we will map the macro environment at the sector level, identify which sectors are structurally bullish, and *only then* hunt for mathematical stock breakouts within those specific sectors. Finally, we will validate those breakouts with rigorous fundamental data before adding them to our portfolio.

## 1. The Pipeline Architecture

Below is the definitive workflow for our quantitative engine. It operates as a strict decision tree, ensuring we only allocate capital to mathematically sound breakouts backed by strong fundamentals, while continuously weeding out weak holdings.

<img src="C:\Users\Yash\Pictures\Mermaid Images\algo_trading_logic.png" alt="algo_trading_logic" style="zoom:20%;" />

## 2. Core Workflow & Domain Responsibilities

Before we write any code, we need a bulletproof research and data foundation. I have broken down the immediate tasks, logic definitions, and literature review requirements by domain below. Please begin gathering resources and formulating methodologies for your respective areas.

### Phase 1: Macro State Detection (The Sector Filter)

*The goal here is to determine "Where" the institutional money is flowing. We do not run these models on individual stocks; we run them on indices (e.g., Nifty Bank, Nifty IT, Nifty Metal).*

- **ARIMA-HMM (Adaptive Trend Mapping):** Research how to use an ARIMA model to map the linear trend of a sector index. We will then feed the *residuals* (the prediction errors) into a Hidden Markov Model. State 0 will represent a stable, trending bull market. State 1 will represent volatile, unpredictable behavior.
- **MS-GARCH (Volatility Clustering):** The Indian market experiences fat-tail risks and clustered volatility. Standard HMMs fail here. Research Markov-Switching GARCH models. We need this model to tell us mathematically if a sector has structurally shifted into a high-volatility "avoid" regime.
- **The Output Rule:** If our macro models flag a sector (e.g., Nifty Pharma) as Bearish/State 1, the pipeline completely ignores all Pharma stocks. We only hunt in Bullish/State 0 sectors.

### Phase 2: Micro Breakout Detection (The Technical Filter)

*Once a sector is approved, we need to find which specific stocks inside it are waking up.*

- **CUSUM (Cumulative Sum) Filters:** Research this sequential analysis technique. We will use CUSUM to mathematically track a stock's deviation from its mean. We only want stocks whose CUSUM score violently breaks a defined statistical threshold, proving a true momentum breakout rather than random noise.
- **Relative Strength HMM (RS-HMM):** Research how to apply an HMM to a ratio line (e.g., Stock Price / Sector Index Price). We need this to mathematically confirm that the stock is currently outperforming its sector peers (Alpha generation).

### Phase 3: Factor Scoring (The Fundamental Filter)

*We will not buy garbage stocks just because they triggered a CUSUM breakout. We must validate the technical signal with fundamental strength.*

- **Cross-Sectional Z-Scoring:** Our data will cover companies > ₹500 Cr. We need a methodology to calculate *sector-neutral* Z-scores for key metrics. This ensures we don't unfairly penalize a capital-intensive manufacturing company for having lower baseline margins than an IT firm.
- **Key Metrics Required:** P/E, P/B, ROE, ROCE, ROI, EPS growth, debt-to-equity, profit margins, revenue growth, and free cash flow indicators.
- **Regime-Conditioned Weighting:** Research how fundamental factor premiums change based on the market state. For example, if the broader Nifty 50 is entering a late-stage bull market, we might algorithmically overweight "Growth" metrics. If the market is choppy, we overweight "Quality" (ROCE, low debt).

### Phase 4: The Dynamic Optimizer (Portfolio Management)

*This is how we maintain a concentrated 20-stock portfolio without excessive churn.*

- **The Swap Logic:** When Phase 3 produces a highly qualified candidate stock, it must fight for its spot. We need a composite scoring model to rank this new candidate against the absolute weakest stock currently in our Top 20. If the candidate wins, we execute the swap. If not, the candidate is rejected.
- **The Monitoring Loop:** We need continuous surveillance of our Top 20. If a current holding triggers an RS-HMM bearish regime transition or breaks its CUSUM baseline, it is instantly flagged for removal, triggering the swap logic above.

### Phase 5: Data Engineering (The Foundation)

*Our models are entirely dependent on clean data.*

- **The Universe:** Locate reliable datasets/APIs for the comprehensive universe of Indian listed companies > ₹500 crore (approx. 2,000 stocks).
- **Clean Historicals:** Source 10-15 years of clean historical daily data for the 12-15 NSE sectoral indices and individual equities. **Crucial:** You must find data that accounts for corporate actions (splits/dividends) to prevent our models from misinterpreting a stock split as a massive price crash.
- **Fundamental Accuracy:** Identify sources for point-in-time fundamental data (quarterly/annual results) to ensure we strictly avoid look-ahead bias during backtesting.

## Next Steps

Please start gathering these resources, research papers (specifically focusing on MS-GARCH, CUSUM in trading, and fundamental factor models), and data links immediately. Create a shared repository for your respective domains.

A well-organized, thoroughly researched foundation is the critical first step before we begin architecting the Python/R environment for this data-driven framework.

Let’s build something incredible this year. Thanks, and I look forward to your contributions.

Best regards,

COEP Quantitative Finance Club