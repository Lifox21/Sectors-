import os
import json
import pandas as pd

# Path Configuration
WORKSPACE_DIR = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM"
PORTFOLIO_STATE_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_portfolio_state.json")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")

def calculate_trades():
    # 1. Load current portfolio state
    with open(PORTFOLIO_STATE_PATH, 'r') as f:
        portfolio = json.load(f)
        
    print("--- Current Portfolio Holdings ---")
    for sym, data in portfolio["holdings"].items():
        print(f"  - {sym}: {data['shares']:.4f} shares (Last price: {data['current_price']})")
    print(f"  - Cash: INR {portfolio['cash']:,.2f}\n")
    
    # 2. Get today's Close prices (from the stock CSVs which were updated to Aug 10, 2026)
    # The target stocks are: 3MINDIA, GESHIP, MCX, HBLENGINE, POLYCAB
    target_symbols = ["3MINDIA", "GESHIP", "MCX", "HBLENGINE", "POLYCAB"]
    all_symbols = list(portfolio["holdings"].keys()) + target_symbols
    
    today_prices = {}
    target_date = "2026-08-10"
    
    for sym in all_symbols:
        file_path = os.path.join(STOCKS_DIR, f"{sym}_daily.csv")
        if os.path.exists(file_path):
            df_stock = pd.read_csv(file_path)
            # Find row for Aug 10, 2026
            row = df_stock[df_stock['Date'] == target_date]
            if len(row) > 0:
                today_prices[sym] = float(row.iloc[0]['Close'])
            else:
                # Use last available row as fallback
                today_prices[sym] = float(df_stock.iloc[-1]['Close'])
                
    print("--- Today's Closing Prices (Aug 10, 2026) ---")
    for sym, price in today_prices.items():
        print(f"  - {sym}: INR {price:,.2f}")
    print()
    
    # 3. Calculate portfolio NAV before trades
    holdings_value = sum(data["shares"] * today_prices.get(sym, data["current_price"]) for sym, data in portfolio["holdings"].items())
    total_nav = portfolio["cash"] + holdings_value
    print(f"Current Portfolio NAV today: INR {total_nav:,.2f}")
    
    # 4. Generate Trade Signals
    exits = []
    buys = []
    rebalances = []
    
    commission_coef = 10 / 10000.0  # 10 bps
    
    # Exits: Sell stocks we hold but are not in target_symbols
    cash_after_exits = portfolio["cash"]
    for held_symbol, data in portfolio["holdings"].items():
        if held_symbol not in target_symbols:
            price = today_prices[held_symbol]
            shares = data["shares"]
            trade_value = shares * price
            commission = trade_value * commission_coef
            cash_after_exits += (trade_value - commission)
            exits.append({
                'Symbol': held_symbol,
                'Action': 'SELL (EXIT)',
                'Shares': shares,
                'Price': price,
                'Value': trade_value,
                'Commission': commission
            })
            
    # Calculate target allocation for each of the 5 target stocks
    target_allocation = total_nav / len(target_symbols)
    print(f"Target allocation per stock (5 targets): INR {target_allocation:,.2f}\n")
    
    # Check buys and rebalances
    for sym in target_symbols:
        price = today_prices[sym]
        curr_shares = portfolio["holdings"].get(sym, {}).get("shares", 0.0)
        curr_value = curr_shares * price
        needed_trade = target_allocation - curr_value
        
        if sym not in portfolio["holdings"]:
            # Pure buy
            shares_to_buy = needed_trade / (price * (1.0 + commission_coef))
            commission = shares_to_buy * price * commission_coef
            buys.append({
                'Symbol': sym,
                'Action': 'BUY (NEW)',
                'Shares': shares_to_buy,
                'Price': price,
                'Value': shares_to_buy * price,
                'Commission': commission
            })
        else:
            # Rebalance existing holding
            if needed_trade > 10.0:  # Buy more to rebalance up
                shares_to_buy = needed_trade / (price * (1.0 + commission_coef))
                commission = shares_to_buy * price * commission_coef
                rebalances.append({
                    'Symbol': sym,
                    'Action': 'BUY (REBALANCE)',
                    'Shares': shares_to_buy,
                    'Price': price,
                    'Value': shares_to_buy * price,
                    'Commission': commission
                })
            elif needed_trade < -target_allocation * 0.10:  # Sell to rebalance down
                shares_to_sell = abs(needed_trade) / price
                commission = shares_to_sell * price * commission_coef
                rebalances.append({
                    'Symbol': sym,
                    'Action': 'SELL (REBALANCE)',
                    'Shares': shares_to_sell,
                    'Price': price,
                    'Value': shares_to_sell * price,
                    'Commission': commission
                })
                
    # Print Trades
    print("="*60)
    print("DAILY TRADING SIGNALS & EXECUTION ALERTS (AUG 10, 2026)")
    print("="*60)
    
    if len(exits) > 0:
        print("SELL TRADES (EXITS):")
        for trade in exits:
            print(f"  - SELL {trade['Shares']:.4f} shares of {trade['Symbol']} @ INR {trade['Price']:,.2f} (Value: INR {trade['Value']:,.2f}, Commission: INR {trade['Commission']:.2f})")
    else:
        print("SELL TRADES: None")
        
    print()
    if len(buys) > 0 or len(rebalances) > 0:
        print("BUY & REBALANCE TRADES:")
        for trade in buys:
            print(f"  - BUY {trade['Shares']:.4f} shares of {trade['Symbol']} @ INR {trade['Price']:,.2f} (Value: INR {trade['Value']:,.2f}, Commission: INR {trade['Commission']:.2f})")
        for trade in rebalances:
            action_label = "BUY (ADD)" if "BUY" in trade['Action'] else "SELL (TRIM)"
            print(f"  - {action_label} {trade['Shares']:.4f} shares of {trade['Symbol']} @ INR {trade['Price']:,.2f} (Value: INR {trade['Value']:,.2f}, Commission: INR {trade['Commission']:.2f})")
    else:
        print("BUY & REBALANCE TRADES: None")
    print("="*60)

if __name__ == '__main__':
    calculate_trades()
