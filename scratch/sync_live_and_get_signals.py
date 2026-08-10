import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# Path Configuration
WORKSPACE_DIR = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM"
INDICES_DIR = os.path.join(WORKSPACE_DIR, "Indices/Daily")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")

sys.path.append(WORKSPACE_DIR)
from live_paper_trading import evaluate_hmm_regime

def sync_live_and_get_signals():
    # 1. Load global ranking to get stock-to-sector mappings
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    symbols = df_rank['Symbol'].unique().tolist()
    
    print(f"Total symbols to fetch: {len(symbols)}")
    
    # 2. Fetch live data using yfinance
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance is not installed. Installing yfinance...")
        os.system("pip install yfinance")
        import yfinance as yf
        
    # Format symbols for yfinance (Yahoo NSE suffix is .NS)
    yf_symbols = [f"{sym}.NS" for sym in symbols]
    
    # Download EOD prices from August 5 to August 11 (covers Aug 6, Aug 7, Aug 10)
    print("Downloading live closing prices from Yahoo Finance...")
    try:
        df_live = yf.download(yf_symbols, start="2026-08-05", end="2026-08-11", group_by='ticker')
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
        
    print("Download completed. Processing closing prices...")
    
    # Extract Close prices
    close_prices = {}
    dates_found = []
    
    # The downloaded dataframe has MultiIndex columns if group_by='ticker'
    # Format: (Ticker, PriceAttribute)
    for yf_sym in yf_symbols:
        sym = yf_sym.replace(".NS", "")
        if yf_sym in df_live.columns.levels[0]:
            df_sym = df_live[yf_sym]
            close_prices[sym] = df_sym['Close']
            if len(dates_found) == 0:
                dates_found = df_sym.index.tolist()
                
    df_closes = pd.DataFrame(close_prices, index=dates_found)
    df_closes = df_closes.interpolate(method='time').ffill().bfill()  # handle missing values
    
    # Format dates as YYYY-MM-DD
    df_closes.index = df_closes.index.strftime('%Y-%m-%d')
    available_dates = df_closes.index.tolist()
    print(f"Available dates in live fetch: {available_dates}")
    
    # We want to identify the new dates after August 6, 2026
    new_dates = [d for d in available_dates if d > "2026-08-06"]
    print(f"New dates to sync: {new_dates}")
    
    if len(new_dates) == 0:
        print("No new dates found. The database is already up to date.")
    else:
        # 3. Update the 32 sector index files with the new dates
        sectors = df_rank['Sector'].unique().tolist()
        
        for date_str in new_dates:
            print(f"Syncing sector index returns for date: {date_str}...")
            # We need the previous date close
            date_idx = available_dates.index(date_str)
            prev_date_str = available_dates[date_idx - 1]
            
            for sec in sectors:
                sec_symbols = df_rank[df_rank['Sector'] == sec]['Symbol'].tolist()
                
                # Compute returns for each symbol in this sector from prev_date to date
                returns = []
                for sym in sec_symbols:
                    if sym in df_closes.columns:
                        p_curr = df_closes.loc[date_str, sym]
                        p_prev = df_closes.loc[prev_date_str, sym]
                        if p_prev > 0 and p_curr > 0:
                            ret = (p_curr - p_prev) / p_prev
                            returns.append(ret)
                            
                avg_return = np.mean(returns) if len(returns) > 0 else 0.0
                
                # Update sector CSV
                csv_path = os.path.join(INDICES_DIR, f"{sec}_daily.csv")
                if os.path.exists(csv_path):
                    df_idx = pd.read_csv(csv_path)
                    
                    # Ensure we don't write duplicate dates
                    if date_str not in df_idx['Date'].values:
                        last_row = df_idx.iloc[-1]
                        prev_close = float(last_row['Close'])
                        new_close = prev_close * (1.0 + avg_return)
                        
                        # Append new row
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
                        
    # 4. Re-run HMM evaluations up to the latest date (August 10, 2026)
    # Get last index row index in banking_daily to find target_idx
    df_bank = pd.read_csv(os.path.join(INDICES_DIR, "banking_daily.csv"))
    latest_date = df_bank['Date'].iloc[-1]
    target_idx = len(df_bank) - 1
    
    print(f"\nEvaluating HMM regimes up to the latest date: {latest_date}...")
    active_sectors = []
    
    for filename in os.listdir(INDICES_DIR):
        if filename.endswith(".csv"):
            sector_name = filename.replace("_daily.csv", "")
            file_path = os.path.join(INDICES_DIR, filename)
            df_sec = pd.read_csv(file_path)
            
            try:
                state = evaluate_hmm_regime(df_sec, target_idx, k=2)
                if state == 0:
                    active_sectors.append(sector_name)
            except Exception as e:
                pass
                
    print(f"\nBullish Sectors (State 0) on {latest_date}:")
    print(", ".join(active_sectors) if len(active_sectors) > 0 else "None")
    
    # 5. Extract the Top 5 individual stocks to invest in today
    df_active_stocks = df_rank[df_rank['Sector'].isin(active_sectors)]
    df_active_stocks = df_active_stocks.sort_values(by='Combined Score', ascending=False)
    
    # Select the top 5
    top_5_investments = df_active_stocks.head(5)
    
    print("\n" + "="*60)
    print(f"TOP 5 RECOMMENDED STOCKS FOR INVESTMENT (AS OF {latest_date})")
    print("="*60)
    print(f"{'Rank':<6} {'Symbol':<12} {'Stock Name':<40} {'Sector':<20} {'Score':<8}")
    print("-"*60)
    for idx, row in top_5_investments.reset_index(drop=True).iterrows():
        print(f"{idx+1:<6} {row['Symbol']:<12} {row['Stock Name']:<40} {row['Sector']:<20} {row['Combined Score']:<8}")
    print("="*60 + "\n")

if __name__ == '__main__':
    sync_live_and_get_signals()
