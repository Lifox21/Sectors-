import os
import sys
import time
import warnings
import numpy as np
import pandas as pd

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from replicate_pipeline import extract_features_df, run_walk_forward

warnings.filterwarnings("ignore")

def debug_speed():
    file_path = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily/banking_daily.csv"
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    k_values = [1, 2, 3, 5, 6, 7, 8, 9, 10, 15, 20, 21]
    
    print("Starting debug run...")
    for k in k_values:
        t0 = time.time()
        
        # Features extraction
        df_features = extract_features_df(df, k)
        df_features = df_features.dropna().reset_index(drop=True)
        
        start_date = df_features['Date'].min()
        split_date = start_date + pd.DateOffset(years=3)
        split_indices = df_features[df_features['Date'] >= split_date].index
        if len(split_indices) == 0:
            print(f"k={k}: No split indices.")
            continue
        t_init = split_indices[0]
        
        # Time the base run
        tb0 = time.time()
        oos_dates, oos_states, oos_probs = run_walk_forward(df_features, t_init, 63, perturb_shift=0)
        tb1 = time.time()
        
        # Time the perturbed run
        tp0 = time.time()
        pert_dates, pert_states, _ = run_walk_forward(df_features, t_init, 63, perturb_shift=5)
        tp1 = time.time()
        
        print(f"k={k}: Base run took {tb1-tb0:.3f}s, Perturbed run took {tp1-tp0:.3f}s, Total k took {time.time()-t0:.3f}s", flush=True)

if __name__ == '__main__':
    debug_speed()
