import numpy as np
import time
from hmmlearn.hmm import GaussianHMM

def run_hmm_bench():
    # Create random features
    np.random.seed(42)
    X = np.random.normal(0, 1, (1000, 3))
    
    # Base fit (from scratch)
    start = time.time()
    hmm = GaussianHMM(n_components=3, covariance_type='full', n_iter=30, random_state=42)
    hmm.fit(X)
    end = time.time()
    print(f"HMM fit from scratch (30 iter): {end - start:.4f} seconds")
    
    # Warm start fit (10 iter)
    prev_startprob = hmm.startprob_
    prev_transmat = hmm.transmat_
    prev_means = hmm.means_
    prev_covars = hmm.covars_
    
    start = time.time()
    hmm_warm = GaussianHMM(n_components=3, covariance_type='full', n_iter=10, init_params='')
    hmm_warm.startprob_ = prev_startprob.copy()
    hmm_warm.transmat_ = prev_transmat.copy()
    hmm_warm.means_ = prev_means.copy()
    hmm_warm.covars_ = prev_covars.copy()
    
    # Slightly new data
    X_new = np.random.normal(0.01, 1, (1050, 3))
    hmm_warm.fit(X_new)
    end = time.time()
    print(f"HMM warm start fit (10 iter): {end - start:.4f} seconds")
    
    # Let's compare with fitting from scratch on new data
    start = time.time()
    hmm_scratch = GaussianHMM(n_components=3, covariance_type='full', n_iter=30, random_state=42)
    hmm_scratch.fit(X_new)
    end = time.time()
    print(f"HMM fit from scratch on new data (30 iter): {end - start:.4f} seconds")
    
    # Compare log likelihoods of paths on X_new
    print("Warm start log probability:", hmm_warm.score(X_new))
    print("Scratch log probability:", hmm_scratch.score(X_new))

if __name__ == '__main__':
    run_hmm_bench()
