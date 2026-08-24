import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# Path Configuration
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDICES_DIR = os.path.join(WORKSPACE_DIR, "Indices/Daily")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")
PORTFOLIO_STATE_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_portfolio_state.json")
TRADE_LOG_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_trade_log.csv")
README_PATH = os.path.join(WORKSPACE_DIR, "README.md")
DAILY_SIGNALS_PATH = os.path.join(WORKSPACE_DIR, "scratch/daily_signals.md")

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
    
    from datetime import timedelta
    today_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    start_date_str = (today_ist - timedelta(days=15)).strftime('%Y-%m-%d')
    end_date_str = (today_ist + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"Downloading closing prices from Yahoo Finance ({start_date_str} to {end_date_str})...")
    try:
        df_live = yf.download(yf_symbols, start=start_date_str, end=end_date_str, group_by='ticker')
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
    sectors_prev_set = set(active_sectors_prev)
    sectors_curr_set = set(active_sectors_curr)
    stocks_prev_set = set(target_symbols_prev)
    stocks_curr_set = set(target_symbols_curr)
    signal_changed = sectors_curr_set != sectors_prev_set or stocks_curr_set != stocks_prev_set
    write_signal_outputs(
        signal_changed=signal_changed,
        latest_date=latest_date,
        active_sectors_curr=active_sectors_curr,
        new_sectors=sectors_curr_set - sectors_prev_set,
        dropped_sectors=sectors_prev_set - sectors_curr_set,
        new_stocks=stocks_curr_set - stocks_prev_set,
        dropped_stocks=stocks_prev_set - stocks_curr_set,
        held_stocks=stocks_curr_set.intersection(stocks_prev_set),
    )
    
    # 5. Calculate holdings value using today's Close prices
    today_prices = {}
    for sym in list(portfolio["holdings"].keys()) + target_symbols_curr:
        if sym in df_closes.columns:
            today_prices[sym] = float(df_closes.loc[latest_date, sym])
            
    # Portfolio NAV calculation before daily rebalancing trades
    current_holdings_val = sum(data["shares"] * today_prices.get(sym, data["current_price"]) for sym, data in portfolio["holdings"].items())
    pre_rebalance_nav = portfolio["cash"] + current_holdings_val
    
    print(f"Date: {latest_date} | Pre-rebalance NAV: INR {pre_rebalance_nav:,.2f}")
    
    # 6. Execute Rebalance Trades only in the market-open execution window.
    trades_executed = []
    commission_coef = 10 / 10000.0  # 10 bps
    
    is_initial_run = (len(portfolio["holdings"]) == 0)
    execute_trades_now = is_market_open_execution_window()
    
    if (signal_changed or is_initial_run) and execute_trades_now:
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
        
        # Sort target symbols by price descending
        target_symbols_curr = sorted(target_symbols_curr, key=lambda s: today_prices.get(s, 0.0), reverse=True)
        
        # Calculate target allocations sequentially to handle high-price stocks
        remaining_nav = total_nav
        num_remaining_stocks = 5
        target_shares = {}
        
        for sym in target_symbols_curr:
            price = today_prices[sym]
            target_alloc = remaining_nav / num_remaining_stocks
            
            # Calculate integer shares within target allocation
            qty = int(target_alloc / (price * (1.0 + commission_coef)))
            
            # If price <= 40k and target_alloc < price, buy exactly 1 share if we have cash
            if qty == 0 and price <= 40000.0 and remaining_nav >= price * (1.0 + commission_coef):
                qty = 1
                
            target_shares[sym] = qty
            cost = qty * price * (1.0 + commission_coef)
            remaining_nav -= cost
            num_remaining_stocks -= 1
            
        # Execute rebalance trades based on target_shares
        for sym in target_symbols_curr:
            price = today_prices[sym]
            target_qty = target_shares.get(sym, 0)
            curr_qty = int(portfolio["holdings"].get(sym, {}).get("shares", 0.0))
            
            diff_qty = target_qty - curr_qty
            
            if diff_qty > 0:  # BUY
                net_cost = diff_qty * price
                comm = net_cost * commission_coef
                total_cost = net_cost + comm
                
                portfolio["cash"] -= total_cost
                if sym not in portfolio["holdings"]:
                    portfolio["holdings"][sym] = {
                        'shares': float(diff_qty),
                        'buy_price': price,
                        'current_price': price
                    }
                else:
                    portfolio["holdings"][sym]['shares'] = float(target_qty)
                    portfolio["holdings"][sym]['current_price'] = price
                    
                trade_record = {
                    'Date': latest_date,
                    'Ticker': sym,
                    'Action': 'BUY',
                    'Shares': float(diff_qty),
                    'Price': price,
                    'Commission': comm,
                    'Cash_Impact': -total_cost
                }
                trade_rows.append(trade_record)
                trades_executed.append(trade_record)
                
            elif diff_qty < 0:  # SELL (Trim or Exit)
                sell_qty = abs(diff_qty)
                net_val = sell_qty * price
                comm = net_val * commission_coef
                net_cash = net_val - comm
                
                portfolio["cash"] += net_cash
                portfolio["holdings"][sym]['shares'] = float(target_qty)
                portfolio["holdings"][sym]['current_price'] = price
                
                if portfolio["holdings"][sym]['shares'] <= 0:
                    del portfolio["holdings"][sym]
                    
                trade_record = {
                    'Date': latest_date,
                    'Ticker': sym,
                    'Action': 'SELL',
                    'Shares': float(sell_qty),
                    'Price': price,
                    'Commission': comm,
                    'Cash_Impact': net_cash
                }
                trade_rows.append(trade_record)
                trades_executed.append(trade_record)
                        
        # Save updated trade logs
        pd.DataFrame(trade_rows).to_csv(TRADE_LOG_PATH, index=False)
    elif signal_changed or is_initial_run:
        print("Trade execution skipped. Trades are only recorded during the 9:30 AM IST execution window.")
        
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
    starting_nav = 150000.0
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
            
    # Format markdown tables outside f-string to prevent backslash syntax errors in Python < 3.12
    holdings_table_str = "\n".join(holdings_rows) if len(holdings_rows) > 0 else "| No active holdings. Currently 100% in cash. | | | | | | | |"
    trades_table_str = "\n".join(trades_rows) if len(trades_rows) > 0 else "| No transactions logged yet. | | | | | | |"

    # Build the full readme content
    readme_content = f"""# COEP Quantitative Finance Club HMM Sector Trading System

This repository implements a **Gaussian Hidden Markov Model (HMM)** sector-switching and ranking trading pipeline. The strategy uses sector regime shifts to dynamically reallocate capital away from bearish sectors into equal-weighted positions in top-performing stocks of bullish sectors.

---

## 📈 Live Paper Portfolio Dashboard

> [!NOTE]
> This paper portfolio was initialized on **August 10, 2026** with a starting capital of **₹150,000.00**.
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
{holdings_table_str}

---

### 📝 Recent Transactions Log (Latest 10)

| Date | Ticker | Action | Shares | Price | Commission (10 bps) | Cash Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
{trades_table_str}

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

def is_market_open_execution_window():
    if os.environ.get("FORCE_TRADE_EXECUTION") == "true":
        return True
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return True

    now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    start_minutes = 8 * 60 + 20
    end_minutes = 10 * 60
    current_minutes = now_ist.hour * 60 + now_ist.minute
    is_weekday = now_ist.weekday() < 5
    return is_weekday and start_minutes <= current_minutes <= end_minutes

def write_signal_outputs(signal_changed, latest_date, active_sectors_curr, new_sectors, dropped_sectors, new_stocks, dropped_stocks, held_stocks):
    github_env_file = os.environ.get('GITHUB_ENV')
    if github_env_file:
        with open(github_env_file, 'a', encoding='utf-8') as f:
            f.write(f"SIGNAL_CHANGE={'true' if signal_changed else 'false'}\n")

    if not signal_changed:
        print("No rebalance alert required. Target sectors and holdings are unchanged.")
        return

    dropped_str = "\n".join([f"* **{s}**" for s in sorted(dropped_stocks)]) if dropped_stocks else "* No exits today."
    new_str = "\n".join([f"* **{s}**" for s in sorted(new_stocks)]) if new_stocks else "* No new buys today."
    held_str = "\n".join([f"* **{s}**" for s in sorted(held_stocks)]) if held_stocks else "* None."

    md_content = f"""# HMM Portfolio Rebalance Alert - {latest_date}

The HMM regime-switching model has detected a change in active sectors or stock rankings today. Please execute the following rebalancing trades.

## Macro Sector Regimes
* **Bullish Sectors Today**: {", ".join(active_sectors_curr) if active_sectors_curr else "None"}
* **Sector Additions**: {", ".join(sorted(new_sectors)) if new_sectors else "None"}
* **Sector Exits**: {", ".join(sorted(dropped_sectors)) if dropped_sectors else "None"}

## Portfolio Action Plan

### SELL (Exits)
Please sell all shares of the following stocks whose sectors turned bearish or whose ranks dropped:
{dropped_str}

### BUY (New Positions)
Please buy equal-weighted positions in the following stocks:
{new_str}

### HOLD (No Action)
Continue holding these positions as-is:
{held_str}
"""
    with open(DAILY_SIGNALS_PATH, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Generated rebalance alert at {DAILY_SIGNALS_PATH}")

if __name__ == '__main__':
    sync_portfolio_and_readme()
