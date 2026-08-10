import numpy as np
import time
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def fit_arima_statsmodels(prices, t_curr, t_end):
    train_close = prices[:t_curr]
    model = ARIMA(train_close, order=(1, 1, 0))
    model_fit = model.fit()
    
    full_close = prices[:t_end]
    applied = model_fit.apply(full_close)
    return applied.resid

def fit_arima_numpy(prices, t_curr, t_end):
    # Diff the prices
    diff = np.diff(prices) # length N-1
    
    # Train set diffs
    train_diff = diff[:t_curr - 1]
    
    # We want to fit y_t = c + phi * y_{t-1} + e_t
    # y = train_diff[1:]
    # x = train_diff[:-1]
    y = train_diff[1:]
    x = train_diff[:-1]
    
    # Fit OLS: y = beta0 + beta1 * x
    X = np.column_stack([np.ones_like(x), x])
    # Solve X * beta = y
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    c, phi = beta[0], beta[1]
    
    # Compute residuals for the entire series
    # For t_end close prices, we have t_end-1 diffs
    diff_full = diff[:t_end - 1]
    
    # Residuals: e_t = y_t - (c + phi * y_{t-1})
    # For the first diff element (diff_full[0]), we don't have a lagged value.
    # We can set the residual to 0.0 or diff_full[0] - mean
    resid = np.zeros(t_end)
    # The first close price has no return, resid[0] = 0
    # The second close price (diff_full[0]) has no lagged return, resid[1] = diff_full[0] - c
    resid[1] = diff_full[0] - c
    
    # For the rest, we use the AR(1) formula
    resid[2:] = diff_full[1:] - (c + phi * diff_full[:-1])
    
    return resid

def run_bench():
    prices = np.random.normal(100, 5, 2800)
    
    # Benchmark statsmodels
    start = time.time()
    for _ in range(50):
        fit_arima_statsmodels(prices, 1000, 1063)
    end = time.time()
    print(f"Statsmodels ARIMA(1,1,0) x 50: {end - start:.4f} seconds")
    
    # Benchmark numpy
    start = time.time()
    for _ in range(50):
        fit_arima_numpy(prices, 1000, 1063)
    end = time.time()
    print(f"Numpy OLS AR(1) x 50: {end - start:.4f} seconds")
    
    # Compare output values
    res_sm = fit_arima_statsmodels(prices, 1000, 1063)
    res_np = fit_arima_numpy(prices, 1000, 1063)
    
    # Print a few values to verify closeness
    print("Statsmodels resid (first 5 of test):", res_sm[1000:1005])
    print("Numpy OLS resid (first 5 of test):", res_np[1000:1005])
    print("Max absolute difference (test):", np.max(np.abs(res_sm[1000:1063] - res_np[1000:1063])))

if __name__ == '__main__':
    run_bench()
