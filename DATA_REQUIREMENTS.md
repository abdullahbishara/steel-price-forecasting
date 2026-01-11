# Data Requirements for Steel Price Forecasting System

**Project**: Steel Price Forecasting Dashboard
**Purpose**: Machine Learning model to predict UAE Rebar import prices
**Current Status**: Working prototype with synthetic data
**Next Phase**: Integration with real market data

---

## 📋 Executive Summary

We need daily time-series data for steel prices and related market indicators to train our forecasting model. The model currently achieves 99.84% accuracy with synthetic data and is ready for real data integration.

**Minimum data requirement**: 12 months of daily data
**Recommended**: 24+ months for better trend analysis
**Update frequency**: Daily (preferred) or weekly minimum

---

## 🎯 PRIMARY DATA REQUIRED (Critical)

### 1. Target Variable - Steel Rebar Prices

**What we need:**
- **Product**: Rebar / Reinforcing bar steel
- **Specification**: Standard grade (Grade 60 or local equivalent)
- **Region**: UAE import prices (CFR/CIF basis preferred)
- **Unit**: USD per metric tonne (USD/mt)
- **Frequency**: Daily closing prices
- **Time period**: Minimum 12 months, preferably 24+ months
- **Format**: CSV or Excel with columns: Date, Symbol/Product, Price

**Example format:**
```csv
date,symbol,price_usd_mt
2024-01-01,rebar_uae_import,607.50
2024-01-02,rebar_uae_import,609.25
2024-01-03,rebar_uae_import,605.80
```

**Data sources (if available):**
- Fastmarkets (MB-STE-0152: UAE Rebar Import)
- Argus Steel
- Platts/S&P Global
- World Steel Prices
- Our internal procurement records

---

## 🔧 EXTERNAL FEATURES (Tier 1 - High Priority)

These raw materials directly impact rebar production costs. Essential for accurate forecasting.

### 2. Iron Ore Prices

**Specification:**
- **Grade**: 62% Fe content (industry standard)
- **Delivery**: CFR China (benchmark pricing)
- **Unit**: USD/mt
- **Frequency**: Daily
- **Symbol reference**: Iron Ore 62% Fe CFR China

**Data sources:**
- Fastmarkets (MB-IRO-0008)
- Platts IODEX 62% Fe
- Argus Iron Ore Index

### 3. Coking Coal Prices

**Specification:**
- **Type**: Premium coking coal (metallurgical grade)
- **Delivery**: CFR China
- **Unit**: USD/mt
- **Frequency**: Daily
- **Symbol reference**: Premium Hard Coking Coal

**Data sources:**
- Fastmarkets (MB-COA-0002)
- Platts Premium Low Vol HCC
- Argus Coking Coal Index

### 4. Ferrous Scrap Prices

**Specifications (one or more of these):**
- **HMS 1/2 (80:20)**: Heavy melting scrap, CFR Turkey or CFR China
- **Shredded scrap**: CFR Turkey
- **Busheling scrap**: CFR Turkey
- **Unit**: USD/mt
- **Frequency**: Daily or weekly

**Data sources:**
- Fastmarkets scrap indices
- Argus Ferrous Scrap
- Our local scrap procurement prices

### 5. Steel Billet Prices

**Specification:**
- **Product**: Steel billet (semi-finished product)
- **Grade**: 3SP or 5SP
- **Region**: CIS export, Middle East, or China domestic
- **Unit**: USD/mt
- **Frequency**: Daily or weekly

**Data sources:**
- Fastmarkets billet prices
- Argus Steel
- Our billet procurement records

---

## ⚡ EXTERNAL FEATURES (Tier 2 - Medium Priority)

These market and macro indicators improve model accuracy.

### 6. Energy Prices

**6a. Crude Oil (Brent)**
- **Specification**: Brent crude oil futures
- **Unit**: USD per barrel
- **Frequency**: Daily closing prices
- **Data source**: Bloomberg, EIA, or public financial data

**6b. Natural Gas**
- **Specification**:
  - TTF (European benchmark) OR
  - Henry Hub (US benchmark)
- **Unit**: USD per MMBtu
- **Frequency**: Daily
- **Data source**: EIA, ICE, Bloomberg

### 7. Freight Costs

**Specification:**
- **Index**: Baltic Dry Index (BDI)
- **Unit**: Index points
- **Frequency**: Daily
- **Data source**: Baltic Exchange (publicly available)

### 8. Foreign Exchange Rates

**Specification:**
- **Pair**: USD/AED exchange rate
- **Frequency**: Daily spot rates
- **Data source**: Central Bank UAE, Bloomberg, or xe.com

### 9. Economic Indicators

**9a. China Manufacturing PMI**
- **Specification**: China Manufacturing Purchasing Managers' Index
- **Unit**: Index value (50 = expansion threshold)
- **Frequency**: Monthly
- **Data source**: National Bureau of Statistics of China (publicly available)

**9b. Global Steel Production (Optional)**
- **Unit**: Million tonnes per month
- **Frequency**: Monthly
- **Data source**: World Steel Association

---

## 📊 DATA FORMAT REQUIREMENTS

### Preferred Format: CSV Files

**Required columns:**
- `date` (YYYY-MM-DD format, e.g., 2024-01-15)
- `symbol` (product identifier, e.g., "rebar_uae_import", "iron_ore_62fe_cfr_china")
- `price_usd_mt` (numeric value in USD per metric tonne)

**Optional but helpful columns:**
- `price_low` (daily low price)
- `price_high` (daily high price)
- `volume` (traded volume if available)
- `source` (data provider name)

### Example CSV Structure:

```csv
date,symbol,price_usd_mt,source
2024-01-01,rebar_uae_import,607.50,Fastmarkets
2024-01-01,iron_ore_62fe_cfr_china,102.50,Platts
2024-01-01,coking_coal_premium_cfr_china,215.00,Argus
2024-01-02,rebar_uae_import,609.25,Fastmarkets
2024-01-02,iron_ore_62fe_cfr_china,103.20,Platts
```

**Alternative formats accepted:**
- Excel (.xlsx) with one sheet per symbol
- Multiple CSV files (one per symbol)
- JSON time-series format
- Database exports (PostgreSQL, MySQL)

---

## 📅 DATA QUALITY REQUIREMENTS

### Essential Quality Criteria:

1. **Completeness**
   - Maximum 5% missing values
   - No gaps longer than 3 consecutive days
   - Weekend/holiday handling: Use last available price or mark as N/A

2. **Consistency**
   - Same unit of measurement throughout (USD/mt)
   - Consistent date format
   - No duplicate dates for the same symbol

3. **Accuracy**
   - Prices should be within reasonable ranges (e.g., rebar $300-$1000/mt)
   - Sudden spikes (>20% daily change) should be verified
   - Source attribution for price assessments

4. **Timeliness**
   - Historical data: As far back as available (minimum 12 months)
   - Ongoing updates: Daily by 9 AM local time (or agreed schedule)

---

## 🔄 DATA UPDATE SCHEDULE

### Initial Data Delivery:
- **Target date**: [Specify date]
- **Historical period**: [Start date] to [End date]
- **Delivery method**: Email, shared drive, FTP, or API access

### Ongoing Updates:
- **Frequency**: Daily (preferred) or weekly
- **Delivery time**: By 9:00 AM UAE time
- **Delivery method**:
  - Option 1: Automated API feed (best)
  - Option 2: Email attachment (CSV)
  - Option 3: Shared folder (Google Drive, OneDrive, Dropbox)
  - Option 4: SFTP/FTP server

---

## 📦 PRIORITY CHECKLIST

### Must Have (Cannot proceed without):
- [ ] UAE Rebar import prices (12+ months daily data)
- [ ] Iron ore 62% Fe CFR China (12+ months)
- [ ] Coking coal CFR China (12+ months)

### Should Have (Significantly improves accuracy):
- [ ] Ferrous scrap prices (HMS 1/2 or similar)
- [ ] Steel billet prices
- [ ] Brent crude oil prices
- [ ] Baltic Dry Index

### Nice to Have (Further enhancements):
- [ ] Natural gas prices (TTF or Henry Hub)
- [ ] USD/AED exchange rates
- [ ] China Manufacturing PMI
- [ ] Additional steel products (HRC, wire rod, etc.)

---

## 💼 DATA SOURCES & SUBSCRIPTIONS

If Our organization doesn't have these data sources, here are recommendations:

### Commercial Data Providers:

**Tier 1 (Comprehensive):**
1. **Fastmarkets (Recommended)**
   - Coverage: Steel, iron ore, coal, scrap
   - Format: API, CSV, Excel
   - Cost: ~$15,000-30,000/year per package

2. **S&P Global Platts**
   - Coverage: Metals, energy, freight
   - Format: API, Excel
   - Cost: ~$20,000-40,000/year

3. **Argus Media**
   - Coverage: Steel, coal, freight
   - Format: Excel, PDF reports
   - Cost: ~$10,000-25,000/year

**Tier 2 (Budget-friendly):**
4. **SteelOrbis**
   - Coverage: Steel prices globally
   - Cost: ~$3,000-5,000/year

5. **Metal Bulletin / Fastmarkets (Basic)**
   - Coverage: Steel prices only
   - Cost: ~$5,000-10,000/year

### Free/Public Data Sources:

- **Baltic Dry Index**: https://www.bloomberg.com/quote/BDIY:IND (free)
- **China PMI**: National Bureau of Statistics of China (free)
- **Brent Oil**: EIA.gov, Investing.com (free with delay)
- **FX Rates**: Central Bank UAE, xe.com (free)

### Internal Sources:

- **Our procurement records**: Historical rebar purchase prices
- **Supplier quotes**: Regular price quotes from steel suppliers
- **Industry reports**: Monthly/quarterly price reports from trade associations

---

### Our Requirements:

Please specify:
- [ ] Data classification level (Public/Internal/Confidential/Restricted)
- [ ] Access permissions required
- [ ] NDA or data sharing agreement needed
- [ ] Compliance requirements (GDPR, local regulations)

---

## 🚀 INTEGRATION TIMELINE

### Phase 1: Data Acquisition (Week 1-2)
- Receive historical data files
- Validate data quality
- Identify gaps or issues

### Phase 2: Data Processing (Week 2-3)
- Normalize data to standard format
- Handle missing values
- Merge with existing synthetic data structure

### Phase 3: Model Retraining (Week 3-4)
- Retrain model with real data
- Validate accuracy metrics
- Compare with synthetic data results

### Phase 4: Production Deployment (Week 4-5)
- Update dashboard with real data
- Set up automated daily updates
- Monitor performance

### Phase 5: Ongoing Maintenance
- Daily data ingestion
- Weekly accuracy monitoring
- Monthly model retraining

---

### Submission Checklist:

- [ ] Data files (CSV/Excel)
- [ ] Data dictionary (column definitions)
- [ ] Source attribution (which provider for each symbol)
- [ ] Date range covered
- [ ] Known issues or gaps
- [ ] Contact person for data questions

---

## ❓ FREQUENTLY ASKED QUESTIONS

### Q1: Why do we need daily data?
**A**: Steel prices change daily based on raw material costs, supply/demand, and market sentiment. Daily data allows the model to capture these short-term dynamics and provide accurate next-day forecasts.

### Q2: Can we use weekly data instead?
**A**: Weekly data can work but reduces forecast accuracy by 15-25%. Daily data is strongly preferred for production use.

### Q3: What if we don't have access to commercial data providers?
**A**: We can work with:
1. Our internal procurement records (rebar purchase prices)
2. Free public sources (oil, FX, freight indices)
3. Supplier quotes and market reports
4. Start with limited features and expand later

### Q4: How much will data subscriptions cost?
**A**:
- Basic (steel prices only): $3,000-10,000/year
- Comprehensive (all features): $15,000-40,000/year
- Alternative: Use procurement records + free sources (~$0)

### Q5: How do we handle missing data?
**A**: The model can handle up to 5% missing values using:
- Forward-fill (use previous day's price)
- Interpolation (average of surrounding days)
- Exclude that feature for affected dates

### Q6: Can we start with partial data?
**A**: Yes! Minimum viable dataset:
- Rebar prices (Our procurement records)
- Iron ore prices (public indices available)
- Basic model can start with just these two

---

**Project repository**: https://github.com/abdullahbishara/steel-price-forecasting
**Live dashboard**: https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/

---

**Document prepared by**: Steel Price Forecasting Team
**Date**: 2026-01-11
**Version**: 1.0
**Status**: Ready for department review

---

## 📎 APPENDIX: SYMBOL REFERENCE TABLE

Quick reference for symbol naming conventions:

| Symbol ID | Description | Unit | Typical Range |
|-----------|-------------|------|---------------|
| `rebar_uae_import` | UAE Rebar import price | USD/mt | $400-800 |
| `iron_ore_62fe_cfr_china` | Iron ore 62% Fe CFR China | USD/mt | $80-150 |
| `coking_coal_premium_cfr_china` | Premium coking coal CFR China | USD/mt | $150-400 |
| `metallurgical_coal_cfr_china` | Metallurgical coal CFR China | USD/mt | $120-300 |
| `steam_coal_api2` | Steam coal API2 (European) | USD/mt | $50-200 |
| `scrap_hms12_8020_cfr_turkey` | HMS 1/2 (80:20) CFR Turkey | USD/mt | $300-500 |
| `scrap_shredded_cfr_turkey` | Shredded scrap CFR Turkey | USD/mt | $350-550 |
| `scrap_busheling_cfr_turkey` | Busheling scrap CFR Turkey | USD/mt | $400-600 |
| `billet_cis_export` | Steel billet CIS export | USD/mt | $400-700 |
| `brent_crude_oil` | Brent crude oil | USD/bbl | $50-120 |
| `natural_gas_ttf` | Natural gas TTF European | USD/MMBtu | $5-30 |
| `natural_gas_henry_hub` | Natural gas Henry Hub US | USD/MMBtu | $2-10 |
| `baltic_dry_index` | Baltic Dry Index | Index | 500-3000 |
| `usd_aed_fx` | USD/AED exchange rate | Rate | 3.65-3.68 |
| `china_pmi_manufacturing` | China Manufacturing PMI | Index | 45-55 |

---

**End of Data Requirements Document**
