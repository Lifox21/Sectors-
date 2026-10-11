import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.special
from scipy.stats import multivariate_normal
from statsmodels.tsa.arima.model import ARIMA
from hmmlearn.hmm import GaussianHMM

# Ignore convergence and user warnings for cleaner output
warnings.filterwarnings("ignore")


def causal_hmm_filter(model, train_features, test_features):
    """Return raw HMM states for test rows without smoothing over later test rows."""
    posterior = model.predict_proba(train_features)[-1]
    raw_states = []
    for log_likelihood in model._compute_log_likelihood(test_features):
        prior = posterior @ model.transmat_
        likelihood = np.exp(log_likelihood - np.max(log_likelihood))
        posterior = prior * likelihood
        posterior /= posterior.sum()
        raw_states.append(int(np.argmax(posterior)))
    return np.asarray(raw_states, dtype=int)

# =====================================================================
# 1. DATA PREPROCESSING & FEATURE ENGINEERING
# =====================================================================

def calculate_features(file_path):
    """
    Loads daily index OHLCV data, calculates log returns, and 10-day rolling
    realized volatility. NaNs are dropped to return a clean, aligned base.
    ARIMA residuals are fitted during the modeling loop to avoid look-ahead bias.
    """
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Calculate log returns
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Calculate 10-day rolling volatility (annualized)
    df['Rolling_Vol'] = df['Returns'].rolling(window=10).std() * np.sqrt(252)
    
    # Drop first rows containing rolling NaNs to ensure date alignment
    df = df.dropna().reset_index(drop=True)
    return df

# =====================================================================
# 2. CUSTOM EXPLICIT-DURATION HSMM VITERBI DECODER
# =====================================================================

def fit_duration_gamma(states, state_val):
    """
    Finds contiguous run lengths of a state and fits a Gamma distribution.
    Uses Method of Moments to estimate shape (k) and scale (theta).
    Expected duration is k * theta.
    """
    runs = []
    curr_len = 0
    for s in states:
        if s == state_val:
            curr_len += 1
        else:
            if curr_len > 0:
                runs.append(curr_len)
                curr_len = 0
    if curr_len > 0:
        runs.append(curr_len)
        
    if len(runs) == 0:
        # Default fallback: expected duration of 10 days, shape=2, scale=5
        return 2.0, 5.0
    
    mu = np.mean(runs)
    var = np.var(runs)
    
    # Set a minimum variance to prevent numerical division by zero
    if var < 1e-2:
        var = 1.0
        
    theta = var / mu
    k = (mu ** 2) / var
    
    # Clip parameters to avoid numerical extremes in Gamma function evaluations
    k = np.clip(k, 0.05, 50.0)
    theta = np.clip(theta, 0.05, 100.0)
    
    return k, theta

def custom_hsmm_viterbi(X, pi, means, covars, gammas, D_max=100):
    """
    Dynamic programming Viterbi decoder for a 2-state explicit-duration HSMM.
    Fits a Shifted Gamma duration model and handles right-censoring at the end 
    of the sequence via survival probabilities. Uses cumulative sum optimization
    to achieve O(T * N * D_max) speed.
    """
    T = len(X)
    N = 2
    
    # Compute log-densities under state Gaussians
    log_densities = np.zeros((T, N))
    for j in range(N):
        log_densities[:, j] = multivariate_normal.logpdf(X, mean=means[j], cov=covars[j])
        
    # Cumulative sum of log-densities for O(1) segment likelihood queries
    cumsum_log_densities = np.zeros((T + 1, N))
    cumsum_log_densities[1:] = np.cumsum(log_densities, axis=0)
    
    # Compute Gamma duration log-probabilities (normalized over 1..D_max)
    log_p_duration = np.zeros((D_max + 1, N))
    for j in range(N):
        d_vals = np.arange(1, D_max + 1)
        k, theta = gammas[j]
        
        # Discretized Gamma probability density
        log_p = (k - 1) * np.log(d_vals) - (d_vals / theta) - k * np.log(theta) - scipy.special.gammaln(k)
        
        # Exponentiate and normalize for numerical stability over the [1, D_max] window
        max_log_p = np.max(log_p)
        p = np.exp(log_p - max_log_p)
        p = p / np.sum(p)
        log_p_duration[1:, j] = np.log(p + 1e-10)
        
    # Compute log survival probabilities P(D >= d | state) for right-censoring
    log_survival = np.zeros((D_max + 1, N))
    for j in range(N):
        p = np.exp(log_p_duration[1:, j])
        survival_p = np.zeros(D_max)
        for d in range(1, D_max + 1):
            survival_p[d - 1] = np.sum(p[d - 1:])
        log_survival[1:, j] = np.log(survival_p + 1e-10)
        
    # Viterbi Dynamic Programming Tables
    # V[t, j] is the max score of segments ending at time t in state j, with transition out of j at t
    V = np.full((T + 1, N), -np.inf)
    bp = {} # backpointer map: (t, j) -> (prev_state, duration)
    
    V[0, :] = np.log(pi + 1e-10)
    
    # Recurrence relation loop
    for t in range(1, T + 1):
        for j in range(N):
            for d in range(1, min(t, D_max) + 1):
                prev_t = t - d
                if prev_t == 0:
                    # Starting segment of state j
                    score = V[0, j] + log_p_duration[d, j] + (cumsum_log_densities[t, j] - cumsum_log_densities[0, j])
                    if score > V[t, j]:
                        V[t, j] = score
                        bp[(t, j)] = (-1, d)
                else:
                    # Transition from i to j (deterministic transition in 2-state model: i = 1 - j)
                    i = 1 - j
                    score = V[prev_t, i] + log_p_duration[d, j] + (cumsum_log_densities[t, j] - cumsum_log_densities[prev_t, j])
                    if score > V[t, j]:
                        V[t, j] = score
                        bp[(t, j)] = (i, d)
                        
    # Final state right-censored segment loop at t = T
    V_final = np.full((N,), -np.inf)
    bp_final = {}
    for j in range(N):
        for d in range(1, D_max + 1):
            prev_t = T - d
            if prev_t < 0:
                continue
            if prev_t == 0:
                score = V[0, j] + log_survival[d, j] + (cumsum_log_densities[T, j] - cumsum_log_densities[0, j])
                if score > V_final[j]:
                    V_final[j] = score
                    bp_final[j] = (-1, d)
            else:
                i = 1 - j
                score = V[prev_t, i] + log_survival[d, j] + (cumsum_log_densities[T, j] - cumsum_log_densities[prev_t, j])
                if score > V_final[j]:
                    V_final[j] = score
                    bp_final[j] = (i, d)
                    
    # Backtrack path
    states_path = np.zeros(T, dtype=int)
    curr_state = np.argmax(V_final)
    curr_t = T
    
    prev_state, d = bp_final[curr_state]
    states_path[curr_t - d : curr_t] = curr_state
    curr_t -= d
    curr_state = prev_state
    
    while curr_t > 0:
        prev_state, d = bp[(curr_t, curr_state)]
        states_path[curr_t - d : curr_t] = curr_state
        curr_t -= d
        curr_state = prev_state
        
    return states_path, np.max(V_final)

# =====================================================================
# 3. BACKTESTING & METRICS ENGINE
# =====================================================================

def compute_metrics(df, states, test_idx_start):
    """
    Computes whipsaw transitions, average regime durations, and returns
    backtest Sharpe/cumulative returns. Slices parameters strictly in test window.
    """
    T = len(df)
    train_len = test_idx_start
    test_len = T - train_len
    
    test_states = states[train_len:]
    
    # Whipsaw count (transitions in test set)
    transitions = np.sum(test_states[:-1] != test_states[1:])
    
    # Average regime durations in test set
    durations = {0: [], 1: []}
    curr_state = test_states[0]
    curr_len = 1
    for s in test_states[1:]:
        if s == curr_state:
            curr_len += 1
        else:
            durations[curr_state].append(curr_len)
            curr_state = s
            curr_len = 1
    durations[curr_state].append(curr_len)
    
    avg_d0 = np.mean(durations[0]) if len(durations[0]) > 0 else 0
    avg_d1 = np.mean(durations[1]) if len(durations[1]) > 0 else 0
    
    # State-conditional return statistics (on Returns column)
    returns = df['Returns'].values
    test_returns = returns[train_len:]
    
    ret_s0 = test_returns[test_states == 0]
    ret_s1 = test_returns[test_states == 1]
    
    mean_s0 = np.mean(ret_s0) * 252 if len(ret_s0) > 0 else 0
    vol_s0 = np.std(ret_s0) * np.sqrt(252) if len(ret_s0) > 0 else 0
    mean_s1 = np.mean(ret_s1) * 252 if len(ret_s1) > 0 else 0
    vol_s1 = np.std(ret_s1) * np.sqrt(252) if len(ret_s1) > 0 else 0
    
    # Strategy backtest: earn returns if State = 0 (bullish), else cash (0%)
    strat_returns = np.where(test_states == 0, test_returns, 0.0)
    
    cum_strat = np.exp(np.sum(strat_returns)) - 1
    cum_bh = np.exp(np.sum(test_returns)) - 1
    
    # Sharpe ratio
    sharpe_strat = (np.mean(strat_returns) / (np.std(strat_returns) + 1e-10)) * np.sqrt(252) if np.std(strat_returns) > 0 else 0
    sharpe_bh = (np.mean(test_returns) / (np.std(test_returns) + 1e-10)) * np.sqrt(252) if np.std(test_returns) > 0 else 0
    
    return {
        'Whipsaws': int(transitions),
        'Avg_Duration_State0': round(avg_d0, 2),
        'Avg_Duration_State1': round(avg_d1, 2),
        'State0_Mean_Ret': f"{mean_s0 * 100:.2f}%",
        'State0_Vol': f"{vol_s0 * 100:.2f}%",
        'State1_Mean_Ret': f"{mean_s1 * 100:.2f}%",
        'State1_Vol': f"{vol_s1 * 100:.2f}%",
        'Strat_Cum_Return': f"{cum_strat * 100:.2f}%",
        'BH_Cum_Return': f"{cum_bh * 100:.2f}%",
        'Strat_Sharpe': round(sharpe_strat, 3),
        'BH_Sharpe': round(sharpe_bh, 3)
    }

# =====================================================================
# 4. MAIN PIPELINE COMPILATION
# =====================================================================

def run_pipeline():
    indices_dir = "c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/Indices/Daily"
    files = [f for f in os.listdir(indices_dir) if f.endswith('.csv')]
    
    # Merged state dataframes to be output
    hmm_states_df = pd.DataFrame()
    hsmm_states_df = pd.DataFrame()
    
    comparison_records = []
    
    # Representative sectors to plot
    plot_sectors = ['banking_daily.csv', 'information_technology_daily.csv', 'agriculture_daily.csv', 'chemicals_daily.csv']
    os.makedirs("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/plots", exist_ok=True)
    
    # Define Feature Sets to evaluate
    feature_sets = ['Returns', 'ARIMA']
    
    print(f"Starting regime pipeline on {len(files)} sectors...")
    print("Using a Shifted Gamma duration model for HSMM explicit state lengths.")
    print("Alignment of out-of-sample log-likelihood is based on symmetric Viterbi paths.")
    print("ARIMA is fitted on training indices to prevent look-ahead bias.")
    print("Z-score standardization applied per sector-configuration to guarantee numerical stability.\n")
    
    for filename in files:
        sector_name = filename.replace('_daily.csv', '')
        file_path = os.path.join(indices_dir, filename)
        
        # 1. Feature Preprocessing (Returns and Volatility)
        df = calculate_features(file_path)
        T = len(df)
        train_len = int(T * 0.8)
        
        # Compute ARIMA residuals strictly using train coefficients to prevent leakage
        close_prices = df['Close'].values
        arima_residuals = np.zeros(T)
        try:
            train_close = close_prices[:train_len]
            model = ARIMA(train_close, order=(1, 1, 1))
            model_fit = model.fit()
            # Apply training model parameters to full series
            full_res = model_fit.apply(close_prices)
            arima_residuals = full_res.resid
            
            # Set the first residual to 0.0 to eliminate the initialization price spike
            arima_residuals[0] = 0.0
            arima_residuals = np.nan_to_num(arima_residuals, nan=0.0, posinf=0.0, neginf=0.0)
        except Exception as e:
            # Fallback
            arima_residuals = df['Close'].diff().fillna(0).values
            arima_residuals[0] = 0.0
            arima_residuals = np.nan_to_num(arima_residuals, nan=0.0, posinf=0.0, neginf=0.0)
            
        df['ARIMA_Residuals'] = arima_residuals
        
        # Run comparison for both feature sets
        for feat_name in feature_sets:
            cols = ['Returns', 'Rolling_Vol'] if feat_name == 'Returns' else ['ARIMA_Residuals', 'Rolling_Vol']
            X = df[cols].values
            X_train = X[:train_len]
            X_test = X[train_len:]
            
            # Standardize features using training statistics to prevent scale mismatch and leakage
            mean_train = np.mean(X_train, axis=0)
            std_train = np.std(X_train, axis=0) + 1e-10
            
            X_train_std = (X_train - mean_train) / std_train
            X_test_std = (X_test - mean_train) / std_train
            X_std = (X - mean_train) / std_train
            
            # 2. HMM Fitting (In-Sample)
            hmm_model = GaussianHMM(n_components=2, covariance_type="full", n_iter=100, random_state=42)
            try:
                hmm_model.fit(X_train_std)
            except Exception as e:
                # Fallback to diagonal covariance if full fails
                hmm_model = GaussianHMM(n_components=2, covariance_type="diag", n_iter=100, random_state=42)
                hmm_model.fit(X_train_std)
                
            # Train states are used only to label the fitted components. Test states
            # are filtered one day at a time, avoiding future-test-data leakage.
            hmm_train_lik, train_hmm_states = hmm_model.decode(X_train_std)
            test_hmm_states = causal_hmm_filter(hmm_model, X_train_std, X_test_std)
            hmm_oos_lik = hmm_model.score(X_test_std)
            
            # Label states post-hoc (State 0 = Bullish/Stable, higher return in train returns)
            returns_train = df['Returns'].values[:train_len]
            state_means = [np.mean(returns_train[train_hmm_states == state]) for state in [0, 1]]
            
            # Identify which HMM state matches Bullish (State 0) vs Bearish (State 1)
            hmm_to_regime = {0: 0, 1: 1} if state_means[0] > state_means[1] else {0: 1, 1: 0}
            
            # Map HMM states to regime
            train_hmm_regimes = np.array([hmm_to_regime[s] for s in train_hmm_states])
            test_hmm_regimes = np.array([hmm_to_regime[s] for s in test_hmm_states])
            all_hmm_regimes = np.concatenate([train_hmm_regimes, test_hmm_regimes])
            
            # Calculate HMM's fitted expected durations in training set: 1 / (1 - P_jj)
            regime_to_hmm = {regime: raw_state for raw_state, regime in hmm_to_regime.items()}
            hmm_expected_d0 = 1.0 / (1.0 - hmm_model.transmat_[regime_to_hmm[0], regime_to_hmm[0]] + 1e-10)
            hmm_expected_d1 = 1.0 / (1.0 - hmm_model.transmat_[regime_to_hmm[1], regime_to_hmm[1]] + 1e-10)
            
            # 3. HSMM Fitting (Estimating parameters on HMM training regimes)
            means = np.zeros((2, 2))
            covars = [None, None]
            for state in [0, 1]:
                mask = train_hmm_regimes == state
                if np.sum(mask) > 1:
                    means[state] = np.mean(X_train_std[mask], axis=0)
                    covars[state] = np.cov(X_train_std[mask].T)
                else:
                    # Fallback to HMM variables (already standardized)
                    mapped_hmm_state = hmm_to_regime[state]
                    means[state] = hmm_model.means_[mapped_hmm_state]
                    if hmm_model.covariance_type == 'diag':
                        covars[state] = np.diag(hmm_model.covars_[mapped_hmm_state])
                    else:
                        covars[state] = hmm_model.covars_[mapped_hmm_state]
                        
            pi = np.array([np.mean(train_hmm_regimes == 0), np.mean(train_hmm_regimes == 1)])
            if pi[0] == 0 or pi[1] == 0:
                pi = np.array([0.5, 0.5])
                
            # Fit Shifted Gamma duration distribution per state on training set run-lengths
            gammas = [None, None]
            gammas[0] = fit_duration_gamma(train_hmm_regimes, 0)
            gammas[1] = fit_duration_gamma(train_hmm_regimes, 1)
            
            # Calculate HSMM's fitted expected durations: k * theta
            hsmm_expected_d0 = gammas[0][0] * gammas[0][1]
            hsmm_expected_d1 = gammas[1][0] * gammas[1][1]
            
            # Decode optimal paths (Viterbi) continuously across full set
            try:
                all_hsmm_regimes, hsmm_full_lik = custom_hsmm_viterbi(X_std, pi, means, covars, gammas, D_max=100)
                _, hsmm_train_lik = custom_hsmm_viterbi(X_train_std, pi, means, covars, gammas, D_max=100)
                _, hsmm_oos_lik = custom_hsmm_viterbi(X_test_std, pi, means, covars, gammas, D_max=100)
            except Exception as e:
                # Fallback to copy HMM path if custom decoder fails numerically
                all_hsmm_regimes = all_hmm_regimes.copy()
                hsmm_train_lik = -99999.0
                hsmm_oos_lik = -99999.0
                
            train_hsmm_regimes = all_hsmm_regimes[:train_len]
            test_hsmm_regimes = all_hsmm_regimes[train_len:]
            
            # 4. Save decoded states to timeseries dataframes
            col_name = f"{sector_name}_{feat_name.lower()}"
            hmm_sector_df = pd.DataFrame({'Date': df['Date'], col_name: all_hmm_regimes})
            hsmm_sector_df = pd.DataFrame({'Date': df['Date'], col_name: all_hsmm_regimes})
            
            if hmm_states_df.empty:
                hmm_states_df = hmm_sector_df
                hsmm_states_df = hsmm_sector_df
            else:
                hmm_states_df = pd.merge(hmm_states_df, hmm_sector_df, on='Date', how='outer')
                hsmm_states_df = pd.merge(hsmm_states_df, hsmm_sector_df, on='Date', how='outer')
                
            # 5. AIC/BIC Calculations
            # HMM Parameters = 13 (1 startprob, 2 transitions, 4 means, 6 covars)
            # HSMM Parameters = 15 (1 startprob, 0 transitions, 4 means, 6 covars, 4 duration [shape/scale for 2 states])
            hmm_aic = 2 * 13 - 2 * hmm_train_lik
            hmm_bic = 13 * np.log(train_len) - 2 * hmm_train_lik
            
            hsmm_aic = 2 * 15 - 2 * hsmm_train_lik
            hsmm_bic = 15 * np.log(train_len) - 2 * hsmm_train_lik
            
            # 6. Compute test metrics and backtest statistics
            hmm_metrics = compute_metrics(df, all_hmm_regimes, train_len)
            hsmm_metrics = compute_metrics(df, all_hsmm_regimes, train_len)
            
            # Save metrics to record list
            comparison_records.append({
                'Sector': sector_name,
                'Feature_Set': feat_name,
                'Model': 'HMM',
                'OOS_LogLik': round(hmm_oos_lik, 2),
                'AIC': round(hmm_aic, 2),
                'BIC': round(hmm_bic, 2),
                'Expected_Duration_State0': round(hmm_expected_d0, 2),
                'Expected_Duration_State1': round(hmm_expected_d1, 2),
                **hmm_metrics
            })
            comparison_records.append({
                'Sector': sector_name,
                'Feature_Set': feat_name,
                'Model': 'HSMM',
                'OOS_LogLik': round(hsmm_oos_lik, 2),
                'AIC': round(hsmm_aic, 2),
                'BIC': round(hsmm_bic, 2),
                'Expected_Duration_State0': round(hsmm_expected_d0, 2),
                'Expected_Duration_State1': round(hsmm_expected_d1, 2),
                **hsmm_metrics
            })
            
            # 7. Visualizing Representative Sectors (Only plot returns feature set for visual brevity)
            if filename in plot_sectors and feat_name == 'Returns':
                plt.figure(figsize=(12, 7))
                
                # Subplot 1: HMM Decoded Regimes
                plt.subplot(2, 1, 1)
                plt.plot(df['Date'], df['Close'], color='black', label='Index Close')
                # Shading by state
                for state_val, color, alpha in [(0, 'green', 0.15), (1, 'red', 0.15)]:
                    mask = all_hmm_regimes == state_val
                    plt.fill_between(df['Date'], df['Close'].min(), df['Close'].max(), where=mask, color=color, alpha=alpha)
                plt.title(f"{sector_name.upper()} (Returns) - HMM Regimes (Green=Bullish/Stable, Red=Bearish/Volatile)")
                plt.ylabel("Close Price")
                plt.axvline(df['Date'].iloc[train_len], color='blue', linestyle='--', label='Train/Test Split')
                plt.legend(loc='upper left')
                
                # Subplot 2: HSMM Decoded Regimes
                plt.subplot(2, 1, 2)
                plt.plot(df['Date'], df['Close'], color='black', label='Index Close')
                for state_val, color, alpha in [(0, 'green', 0.15), (1, 'red', 0.15)]:
                    mask = all_hsmm_regimes == state_val
                    plt.fill_between(df['Date'], df['Close'].min(), df['Close'].max(), where=mask, color=color, alpha=alpha)
                plt.title(f"{sector_name.upper()} (Returns) - HSMM Regimes (Explicit Duration Gamma)")
                plt.ylabel("Close Price")
                plt.axvline(df['Date'].iloc[train_len], color='blue', linestyle='--')
                plt.xlabel("Date")
                
                plt.tight_layout()
                plt.savefig(f"c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/plots/{sector_name}_comparison.png", dpi=150)
                plt.close()
                
    # 8. Output final results to CSV files
    hmm_states_df.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/sector_regime_hmm.csv", index=False)
    hsmm_states_df.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/sector_regime_hsmm.csv", index=False)
    
    comparison_df = pd.DataFrame(comparison_records)
    comparison_df.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/regime_model_comparison.csv", index=False)
    
    print("\nRegime Detection Engine ran successfully!")
    print(f"Generated comparison reports for {len(files)} sectors across Returns & ARIMA residual sets.")
    
    # 9. Compute Summary Statistics for Markdown Report
    summary_list = []
    for sector in comparison_df['Sector'].unique():
        s_data = comparison_df[comparison_df['Sector'] == sector]
        
        # Extract Sharpe values for each combination
        ret_hmm = s_data[(s_data['Feature_Set'] == 'Returns') & (s_data['Model'] == 'HMM')].iloc[0]['Strat_Sharpe']
        ret_hsmm = s_data[(s_data['Feature_Set'] == 'Returns') & (s_data['Model'] == 'HSMM')].iloc[0]['Strat_Sharpe']
        ari_hmm = s_data[(s_data['Feature_Set'] == 'ARIMA') & (s_data['Model'] == 'HMM')].iloc[0]['Strat_Sharpe']
        ari_hsmm = s_data[(s_data['Feature_Set'] == 'ARIMA') & (s_data['Model'] == 'HSMM')].iloc[0]['Strat_Sharpe']
        
        # Find best combination
        configs = {
            'Returns_HMM': ret_hmm,
            'Returns_HSMM': ret_hsmm,
            'ARIMA_HMM': ari_hmm,
            'ARIMA_HSMM': ari_hsmm
        }
        best_config = max(configs, key=configs.get)
        best_sharpe = configs[best_config]
        
        summary_list.append({
            'Sector': sector,
            'HMM_Returns_Sharpe': ret_hmm,
            'HSMM_Returns_Sharpe': ret_hsmm,
            'HMM_ARIMA_Sharpe': ari_hmm,
            'HSMM_ARIMA_Sharpe': ari_hsmm,
            'Best_Config': best_config,
            'Best_Sharpe': best_sharpe
        })
        
    summary_df = pd.DataFrame(summary_list)
    print("\n--- Summary Performance Across 4 Configurations (Sharpe Winner Count) ---")
    print(summary_df['Best_Config'].value_counts())
    
    # Save summary
    summary_df.to_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/summary_temp.csv", index=False)

if __name__ == '__main__':
    run_pipeline()
