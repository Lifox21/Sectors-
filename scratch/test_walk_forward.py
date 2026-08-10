import os
import time
import warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from hmmlearn.hmm import GaussianHMM

warnings.filterwarnings("ignore")

def test_single_sector():
    file_path = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily/banking_daily.csv"
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # 1. Causal Candle Smoothing
    k = 5
    df_smoothed = df.copy()
    for col in ['Open', 'High', 'Low', 'Close']:
        df_smoothed[col] = df_smoothed[col].rolling(window=k).mean()
    
    # Drop rolling NaNs
    df_smoothed = df_smoothed.dropna().reset_index(drop=True)
    
    # Features
    df_smoothed['Smoothed_Returns'] = np.log(df_smoothed['Close'] / df_smoothed['Close'].shift(1))
    df_smoothed['Smoothed_Vol'] = df_smoothed['Smoothed_Returns'].rolling(window=10).std()
    df_smoothed['Log_Vol'] = np.log(df_smoothed['Smoothed_Vol'] + 1e-8)
    
    df_features = df_smoothed.dropna().reset_index(drop=True)
    
    # Initial 3 years training window
    # Find split index
    start_date = df_features['Date'].min()
    split_date = start_date + pd.DateOffset(years=3)
    t_init = df_features[df_features['Date'] >= split_date].index[0]
    
    T = len(df_features)
    block_size = 63  # 1 quarter
    
    print(f"Data length: {T}, Initial train length: {t_init}, Walk-forward length: {T - t_init}")
    
    t_curr = t_init
    oos_dates = []
    oos_regimes = []
    
    start_time = time.time()
    
    # Walk-forward loop
    while t_curr < T:
        t_end = min(t_curr + block_size, T)
        
        # Fit ARIMA(1,1,0) on Close price to get residuals
        train_close = df_features['Close'].iloc[:t_curr].values
        arima_model = ARIMA(train_close, order=(1, 1, 0))
        arima_fit = arima_model.fit()
        
        # Apply to get residuals
        full_close = df_features['Close'].iloc[:t_end].values
        applied = arima_fit.apply(full_close)
        residuals = applied.resid
        residuals[np.isnan(residuals)] = 0.0
        
        # Add residual feature
        df_features.loc[:t_end-1, 'ARIMA_Resid'] = residuals
        
        # Features to fit HMM
        cols = ['Smoothed_Returns', 'Log_Vol', 'ARIMA_Resid']
        train_x = df_features[cols].iloc[:t_curr].values
        oos_x = df_features[cols].iloc[t_curr:t_end].values
        
        # Scale
        mean = np.mean(train_x, axis=0)
        std = np.std(train_x, axis=0) + 1e-8
        train_x_scaled = (train_x - mean) / std
        oos_x_scaled = (oos_x - mean) / std
        
        # Fit HMM
        hmm = GaussianHMM(n_components=3, covariance_type='full', n_iter=30, random_state=42)
        try:
            hmm.fit(train_x_scaled)
        except Exception as e:
            hmm = GaussianHMM(n_components=3, covariance_type='diag', n_iter=30, random_state=42)
            hmm.fit(train_x_scaled)
            
        # Sort states
        train_states = hmm.predict(train_x_scaled)
        train_returns = df_features['Smoothed_Returns'].iloc[:t_curr].values
        state_means = []
        for s in range(3):
            state_mask = (train_states == s)
            if np.sum(state_mask) > 0:
                state_means.append(np.mean(train_returns[state_mask]))
            else:
                state_means.append(-999.0)
                
        sorted_indices = np.argsort(state_means)
        mapping = {sorted_indices[2]: 0, sorted_indices[1]: 1, sorted_indices[0]: 2}
        
        # Predict OOS
        oos_states = hmm.predict(oos_x_scaled)
        oos_labels = [mapping[s] for s in oos_states]
        
        oos_dates.extend(df_features['Date'].iloc[t_curr:t_end].tolist())
        oos_regimes.extend(oos_labels)
        
        t_curr = t_end
        
    end_time = time.time()
    print(f"Time taken for walk-forward HMM fitting on 1 sector: {end_time - start_time:.4f} seconds")
    print(f"Decoded {len(oos_regimes)} walk-forward points.")
    print("State value counts:", pd.Series(oos_regimes).value_counts().to_dict())

if __name__ == '__main__':
    test_single_sector()
