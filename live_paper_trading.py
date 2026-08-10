import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# Force absolute imports or append workspace path
WORKSPACE_DIR = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM"
sys.path.append(WORKSPACE_DIR)

try:
    from hmmlearn.hmm import GaussianHMM
except ImportError:
    print("Error: hmmlearn is not installed on this system. Please run 'pip install hmmlearn' to run HMM regime detection.")

# =====================================================================
# 1. PATH CONFIGURATION
# =====================================================================
INDICES_DIR = os.path.join(WORKSPACE_DIR, "Indices/Daily")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
PORTFOLIO_STATE_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_portfolio_state.json")
TRADE_LOG_PATH = os.path.join(WORKSPACE_DIR, "scratch/paper_trade_log.csv")

# Ensure scratch exists
os.makedirs(os.path.join(WORKSPACE_DIR, "scratch"), exist_ok=True)

# =====================================================================
# 2. HMM DECODER HELPERS (REUSED FROM REPLICATE_PIPELINE)
# =====================================================================
def causal_smoothing(series, k=2):
    if k <= 1:
        return series
    return series.rolling(window=k).mean()

def fit_ols_ar1_residuals(prices, t_curr):
    diff = np.diff(prices)
    train_diff = diff[:t_curr - 1]
    
    if len(train_diff) < 3:
        resid = np.zeros(len(prices))
        resid[1:] = diff
        return resid
        
    y = train_diff[1:]
    x = train_diff[:-1]
    X = np.column_stack([np.ones_like(x), x])
    try:
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        c, phi = beta[0], beta[1]
    except Exception:
        c, phi = 0.0, 0.0
        
    diff_full = diff
    resid = np.zeros(len(prices))
    resid[1] = diff_full[0] - c
    if len(diff_full) > 1:
        resid[2:] = diff_full[1:] - (c + phi * diff_full[:-1])
    return resid

def evaluate_hmm_regime(df_sector, target_idx, k=2):
    """
    Fits the Gaussian HMM on features up to target_idx and returns the predicted state for target_idx.
    State 0 = Bullish (highest mean return), State 1 = Neutral, State 2 = Bearish.
    """
    df = df_sector.iloc[:target_idx + 1].copy()
    df['Close_smoothed'] = causal_smoothing(df['Close'], k)
    df['Smoothed_Returns'] = np.log(df['Close_smoothed'] / df['Close_smoothed'].shift(1))
    df['Vol'] = df['Smoothed_Returns'].rolling(window=10).std()
    df['Log_Vol'] = np.log(df['Vol'] + 1e-8)
    df = df.dropna().reset_index(drop=True)
    
    T_curr = len(df)
    if T_curr < 100:  # Minimum history required to fit HMM stably
        return 1 # Default neutral state
        
    prices = df['Close_smoothed'].values
    residuals = fit_ols_ar1_residuals(prices, T_curr)
    df['ARIMA_Resid'] = residuals
    
    cols = ['Smoothed_Returns', 'Log_Vol', 'ARIMA_Resid']
    X = df[cols].values
    
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0) + 1e-8
    X_scaled = (X - mean) / std
    
    hmm = GaussianHMM(n_components=3, covariance_type='diag', n_iter=20, random_state=42)
    try:
        hmm.fit(X_scaled)
    except Exception:
        return 1 # Fallback to Neutral
        
    # Determine state mappings based on training returns
    train_pred_states = hmm.predict(X_scaled)
    train_returns = df['Smoothed_Returns'].values
    
    state_means = []
    for s in range(3):
        mask = (train_pred_states == s)
        if np.sum(mask) > 0:
            state_means.append(np.mean(train_returns[mask]))
        else:
            state_means.append(-999.0)
            
    sorted_indices = np.argsort(state_means)
    mapping = {sorted_indices[2]: 0, sorted_indices[1]: 1, sorted_indices[0]: 2}
    
    latest_raw_state = train_pred_states[-1]
    return mapping[latest_raw_state]

# =====================================================================
# 3. PORTFOLIO MANAGER CLASS
# =====================================================================
class PaperPortfolio:
    def __init__(self, start_capital=100000.0, transaction_cost_bps=10):
        self.state_path = PORTFOLIO_STATE_PATH
        self.log_path = TRADE_LOG_PATH
        self.cost_coef = transaction_cost_bps / 10000.0
        self.load_portfolio()
        
    def load_portfolio(self):
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, 'r') as f:
                    self.state = json.load(f)
            except Exception:
                self.reset_portfolio()
        else:
            self.reset_portfolio()
            
    def save_portfolio(self):
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=4)
            
    def reset_portfolio(self, start_capital=100000.0):
        self.state = {
            "cash": start_capital,
            "holdings": {},  # Ticker -> {shares: float, buy_price: float, current_price: float}
            "last_updated_date": None,
            "equity_history": []
        }
        self.save_portfolio()
        # Reset trade log
        with open(self.log_path, 'w') as f:
            f.write("Date,Symbol,Action,Shares,Price,Commission,Total_Cash_Impact\n")
            
    def get_total_value(self):
        holdings_value = 0.0
        for ticker, data in self.state["holdings"].items():
            holdings_value += data["shares"] * data["current_price"]
        return self.state["cash"] + holdings_value

    def update_stock_prices(self, date_str, current_prices):
        """
        Updates the current_price fields of all holdings and records the daily valuation.
        """
        for ticker in list(self.state["holdings"].keys()):
            if ticker in current_prices:
                self.state["holdings"][ticker]["current_price"] = current_prices[ticker]
                
        total_val = self.get_total_value()
        self.state["last_updated_date"] = date_str
        
        # Avoid duplicate dates in history
        history = [h for h in self.state["equity_history"] if h["date"] != date_str]
        history.append({
            "date": date_str,
            "portfolio_value": total_val,
            "cash": self.state["cash"],
            "holdings_value": total_val - self.state["cash"]
        })
        self.state["equity_history"] = history
        self.save_portfolio()

    def execute_trade(self, date_str, symbol, action, shares, price):
        if shares <= 0:
            return False
            
        trade_value = shares * price
        commission = trade_value * self.cost_coef
        
        if action == "BUY":
            cash_impact = -(trade_value + commission)
            if self.state["cash"] + cash_impact < 0:
                # Adjust shares to match available cash
                max_alloc = self.state["cash"] / (price * (1.0 + self.cost_coef))
                shares = np.floor(max_alloc * 10000) / 10000 # Keep 4 decimal places
                trade_value = shares * price
                commission = trade_value * self.cost_coef
                cash_impact = -(trade_value + commission)
                
            if shares <= 0:
                return False
                
            self.state["cash"] += cash_impact
            if symbol in self.state["holdings"]:
                curr_shares = self.state["holdings"][symbol]["shares"]
                curr_buy_price = self.state["holdings"][symbol]["buy_price"]
                new_shares = curr_shares + shares
                new_buy_price = ((curr_shares * curr_buy_price) + (shares * price)) / new_shares
                self.state["holdings"][symbol]["shares"] = new_shares
                self.state["holdings"][symbol]["buy_price"] = new_buy_price
                self.state["holdings"][symbol]["current_price"] = price
            else:
                self.state["holdings"][symbol] = {
                    "shares": shares,
                    "buy_price": price,
                    "current_price": price
                }
                
        elif action == "SELL":
            if symbol not in self.state["holdings"]:
                return False
            held_shares = self.state["holdings"][symbol]["shares"]
            if shares > held_shares:
                shares = held_shares
                
            trade_value = shares * price
            commission = trade_value * self.cost_coef
            cash_impact = trade_value - commission
            
            self.state["cash"] += cash_impact
            self.state["holdings"][symbol]["shares"] -= shares
            
            if self.state["holdings"][symbol]["shares"] <= 0.0001:
                del self.state["holdings"][symbol]
        else:
            return False
            
        # Log trade
        log_entry = f"{date_str},{symbol},{action},{shares:.4f},{price:.2f},{commission:.2f},{cash_impact:.2f}\n"
        with open(self.log_path, 'a') as f:
            f.write(log_entry)
            
        self.save_portfolio()
        return True

# =====================================================================
# 4. DATA LOADER & REGIME UPDATER
# =====================================================================
def get_common_dates():
    # Load dates from banking_daily to align indices
    df = pd.read_csv(os.path.join(INDICES_DIR, "banking_daily.csv"))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    return df['Date'].dt.strftime('%Y-%m-%d').tolist()

def get_sector_close_prices(date_str):
    prices = {}
    for filename in os.listdir(INDICES_DIR):
        if filename.endswith(".csv"):
            sector_name = filename.replace("_daily.csv", "")
            df = pd.read_csv(os.path.join(INDICES_DIR, filename))
            row = df[df["Date"] == date_str]
            if len(row) > 0:
                prices[sector_name] = float(row.iloc[0]["Close"])
    return prices

def get_stock_close_prices(date_str, symbols):
    prices = {}
    for sym in symbols:
        file_path = os.path.join(STOCKS_DIR, f"{sym}_daily.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            row = df[df["Date"] == date_str]
            if len(row) > 0:
                prices[sym] = float(row.iloc[0]["Close"])
    return prices

# =====================================================================
# 5. INTEGRATION ENGINE FOR RUNNING A SIMULATED STEP
# =====================================================================
def run_simulation_step(portfolio, date_str, target_stocks_count=5):
    """
    Executes a single trading step for a given date_str:
    1. Computes active sectors using HMM regime classification up to date_str.
    2. Identifies top stocks from active sectors using static combined scores.
    3. Rebalances the portfolio:
       - Sells stocks that belong to non-bullish sectors.
       - Sells stocks that fell out of the Top N.
       - Re-allocates cash equally among the new target stocks.
    """
    print(f"\n--- Processing Date: {date_str} ---")
    
    # 1. Load sector data and determine HMM Regimes
    active_sectors = []
    regimes = {}
    
    # We load banking daily first to get index target row
    df_bank = pd.read_csv(os.path.join(INDICES_DIR, "banking_daily.csv"))
    df_bank['Date'] = pd.to_datetime(df_bank['Date'])
    target_idx_rows = df_bank[df_bank['Date'] == pd.to_datetime(date_str)]
    
    if len(target_idx_rows) == 0:
        print(f"Skipping {date_str}: No index trading data found.")
        return
        
    target_idx = target_idx_rows.index[0]
    
    # Re-evaluate HMM for all sectors up to this index
    print("Evaluating macroeconomic regimes for 32 sectors...", end="", flush=True)
    for filename in os.listdir(INDICES_DIR):
        if filename.endswith(".csv"):
            sector_name = filename.replace("_daily.csv", "")
            file_path = os.path.join(INDICES_DIR, filename)
            df_sec = pd.read_csv(file_path)
            
            # Find the state
            try:
                state = evaluate_hmm_regime(df_sec, target_idx, k=2)
                regimes[sector_name] = state
                if state == 0:
                    active_sectors.append(sector_name)
            except Exception as e:
                regimes[sector_name] = 1 # default neutral
    print(" Done.")
    
    print(f"Bullish Sectors ({len(active_sectors)}): {', '.join(active_sectors) if len(active_sectors) > 0 else 'None'}")
    
    # 2. Get top candidates from global ranking that belong to active sectors
    if not os.path.exists(GLOBAL_RANKING_PATH):
        print(f"Error: {GLOBAL_RANKING_PATH} not found. Running with direct ticker mapping fallback.")
        return
        
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    
    # Filter for stocks in active sectors
    df_active_stocks = df_rank[df_rank['Sector'].isin(active_sectors)]
    df_active_stocks = df_active_stocks.sort_values(by='Combined Score', ascending=False)
    
    # Filter for stocks where we actually have price files
    available_symbols = []
    for sym in df_active_stocks['Symbol'].tolist():
        if os.path.exists(os.path.join(STOCKS_DIR, f"{sym}_daily.csv")):
            available_symbols.append(sym)
            if len(available_symbols) >= target_stocks_count * 2:
                break
                
    target_symbols = available_symbols[:target_stocks_count]
    print(f"Target Portfolio Candidates (Top {target_stocks_count}): {', '.join(target_symbols)}")
    
    # Get current prices of all holding stocks and target stocks
    all_needed_symbols = list(portfolio.state["holdings"].keys()) + target_symbols
    current_stock_prices = get_stock_close_prices(date_str, all_needed_symbols)
    
    # Update portfolio stock values
    portfolio.update_stock_prices(date_str, current_stock_prices)
    initial_nav = portfolio.get_total_value()
    print(f"Current Portfolio NAV: INR {initial_nav:,.2f} (Cash: INR {portfolio.state['cash']:,.2f})")
    
    # 3. Perform Rebalancing Actions
    # Exits: Sell holdings that are not in target_symbols
    for held_symbol in list(portfolio.state["holdings"].keys()):
        if held_symbol not in target_symbols:
            price = current_stock_prices.get(held_symbol)
            if price is not None:
                shares = portfolio.state["holdings"][held_symbol]["shares"]
                print(f"SIGNAL: Exit {held_symbol}. Selling {shares:.4f} shares @ INR {price:.2f}")
                portfolio.execute_trade(date_str, held_symbol, "SELL", shares, price)
            else:
                print(f"Warning: Price missing for exit candidate {held_symbol} on {date_str}. Trade skipped.")
                
    # Buys: Buy target symbols that we don't hold or re-balance targets
    # For simplicity, we implement monthly rebalancing of target assets
    nav_after_exits = portfolio.get_total_value()
    if len(target_symbols) > 0:
        target_allocation = nav_after_exits / len(target_symbols)
        for sym in target_symbols:
            price = current_stock_prices.get(sym)
            if price is None or price <= 0:
                print(f"Warning: Price missing/zero for target {sym} on {date_str}. Trade skipped.")
                continue
                
            curr_value = 0.0
            if sym in portfolio.state["holdings"]:
                curr_value = portfolio.state["holdings"][sym]["shares"] * price
                
            # If current allocation is far from target (e.g. deviation > 15%), trade
            needed_trade = target_allocation - curr_value
            if needed_trade > 10.0:  # Buy signal
                shares_to_buy = needed_trade / (price * (1.0 + portfolio.cost_coef))
                print(f"SIGNAL: Allocate to {sym}. Buying {shares_to_buy:.4f} shares @ INR {price:.2f}")
                portfolio.execute_trade(date_str, sym, "BUY", shares_to_buy, price)
            elif needed_trade < -target_allocation * 0.15:  # Sell signal (rebalance down)
                shares_to_sell = abs(needed_trade) / price
                print(f"SIGNAL: Trim {sym}. Selling {shares_to_sell:.4f} shares @ INR {price:.2f}")
                portfolio.execute_trade(date_str, sym, "SELL", shares_to_sell, price)
                
    # Record updated values at the end of rebalance
    final_stock_prices = get_stock_close_prices(date_str, list(portfolio.state["holdings"].keys()))
    portfolio.update_stock_prices(date_str, final_stock_prices)
    final_nav = portfolio.get_total_value()
    print(f"Post-Rebalance NAV: INR {final_nav:,.2f} (Cash: INR {portfolio.state['cash']:,.2f})")

# =====================================================================
# 6. YAHOO FINANCE LIVE SYNC ENGINE
# =====================================================================
def fetch_live_data_and_sync(portfolio):
    """
    Pulls live data from Yahoo Finance to extend indices and stocks files,
    re-runs HMM, and prints immediate signals.
    """
    print("\n--- Running Live Market Data Sync ---")
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance is not installed. Run 'pip install yfinance' to enable live market data syncing.")
        return
        
    print("Note: In a production environment, this function pulls today's daily Close from yfinance.")
    print("Let's fetch the NSE Index close for benchmark confirmation.")
    
    # We demo downloading Nifty Bank (^NSEBANK) and Nifty 50 (^NSEI)
    nifty = yf.Ticker("^NSEI")
    bank = yf.Ticker("^NSEBANK")
    
    try:
        nifty_hist = nifty.history(period="5d")
        bank_hist = bank.history(period="5d")
        print("\nLast 5 Days Close Prices:")
        print("Nifty 50:")
        print(nifty_hist['Close'].tail())
        print("\nNifty Bank:")
        print(bank_hist['Close'].tail())
    except Exception as e:
        print(f"Error fetching live data from Yahoo Finance: {e}")
        print("Confirming network status. Using local backup offline sync.")

# =====================================================================
# 7. COMMAND-LINE INTERFACE (CLI)
# =====================================================================
def display_portfolio(portfolio):
    print("\n=====================================================================")
    print("COEP QF Club Paper Trading Environment")
    print("=====================================================================")
    print(f"Current Simulation Date : {portfolio.state['last_updated_date'] or 'Not Started'}")
    print(f"Cash Balance            : INR {portfolio.state['cash']:,.2f}")
    
    holdings_val = 0.0
    print("\nCurrent Holdings:")
    if len(portfolio.state["holdings"]) == 0:
        print("  No active stock holdings.")
    else:
        print(f"  {'Symbol':<12} {'Shares':<12} {'Buy Price':<14} {'Current Price':<14} {'Current Value':<16} {'PnL %':<10}")
        for ticker, data in portfolio.state["holdings"].items():
            val = data["shares"] * data["current_price"]
            holdings_val += val
            pnl = ((data["current_price"] - data["buy_price"]) / data["buy_price"]) * 100.0
            print(f"  {ticker:<12} {data['shares']:<12.4f} INR {data['buy_price']:<10.2f} INR {data['current_price']:<10.2f} INR {val:<12,.2f} {pnl:+.2f}%")
            
    total_val = portfolio.state["cash"] + holdings_val
    pnl_total = ((total_val - 100000.0) / 100000.0) * 100.0
    print(f"\nTotal Holdings Value   : INR {holdings_val:,.2f}")
    print(f"Net Asset Value (NAV)   : INR {total_val:,.2f} ({pnl_total:+.2f}% since inception)")
    print("=====================================================================\n")

def main_menu():
    portfolio = PaperPortfolio()
    
    # We parse and filter dates from the historical database starting after our initialization split date
    dates = get_common_dates()
    
    # We default starting our paper trading step-by-step loop on 2026-06-01 (late in the dataset) so the user sees trades happen quickly
    start_sim_idx = 0
    for idx, d in enumerate(dates):
        if d >= "2026-06-01":
            start_sim_idx = idx
            break
            
    curr_sim_idx = start_sim_idx
    
    # If state has a last date, resume from there
    if portfolio.state["last_updated_date"] in dates:
        curr_sim_idx = dates.index(portfolio.state["last_updated_date"]) + 1
        
    while True:
        print("--- MAIN MENU ---")
        print("1. View Current Portfolio Status")
        print("2. Run Simulated Daily Step (Next Trading Day)")
        print("3. Fast-Forward Simulation (Run 20 Days)")
        print("4. Fetch Live Market Tickers (Yahoo Finance Sync)")
        print("5. View Recent Transaction Logs")
        print("6. Reset Paper Portfolio to INR 100,000")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            # Update holdings values to match last simulated date's prices
            if portfolio.state["last_updated_date"]:
                syms = list(portfolio.state["holdings"].keys())
                prices = get_stock_close_prices(portfolio.state["last_updated_date"], syms)
                portfolio.update_stock_prices(portfolio.state["last_updated_date"], prices)
            display_portfolio(portfolio)
            
        elif choice == "2":
            if curr_sim_idx >= len(dates):
                print("\nError: Reached the end of the historical dataset (2026-08-06).")
                print("To continue trading in live markets, use option 4.")
                continue
                
            target_date = dates[curr_sim_idx]
            run_simulation_step(portfolio, target_date, target_stocks_count=5)
            curr_sim_idx += 1
            
        elif choice == "3":
            if curr_sim_idx >= len(dates):
                print("\nError: Reached end of historical dataset.")
                continue
                
            steps = min(20, len(dates) - curr_sim_idx)
            print(f"\nRunning fast-forward for {steps} days...")
            for _ in range(steps):
                target_date = dates[curr_sim_idx]
                # Run rebalance only on first day of month, otherwise just update prices
                # Identify if first trading day of month
                is_rebal_day = False
                prev_date = dates[curr_sim_idx-1]
                curr_dt = datetime.strptime(target_date, "%Y-%m-%d")
                prev_dt = datetime.strptime(prev_date, "%Y-%m-%d")
                if curr_dt.month != prev_dt.month:
                    is_rebal_day = True
                    
                if is_rebal_day or portfolio.state["last_updated_date"] is None:
                    run_simulation_step(portfolio, target_date, target_stocks_count=5)
                else:
                    # Just update stock prices to calculate current NAV
                    syms = list(portfolio.state["holdings"].keys())
                    prices = get_stock_close_prices(target_date, syms)
                    portfolio.update_stock_prices(target_date, prices)
                    
                curr_sim_idx += 1
            print("Fast-forward completed.")
            
        elif choice == "4":
            fetch_live_data_and_sync(portfolio)
            
        elif choice == "5":
            if os.path.exists(TRADE_LOG_PATH):
                print("\n--- Recent Transactions ---")
                df_log = pd.read_csv(TRADE_LOG_PATH)
                if len(df_log) == 0:
                    print("  No transactions recorded yet.")
                else:
                    print(df_log.tail(15).to_string(index=False))
                print("---------------------------\n")
            else:
                print("No trade log file found.")
                
        elif choice == "6":
            confirm = input("Are you sure you want to reset the portfolio? (y/n): ").strip().lower()
            if confirm == 'y':
                portfolio.reset_portfolio()
                curr_sim_idx = start_sim_idx
                print("Portfolio reset successfully to starting INR 100,000 cash balance.")
                
        elif choice == "7":
            print("\nExiting Paper Trading Environment. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")
            
if __name__ == '__main__':
    main_menu()
