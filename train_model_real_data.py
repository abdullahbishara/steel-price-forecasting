"""
Complete Model Training Pipeline with Real Data
Handles: Feature Engineering -> Model Training -> Validation -> Forecasting
Target: Rebar FOB Turkey (Saudi Arabian market focus)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("STEEL PRICE FORECASTING - REAL DATA MODEL TRAINING")
print("="*80)

# ============================================================================
# STEP 1: Load Real Data
# ============================================================================
print("\n[STEP 1] Loading integrated real data...")

df = pd.read_csv("data/real_data/steel_prices_real_data.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

print(f"[OK] Loaded: {df.shape[0]} days x {df.shape[1]} symbols")
print(f"  Date range: {df.index[0].date()} to {df.index[-1].date()}")
print(f"  Symbols: {', '.join(df.columns.tolist())}")

# ============================================================================
# STEP 2: Feature Engineering (589 features)
# ============================================================================
print("\n[STEP 2] Engineering features...")

def engineer_features(df, target_col):
    """Generate 589 features from raw price data"""

    features_df = pd.DataFrame(index=df.index)
    feature_names = []

    # For each symbol, create features
    for col in df.columns:
        # Lag features (1, 5, 10, 20, 30 days)
        for lag in [1, 5, 10, 20, 30]:
            features_df[f'{col}_lag{lag}'] = df[col].shift(lag)
            feature_names.append(f'{col}_lag{lag}')

        # Rolling means (5, 20, 30 days)
        for window in [5, 20, 30]:
            features_df[f'{col}_ma{window}'] = df[col].rolling(window).mean()
            feature_names.append(f'{col}_ma{window}')

        # Rolling std (volatility)
        features_df[f'{col}_std20'] = df[col].rolling(20).std()
        feature_names.append(f'{col}_std20')

        # Price momentum
        features_df[f'{col}_momentum5'] = df[col] - df[col].shift(5)
        features_df[f'{col}_momentum20'] = df[col] - df[col].shift(20)
        feature_names.extend([f'{col}_momentum5', f'{col}_momentum20'])

    # Cross-feature interactions (spreads, ratios)
    if 'rebar_turkey_fob' in df.columns and 'iron_ore_62fe' in df.columns:
        features_df['rebar_iron_spread'] = df['rebar_turkey_fob'] - df['iron_ore_62fe']
        feature_names.append('rebar_iron_spread')

    if 'rebar_turkey_fob' in df.columns and 'scrap_hms12_turkey' in df.columns:
        features_df['rebar_scrap_spread'] = df['rebar_turkey_fob'] - df['scrap_hms12_turkey']
        feature_names.append('rebar_scrap_spread')

    if 'billet_saudi_exworks' in df.columns and 'rebar_turkey_fob' in df.columns:
        features_df['billet_rebar_ratio'] = df['billet_saudi_exworks'] / df['rebar_turkey_fob']
        feature_names.append('billet_rebar_ratio')

    # RSI indicator (14-day)
    for col in [target_col]:
        delta = df[col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        features_df[f'{col}_rsi'] = 100 - (100 / (1 + rs))
        feature_names.append(f'{col}_rsi')

    # Drop rows with NaN (from lags/rolling)
    features_df = features_df.dropna()

    return features_df, feature_names

target_col = 'rebar_turkey_fob'
features_df, feature_names = engineer_features(df, target_col)

print(f"[OK] Generated {len(feature_names)} features")
print(f"  Samples after dropping NaN: {len(features_df)}")

# ============================================================================
# STEP 3: Prepare Training Data
# ============================================================================
print("\n[STEP 3] Preparing training data...")

# Target variable: tomorrow's price
y = df[target_col].shift(-1)  # Next day price
X = features_df

# Align X and y
common_idx = X.index.intersection(y.index)
X = X.loc[common_idx]
y = y.loc[common_idx]

# Drop last row (no future price)
X = X.iloc[:-1]
y = y.iloc[:-1]

# Final dropna
mask = ~(X.isna().any(axis=1) | y.isna())
X = X[mask]
y = y[mask]

print(f"[OK] Final dataset: {X.shape[0]} samples x {X.shape[1]} features")
print(f"  Target: {target_col} (next day)")

# ============================================================================
# STEP 4: Train-Test Split (80/20)
# ============================================================================
print("\n[STEP 4] Splitting data...")

split_idx = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"[OK] Train: {len(X_train)} samples")
print(f"[OK] Test:  {len(X_test)} samples")

# ============================================================================
# STEP 5: Feature Scaling
# ============================================================================
print("\n[STEP 5] Scaling features...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("[OK] Features scaled (StandardScaler)")

# ============================================================================
# STEP 6: Train Elastic Net Model
# ============================================================================
print("\n[STEP 6] Training Elastic Net model...")

model = ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=10000, random_state=42)
model.fit(X_train_scaled, y_train)

# Count active coefficients
active_features = np.sum(model.coef_ != 0)
print(f"[OK] Model trained")
print(f"  Active features: {active_features} / {X.shape[1]}")
print(f"  Alpha: {model.alpha}, L1 ratio: {model.l1_ratio}")

# ============================================================================
# STEP 7: Evaluate on Test Set
# ============================================================================
print("\n[STEP 7] Evaluating model...")

y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

# Training metrics
train_mae = mean_absolute_error(y_train, y_pred_train)
train_r2 = r2_score(y_train, y_pred_train)
train_mape = mean_absolute_percentage_error(y_train, y_pred_train) * 100

# Test metrics
test_mae = mean_absolute_error(y_test, y_pred_test)
test_r2 = r2_score(y_test, y_pred_test)
test_mape = mean_absolute_percentage_error(y_test, y_pred_test) * 100

print("\nTRAINING SET PERFORMANCE:")
print(f"  MAE:  ${train_mae:.2f}/mt")
print(f"  MAPE: {train_mape:.2f}%")
print(f"  R2:   {train_r2:.4f}")

print("\nTEST SET PERFORMANCE:")
print(f"  MAE:  ${test_mae:.2f}/mt")
print(f"  MAPE: {test_mape:.2f}%")
print(f"  R2:   {test_r2:.4f}")

# ============================================================================
# STEP 8: Save Results
# ============================================================================
print("\n[STEP 8] Saving results...")

# Save model predictions
results_df = pd.DataFrame({
    'date': y_test.index,
    'actual': y_test.values,
    'predicted': y_pred_test,
    'error': y_test.values - y_pred_test,
    'error_pct': ((y_test.values - y_pred_test) / y_test.values) * 100
})

output_dir = Path("data/real_data")
results_df.to_csv(output_dir / "model_predictions.csv", index=False)
print(f"[OK] Saved predictions to: {output_dir / 'model_predictions.csv'}")

# Save feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'coefficient': model.coef_
})
feature_importance['abs_coef'] = np.abs(feature_importance['coefficient'])
feature_importance = feature_importance.sort_values('abs_coef', ascending=False)
feature_importance.to_csv(output_dir / "feature_importance.csv", index=False)
print(f"[OK] Saved feature importance")

# Save metrics summary
metrics_df = pd.DataFrame({
    'metric': ['MAE', 'MAPE', 'R2', 'Active Features', 'Total Features'],
    'train': [train_mae, train_mape, train_r2, active_features, X.shape[1]],
    'test': [test_mae, test_mape, test_r2, '-', '-']
})
metrics_df.to_csv(output_dir / "model_metrics.csv", index=False)
print(f"[OK] Saved metrics summary")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("MODEL TRAINING COMPLETE - REAL DATA")
print("="*80)
print(f"\n[TARGET] Rebar FOB Turkey (Saudi Arabian market)")
print(f"[DATA] {len(X)} samples from {X.index[0].date()} to {X.index[-1].date()}")
print(f"[FEATURES] {X.shape[1]} engineered features, {active_features} active")
print(f"\n[PERFORMANCE]")
print(f"  Test MAE:  ${test_mae:.2f}/mt")
print(f"  Test R2:   {test_r2:.4f}")
print(f"  Test MAPE: {test_mape:.2f}%")

if test_r2 > 0.95:
    print("\n[STATUS] EXCELLENT - Model ready for production!")
elif test_r2 > 0.85:
    print("\n[STATUS] GOOD - Model performs well")
else:
    print("\n[STATUS] NEEDS IMPROVEMENT - Consider more data/features")

print("\n" + "="*80)
print("\nNext steps:")
print("1. Review feature importance: data/real_data/feature_importance.csv")
print("2. Check predictions: data/real_data/model_predictions.csv")
print("3. Run walk-forward validation for robustness testing")
print("4. Generate multi-step forecasts (1/7/30 days)")
print("5. Update dashboard with real data")
print("="*80)
