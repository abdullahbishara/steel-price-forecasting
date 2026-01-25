"""
Real Data Integration Script
Integrates client-provided Excel files into unified dataset for model training
Target: Rebar FOB Turkey (Saudi Arabian market focus)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("STEEL PRICE FORECASTING - REAL DATA INTEGRATION")
print("="*80)

# Create output directory
output_dir = Path("data/real_data")
output_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# STEP 1: Load all Excel files
# ============================================================================
print("\n[STEP 1] Loading Excel files...")

def load_excel_data(filename, symbol_name):
    """Load Excel file, skip headers, extract date and avg price"""
    try:
        file_path = Path("New dataset") / filename
        df = pd.read_excel(file_path, skiprows=8)

        # Get column names
        date_col = df.columns[0]
        price_col = df.columns[-1]  # Avg is last column

        # Extract date and avg price
        df = df.iloc[:, [0, -1]]  # First and last columns
        df.columns = ['date', 'price']

        # Remove first row if it's headers
        if df['date'].iloc[0] == 'Dates':
            df = df.iloc[1:]

        # Convert to proper types
        df['date'] = pd.to_datetime(df['date'], format='%d %b %Y', errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Remove NaN
        df = df.dropna()

        # Add symbol
        df['symbol'] = symbol_name

        print(f"  [OK] {symbol_name}: {len(df)} records ({df['date'].min().date()} to {df['date'].max().date()})")

        return df

    except Exception as e:
        print(f"  [ERROR] {symbol_name}: Error - {str(e)}")
        return None

# Load all data files
data_files = {
    # DAILY DATA
    'rebar_turkey_fob': 'Rebar-Turkey-FOB-price_01-Dec-2023_20-Jan-2026.xlsx',
    'iron_ore_62fe': '62FeIronOre_01-Dec-2023_31-Dec-2025.xlsx',
    'scrap_hms12_turkey': 'Scrap-price-turkey-cfr_01-Dec-2023_31-Dec-2025.xlsx',

    # WEEKLY DATA - Billet
    'billet_saudi_exworks': 'billet-saudi-arabia-ex-works-sart_06-Dec-2023_14-Jan-2026.xlsx',
    'billet_gcc_cfr': 'billet-gcc-cfr-usdt_06-Dec-2023_15-Jan-2026.xlsx',
    'billet_cis_fob': 'cis-black-sea-port-billet-usdt-fob_01-Dec-2023_16-Jan-2026.xlsx',

    # WEEKLY DATA - Coal/Coke
    'coking_coal_australia': 'hard-coking-coal_01-Dec-2023_26-Dec-2025.xlsx',
    'coke_lvliang_china': 'Lvliang-quasi-first-coke-cnyt-ex-works_01-Dec-2023_26-Dec-2025.xlsx',
    'coke_rizhao_china': 'quasi-first-grade-coke-fot-rizhao-port-cnyt_01-Dec-2023_26-Dec-2025.xlsx',

    # OPTIONAL - UAE Rebar for reference only
    'rebar_uae_exworks': 'rebar-uae-ex-works-aedt_01-Dec-2023_31-Dec-2025.xlsx',
}

# Load all files
all_data = []
for symbol, filename in data_files.items():
    df = load_excel_data(filename, symbol)
    if df is not None:
        all_data.append(df)

print(f"\n[OK] Successfully loaded {len(all_data)} data files")

# ============================================================================
# STEP 2: Currency Conversions
# ============================================================================
print("\n[STEP 2] Converting currencies to USD...")

# SAR to USD (fixed peg)
SAR_TO_USD = 1.0 / 3.75

# CNY to USD (we'll use approximate historical rates for the period)
# Dec 2023 - Jan 2026 average: ~0.14 USD per CNY
CNY_TO_USD = 0.14

for i, df in enumerate(all_data):
    symbol = df['symbol'].iloc[0]

    if 'saudi' in symbol and 'sar' in data_files[symbol].lower():
        # Convert SAR to USD
        df['price'] = df['price'] * SAR_TO_USD
        df['currency'] = 'USD (converted from SAR)'
        print(f"  [OK] {symbol}: Converted SAR -> USD (rate: {SAR_TO_USD:.4f})")

    elif 'china' in symbol or 'cny' in data_files[symbol].lower():
        # Convert CNY to USD
        df['price'] = df['price'] * CNY_TO_USD
        df['currency'] = 'USD (converted from CNY)'
        print(f"  [OK] {symbol}: Converted CNY -> USD (rate: {CNY_TO_USD:.4f})")

    else:
        df['currency'] = 'USD'

# ============================================================================
# STEP 3: Determine Frequency (Daily vs Weekly)
# ============================================================================
print("\n[STEP 3] Determining data frequency...")

daily_symbols = []
weekly_symbols = []

for df in all_data:
    symbol = df['symbol'].iloc[0]

    # Calculate average time difference
    df_sorted = df.sort_values('date')
    time_diffs = df_sorted['date'].diff().dt.days.dropna()
    avg_diff = time_diffs.median()

    if avg_diff < 4:  # Less than 4 days = daily data
        daily_symbols.append(symbol)
        print(f"  [OK] {symbol}: DAILY (avg gap: {avg_diff:.1f} days)")
    else:  # Weekly data
        weekly_symbols.append(symbol)
        print(f"  [OK] {symbol}: WEEKLY (avg gap: {avg_diff:.1f} days)")

# ============================================================================
# STEP 4: Forward-fill Weekly Data to Daily
# ============================================================================
print("\n[STEP 4] Forward-filling weekly data to daily...")

# Get date range from daily data (rebar turkey)
rebar_df = [df for df in all_data if df['symbol'].iloc[0] == 'rebar_turkey_fob'][0]
date_range = pd.date_range(start=rebar_df['date'].min(), end=rebar_df['date'].max(), freq='D')

daily_data_filled = []

for df in all_data:
    symbol = df['symbol'].iloc[0]

    if symbol in weekly_symbols:
        # Create daily index
        df_daily = pd.DataFrame({'date': date_range})

        # Merge with weekly data
        df = df.sort_values('date')
        df_daily = df_daily.merge(df, on='date', how='left')

        # Forward fill prices
        df_daily['price'] = df_daily['price'].fillna(method='ffill')
        df_daily['symbol'] = symbol

        # Count how many values filled
        filled_count = df_daily['price'].notna().sum()
        print(f"  [OK] {symbol}: {len(df)} weekly -> {filled_count} daily records")

        daily_data_filled.append(df_daily[['date', 'symbol', 'price']])
    else:
        # Already daily, just keep it
        daily_data_filled.append(df[['date', 'symbol', 'price']])

# ============================================================================
# STEP 5: Merge All Data into Wide Format
# ============================================================================
print("\n[STEP 5] Merging all data sources...")

# Concatenate all dataframes
df_all = pd.concat(daily_data_filled, ignore_index=True)

# Pivot to wide format (one column per symbol)
df_wide = df_all.pivot(index='date', columns='symbol', values='price')

# Sort by date
df_wide = df_wide.sort_index()

# Forward fill any remaining NaN (for edge cases)
df_wide = df_wide.fillna(method='ffill')

# Backward fill for beginning NaN
df_wide = df_wide.fillna(method='bfill')

print(f"\n[OK] Merged dataset shape: {df_wide.shape[0]} days × {df_wide.shape[1]} symbols")
print(f"  Date range: {df_wide.index[0].date()} to {df_wide.index[-1].date()}")
print(f"  Missing values: {df_wide.isna().sum().sum()}")

# ============================================================================
# STEP 6: Save Processed Data
# ============================================================================
print("\n[STEP 6] Saving processed data...")

# Reset index to make date a column
df_wide_export = df_wide.reset_index()

# Save to CSV
output_file = output_dir / "steel_prices_real_data.csv"
df_wide_export.to_csv(output_file, index=False)
print(f"  [OK] Saved to: {output_file}")

# Also save long format for reference
df_all_export = df_all.sort_values(['date', 'symbol'])
long_output_file = output_dir / "steel_prices_real_data_long.csv"
df_all_export.to_csv(long_output_file, index=False)
print(f"  [OK] Saved long format to: {long_output_file}")

# ============================================================================
# STEP 7: Data Quality Report
# ============================================================================
print("\n[STEP 7] Data Quality Report...")
print("="*80)

# Summary statistics
print("\n SUMMARY STATISTICS:\n")
summary = df_wide.describe()
print(summary)

print("\n PRICE RANGES BY SYMBOL:\n")
for col in df_wide.columns:
    print(f"  {col:30s}: ${df_wide[col].min():7.2f} - ${df_wide[col].max():7.2f} (avg: ${df_wide[col].mean():7.2f})")

print("\n DATA COVERAGE:\n")
for col in df_wide.columns:
    coverage = (df_wide[col].notna().sum() / len(df_wide)) * 100
    print(f"  {col:30s}: {coverage:5.1f}% complete")

print("\n[READY] READY FOR MODEL TRAINING")
print("="*80)

print("\n[TARGET] TARGET VARIABLE: rebar_turkey_fob")
print(" FEATURE VARIABLES:", len(df_wide.columns) - 1, "symbols")
print(f" TOTAL SAMPLES: {len(df_wide)} days")
print(f" DATE RANGE: {df_wide.index[0].date()} to {df_wide.index[-1].date()}")

print("\n" + "="*80)
print("DATA INTEGRATION COMPLETE!")
print("="*80)
print("\nNext step: Run feature engineering script")
print("Command: python engineer_features_real_data.py")
