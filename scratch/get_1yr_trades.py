import os
import pandas as pd

# Path Configuration
WORKSPACE_DIR = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM"
INDICES_REGIME_PATH = os.path.join(WORKSPACE_DIR, "sector_regime_hmm.csv")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")

def extract_trades():
    # Load HMM sector regimes
    df_regimes = pd.read_csv(INDICES_REGIME_PATH)
    df_regimes['Date'] = pd.to_datetime(df_regimes['Date'])
    df_regimes = df_regimes.sort_values('Date').reset_index(drop=True)
    
    # Filter for the last 1 year (2025-08-06 to 2026-08-06)
    start_date = pd.to_datetime("2025-08-06")
    end_date = pd.to_datetime("2026-08-06")
    df_regimes_filtered = df_regimes[(df_regimes['Date'] >= start_date) & (df_regimes['Date'] <= end_date)].reset_index()
    
    dates = df_regimes_filtered['Date'].tolist()
    
    # Load stock rankings
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    
    # Pre-load stock daily price files
    stock_dfs = {}
    for sym in df_rank['Symbol'].unique():
        file_path = os.path.join(STOCKS_DIR, f"{sym}_daily.csv")
        if os.path.exists(file_path):
            df_stock = pd.read_csv(file_path)
            df_stock['Date'] = pd.to_datetime(df_stock['Date'])
            df_stock = df_stock.set_index('Date')
            stock_dfs[sym] = df_stock
            
    sectors = [col.replace('_returns', '') for col in df_regimes.columns if col.endswith('_returns')]
    
    # Initialize Portfolio
    cash = 100000.0
    holdings = {}
    commission_coef = 10 / 10000.0
    
    trades = []
    current_month = None
    
    for idx, d in enumerate(dates):
        orig_row_idx = df_regimes_filtered.loc[idx, 'index']
        d_str = d.strftime('%Y-%m-%d')
        
        current_prices = {}
        for sym in list(holdings.keys()):
            if sym in stock_dfs and d in stock_dfs[sym].index:
                current_prices[sym] = float(stock_dfs[sym].loc[d, 'Close'])
            else:
                current_prices[sym] = holdings[sym]
                
        # NAV
        holdings_value = sum(shares * current_prices.get(sym, 0.0) for sym, shares in holdings.items())
        total_nav = cash + holdings_value
        
        # Monthly Rebalance
        is_rebal_day = False
        if current_month is None or d.month != current_month:
            is_rebal_day = True
            current_month = d.month
            
        if is_rebal_day or idx == 0:
            # Bullish sectors
            active_sectors = []
            for sec in sectors:
                col_name = f"{sec}_returns"
                if col_name in df_regimes.columns:
                    state = df_regimes.loc[orig_row_idx, col_name]
                    if state == 0:
                        active_sectors.append(sec)
                        
            # Target stocks
            df_active = df_rank[df_rank['Sector'].isin(active_sectors)]
            df_active = df_active.sort_values(by='Combined Score', ascending=False)
            
            target_symbols = []
            for sym in df_active['Symbol'].tolist():
                if sym in stock_dfs and d in stock_dfs[sym].index:
                    target_symbols.append(sym)
                    if len(target_symbols) >= 5:
                        break
                        
            if len(target_symbols) == 0:
                # Sell all
                for sym in list(holdings.keys()):
                    price = current_prices.get(sym)
                    if price is not None:
                        shares = holdings[sym]
                        trade_value = shares * price
                        commission = trade_value * commission_coef
                        cash += (trade_value - commission)
                        trades.append({
                            'Date': d_str,
                            'Symbol': sym,
                            'Action': 'SELL (LIQUIDATE)',
                            'Shares': round(shares, 4),
                            'Price': round(price, 2),
                            'Trade_Value': round(trade_value, 2),
                            'Commission': round(commission, 2)
                        })
                holdings = {}
            else:
                # Sell non-targets
                for sym in list(holdings.keys()):
                    if sym not in target_symbols:
                        price = current_prices.get(sym)
                        if price is not None:
                            shares = holdings[sym]
                            trade_value = shares * price
                            commission = trade_value * commission_coef
                            cash += (trade_value - commission)
                            trades.append({
                                'Date': d_str,
                                'Symbol': sym,
                                'Action': 'SELL (EXIT)',
                                'Shares': round(shares, 4),
                                'Price': round(price, 2),
                                'Trade_Value': round(trade_value, 2),
                                'Commission': round(commission, 2)
                            })
                            del holdings[sym]
                            
                # Recalculate NAV
                nav_after_exits = cash + sum(holdings.get(s, 0.0) * current_prices.get(s, 0.0) for s in holdings)
                target_allocation = nav_after_exits / len(target_symbols)
                
                # Buy target
                for sym in target_symbols:
                    price = float(stock_dfs[sym].loc[d, 'Close'])
                    current_val = holdings.get(sym, 0.0) * price
                    needed_trade = target_allocation - current_val
                    
                    if needed_trade > 1.0: # Buy
                        shares_to_buy = needed_trade / (price * (1.0 + commission_coef))
                        commission = shares_to_buy * price * commission_coef
                        cash -= (shares_to_buy * price + commission)
                        holdings[sym] = holdings.get(sym, 0.0) + shares_to_buy
                        trades.append({
                            'Date': d_str,
                            'Symbol': sym,
                            'Action': 'BUY',
                            'Shares': round(shares_to_buy, 4),
                            'Price': round(price, 2),
                            'Trade_Value': round(shares_to_buy * price, 2),
                            'Commission': round(commission, 2)
                        })
                    elif needed_trade < -target_allocation * 0.15: # Trim
                        shares_to_sell = abs(needed_trade) / price
                        commission = shares_to_sell * price * commission_coef
                        cash += (shares_to_sell * price - commission)
                        holdings[sym] -= shares_to_sell
                        trades.append({
                            'Date': d_str,
                            'Symbol': sym,
                            'Action': 'SELL (TRIM)',
                            'Shares': round(shares_to_sell, 4),
                            'Price': round(price, 2),
                            'Trade_Value': round(shares_to_sell * price, 2),
                            'Commission': round(commission, 2)
                        })
                        
    df_trades = pd.DataFrame(trades)
    df_trades.to_csv(os.path.join(WORKSPACE_DIR, "scratch/recent_1yr_trades.csv"), index=False)
    
    print(f"\n--- Trade Logs (Total: {len(df_trades)} Trades) ---")
    print(df_trades.to_string(index=False))

if __name__ == '__main__':
    extract_trades()
