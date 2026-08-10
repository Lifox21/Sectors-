import os
import sys
import time
import warnings
import numpy as np
import pandas as pd

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from replicate_pipeline import process_sector_all_k

warnings.filterwarnings("ignore")

def analyze_subset():
    indices_dir = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily"
    # Select the first 8 sectors
    completed_sectors = [
        'airlines_daily.csv', 'banking_daily.csv', 'automobiles_daily.csv',
        'agriculture_daily.csv', 'building_materials_daily.csv',
        'capital_goods_daily.csv', 'chemicals_daily.csv', 'consumer_durables_daily.csv'
    ]
    
    k_values = [1, 2, 3, 5, 6, 7, 8, 9, 10, 15, 20, 21]
    block_size = 63
    
    print(f"Analyzing {len(completed_sectors)} completed sectors across {len(k_values)} k values...", flush=True)
    
    sector_results = []
    
    for filename in completed_sectors:
        file_path = os.path.join(indices_dir, filename)
        sector_name = filename.replace('_daily.csv', '')
        t0 = time.time()
        try:
            _, results = process_sector_all_k(file_path, k_values, block_size)
            for k in k_values:
                if k in results:
                    sector_results.append({
                        'sector': sector_name,
                        'k': k,
                        'whipsaw_ratio': results[k]['whipsaw_ratio'],
                        'signal_lag': results[k]['signal_lag'],
                        'transition_stability': results[k]['transition_stability']
                    })
            print(f"Processed {sector_name} in {time.time()-t0:.2f}s", flush=True)
        except Exception as e:
            print(f"Error for {sector_name}: {e}", flush=True)
            
    df = pd.DataFrame(sector_results)
    
    # Calculate aggregate metrics across these 8 sectors
    agg = df.groupby('k').agg({
        'whipsaw_ratio': 'mean',
        'signal_lag': 'mean',
        'transition_stability': 'mean'
    }).reset_index()
    
    # Scale to get composite cost
    def min_max_scale(series):
        s_min, s_max = series.min(), series.max()
        if s_max == s_min:
            return pd.Series(0.0, index=series.index)
        return (series - s_min) / (s_max - s_min)
        
    agg['whipsaw_norm'] = min_max_scale(agg['whipsaw_ratio'])
    agg['lag_norm'] = min_max_scale(agg['signal_lag'])
    agg['stability_norm'] = min_max_scale(agg['transition_stability'])
    agg['composite_cost'] = agg['whipsaw_norm'] + agg['lag_norm'] + (1.0 - agg['stability_norm'])
    
    print("\n========================================================")
    print("AGGREGATE SENSITIVITY METRICS (8 SECTORS SUBSET)")
    print("========================================================")
    print(agg.to_string(index=False))
    print("========================================================\n")
    
    optimal_idx = agg['composite_cost'].idxmin()
    optimal_k = int(agg.loc[optimal_idx, 'k'])
    print(f"Subset Optimal k Selected: {optimal_k}")

if __name__ == '__main__':
    analyze_subset()
