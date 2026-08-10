import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from replicate_pipeline import extract_features_df, fit_ols_ar1_residuals

warnings.filterwarnings("ignore")

def test_agri():
    file_path = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily/agriculture_daily.csv"
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    k = 1
    df_features = extract_features_df(df, k)
    df_features = df_features.dropna().reset_index(drop=True)
    
    start_date = df_features['Date'].min()
    split_date = start_date + pd.DateOffset(years=3)
    t_init = df_features[df_features['Date'] >= split_date].index[0]
    
    T = len(df_features)
    t_curr = t_init
    block_size = 63
    
    print(f"Data length: {T}, t_init: {t_init}", flush=True)
    
    last_hmm = None
    step = 0
    t_start = time.time()
    
    while t_curr < T:
        t_end = min(t_curr + block_size, T)
        
        t0 = time.time()
        prices = df_features['Close_smoothed'].values
        residuals = fit_ols_ar1_residuals(prices, t_curr, t_end)
        t_arima = time.time() - t0
        
        t1 = time.time()
        df_temp = df_features.copy()
        df_temp['ARIMA_Resid'] = 0.0
        df_temp.iloc[:t_end, df_temp.columns.get_loc('ARIMA_Resid')] = residuals
        
        cols = ['Smoothed_Returns', 'Log_Vol', 'ARIMA_Resid']
        train_x = df_temp[cols].iloc[:t_curr].values
        oos_x = df_temp[cols].iloc[t_curr:t_end].values
        
        mean = np.mean(train_x, axis=0)
        std = np.std(train_x, axis=0) + 1e-8
        
        train_x_scaled = (train_x - mean) / std
        t_feat = time.time() - t1
        
        t2 = time.time()
        # Fit HMM with diag covariance and n_iter=5 for warm starts
        if last_hmm is None:
            hmm = GaussianHMM(n_components=3, covariance_type='diag', n_iter=15, random_state=42)
            hmm.fit(train_x_scaled)
        else:
            hmm = GaussianHMM(n_components=3, covariance_type='diag', n_iter=5, init_params='')
            hmm.n_features = 3
            hmm.startprob_ = last_hmm.startprob_.copy()
            hmm.transmat_ = last_hmm.transmat_.copy()
            hmm.means_ = last_hmm.means_.copy()
            
            # Extract diagonal elements for 'diag' covariance
            if last_hmm.covariance_type == 'diag':
                if last_hmm.covars_.ndim == 3:
                    hmm.covars_ = np.array([np.diag(c) for c in last_hmm.covars_]).copy()
                else:
                    hmm.covars_ = last_hmm.covars_.copy()
            else:
                hmm.covars_ = last_hmm.covars_.copy()
                
            try:
                hmm.fit(train_x_scaled)
            except Exception as e:
                hmm = GaussianHMM(n_components=3, covariance_type='diag', n_iter=20, random_state=42)
                hmm.fit(train_x_scaled)
                
        t_hmm = time.time() - t2
        
        print(f"Step {step}: ARIMA={t_arima:.4f}s, Feat={t_feat:.4f}s, HMM={t_hmm:.4f}s, Total={time.time()-t0:.4f}s", flush=True)
        
        last_hmm = hmm
        t_curr = t_end
        step += 1
        
    print(f"k=1: Diag covariance HMM walk-forward took {time.time() - t_start:.3f}s", flush=True)

if __name__ == '__main__':
    test_agri()
