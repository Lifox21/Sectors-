import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

# Path Configuration
WORKSPACE_DIR = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM"
INDICES_DIR = os.path.join(WORKSPACE_DIR, "Indices/Daily")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")
PORTFOLIO_STATE_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_portfolio_state.json")
TRADE_LOG_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_trade_log.csv")
README_PATH = os.path.join(WORKSPACE_DIR, "README.md")

sys.path.append(WORKSPACE_DIR)
from live_paper_trading import evaluate_hmm_regime

def sync_portfolio_and_readme():
    print("Starting Daily Portfolio Valuation and Sync Pipeline...")
    
    # 1. Load global ranking to get stock-to-sector mappings
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    symbols = df_rank['Symbol'].unique().tolist()
    
    # 2. Fetch live daily closing prices from yfinance
    try:
        import yfinance as yf
    except ImportError:
        print("Installing yfinance...")
        os.system("pip install yfinance")
        import yfinance as yf
        
    yf_symbols = [f"{sym}.NS" for sym in symbols]
    
    print("Downloading closing prices from Yahoo Finance...")
    try:
        df_live = yf.download(yf_symbols, start="2026-08-05", end="2026-08-11", group_by='ticker')
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
        
    close_prices = {}
    dates_found = []
    
    for yf_sym in yf_symbols:
        sym = yf_sym.replace(".NS", "")
        if yf_sym in df_live.columns.levels[0]:
            df_sym = df_live[yf_sym]
            close_prices[sym] = df_sym['Close']
            if len(dates_found) == 0:
                dates_found = df_sym.index.tolist()
                
    df_closes = pd.DataFrame(close_prices, index=dates_found)
    df_closes = df_closes.interpolate(method='time').ffill().bfill()
    df_closes.index = df_closes.index.strftime('%Y-%m-%d')
    available_dates = df_closes.index.tolist()
    
    # Sync Indices files with any new dates
    new_dates = [d for d in available_dates if d > "2026-08-06"]
    sectors = df_rank['Sector'].unique().tolist()
    
    if len(new_dates) > 0:
        print(f"Syncing daily sector indices for new dates: {new_dates}")
        for date_str in new_dates:
            date_idx = available_dates.index(date_str)
            prev_date_str = available_dates[date_idx - 1]
            
            for sec in sectors:
                sec_symbols = df_rank[df_rank['Sector'] == sec]['Symbol'].tolist()
                returns = []
                for sym in sec_symbols:
                    if sym in df_closes.columns:
                        p_curr = df_closes.loc[date_str, sym]
                        p_prev = df_closes.loc[prev_date_str, sym]
                        if p_prev > 0 and p_curr > 0:
                            returns.append((p_curr - p_prev) / p_prev)
                            
                avg_return = np.mean(returns) if len(returns) > 0 else 0.0
                
                csv_path = os.path.join(INDICES_DIR, f"{sec}_daily.csv")
                if os.path.exists(csv_path):
                    df_idx = pd.read_csv(csv_path)
                    if date_str not in df_idx['Date'].values:
                        last_row = df_idx.iloc[-1]
                        prev_close = float(last_row['Close'])
                        new_close = prev_close * (1.0 + avg_return)
                        
                        new_row = {
                            'Date': date_str,
                            'Open': new_close,
                            'High': new_close,
                            'Low': new_close,
                            'Close': new_close,
                            'Volume': 0.0
                        }
                        df_idx = pd.concat([df_idx, pd.DataFrame([new_row])], ignore_index=True)
                        df_idx.to_csv(csv_path, index=False)
                        
    # 3. Load current portfolio state
    with open(PORTFOLIO_STATE_PATH, 'r') as f:
        portfolio = json.load(f)
        
    df_bank = pd.read_csv(os.path.join(INDICES_DIR, "banking_daily.csv"))
    idx_curr = len(df_bank) - 1
    idx_prev = len(df_bank) - 2
    
    latest_date = df_bank['Date'].iloc[idx_curr]
    prev_date = df_bank['Date'].iloc[idx_prev]
    
    # 4. Evaluate target stocks for today vs yesterday
    active_sectors_curr = []
    active_sectors_prev = []
    
    for filename in os.listdir(INDICES_DIR):
        if filename.endswith(".csv"):
            sector_name = filename.replace("_daily.csv", "")
            file_path = os.path.join(INDICES_DIR, filename)
            df_sec = pd.read_csv(file_path)
            
            try:
                state_curr = evaluate_hmm_regime(df_sec, idx_curr, k=2)
                if state_curr == 0:
                    active_sectors_curr.append(sector_name)
            except Exception:
                pass
                
            try:
                state_prev = evaluate_hmm_regime(df_sec, idx_prev, k=2)
                if state_prev == 0:
                    active_sectors_prev.append(sector_name)
            except Exception:
                pass
                
    # Select today's target 5 stocks
    df_active_curr = df_rank[df_rank['Sector'].isin(active_sectors_curr)]
    df_active_curr = df_active_curr.sort_values(by='Combined Score', ascending=False)
    target_symbols_curr = []
    for sym in df_active_curr['Symbol'].tolist():
        if sym in df_closes.columns and latest_date in df_closes.index:
            target_symbols_curr.append(sym)
            if len(target_symbols_curr) >= 5:
                break
                
    # Select yesterday's target 5 stocks
    df_active_prev = df_rank[df_rank['Sector'].isin(active_sectors_prev)]
    df_active_prev = df_active_prev.sort_values(by='Combined Score', ascending=False)
    target_symbols_prev = []
    for sym in df_active_prev['Symbol'].tolist():
        if sym in df_closes.columns and prev_date in df_closes.index:
            target_symbols_prev.append(sym)
            if len(target_symbols_prev) >= 5:
                break
                
    # Compare target signals
    signal_changed = (set(target_symbols_curr) != set(target_symbols_prev))
    
    # 5. Calculate holdings value using today's Close prices
    today_prices = {}
    for sym in list(portfolio["holdings"].keys()) + target_symbols_curr:
        if sym in df_closes.columns:
            today_prices[sym] = float(df_closes.loc[latest_date, sym])
            
    # Portfolio NAV calculation before daily rebalancing trades
    current_holdings_val = sum(data["shares"] * today_prices.get(sym, data["current_price"]) for sym, data in portfolio["holdings"].items())
    pre_rebalance_nav = portfolio["cash"] + current_holdings_val
    
    print(f"Date: {latest_date} | Pre-rebalance NAV: INR {pre_rebalance_nav:,.2f}")
    
    # 6. Execute Rebalance Trades (if signal changed OR portfolio holds no positions)
    trades_executed = []
    commission_coef = 10 / 10000.0  # 10 bps
    
    is_initial_run = (len(portfolio["holdings"]) == 0)
    
    if signal_changed or is_initial_run:
        print(f"Signal change detected (or initial portfolio reset). Executing rebalancing trades on {latest_date}...")
        
        # Load trade log file to append
        trade_rows = []
        if os.path.exists(TRADE_LOG_PATH):
            df_log = pd.read_csv(TRADE_LOG_PATH)
            trade_rows = df_log.to_dict('records')
            
        # Step 6a: SELL exits (stocks held but not in today's targets)
        exited_symbols = []
        for held_sym, data in list(portfolio["holdings"].items()):
            if held_sym not in target_symbols_curr:
                price = today_prices[held_sym]
                shares = data["shares"]
                val = shares * price
                comm = val * commission_coef
                net_cash = val - comm
                
                portfolio["cash"] += net_cash
                exited_symbols.append(held_sym)
                del portfolio["holdings"][held_sym]
                
                trade_record = {
                    'Date': latest_date,
                    'Ticker': held_sym,
                    'Action': 'SELL',
                    'Shares': shares,
                    'Price': price,
                    'Commission': comm,
                    'Cash_Impact': net_cash
                }
                trade_rows.append(trade_record)
                trades_executed.append(trade_record)
                
        # Total NAV recalculation after exits (NAV should be constant minus commissions)
        current_holdings_val = sum(data["shares"] * today_prices.get(sym, data["current_price"]) for sym, data in portfolio["holdings"].items())
        total_nav = portfolio["cash"] + current_holdings_val
        
        # Allocation per stock (each target gets 1/5 of total NAV)
        target_allocation = total_nav / 5.0
        
        # Step 6b: BUY entries / REBALANCE existing
        for sym in target_symbols_curr:
            price = today_prices[sym]
            curr_shares = portfolio["holdings"].get(sym, {}).get("shares", 0.0)
            curr_val = curr_shares * price
            deviation = target_allocation - curr_val
            
            if sym not in portfolio["holdings"]:
                # Pure Buy
                shares_to_buy = deviation / (price * (1.0 + commission_coef))
                net_cost = shares_to_buy * price
                comm = net_cost * commission_coef
                total_cost = net_cost + comm
                
                portfolio["cash"] -= total_cost
                portfolio["holdings"][sym] = {
                    'shares': shares_to_buy,
                    'buy_price': price,
                    'current_price': price
                }
                
                trade_record = {
                    'Date': latest_date,
                    'Ticker': sym,
                    'Action': 'BUY',
                    'Shares': shares_to_buy,
                    'Price': price,
                    'Commission': comm,
                    'Cash_Impact': -total_cost
                }
                trade_rows.append(trade_record)
                trades_executed.append(trade_record)
            else:
                # Rebalance check (if deviation > 5% allocation threshold)
                if abs(deviation) > target_allocation * 0.05:
                    if deviation > 0:  # Buy to add
                        shares_to_buy = deviation / (price * (1.0 + commission_coef))
                        net_cost = shares_to_buy * price
                        comm = net_cost * commission_coef
                        total_cost = net_cost + comm
                        
                        portfolio["cash"] -= total_cost
                        portfolio["holdings"][sym]['shares'] += shares_to_buy
                        portfolio["holdings"][sym]['current_price'] = price
                        
                        trade_record = {
                            'Date': latest_date,
                            'Ticker': sym,
                            'Action': 'BUY_REBAL',
                            'Shares': shares_to_buy,
                            'Price': price,
                            'Commission': comm,
                            'Cash_Impact': -total_cost
                        }
                        trade_rows.append(trade_record)
                        trades_executed.append(trade_record)
                    else:  # Sell to trim
                        shares_to_sell = abs(deviation) / price
                        net_val = shares_to_sell * price
                        comm = net_val * commission_coef
                        net_cash = net_val - comm
                        
                        portfolio["cash"] += net_cash
                        portfolio["holdings"][sym]['shares'] -= shares_to_sell
                        portfolio["holdings"][sym]['current_price'] = price
                        
                        trade_record = {
                            'Date': latest_date,
                            'Ticker': sym,
                            'Action': 'SELL_REBAL',
                            'Shares': shares_to_sell,
                            'Price': price,
                            'Commission': comm,
                            'Cash_Impact': net_cash
                        }
                        trade_rows.append(trade_record)
                        trades_executed.append(trade_record)
                        
        # Save updated trade logs
        pd.DataFrame(trade_rows).to_csv(TRADE_LOG_PATH, index=False)
        
    # 7. Update current prices of holdings in state for today's close
    for sym, data in portfolio["holdings"].items():
        data["current_price"] = today_prices.get(sym, data["current_price"])
        
    # Final NAV update
    final_holdings_val = sum(data["shares"] * data["current_price"] for sym, data in portfolio["holdings"].items())
    final_nav = portfolio["cash"] + final_holdings_val
    
    # 8. Record today's NAV in history (avoid duplicate rows for same date)
    portfolio["last_updated_date"] = latest_date
    history_dates = [h["date"] for h in portfolio["nav_history"]]
    if latest_date not in history_dates:
        portfolio["nav_history"].append({
            'date': latest_date,
            'nav': final_nav
        })
    else:
        # Update existing record
        for record in portfolio["nav_history"]:
            if record["date"] == latest_date:
                record["nav"] = final_nav
                
    # Save portfolio state
    with open(PORTFOLIO_STATE_PATH, 'w') as f:
        json.dump(portfolio, f, indent=2)
        
    print(f"Sync complete. Final NAV: INR {final_nav:,.2f}")
    
    # 9. Rewrite README.md dashboard
    generate_readme_dashboard(portfolio, latest_date, df_rank)

def generate_readme_dashboard(portfolio, latest_date, df_rank):
    starting_nav = 100000.0
    current_nav = portfolio["cash"] + sum(d["shares"] * d["current_price"] for s, d in portfolio["holdings"].items())
    total_roi = ((current_nav - starting_nav) / starting_nav) * 100.0
    
    # Calculate holdings rows
    holdings_rows = []
    for sym, data in portfolio["holdings"].items():
        avg_cost = data["buy_price"]
        curr_price = data["current_price"]
        shares = data["shares"]
        mkt_val = shares * curr_price
        roi = ((curr_price - avg_cost) / avg_cost) * 100.0
        alloc = (mkt_val / current_nav) * 100.0
        
        # Get sector name
        sec_row = df_rank[df_rank['Symbol'] == sym]
        sec_name = sec_row.iloc[0]['Sector'] if len(sec_row) > 0 else 'Unknown'
        
        holdings_rows.append(
            f"| **{sym}** | {sec_name} | {shares:.4f} | ₹{avg_cost:,.2f} | ₹{curr_price:,.2f} | ₹{mkt_val:,.2f} | {roi:+.2f}% | {alloc:.1f}% |"
        )
        
    # Get last 10 trades from log
    trades_rows = []
    if os.path.exists(TRADE_LOG_PATH):
        df_log = pd.read_csv(TRADE_LOG_PATH)
        for _, r in df_log.tail(10).iloc[::-1].iterrows():
            impact_sign = "+" if r['Cash_Impact'] > 0 else ""
            trades_rows.append(
                f"| {r['Date']} | **{r['Ticker']}** | `{r['Action']}` | {r['Shares']:.4f} | ₹{r['Price']:,.2f} | ₹{r['Commission']:.2f} | {impact_sign}₹{r['Cash_Impact']:,.2f} |"
            )
            
    # Build the full readme content
    readme_content = f"""# COEP Quantitative Finance Club HMM Sector Trading System

This repository implements a **Gaussian Hidden Markov Model (HMM)** sector-switching and ranking trading pipeline. The strategy uses sector regime shifts to dynamically reallocate capital away from bearish sectors into equal-weighted positions in top-performing stocks of bullish sectors.

---

## 📈 Live Paper Portfolio Dashboard

> [!NOTE]
> This paper portfolio was initialized on **August 10, 2026** with a starting capital of **₹100,000.00**.
> The metrics below are automatically updated at daily market close.

### 📊 Portfolio Summary

| Metric | Value |
| :--- | :--- |
| 💰 **Total Net Asset Value (NAV)** | **₹{current_nav:,.2f}** |
| 🏦 **Cash Balance** | **₹{portfolio['cash']:,.2f}** |
| 📊 **Total Return (ROI)** | **{total_roi:+.4f}%** |
| 📅 **Last Synchronization** | **{latest_date}** |
| 🏁 **Portfolio Start Date** | **2026-08-10** |

---

### 💼 Current Asset Allocations

| Stock Symbol | Sector | Shares | Avg Cost Price | Current Close | Market Value | ROI (%) | Allocation (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
{"\n".join(holdings_rows) if len(holdings_rows) > 0 else "| No active holdings. Currently 100% in cash. | | | | | | | |"}

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
{"\n".join(trades_rows) if len(trades_rows) > 0 else "| No transactions logged yet. | | | | | | |"}

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
"""
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme_content)
        
    print(f"Generated updated README.md at {README_PATH}")

if __name__ == '__main__':
    sync_portfolio_and_readme()
