"""
Walk-Forward Benchmark Simulation (2022-2026)
COEP Quantitative Finance Club - HMM Sector Rotation Strategy

Tests the impact of turnover dampeners (SwapPolicy + Sector Caps + Stop Loss)
under full realistic Indian equity cash delivery cost modeling (STT, Stamp Duty,
Exchange Turnover, SEBI Fees, GST, DP Charges, and Slippage).
"""

import os
import sys
import math
import numpy as np
import pandas as pd
from datetime import datetime

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from strategy_core import SwapPolicy, apply_sector_caps

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDICES_REGIME_PATH = os.path.join(WORKSPACE_DIR, "sector_regime_hmm.csv")
GLOBAL_RANKING_PATH = os.path.join(WORKSPACE_DIR, "scored_csv/global_ranking.csv")
STOCKS_DIR = os.path.join(WORKSPACE_DIR, "Stocks/Daily")
OUTPUT_CSV_PATH = os.path.join(WORKSPACE_DIR, "scratch/walkforward_2022_2026_comparison.csv")

def calculate_indian_trade_costs(side: str, trade_value: float) -> float:
    """
    Computes exact statutory Indian equity cash delivery friction.
    """
    if trade_value <= 0:
        return 0.0
    
    slippage = trade_value * 0.0010         # 10 bps slippage
    exch_txn = trade_value * 0.0000345      # NSE 0.00345%
    sebi_fee = trade_value * 0.0000010      # SEBI Rs 10 / Cr
    gst = (exch_txn + sebi_fee) * 0.18      # 18% GST on exchange + sebi
    
    if side.upper() == 'BUY':
        stamp_duty = trade_value * 0.00015  # Stamp duty 1.5 bps
        stt = 0.0
        dp_charge = 0.0
    else: # SELL
        stamp_duty = 0.0
        stt = trade_value * 0.0010          # STT 10 bps on sell
        dp_charge = 15.93                   # CDSL/NSDL DP charge per scrip exit
        
    return slippage + exch_txn + sebi_fee + gst + stamp_duty + stt + dp_charge

def load_data():
    df_regimes = pd.read_csv(INDICES_REGIME_PATH)
    df_regimes['Date'] = pd.to_datetime(df_regimes['Date'])
    df_regimes = df_regimes.sort_values('Date').reset_index(drop=True)
    
    # Filter for 2022-2026 period
    df_regimes = df_regimes[df_regimes['Date'] >= pd.to_datetime('2022-01-01')].reset_index(drop=True)
    
    df_rank = pd.read_csv(GLOBAL_RANKING_PATH)
    rank_scores = dict(zip(df_rank['Symbol'], df_rank['Combined Score']))
    stock_sectors = dict(zip(df_rank['Symbol'], df_rank['Sector']))
    
    # Load prices for ranked stocks
    stock_dfs = {}
    for sym in df_rank['Symbol'].unique():
        fpath = os.path.join(STOCKS_DIR, f"{sym}_daily.csv")
        if os.path.exists(fpath):
            df_s = pd.read_csv(fpath)
            df_s['Date'] = pd.to_datetime(df_s['Date'])
            df_s = df_s.set_index('Date')
            stock_dfs[sym] = df_s
            
    sectors = [col.replace('_returns', '') for col in df_regimes.columns if col.endswith('_returns')]
    return df_regimes, df_rank, rank_scores, stock_sectors, stock_dfs, sectors

def simulate_engine(mode: str, initial_capital: float = 150000.0):
    df_regimes, df_rank, rank_scores, stock_sectors, stock_dfs, sectors = load_data()
    dates = df_regimes['Date'].tolist()
    
    cash = initial_capital
    holdings = {}        # sym -> shares
    entry_prices = {}    # sym -> entry price
    entry_indices = {}   # sym -> bar index of entry
    peak_prices = {}     # sym -> peak price
    
    total_friction_paid = 0.0
    trade_count = 0
    winning_trades = 0
    closed_trades = 0
    
    swap_policy = SwapPolicy(swap_margin=0.15, min_holding_days=5, stop_loss_pct=0.08)
    stop_loss_pct = 0.08 # -8% trailing stop loss
    
    history = []
    current_month = None
    
    for idx, d in enumerate(dates):
        d_str = d.strftime('%Y-%m-%d')
        
        # 1. Update prices & check stop loss
        current_prices = {}
        for sym in list(holdings.keys()):
            if sym in stock_dfs and d in stock_dfs[sym].index:
                p = float(stock_dfs[sym].loc[d, 'Close'])
                current_prices[sym] = p
                peak_prices[sym] = max(peak_prices.get(sym, p), p)
            else:
                current_prices[sym] = entry_prices.get(sym, 1.0)
                
        # 2. Determine Bullish Sectors (State 0)
        active_sectors = []
        for sec in sectors:
            col = f"{sec}_returns"
            if col in df_regimes.columns and df_regimes.loc[idx, col] == 0:
                active_sectors.append(sec)
                
        # 3. Determine Rebalance Day
        is_rebalance_day = False
        if mode == 'monthly':
            if current_month is None or d.month != current_month:
                is_rebalance_day = True
                current_month = d.month
        elif mode in ('naive_daily', 'enhanced'):
            is_rebalance_day = True # evaluates every trading day
            
        if is_rebalance_day:
            df_active = df_rank[df_rank['Sector'].isin(active_sectors)].copy()
            df_active = df_active.sort_values(by='Combined Score', ascending=False)
            
            # Filter available stocks with trading data today
            available_symbols = [s for s in df_active['Symbol'] if s in stock_dfs and d in stock_dfs[s].index]
            df_active = df_active[df_active['Symbol'].isin(available_symbols)].copy()
            
            if mode == 'naive_daily':
                # No sector caps, no swap buffer
                target_symbols = available_symbols[:5]
            elif mode == 'monthly':
                # Monthly rebalance with top 5
                target_symbols = available_symbols[:5]
            elif mode == 'enhanced':
                holdings_dict = {}
                for s, sh in holdings.items():
                    entry_idx = entry_indices.get(s, idx)
                    holdings_dict[s] = {
                        "shares": sh,
                        "buy_price": entry_prices.get(s, current_prices.get(s, 0.0)),
                        "entry_date": dates[entry_idx].strftime('%Y-%m-%d'),
                        "sector": stock_sectors.get(s, "unknown")
                    }
                
                target_symbols, _, _ = swap_policy.evaluate_portfolio(
                    holdings=holdings_dict,
                    active_sectors=active_sectors,
                    candidate_df=df_active,
                    current_date_str=d_str,
                    max_positions=5,
                    max_per_sector=1,
                    live_prices=current_prices,
                )
                
            # Execute Rebalance:
            if len(target_symbols) == 0:
                # Liquidate all
                for sym in list(holdings.keys()):
                    p = current_prices.get(sym, 0.0)
                    if p > 0:
                        shares = holdings.pop(sym)
                        tval = shares * p
                        cost = calculate_indian_trade_costs('SELL', tval)
                        total_friction_paid += cost
                        cash += (tval - cost)
                        trade_count += 1
                        closed_trades += 1
                        if p > entry_prices.get(sym, p):
                            winning_trades += 1
                        entry_prices.pop(sym, None)
                        entry_indices.pop(sym, None)
                        peak_prices.pop(sym, None)
            else:
                # Sell exits (not in target)
                for sym in list(holdings.keys()):
                    if sym not in target_symbols:
                        p = current_prices.get(sym, 0.0)
                        if p > 0:
                            shares = holdings.pop(sym)
                            tval = shares * p
                            cost = calculate_indian_trade_costs('SELL', tval)
                            total_friction_paid += cost
                            cash += (tval - cost)
                            trade_count += 1
                            closed_trades += 1
                            if p > entry_prices.get(sym, p):
                                winning_trades += 1
                            entry_prices.pop(sym, None)
                            entry_indices.pop(sym, None)
                            peak_prices.pop(sym, None)
                            
                # Equal-weight target allocation
                port_val = cash + sum(holdings.get(s, 0.0) * current_prices.get(s, 0.0) for s in holdings)
                target_alloc = port_val / len(target_symbols)
                
                # Allocate cash to new/underweighted targets
                for sym in target_symbols:
                    p = float(stock_dfs[sym].loc[d, 'Close'])
                    curr_val = holdings.get(sym, 0.0) * p
                    diff = target_alloc - curr_val
                    
                    if diff > 100.0 and cash > 200.0: # Buy
                        buy_budget = min(diff, cash)
                        cost_est = calculate_indian_trade_costs('BUY', buy_budget)
                        net_cash = buy_budget - cost_est
                        if net_cash > 0:
                            shares_to_buy = net_cash / p
                            cost_act = calculate_indian_trade_costs('BUY', shares_to_buy * p)
                            cash -= (shares_to_buy * p + cost_act)
                            total_friction_paid += cost_act
                            
                            if sym not in holdings:
                                entry_prices[sym] = p
                                entry_indices[sym] = idx
                                peak_prices[sym] = p
                            holdings[sym] = holdings.get(sym, 0.0) + shares_to_buy
                            trade_count += 1

        # Calculate EOD NAV
        eod_prices = {}
        for sym in holdings:
            if sym in stock_dfs and d in stock_dfs[sym].index:
                eod_prices[sym] = float(stock_dfs[sym].loc[d, 'Close'])
            else:
                eod_prices[sym] = current_prices.get(sym, entry_prices.get(sym, 1.0))
        h_val = sum(shares * eod_prices.get(sym, 0.0) for sym, shares in holdings.items())
        nav = cash + h_val
        
        history.append({
            'Date': d_str,
            'NAV': nav,
            'Cash': cash,
            'Holdings_Value': h_val,
            'Holdings_Count': len(holdings),
            'Active_Holdings': ",".join(holdings.keys())
        })
        
    df_res = pd.DataFrame(history)
    df_res['Returns'] = df_res['NAV'].pct_change().fillna(0.0)
    
    num_days = len(df_res)
    years = num_days / 252.0
    final_nav = df_res['NAV'].iloc[-1]
    cagr = (final_nav / initial_capital) ** (1.0 / years) - 1.0
    
    rf = 0.065 # 6.5% Indian risk-free rate
    rf_daily = (1.0 + rf)**(1/252) - 1.0
    excess_ret = df_res['Returns'] - rf_daily
    sharpe = np.mean(excess_ret) / (np.std(excess_ret) + 1e-10) * np.sqrt(252)
    
    cummax = df_res['NAV'].cummax()
    max_dd = ((cummax - df_res['NAV']) / cummax).max()
    win_rate = (winning_trades / max(1, closed_trades)) * 100.0
    
    return {
        'mode': mode,
        'final_nav': final_nav,
        'cagr': cagr,
        'total_return': (final_nav - initial_capital) / initial_capital * 100.0,
        'sharpe': sharpe,
        'max_dd': max_dd * 100.0,
        'total_trades': trade_count,
        'friction_paid': total_friction_paid,
        'win_rate': win_rate,
        'history_df': df_res
    }

def main():
    print("================================================================================")
    print(" RUNNING COMPREHENSIVE WALK-FORWARD BENCHMARK (2022 - 2026)")
    print(" Including Full Indian Delivery Statutory Taxes, Fees, DP Charges & Slippage")
    print("================================================================================\n")
    
    modes = ['naive_daily', 'enhanced', 'monthly']
    labels = {
        'naive_daily': 'Naive Daily (No Caps, No Swap Buffer)',
        'enhanced':    'Enhanced Architecture (15% Swap Hurdle + 5D Dwell + Sector Cap)',
        'monthly':     'Monthly Rebalance (Baseline Low-Turnover Benchmark)'
    }
    
    results = {}
    for m in modes:
        print(f"[*] Simulating mode: {labels[m]}...")
        res = simulate_engine(m, initial_capital=150000.0)
        results[m] = res
        print(f"    -> Final NAV: Rs. {res['final_nav']:,.2f} | CAGR: {res['cagr']*100:.2f}% | Sharpe: {res['sharpe']:.2f} | Trades: {res['total_trades']} | Friction: Rs. {res['friction_paid']:,.2f}")
        
    print("\n" + "="*85)
    print(" 2022-2026 WALK-FORWARD BENCHMARK COMPARISON MATRIX (NET OF ALL TAXES & FEES)")
    print("="*85)
    print(f"{'Metric':<30} | {'Naive Daily':<16} | {'Enhanced Daily':<16} | {'Monthly Benchmark':<16}")
    print("-"*85)
    
    print(f"{'Starting Capital':<30} | {'Rs. 1,50,000':<16} | {'Rs. 1,50,000':<16} | {'Rs. 1,50,000':<16}")
    print(f"{'Ending Portfolio NAV':<30} | Rs. {results['naive_daily']['final_nav']:<12,.0f} | Rs. {results['enhanced']['final_nav']:<12,.0f} | Rs. {results['monthly']['final_nav']:<12,.0f}")
    print(f"{'Total Net Return (%)':<30} | {results['naive_daily']['total_return']:>14.2f}% | {results['enhanced']['total_return']:>14.2f}% | {results['monthly']['total_return']:>14.2f}%")
    print(f"{'Annualized CAGR (%)':<30} | {results['naive_daily']['cagr']*100:>14.2f}% | {results['enhanced']['cagr']*100:>14.2f}% | {results['monthly']['cagr']*100:>14.2f}%")
    print(f"{'Sharpe Ratio (Rf=6.5%)':<30} | {results['naive_daily']['sharpe']:>15.2f} | {results['enhanced']['sharpe']:>15.2f} | {results['monthly']['sharpe']:>15.2f}")
    print(f"{'Max Drawdown (%)':<30} | -{results['naive_daily']['max_dd']:>13.2f}% | -{results['enhanced']['max_dd']:>13.2f}% | -{results['monthly']['max_dd']:>13.2f}%")
    print(f"{'Total Trades Executed':<30} | {results['naive_daily']['total_trades']:>15} | {results['enhanced']['total_trades']:>15} | {results['monthly']['total_trades']:>15}")
    print(f"{'Taxes & Slippage Paid':<30} | Rs. {results['naive_daily']['friction_paid']:<12,.0f} | Rs. {results['enhanced']['friction_paid']:<12,.0f} | Rs. {results['monthly']['friction_paid']:<12,.0f}")
    print(f"{'Exit Win Rate (%)':<30} | {results['naive_daily']['win_rate']:>14.1f}% | {results['enhanced']['win_rate']:>14.1f}% | {results['monthly']['win_rate']:>14.1f}%")
    print("="*85 + "\n")

    # Save comparison history
    df_comp = pd.DataFrame({
        'Date': results['enhanced']['history_df']['Date'],
        'NAV_Naive_Daily': results['naive_daily']['history_df']['NAV'],
        'NAV_Enhanced_Architecture': results['enhanced']['history_df']['NAV'],
        'NAV_Monthly_Benchmark': results['monthly']['history_df']['NAV'],
    })
    df_comp.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"[+] Saved complete daily equity curves to: {OUTPUT_CSV_PATH}")

if __name__ == '__main__':
    main()
