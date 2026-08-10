import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# Path Configuration
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDICES_DIR = os.path.join(WORKSPACE_DIR, "Indices/Daily")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")

sys.path.append(WORKSPACE_DIR)
from live_paper_trading import evaluate_hmm_regime

def sync_live_and_get_signals():
    # 1. Load global ranking to get stock-to-sector mappings
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    symbols = df_rank['Symbol'].unique().tolist()
    
    # 2. Fetch live data using yfinance
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance is not installed. Installing yfinance...")
        os.system("pip install yfinance")
        import yfinance as yf
        
    yf_symbols = [f"{sym}.NS" for sym in symbols]
    
    print("Downloading live closing prices from Yahoo Finance...")
    try:
        df_live = yf.download(yf_symbols, start="2026-08-05", end="2026-08-11", group_by='ticker')
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
        
    print("Download completed. Processing closing prices...")
    
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
    print(f"Available dates in live fetch: {available_dates}")
    
    new_dates = [d for d in available_dates if d > "2026-08-06"]
    print(f"New dates to sync: {new_dates}")
    
    sectors = df_rank['Sector'].unique().tolist()
    
    if len(new_dates) > 0:
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
                        
    # 4. Compare HMM evaluations for Today (T) vs Yesterday (T-1)
    df_bank = pd.read_csv(os.path.join(INDICES_DIR, "banking_daily.csv"))
    
    idx_curr = len(df_bank) - 1
    idx_prev = len(df_bank) - 2
    
    latest_date = df_bank['Date'].iloc[idx_curr]
    prev_date = df_bank['Date'].iloc[idx_prev]
    
    print(f"\nEvaluating HMM regimes for Yesterday ({prev_date}) vs Today ({latest_date})...")
    
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
                
    # Select target stocks for today
    df_active_curr = df_rank[df_rank['Sector'].isin(active_sectors_curr)]
    df_active_curr = df_active_curr.sort_values(by='Combined Score', ascending=False)
    target_symbols_curr = []
    for sym in df_active_curr['Symbol'].tolist():
        if sym in df_closes.columns and latest_date in df_closes.index:
            target_symbols_curr.append(sym)
            if len(target_symbols_curr) >= 5:
                break
                
    # Select target stocks for yesterday
    df_active_prev = df_rank[df_rank['Sector'].isin(active_sectors_prev)]
    df_active_prev = df_active_prev.sort_values(by='Combined Score', ascending=False)
    target_symbols_prev = []
    for sym in df_active_prev['Symbol'].tolist():
        if sym in df_closes.columns and prev_date in df_closes.index:
            target_symbols_prev.append(sym)
            if len(target_symbols_prev) >= 5:
                break
                
    # 5. Signal Change Detection and Alert Generation
    sectors_prev_set = set(active_sectors_prev)
    sectors_curr_set = set(active_sectors_curr)
    
    stocks_prev_set = set(target_symbols_prev)
    stocks_curr_set = set(target_symbols_curr)
    
    new_sectors = sectors_curr_set - sectors_prev_set
    dropped_sectors = sectors_prev_set - sectors_curr_set
    
    new_stocks = stocks_curr_set - stocks_prev_set
    dropped_stocks = stocks_prev_set - stocks_curr_set
    held_stocks = stocks_curr_set.intersection(stocks_prev_set)
    
    signal_changed = (len(new_sectors) > 0 or len(dropped_sectors) > 0 or len(new_stocks) > 0 or len(dropped_stocks) > 0)
    
    print("\n" + "="*50)
    print("SIGNAL UPDATE CHECK")
    print("="*50)
    print(f"Sector Additions: {', '.join(new_sectors) if len(new_sectors) > 0 else 'None'}")
    print(f"Sector Exits    : {', '.join(dropped_sectors) if len(dropped_sectors) > 0 else 'None'}")
    print(f"Stock Additions : {', '.join(new_stocks) if len(new_stocks) > 0 else 'None'}")
    print(f"Stock Exits     : {', '.join(dropped_stocks) if len(dropped_stocks) > 0 else 'None'}")
    print(f"Signal Changed? : {signal_changed}")
    print("="*50)
    
    # Write environment variable and alert markdown if signal changed
    if signal_changed:
        # Write GITHUB_ENV variable for GitHub Action workflow
        github_env_file = os.environ.get('GITHUB_ENV')
        if github_env_file:
            with open(github_env_file, 'a') as f:
                f.write("SIGNAL_CHANGE=true\n")
                
        # Build Markdown Alert
        dropped_str = "\n".join([f"* **{s}**" for s in dropped_stocks]) if len(dropped_stocks) > 0 else "* No exits today."
        new_str = "\n".join([f"* **{s}**" for s in new_stocks]) if len(new_stocks) > 0 else "* No new buys today."
        held_str = "\n".join([f"* **{s}**" for s in held_stocks]) if len(held_stocks) > 0 else "* None."
        
        md_content = f"""# HMM Portfolio Rebalance Alert - {latest_date}

The HMM regime-switching model has detected a change in active sectors or stock rankings today. Please execute the following rebalancing trades.

## Macro Sector Regimes
* **Bullish Sectors Today**: {", ".join(active_sectors_curr) if len(active_sectors_curr) > 0 else "None"}
* **Sector Additions**: {", ".join(new_sectors) if len(new_sectors) > 0 else "None"}
* **Sector Exits**: {", ".join(dropped_sectors) if len(dropped_sectors) > 0 else "None"}

## Portfolio Action Plan

### 🚨 SELL (Exits)
Please sell all shares of the following stocks (their sectors have turned bearish or their ranks dropped):
{dropped_str}

### 🚀 BUY (New Positions)
Please buy equal-weighted positions in the following stocks:
{new_str}

### 💎 HOLD (No Action)
Continue holding these positions as-is:
{held_str}
"""
        with open(os.path.join(WORKSPACE_DIR, "scratch/daily_signals.md"), 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print("Generated scratch/daily_signals.md with latest rebalancing instructions.")
    else:
        print("No rebalance actions required today. Target holdings are unchanged.")

if __name__ == '__main__':
    sync_live_and_get_signals()
