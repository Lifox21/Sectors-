import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("c:/Users/Ved Bajaj/Desktop/Lifox/QF Club/HHM/regime_model_comparison.csv")

# Filter out failed runs (if any)
df = df[df['OOS_LogLik'] > -99999.0]

print("--- AGGREGATE MODEL COMPARISON (ALL SECTORS & FEATURE SETS) ---")
agg = df.groupby(['Feature_Set', 'Model']).agg({
    'OOS_LogLik': 'mean',
    'AIC': 'mean',
    'BIC': 'mean',
    'Whipsaws': 'mean',
    'Avg_Duration_State0': 'mean',
    'Expected_Duration_State0': 'mean',
    'Avg_Duration_State1': 'mean',
    'Expected_Duration_State1': 'mean',
    'Strat_Sharpe': 'mean',
    'BH_Sharpe': 'mean',
    'Strat_Cum_Return': 'mean',
    'BH_Cum_Return': 'mean'
}).reset_index()

print(agg.to_string(index=False))

# Count wins sector-by-sector
print("\n--- SECTOR-BY-SECTOR HEAD-TO-HEAD WINS (HSMM VS HMM) ---")
whipsaw_wins = 0
sharpe_wins = 0
total_comparisons = 0

for (sector, feat), group in df.groupby(['Sector', 'Feature_Set']):
    if len(group) == 2:
        total_comparisons += 1
        hmm_row = group[group['Model'] == 'HMM'].iloc[0]
        hsmm_row = group[group['Model'] == 'HSMM'].iloc[0]
        
        # Whipsaw win: HSMM has fewer or equal transitions (fewer is better)
        if hsmm_row['Whipsaws'] < hmm_row['Whipsaws']:
            whipsaw_wins += 1
            
        # Sharpe win: HSMM has higher Sharpe ratio
        if hsmm_row['Strat_Sharpe'] > hmm_row['Strat_Sharpe']:
            sharpe_wins += 1

print(f"Total Sector-Feature Combinations compared: {total_comparisons}")
print(f"HSMM wins on Whipsaws (fewer transitions): {whipsaw_wins} / {total_comparisons} ({whipsaw_wins/total_comparisons:.1%})")
print(f"HSMM wins on Sharpe Ratio (higher return/risk): {sharpe_wins} / {total_comparisons} ({sharpe_wins/total_comparisons:.1%})")

# Let's count how many times HSMM had fewer or equal whipsaws
whipsaw_less_equal = 0
for (sector, feat), group in df.groupby(['Sector', 'Feature_Set']):
    if len(group) == 2:
        hmm_row = group[group['Model'] == 'HMM'].iloc[0]
        hsmm_row = group[group['Model'] == 'HSMM'].iloc[0]
        if hsmm_row['Whipsaws'] <= hmm_row['Whipsaws']:
            whipsaw_less_equal += 1
print(f"HSMM had fewer or equal Whipsaws: {whipsaw_less_equal} / {total_comparisons} ({whipsaw_less_equal/total_comparisons:.1%})")

# Print average calibration error: |Avg_Duration - Expected_Duration|
df['Dur_Error_State0'] = np.abs(df['Avg_Duration_State0'] - df['Expected_Duration_State0'])
df['Dur_Error_State1'] = np.abs(df['Avg_Duration_State1'] - df['Expected_Duration_State1'])

print("\n--- EXPECTED VS ACTUAL DURATION CALIBRATION ERROR ---")
calibration = df.groupby(['Feature_Set', 'Model']).agg({
    'Dur_Error_State0': 'mean',
    'Dur_Error_State1': 'mean'
}).reset_index()
print(calibration.to_string(index=False))
