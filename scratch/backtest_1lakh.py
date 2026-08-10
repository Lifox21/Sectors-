import os
import numpy as np
import pandas as pd

def run_historical_backtest():
    indices_dir = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily"
    files = [f for f in os.listdir(indices_dir) if f.endswith('.csv')]
    
    # Load decoded regimes
    hmm_regimes = pd.read_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/sector_regime_hmm.csv")
    hsmm_regimes = pd.read_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/sector_regime_hsmm.csv")
    
    hmm_regimes['Date'] = pd.to_datetime(hmm_regimes['Date'])
    hsmm_regimes['Date'] = pd.to_datetime(hsmm_regimes['Date'])
    
    records = []
    initial_capital = 100000.0  # 1 Lakh Rupees
    
    for filename in files:
        sector_name = filename.replace('_daily.csv', '')
        file_path = os.path.join(indices_dir, filename)
        
        # Load daily prices
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Calculate daily log returns
        df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        df = df.dropna().reset_index(drop=True)
        
        # Merge price return with HMM and HSMM regimes
        df_merged = pd.merge(df[['Date', 'Returns']], hmm_regimes[['Date', f"{sector_name}_returns", f"{sector_name}_arima"]], on='Date', how='inner')
        df_merged = pd.merge(df_merged, hsmm_regimes[['Date', f"{sector_name}_returns", f"{sector_name}_arima"]], on='Date', how='inner', suffixes=('_hmm', '_hsmm'))
        
        # Align column names:
        # returns_hmm = f"{sector_name}_returns_hmm"
        # arima_hmm = f"{sector_name}_arima" (from hmm_regimes)
        # returns_hsmm = f"{sector_name}_returns_hsmm"
        # arima_hsmm = f"{sector_name}_arima" (from hsmm_regimes, suffixed as _hsmm)
        
        # Rename columns for convenience
        cols_map = {
            f"{sector_name}_returns_hmm": 'hmm_returns_state',
            f"{sector_name}_arima_hmm": 'hmm_arima_state',
            f"{sector_name}_returns_hsmm": 'hsmm_returns_state',
            f"{sector_name}_arima_hsmm": 'hsmm_arima_state'
        }
        df_merged = df_merged.rename(columns=cols_map)
        
        # Drop rows with NaNs in regimes (dates where regime is not available yet)
        df_merged = df_merged.dropna().reset_index(drop=True)
        
        if len(df_merged) == 0:
            continue
            
        start_date = df_merged['Date'].min()
        end_date = df_merged['Date'].max()
        years = (end_date - start_date).days / 365.25
        
        returns = df_merged['Returns'].values
        
        # Buy & Hold Performance
        bh_final = initial_capital * np.exp(np.sum(returns))
        bh_cagr = (bh_final / initial_capital) ** (1.0 / years) - 1.0
        
        # HMM Returns Strategy Performance
        hmm_ret_mask = (df_merged['hmm_returns_state'].values == 0)
        hmm_ret_final = initial_capital * np.exp(np.sum(np.where(hmm_ret_mask, returns, 0.0)))
        hmm_ret_cagr = (hmm_ret_final / initial_capital) ** (1.0 / years) - 1.0
        
        # HSMM Returns Strategy Performance
        hsmm_ret_mask = (df_merged['hsmm_returns_state'].values == 0)
        hsmm_ret_final = initial_capital * np.exp(np.sum(np.where(hsmm_ret_mask, returns, 0.0)))
        hsmm_ret_cagr = (hsmm_ret_final / initial_capital) ** (1.0 / years) - 1.0
        
        # HMM ARIMA Strategy Performance
        hmm_ari_mask = (df_merged['hmm_arima_state'].values == 0)
        hmm_ari_final = initial_capital * np.exp(np.sum(np.where(hmm_ari_mask, returns, 0.0)))
        hmm_ari_cagr = (hmm_ari_final / initial_capital) ** (1.0 / years) - 1.0
        
        # HSMM ARIMA Strategy Performance
        hsmm_ari_mask = (df_merged['hsmm_arima_state'].values == 0)
        hsmm_ari_final = initial_capital * np.exp(np.sum(np.where(hsmm_ari_mask, returns, 0.0)))
        hsmm_ari_cagr = (hsmm_ari_final / initial_capital) ** (1.0 / years) - 1.0
        
        records.append({
            'Sector': sector_name,
            'Start_Date': start_date.strftime('%Y-%m-%d'),
            'End_Date': end_date.strftime('%Y-%m-%d'),
            'Years': round(years, 2),
            'BH_Final': round(bh_final, 2),
            'BH_CAGR': f"{bh_cagr * 100:.2f}%",
            'HMM_Returns_Final': round(hmm_ret_final, 2),
            'HMM_Returns_CAGR': f"{hmm_ret_cagr * 100:.2f}%",
            'HSMM_Returns_Final': round(hsmm_ret_final, 2),
            'HSMM_Returns_CAGR': f"{hsmm_ret_cagr * 100:.2f}%",
            'HMM_ARIMA_Final': round(hmm_ari_final, 2),
            'HMM_ARIMA_CAGR': f"{hmm_ari_cagr * 100:.2f}%",
            'HSMM_ARIMA_Final': round(hsmm_ari_final, 2),
            'HSMM_ARIMA_CAGR': f"{hsmm_ari_cagr * 100:.2f}%"
        })
        
    out_df = pd.DataFrame(records)
    out_df.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/strategy_performance_1lakh.csv", index=False)
    
    # Compute aggregates (numerical conversion first)
    print("\n=== HISTORICAL BACKTEST SUMMARY (2015-2026) ===")
    print(f"Initial Capital: INR 1,00,000 per sector (Total Universe Capital: INR 32,00,000)\n")
    
    # Convert string CAGR back to float for average
    bh_finals = [r['BH_Final'] for r in records]
    hmm_ret_finals = [r['HMM_Returns_Final'] for r in records]
    hsmm_ret_finals = [r['HSMM_Returns_Final'] for r in records]
    hmm_ari_finals = [r['HMM_ARIMA_Final'] for r in records]
    hsmm_ari_finals = [r['HSMM_ARIMA_Final'] for r in records]
    
    cagrs_bh = [float(r['BH_CAGR'].replace('%', '')) for r in records]
    cagrs_hmm_ret = [float(r['HMM_Returns_CAGR'].replace('%', '')) for r in records]
    cagrs_hsmm_ret = [float(r['HSMM_Returns_CAGR'].replace('%', '')) for r in records]
    cagrs_hmm_ari = [float(r['HMM_ARIMA_CAGR'].replace('%', '')) for r in records]
    cagrs_hsmm_ari = [float(r['HSMM_ARIMA_CAGR'].replace('%', '')) for r in records]
    
    print(f"Buy & Hold:           Avg Final Capital: INR {np.mean(bh_finals):,.2f}  (Avg CAGR: {np.mean(cagrs_bh):.2f}%)")
    print(f"HMM Returns Strategy: Avg Final Capital: INR {np.mean(hmm_ret_finals):,.2f}  (Avg CAGR: {np.mean(cagrs_hmm_ret):.2f}%)")
    print(f"HSMM Returns Strategy:Avg Final Capital: INR {np.mean(hsmm_ret_finals):,.2f}  (Avg CAGR: {np.mean(cagrs_hsmm_ret):.2f}%)")
    print(f"HMM ARIMA Strategy:   Avg Final Capital: INR {np.mean(hmm_ari_finals):,.2f}  (Avg CAGR: {np.mean(cagrs_hmm_ari):.2f}%)")
    print(f"HSMM ARIMA Strategy:  Avg Final Capital: INR {np.mean(hsmm_ari_finals):,.2f}  (Avg CAGR: {np.mean(cagrs_hsmm_ari):.2f}%)")
    
    # Calculate portfolio values (summing across all 32 sectors)
    print("\n--- Portfolio Total Value (Starting Capital: INR 32,00,000) ---")
    print(f"Buy & Hold:           Final Portfolio Value: INR {np.sum(bh_finals):,.2f}")
    print(f"HMM Returns Strategy: Final Portfolio Value: INR {np.sum(hmm_ret_finals):,.2f}")
    print(f"HSMM Returns Strategy:Final Portfolio Value: INR {np.sum(hsmm_ret_finals):,.2f}")
    print(f"HMM ARIMA Strategy:   Final Portfolio Value: INR {np.sum(hmm_ari_finals):,.2f}")
    print(f"HSMM ARIMA Strategy:  Final Portfolio Value: INR {np.sum(hsmm_ari_finals):,.2f}")

if __name__ == '__main__':
    run_historical_backtest()
