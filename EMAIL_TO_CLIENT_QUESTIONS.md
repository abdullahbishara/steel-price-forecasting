# Email to Client - Data Integration Questions

---

**Subject**: Steel Price Forecasting - Data Integration Questions

---

Dear [Client Name],

Thank you for providing the historical price data files. I've reviewed all 10 datasets and they look excellent - we have 2+ years of quality data covering the key market indicators.

Before I begin integrating the data and retraining the forecasting model, I have a few questions to ensure the model is optimized for your specific needs in the **Saudi Arabian market**:

---

## 1. Target Variable Confirmation

You mentioned that **Rebar FOB Turkey** should be the reference price (not Rebar CFR UAE). I want to confirm:

**Question**: Since you're operating in the Saudi Arabian market, are we forecasting:
- **Option A**: Rebar FOB Turkey (export price from Turkey) - as the global benchmark
- **Option B**: Rebar prices in Saudi Arabia local market (related to the UAE Ex-Works data)
- **Option C**: Both - forecast Turkey FOB and then model the basis/spread to Saudi market

**Why this matters**: The model can predict Turkish export prices, but if you're procuring in Saudi Arabia, there may be a freight/import premium we should account for.

---

## 2. Billet Price Selection

You've provided three billet price sources:
1. **CIS Black Sea Billet FOB** (Russian/Ukrainian origin)
2. **GCC Billet CFR** (delivered to Gulf region)
3. **Saudi Arabia Billet Ex-Works** (local Saudi production)

**Question**: Which billet source is most relevant for your operations?
- If you source from local Saudi producers → Use Saudi Arabia Ex-Works
- If you import from GCC region → Use GCC CFR
- If tracking global benchmark → Use CIS FOB

**My recommendation**: For Saudi Arabian market, I suggest using **Saudi Arabia Billet Ex-Works** as the primary indicator (most directly relevant), with GCC CFR as a secondary feature.

---

## 3. Currency Conversion

Some data files are in local currencies:
- **Chinese Coke prices**: CNY (Chinese Yuan)
- **Saudi Billet**: SAR (Saudi Riyal)

**Question**: What exchange rates should I use for conversion to USD?
- **Option A**: Use current market rates (as of today)
- **Option B**: Use historical daily FX rates for each date (more accurate but requires FX data)
- **Option C**: Fixed rates (e.g., SAR = 3.75 USD, CNY = 0.14 USD)

**My recommendation**: For Saudi Riyal, we can use the fixed peg (3.75 SAR = 1 USD). For Chinese Yuan, I can fetch historical rates from public sources.

---

## 4. Weekly to Daily Data Conversion

Some price series are weekly (Coal, Coke, Billet) while others are daily (Rebar, Iron Ore, Scrap):
- **Coking Coal**: ~110 weekly observations
- **Coke (China)**: ~110 weekly observations
- **Billet prices**: ~112 weekly observations

**Question**: How should I handle weekly data for daily forecasting?
- **Option A**: Forward-fill (use same value for all days in the week)
- **Option B**: Linear interpolation (smooth transition between weeks)
- **Option C**: Keep weekly and aggregate daily data to weekly (less granular forecasts)

**My recommendation**: Use **forward-fill** method - this assumes prices stay stable within the week until new assessment comes out (common industry practice for weekly indices).

---

## 5. Missing Data Sources

To further improve model accuracy, do you have access to any of these additional data sources?

**Energy Prices:**
- [ ] Brent Crude Oil (daily)
- [ ] Natural Gas (TTF or Henry Hub)

**Freight Costs:**
- [ ] Baltic Dry Index (shipping costs)

**Economic Indicators:**
- [ ] China Manufacturing PMI
- [ ] Saudi Arabia PMI or construction activity

**Foreign Exchange:**
- [ ] USD/SAR rate (probably fixed at 3.75, but worth confirming)

**Other Steel Products:**
- [ ] HRC (Hot Rolled Coil) prices
- [ ] Wire rod prices

**Note**: If not immediately available, we can proceed without these and add them later. The current dataset is already comprehensive.

---

## 6. Data Update Frequency

**Question**: Moving forward, how often will you be providing updated data?
- Daily exports from your data provider?
- Weekly updates?
- Monthly batches?

**Why this matters**: This determines whether we set up automated daily retraining or manual periodic updates.

---

## 7. Forecast Use Case

To optimize the model for your specific needs:

**Question**: What are the primary use cases for the forecasts?
- **Procurement timing**: When to place orders for rebar/billet purchases?
- **Contract pricing**: Setting prices for customer contracts?
- **Budget planning**: Financial forecasting for projects?
- **Risk management**: Hedging strategies for price volatility?
- **All of the above**?

**Why this matters**: Different use cases may prioritize different forecast horizons (1-day for trading, 30-day for budgets, etc.).

---

## 8. Saudi Market-Specific Considerations

Since you're operating in Saudi Arabia:

**Question**: Are there any Saudi-specific factors we should incorporate?
- Local production capacity changes (new mills, capacity expansions)
- Import duties or trade policies
- Seasonal demand patterns (construction seasons)
- Regional supply dynamics (GCC trade flows)

---

## My Recommendations (Summary)

Based on the data provided and your Saudi Arabian market focus, here's what I recommend:

✅ **Target**: Forecast **Rebar FOB Turkey** as global benchmark
✅ **Billet**: Use **Saudi Arabia Billet Ex-Works** + **GCC Billet CFR** as features
✅ **Currency**: SAR = 3.75 USD (fixed peg), fetch historical CNY rates
✅ **Frequency**: Forward-fill weekly data to daily
✅ **Proceed**: Start with current dataset, add energy/freight data later if available

**Timeline**:
- Once you confirm the above, I can have the model retrained with real data within **24-48 hours**
- Initial results (accuracy metrics, sample forecasts) ready for your review
- Dashboard updated with real data and new target variable

---

## Next Steps

**Option 1**: If you're comfortable with my recommendations above, simply reply "Proceed with recommendations" and I'll start immediately.

**Option 2**: If you'd like to discuss any points, let's schedule a quick 15-minute call to align.

**Option 3**: Answer the specific questions above that are most critical for your use case, and I'll proceed with sensible defaults for the rest.

---

Looking forward to your guidance so we can deliver the most accurate and relevant forecasting system for your Saudi Arabian operations.

Best regards,

Abdullah
Steel Price Forecasting Project
Email: [Your Email]
Phone: [Your Phone]

---

**Attachments**:
- Data files received (confirmed)
- Current dashboard: https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/

**Project Repository**: https://github.com/abdullahbishara/steel-price-forecasting
