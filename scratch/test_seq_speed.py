import os
import sys
import time
import warnings
import numpy as np
import pandas as pd

# Add parent directory to sys.path to find replicate_pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from replicate_pipeline import process_sector_all_k

warnings.filterwarnings("ignore")

def test_speed():
    file_path = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily/banking_daily.csv"
    k_values = [1, 2, 3, 5, 6, 7, 8, 9, 10, 15, 20, 21]
    
    start_time = time.time()
    sector_name, results = process_sector_all_k(file_path, k_values)
    end_time = time.time()
    
    print(f"Processed 1 sector for all 12 k values in {end_time - start_time:.4f} seconds sequentially.")
    print("k values processed successfully:", list(results.keys()))

if __name__ == '__main__':
    test_speed()
