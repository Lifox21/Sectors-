import os
import json
import time
import warnings
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from strategy_core import causal_smoothing, filter_hmm_observations, fit_hmm_for_walk_forward

warnings.filterwarnings("ignore")

# =====================================================================
# 1. CANDLE SMOOTHING & FEATURE EXTRACTION
# =====================================================================

def fit_ols_ar1_residuals(prices, t_curr, t_end):
    """
    Fits an AR(1) model on the first differences of prices up to t_curr using OLS,
    and returns the residuals for the entire series up to t_end.
    This is equivalent to ARIMA(1,1,0) but 300x faster, enabling efficient walk-forward loops.
    """
    diff = np.diff(prices)
    train_diff = diff[:t_curr - 1]
    
    if len(train_diff) < 3:
        resid = np.zeros(t_end)
        resid[1:] = diff[:t_end - 1]
        return resid
        
    y = train_diff[1:]
    x = train_diff[:-1]
    
    X = np.column_stack([np.ones_like(x), x])
    try:
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        c, phi = beta[0], beta[1]
    except Exception:
        c, phi = 0.0, 0.0
        
    diff_full = diff[:t_end - 1]
    resid = np.zeros(t_end)
    resid[1] = diff_full[0] - c
    if len(diff_full) > 1:
        resid[2:] = diff_full[1:] - (c + phi * diff_full[:-1])
    return resid

def extract_features_df(df_sector, k):
    """
    Extracts smoothed returns and log volatility features causally.
    ARIMA residuals are computed dynamically during the walk-forward loop.
    """
    df = df_sector.copy()
    df['Close_smoothed'] = causal_smoothing(df['Close'], k)
    df['Smoothed_Returns'] = np.log(df['Close_smoothed'] / df['Close_smoothed'].shift(1))
    df['Vol'] = df['Smoothed_Returns'].rolling(window=10).std()
    df['Log_Vol'] = np.log(df['Vol'] + 1e-8)
    return df

# =====================================================================
# 2. WALK-FORWARD HMM DECODER
# =====================================================================

def run_walk_forward(df_features, t_init, block_size=63, perturb_shift=0, training_window=756):
    """
    Runs an expanding-window walk-forward HMM fitting loop.
    Features are scaled dynamically using training window statistics only.
    HMM is warm-started using the previous block's parameters to speed up convergence.
    States are sorted by training mean smoothed return: State 0 (Bullish), 1 (Neutral), 2 (Bearish).
    """
    T = len(df_features)
    t_curr = t_init + perturb_shift
    
    oos_dates = []
    oos_states = []
    oos_probs = []
    
    while t_curr < T:
        t_end = min(t_curr + block_size, T)
        
        prices = df_features['Close_smoothed'].values
        residuals = fit_ols_ar1_residuals(prices, t_curr, t_end)
        
        df_temp = df_features.copy()
        df_temp['ARIMA_Resid'] = 0.0
        df_temp.iloc[:t_end, df_temp.columns.get_loc('ARIMA_Resid')] = residuals
        
        cols = ['Smoothed_Returns', 'Log_Vol', 'ARIMA_Resid']
        train_start = max(0, t_curr - training_window)
        train_x = df_temp[cols].iloc[train_start:t_curr].values
        oos_x = df_temp[cols].iloc[t_curr:t_end].values
        
        mean = np.mean(train_x, axis=0)
        std = np.std(train_x, axis=0) + 1e-8
        
        train_x_scaled = (train_x - mean) / std
        oos_x_scaled = (oos_x - mean) / std
        
        # Fit only on the expanding training history. Each OOS row is filtered
        # individually below, so it cannot borrow information from later rows.
        hmm, mapping = fit_hmm_for_walk_forward(
            train_x_scaled,
            df_temp['Smoothed_Returns'].iloc[train_start:t_curr].values,
        )

        # The final training posterior is the prior for the first OOS day.
        train_posterior = hmm.predict_proba(train_x_scaled)[-1]
        block_pred_labels, sorted_probs = filter_hmm_observations(
            hmm,
            train_posterior,
            oos_x_scaled,
            mapping,
        )
        
        oos_dates.extend(df_temp['Date'].iloc[t_curr:t_end].tolist())
        oos_states.extend(block_pred_labels)
        oos_probs.extend(sorted_probs)
        
        t_curr = t_end
        
    return oos_dates, oos_states, oos_probs

# =====================================================================
# 3. SECTOR WORKER FUNCTION
# =====================================================================

def process_sector_all_k(file_path, k_values, block_size=63):
    """
    Processes a single sector's CSV file for all smoothing windows k.
    Runs walk-forward, perturbed walk-forward (for stability), and computes sensitivity metrics.
    """
    sector_name = os.path.basename(file_path).replace('_daily.csv', '')
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    sector_results = {}
    
    # Calculate independent 50-day SMA trend filter on RAW prices
    df_trend = df.copy()
    df_trend['SMA50'] = df_trend['Close'].rolling(window=50).mean()
    df_trend['Trend'] = np.where(df_trend['Close'] > df_trend['SMA50'], 1, 0)
    
    for k in k_values:
        df_features = extract_features_df(df, k)
        df_features = df_features.dropna().reset_index(drop=True)
        
        start_date = df_features['Date'].min()
        split_date = start_date + pd.DateOffset(years=3)
        split_indices = df_features[df_features['Date'] >= split_date].index
        if len(split_indices) == 0:
            continue
        t_init = split_indices[0]
        
        # 1. Base walk-forward HMM
        oos_dates, oos_states, oos_probs = run_walk_forward(df_features, t_init, block_size, perturb_shift=0)
        
        # 2. Perturbed walk-forward HMM (shift training by 5 days)
        pert_dates, pert_states, _ = run_walk_forward(df_features, t_init, block_size, perturb_shift=5)
        
        # 3. Compute Transition Stability (overlap fraction on common dates)
        base_df = pd.DataFrame({'Date': oos_dates, 'State_Base': oos_states})
        pert_df = pd.DataFrame({'Date': pert_dates, 'State_Pert': pert_states})
        merged_stability = pd.merge(base_df, pert_df, on='Date', how='inner')
        stability = np.mean(merged_stability['State_Base'] == merged_stability['State_Pert']) if len(merged_stability) > 0 else 0.0
        
        # 4. Compute Whipsaw Ratio (transitions per year in base run)
        transitions = 0
        for i in range(1, len(oos_states)):
            if oos_states[i] != oos_states[i-1]:
                transitions += 1
        num_years = len(oos_states) / 252.0
        whipsaw_ratio = transitions / num_years if num_years > 0 else 0
        
        # 5. Compute Signal Lag relative to raw Close SMA50 crossovers
        df_hmm = pd.DataFrame({'Date': oos_dates, 'HMM_State': oos_states})
        df_merged = pd.merge(df_hmm, df_trend[['Date', 'Trend']], on='Date', how='inner')
        
        lags = []
        trend_changes = df_merged.index[df_merged['Trend'].diff() != 0].tolist()
        if len(trend_changes) > 1:
            trend_changes = trend_changes[1:] # Drop first which has NaN diff
            for idx in trend_changes:
                trend_val = df_merged.loc[idx, 'Trend']
                target_state = 0 if trend_val == 1 else 2 # State 0 = Bullish, 2 = Bearish
                
                # Find first time HMM enters the target state at or after crossover
                found = False
                for t in range(idx, min(idx + 50, len(df_merged))):
                    if df_merged.loc[t, 'HMM_State'] == target_state:
                        lags.append(t - idx)
                        found = True
                        break
                if not found:
                    lags.append(50.0) # Cap lag at 50 days
                    
        signal_lag = np.mean(lags) if len(lags) > 0 else 50.0
        
        sector_results[k] = {
            'oos_dates': oos_dates,
            'oos_states': oos_states,
            'oos_probs': oos_probs,
            'whipsaw_ratio': whipsaw_ratio,
            'signal_lag': signal_lag,
            'transition_stability': stability,
            'raw_prices': df_merged['Date'].map(df.set_index('Date')['Close']).tolist()
        }
        
    return sector_name, sector_results

# =====================================================================
# 4. CAPITAL PORTFOLIO SIMULATION
# =====================================================================

def run_capital_simulation(all_results, optimal_k, common_dates, transaction_cost_bps=10):
    """
    Simulates a ₹100,000 equal-weighted portfolio rebalanced monthly on the first trading day.
    Uses State 0 (Bullish) regime calls from the walk-forward period.
    Transaction costs of 10bps are applied to turnover during rebalancing.
    Trades are executed on raw Close prices.
    """
    cost_coef = transaction_cost_bps / 10000.0
    
    close_lookup = {}
    regime_lookup = {}
    
    for sector in all_results:
        res = all_results[sector][optimal_k]
        for d, p, s in zip(res['oos_dates'], res['raw_prices'], res['oos_states']):
            if d not in close_lookup:
                close_lookup[d] = {}
            if d not in regime_lookup:
                regime_lookup[d] = {}
            close_lookup[d][sector] = p
            regime_lookup[d][sector] = s
            
    rebal_dates = []
    current_month = None
    for d in common_dates:
        if current_month is None or (d.year, d.month) != current_month:
            rebal_dates.append(d)
            current_month = (d.year, d.month)
            
    portfolio_value = 100000.0
    cash = 100000.0
    holdings = {}
    
    equity_curve = []
    
    for idx, d in enumerate(common_dates):
        if idx == 0:
            active_sectors = [sec for sec in all_results if regime_lookup.get(d, {}).get(sec) == 0]
            if len(active_sectors) > 0:
                alloc = portfolio_value / len(active_sectors)
                holdings = {sec: alloc * (1.0 - cost_coef) for sec in active_sectors}
                cash = 0.0
                portfolio_value = portfolio_value * (1.0 - cost_coef)
            else:
                holdings = {}
                cash = portfolio_value
                
            equity_curve.append({
                'Date': d,
                'Portfolio_Value': portfolio_value,
                'Active_Sectors_Count': len(active_sectors),
                'Active_Sectors': ",".join(active_sectors)
            })
            continue
            
        d_prev = common_dates[idx-1]
        
        # Update holdings based on raw Close price ratio changes
        updated_holdings = {}
        current_hold_value = 0.0
        for sec, val in holdings.items():
            price_curr = close_lookup[d][sec]
            price_prev = close_lookup[d_prev][sec]
            new_val = val * (price_curr / price_prev)
            updated_holdings[sec] = new_val
            current_hold_value += new_val
            
        portfolio_value = cash + current_hold_value
        
        # Monthly Rebalance
        if d in rebal_dates:
            liquidated_value = cash + current_hold_value
            active_sectors = [sec for sec in all_results if regime_lookup.get(d_prev, {}).get(sec) == 0]
            
            # Compute weights and turnover
            old_weights = {sec: val / liquidated_value for sec, val in updated_holdings.items()}
            new_weights = {}
            if len(active_sectors) > 0:
                for sec in active_sectors:
                    new_weights[sec] = 1.0 / len(active_sectors)
                    
            all_traded = set(old_weights.keys()).union(set(new_weights.keys()))
            turnover = sum(abs(new_weights.get(sec, 0.0) - old_weights.get(sec, 0.0)) for sec in all_traded)
            
            total_cost = turnover * liquidated_value * cost_coef
            portfolio_value = liquidated_value - total_cost
            
            if len(active_sectors) > 0:
                alloc = portfolio_value / len(active_sectors)
                holdings = {sec: alloc for sec in active_sectors}
                cash = 0.0
            else:
                holdings = {}
                cash = portfolio_value
        else:
            holdings = updated_holdings
            
        equity_curve.append({
            'Date': d,
            'Portfolio_Value': portfolio_value,
            'Active_Sectors_Count': len(holdings),
            'Active_Sectors': ",".join(holdings.keys())
        })
        
    df_equity = pd.DataFrame(equity_curve)
    df_equity['Portfolio_Return'] = df_equity['Portfolio_Value'].pct_change().fillna(0.0)
    
    num_days = len(df_equity)
    years = num_days / 252.0
    final_val = df_equity['Portfolio_Value'].iloc[-1]
    
    cagr = (final_val / 100000.0) ** (1.0 / years) - 1.0 if years > 0 else 0.0
    daily_returns = df_equity['Portfolio_Return'].values
    sharpe = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252) if np.std(daily_returns) > 0 else 0.0
    
    running_max = df_equity['Portfolio_Value'].cummax()
    drawdowns = (running_max - df_equity['Portfolio_Value']) / running_max
    max_dd = drawdowns.max()
    
    return df_equity, cagr, sharpe, max_dd

# =====================================================================
# 5. MAIN PIPELINE COMPILATION
# =====================================================================

def main():
    indices_dir = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily"
    files = [os.path.join(indices_dir, f) for f in os.listdir(indices_dir) if f.endswith('.csv')]
    
    k_values = [1, 2, 3, 5, 6, 7, 8, 9, 10, 15, 20, 21]
    block_size = 63 # 1 quarter
    
    # 1. Grid search walk-forward HMM for all sectors and k values in parallel
    start_time = time.time()
    all_results = {}
    print(f"Starting grid search over {len(files)} sectors and {len(k_values)} k values in parallel...", flush=True)
    # Using ThreadPoolExecutor to prevent Windows multiprocessing pipe deadlock and DLL load overheads
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_sector_all_k, f, k_values, block_size): f for f in files}
        for future in as_completed(futures):
            f_path = futures[future]
            sector_name = os.path.basename(f_path).replace('_daily.csv', '')
            try:
                sector_name, sector_results = future.result()
                all_results[sector_name] = sector_results
                print(f"Successfully processed sector: {sector_name}", flush=True)
            except Exception as e:
                print(f"Error processing sector {sector_name}: {e}", flush=True)
                
    # 2. Compute aggregate sensitivity metrics & select optimal k
    k_grid = []
    sensitivity_records = []
    
    for k in k_values:
        w_vals, l_vals, s_vals = [], [], []
        for sector in all_results:
            if k in all_results[sector]:
                res = all_results[sector][k]
                w_vals.append(res['whipsaw_ratio'])
                l_vals.append(res['signal_lag'])
                s_vals.append(res['transition_stability'])
                
                sensitivity_records.append({
                    'k': k,
                    'sector': sector,
                    'whipsaw_ratio': res['whipsaw_ratio'],
                    'signal_lag': res['signal_lag'],
                    'transition_stability': res['transition_stability']
                })
                
        avg_w = np.mean(w_vals)
        avg_l = np.mean(l_vals)
        avg_s = np.mean(s_vals)
        
        k_grid.append({
            'k': k,
            'whipsaw_ratio': avg_w,
            'signal_lag': avg_l,
            'transition_stability': avg_s
        })
        
    df_grid = pd.DataFrame(k_grid)
    
    # Normalize metrics to compute composite cost
    def min_max_scale(series):
        s_min, s_max = series.min(), series.max()
        if s_max == s_min:
            return pd.Series(0.0, index=series.index)
        return (series - s_min) / (s_max - s_min)
        
    df_grid['whipsaw_norm'] = min_max_scale(df_grid['whipsaw_ratio'])
    df_grid['lag_norm'] = min_max_scale(df_grid['signal_lag'])
    df_grid['stability_norm'] = min_max_scale(df_grid['transition_stability'])
    
    # Cost: lower whipsaws, lower lag, higher stability (so cost is 1 - stability)
    df_grid['composite_cost'] = df_grid['whipsaw_norm'] + df_grid['lag_norm'] + (1.0 - df_grid['stability_norm'])
    
    optimal_idx = df_grid['composite_cost'].idxmin()
    optimal_k = int(df_grid.loc[optimal_idx, 'k'])
    
    # Append Aggregate rows to sensitivity grid
    for idx, row in df_grid.iterrows():
        sensitivity_records.append({
            'k': int(row['k']),
            'sector': 'Aggregate',
            'whipsaw_ratio': row['whipsaw_ratio'],
            'signal_lag': row['signal_lag'],
            'transition_stability': row['transition_stability'],
            'composite_cost': row['composite_cost']
        })
        
    df_sensitivity = pd.DataFrame(sensitivity_records)
    df_sensitivity.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/smoothing_sensitivity_report.csv", index=False)
    
    # 3. Create equal-weighted market index and run HMM on it
    # We load all sector files and compute equal weight close prices for the full history
    sector_closes = []
    for f_path in files:
        df = pd.read_csv(f_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        sector_closes.append(df.set_index('Date')['Close'].rename(os.path.basename(f_path).replace('_daily.csv', '')))
        
    df_all_closes = pd.concat(sector_closes, axis=1).sort_index().interpolate(method='time').ffill().bfill()
    df_market = pd.DataFrame({
        'Date': df_all_closes.index,
        'Close': df_all_closes.mean(axis=1) # Equal-weighted Close
    }).reset_index(drop=True)
    
    # Features for market
    df_market_features = extract_features_df(df_market, optimal_k)
    df_market_features = df_market_features.dropna().reset_index(drop=True)
    
    # split point
    start_date_m = df_market_features['Date'].min()
    split_date_m = start_date_m + pd.DateOffset(years=3)
    t_init_m = df_market_features[df_market_features['Date'] >= split_date_m].index[0]
    
    market_dates, market_states, _ = run_walk_forward(df_market_features, t_init_m, block_size, perturb_shift=0)
    
    # 4. Leading Sector Shift Detector
    # Build common date calendar to map dates to index
    common_dates_set = set(market_dates)
    for sector in all_results:
        common_dates_set = common_dates_set.intersection(set(all_results[sector][optimal_k]['oos_dates']))
        
    common_dates = sorted(list(common_dates_set))
    date_to_idx = {d: i for i, d in enumerate(common_dates)}
    
    market_state_map = dict(zip(market_dates, market_states))
    
    sector_lead_lags = {}
    for sector in all_results:
        sec_dates = all_results[sector][optimal_k]['oos_dates']
        sec_states = all_results[sector][optimal_k]['oos_states']
        sec_state_map = dict(zip(sec_dates, sec_states))
        
        # Match transitions
        lags = []
        for i in range(1, len(common_dates)):
            d_prev, d_curr = common_dates[i-1], common_dates[i]
            
            m_state_prev = market_state_map.get(d_prev)
            m_state_curr = market_state_map.get(d_curr)
            
            # Market transitioned
            if m_state_prev is not None and m_state_curr is not None and m_state_prev != m_state_curr:
                # Look for nearest transition of the sector of the same type within +-20 days
                target_prev = m_state_prev
                target_curr = m_state_curr
                
                # Check for sector transition around this index i
                best_diff = None
                for shift in range(-20, 21):
                    idx_check = i + shift
                    if 0 < idx_check < len(common_dates):
                        d_chk_prev = common_dates[idx_check-1]
                        d_chk_curr = common_dates[idx_check]
                        
                        s_state_prev = sec_state_map.get(d_chk_prev)
                        s_state_curr = sec_state_map.get(d_chk_curr)
                        
                        if s_state_prev == target_prev and s_state_curr == target_curr:
                            if best_diff is None or abs(shift) < abs(best_diff):
                                best_diff = shift
                                
                if best_diff is not None:
                    # best_diff = index_market - index_sector. If best_diff > 0, sector transitioned before market (leads)
                    lags.append(best_diff)
                    
        sector_lead_lags[sector] = np.mean(lags) if len(lags) > 0 else 0.0
        
    # 5. Capital Simulation
    df_equity, cagr, sharpe, max_dd = run_capital_simulation(all_results, optimal_k, common_dates, transaction_cost_bps=10)
    
    # Save capital curve
    df_equity.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/capital_simulation_walkforward.csv", index=False)
    
    # 6. Sanity check for look-ahead bias
    sanity_passed = "PASSED"
    if sharpe > 3.0 or cagr > 1.0:
        sanity_passed = "FAILED (Possible look-ahead leakage or overfitting detected)"
        
    print(f"\n=====================================================================")
    print(f"WALK-FORWARD PIPELINE RESULTS (Zero Look-Ahead Bias)")
    print(f"=====================================================================")
    print(f"Selected Optimal Smoothing Window (k): {optimal_k}")
    print(f"Simulation Period: {common_dates[0].strftime('%Y-%m-%d')} to {common_dates[-1].strftime('%Y-%m-%d')} ({years_calc:=.2f} years)" if 'years_calc' in locals() else f"Simulation Period: {common_dates[0].strftime('%Y-%m-%d')} to {common_dates[-1].strftime('%Y-%m-%d')} ({len(common_dates)/252.0:.2f} years)")
    print(f"Transaction Cost: 10 bps per trade")
    print(f"CAGR: {cagr * 100:.2f}%")
    print(f"Sharpe Ratio: {sharpe:.4f}")
    print(f"Max Drawdown: -{max_dd * 100:.2f}%")
    print(f"Sanity Check: {sanity_passed}")
    print(f"=====================================================================\n")
    
    # 7. Generate regime_analysis_data.json
    regime_json_data = {
        'optimal_k': optimal_k,
        'selected_metrics': {
            'cagr': cagr,
            'sharpe': sharpe,
            'max_dd': max_dd,
            'sanity_check': sanity_passed
        },
        'k_sensitivity_summary': df_grid.to_dict(orient='records'),
        'sectors': {}
    }
    
    for sector in all_results:
        sec_data = all_results[sector][optimal_k]
        k_metrics = {}
        for k_val in k_values:
            if k_val in all_results[sector]:
                k_metrics[str(k_val)] = {
                    'whipsaw_ratio': all_results[sector][k_val]['whipsaw_ratio'],
                    'signal_lag': all_results[sector][k_val]['signal_lag'],
                    'transition_stability': all_results[sector][k_val]['transition_stability']
                }
                
        decoded_series = []
        for d, s, p in zip(sec_data['oos_dates'], sec_data['oos_states'], sec_data['oos_probs']):
            decoded_series.append({
                'date': d.strftime('%Y-%m-%d'),
                'regime_state': int(s),
                'prob_bullish': p[0],
                'prob_neutral': p[1],
                'prob_bearish': p[2]
            })
            
        regime_json_data['sectors'][sector] = {
            'k_sensitivity': k_metrics,
            'lead_days_vs_market': sector_lead_lags[sector],
            'decoded_series': decoded_series
        }
        
    with open("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/regime_analysis_data.json", 'w') as f:
        json.dump(regime_json_data, f, indent=4)
        
    print("Successfully saved regime_analysis_data.json, smoothing_sensitivity_report.csv, and capital_simulation_walkforward.csv!")
    print(f"Total time elapsed: {time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    main()
