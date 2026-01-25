# Email to Client - Short Version

---

**Subject**: Quick Questions on Steel Price Data Integration

---

Dear [Client Name],

Thank you for the data files - they look great! Before I integrate and retrain the model, I need quick clarification on a few points:

**1. Target Variable**
You mentioned using Rebar FOB Turkey instead of UAE CFR. Confirmed - I'll use **Rebar FOB Turkey** as the target.

**2. Billet Price (3 sources provided)**
Which is most relevant for your Saudi operations?
- Saudi Arabia Billet Ex-Works (local)
- GCC Billet CFR (regional)
- CIS Black Sea FOB (global)

**My suggestion**: Use Saudi Ex-Works as primary.

**3. Currency Conversions**
- SAR → USD: Use 3.75 fixed rate?
- CNY → USD: Use historical market rates?

**4. Weekly to Daily Data**
Coal/Coke/Billet data is weekly. Should I use **forward-fill** method to convert to daily?

**5. Additional Data**
Do you have access to:
- Brent Oil prices (daily)
- Freight costs (Baltic Dry Index)
- FX rates, PMI, or other indicators

If not immediately available, we can proceed without them.

---

**My Recommendation**:
I can proceed with sensible defaults (Saudi Billet as primary, forward-fill for weekly data, standard FX conversions) unless you have specific preferences.

**Timeline**: 24-48 hours to retrain model and show results once you confirm.

Reply "Proceed" if you're comfortable with the above, or let me know your preferences.

Best regards,
Abdullah

---

**Current Dashboard**: https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/
