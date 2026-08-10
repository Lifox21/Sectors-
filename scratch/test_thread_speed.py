import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from replicate_pipeline import process_sector_all_k

warnings.filterwarnings("ignore")

def test_threads():
    indices_dir = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily"
    files = [os.path.join(indices_dir, f) for f in os.listdir(indices_dir) if f.endswith('.csv')][:4]
    
    k_values = [1, 2, 3, 5, 6, 7, 8, 9, 10, 15, 20, 21]
    block_size = 63
    
    start_time = time.time()
    print("Starting ThreadPoolExecutor test on 4 sectors...", flush=True)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_sector_all_k, f, k_values, block_size): f for f in files}
        for future in futures:
            try:
                sector_name, results = future.result()
                print(f"Processed sector: {sector_name} in {time.time() - start_time:.2f}s", flush=True)
            except Exception as e:
                print(f"Error for {futures[future]}: {e}", flush=True)
                
    print(f"Completed 4 sectors in {time.time() - start_time:.2f} seconds.")

if __name__ == '__main__':
    test_threads()
