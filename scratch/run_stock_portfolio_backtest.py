import os
import numpy as np
import pandas as pd
from datetime import datetime

# Path Configuration
WORKSPACE_DIR = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM"
INDICES_REGIME_PATH = os.path.join(WORKSPACE_DIR, "sector_regime_hmm.csv")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")
OUTPUT_CSV_PATH = os.path.join(WORKSPACE_DIR, "scratch/stock_portfolio_backtest_results.csv")

def run_backtest():
    # 1. Load HMM sector regimes
    df_regimes = pd.read_csv(INDICES_REGIME_PATH)
    df_regimes['Date'] = pd.to_datetime(df_regimes['Date'])
    df_regimes = df_regimes.sort_values('Date').reset_index(drop=True)
    dates = df_regimes['Date'].tolist()
    
    # 2. Load stock rankings
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    
    # Pre-load stock daily price files to optimize speed
    stock_dfs = {}
    print("Loading stock daily price files...")
    for sym in df_rank['Symbol'].unique():
        file_path = os.path.join(STOCKS_DIR, f"{sym}_daily.csv")
        if os.path.exists(file_path):
            df_stock = pd.read_csv(file_path)
            df_stock['Date'] = pd.to_datetime(df_stock['Date'])
            df_stock = df_stock.set_index('Date')
            stock_dfs[sym] = df_stock
            
    print(f"Loaded price history for {len(stock_dfs)} stocks.")
    
    # Find all sectors in the dataset
    # Sector columns in regimes are formatted as {sector_name}_returns or {sector_name}_arima
    sectors = [col.replace('_returns', '') for col in df_regimes.columns if col.endswith('_returns')]
    
    # Initialize Portfolio
    capital = 100000.0
    cash = capital
    holdings = {} # Symbol -> shares
    
    commission_coef = 10 / 10000.0  # 10 bps
    
    portfolio_history = []
    trade_count = 0
    
    current_month = None
    
    print("\nStarting simulation loop from 2015 to 2026...")
    for idx, d in enumerate(dates):
        d_str = d.strftime('%Y-%m-%d')
        
        # Get Close prices of currently held stocks for today
        current_prices = {}
        for sym in list(holdings.keys()):
            if sym in stock_dfs and d in stock_dfs[sym].index:
                current_prices[sym] = float(stock_dfs[sym].loc[d, 'Close'])
            else:
                # If price is missing (e.g. trading halt), use previous close or drop it
                current_prices[sym] = holdings[sym] # fallback
                
        # Calculate daily NAV before rebalancing
        holdings_value = sum(shares * current_prices.get(sym, 0.0) for sym, shares in holdings.items())
        total_nav = cash + holdings_value
        
        # Check if first day of month (Rebalance Day)
        is_rebal_day = False
        if current_month is None or d.month != current_month:
            is_rebal_day = True
            current_month = d.month
            
        # Rebalance Logic
        if is_rebal_day or idx == 0:
            # 1. Identify active sectors (State 0 in the HMM returns model)
            active_sectors = []
            for sec in sectors:
                col_name = f"{sec}_returns"
                if col_name in df_regimes.columns:
                    state = df_regimes.loc[idx, col_name]
                    # State 0 is Bullish
                    if state == 0:
                        active_sectors.append(sec)
                        
            # 2. Select top stocks in these sectors
            df_active = df_rank[df_rank['Sector'].isin(active_sectors)]
            df_active = df_active.sort_values(by='Combined Score', ascending=False)
            
            # Select top 5 stocks that have trading data today
            target_symbols = []
            for sym in df_active['Symbol'].tolist():
                if sym in stock_dfs and d in stock_dfs[sym].index:
                    target_symbols.append(sym)
                    if len(target_symbols) >= 5:
                        break
            
            # If no bullish sectors or stocks, hold 100% cash
            if len(target_symbols) == 0:
                # Sell all holdings
                for sym in list(holdings.keys()):
                    price = current_prices.get(sym)
                    if price is not None:
                        shares = holdings[sym]
                        trade_value = shares * price
                        commission = trade_value * commission_coef
                        cash += (trade_value - commission)
                        trade_count += 1
                holdings = {}
            else:
                # 3. Rebalance targets: Sell non-targets
                for sym in list(holdings.keys()):
                    if sym not in target_symbols:
                        price = current_prices.get(sym)
                        if price is not None:
                            shares = holdings[sym]
                            trade_value = shares * price
                            commission = trade_value * commission_coef
                            cash += (trade_value - commission)
                            del holdings[sym]
                            trade_count += 1
                            
                # Recalculate NAV after exits
                nav_after_exits = cash + sum(holdings.get(s, 0.0) * current_prices.get(s, 0.0) for s in holdings)
                
                # Equal-weight target allocation
                target_allocation = nav_after_exits / len(target_symbols)
                
                # 4. Allocate cash to targets
                for sym in target_symbols:
                    price = float(stock_dfs[sym].loc[d, 'Close'])
                    current_val = holdings.get(sym, 0.0) * price
                    needed_trade = target_allocation - current_val
                    
                    if needed_trade > 1.0: # Buy
                        shares_to_buy = needed_trade / (price * (1.0 + commission_coef))
                        commission = shares_to_buy * price * commission_coef
                        cash -= (shares_to_buy * price + commission)
                        holdings[sym] = holdings.get(sym, 0.0) + shares_to_buy
                        trade_count += 1
                    elif needed_trade < -target_allocation * 0.15: # Sell trim
                        shares_to_sell = abs(needed_trade) / price
                        commission = shares_to_sell * price * commission_coef
                        cash += (shares_to_sell * price - commission)
                        holdings[sym] -= shares_to_sell
                        trade_count += 1
                        
            # Recalculate final holdings values for output
            current_prices = {sym: float(stock_dfs[sym].loc[d, 'Close']) for sym in holdings}
            holdings_value = sum(shares * current_prices.get(sym, 0.0) for sym, shares in holdings.items())
            total_nav = cash + holdings_value
            
        portfolio_history.append({
            'Date': d_str,
            'NAV': total_nav,
            'Cash': cash,
            'Holdings_Value': holdings_value,
            'Holdings_Count': len(holdings),
            'Active_Holdings': ",".join(holdings.keys())
        })
        
    df_history = pd.DataFrame(portfolio_history)
    df_history.to_csv(OUTPUT_CSV_PATH, index=False)
    
    # Compute Metrics
    df_history['Returns'] = df_history['NAV'].pct_change().fillna(0.0)
    
    num_days = len(df_history)
    years = num_days / 252.0
    final_nav = df_history['NAV'].iloc[-1]
    
    cagr = (final_nav / capital) ** (1.0 / years) - 1.0
    sharpe = np.mean(df_history['Returns']) / (np.std(df_history['Returns']) + 1e-10) * np.sqrt(252)
    
    running_max = df_history['NAV'].cummax()
    drawdowns = (running_max - df_history['NAV']) / running_max
    max_dd = drawdowns.max()
    
    print("\n" + "="*50)
    print("STOCK-LEVEL PAPER PORTFOLIO BACKTEST SUMMARY (2015-2026)")
    print("="*50)
    print(f"Simulation Period    : {df_history['Date'].iloc[0]} to {df_history['Date'].iloc[-1]} ({years:.2f} years)")
    print(f"Starting Capital     : INR {capital:,.2f}")
    print(f"Final Portfolio NAV  : INR {final_nav:,.2f}")
    print(f"Total Net Return     : +{(final_nav - capital) / capital * 100:.2f}%")
    print(f"Annualized CAGR      : {cagr * 100:.2f}%")
    print(f"Sharpe Ratio         : {sharpe:.4f}")
    print(f"Maximum Drawdown     : -{max_dd * 100:.2f}%")
    print(f"Total Trades Executed: {trade_count}")
    print("-"*50)
    print("Final Active Holdings:")
    for sym, shares in holdings.items():
        if sym in stock_dfs and dates[-1] in stock_dfs[sym].index:
            p = float(stock_dfs[sym].loc[dates[-1], 'Close'])
            print(f"  - {sym}: {shares:.4f} shares @ INR {p:.2f} (Value: INR {shares*p:,.2f})")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_backtest()
