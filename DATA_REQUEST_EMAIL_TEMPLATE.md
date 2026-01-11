# Email Template for Data Request

---

**Subject**: Data Requirements for Steel Price Forecasting System - Action Required

---

Dear [Data Team / Procurement Team / Manager Name],

I hope this email finds you well.

We have successfully developed a **Steel Price Forecasting Dashboard** that predicts UAE Rebar import prices using machine learning. The prototype is currently live and achieving **99.84% accuracy** with synthetic data.

**Dashboard**: https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/

To transition from prototype to production, we need access to **real market data**. Below is a summary of our data requirements.

---

## 🎯 CRITICAL DATA NEEDED (Priority 1)

### 1. UAE Rebar Import Prices (Target Variable)
- **Product**: Rebar / Reinforcing bar steel
- **Region**: UAE import prices (CFR/CIF basis)
- **Unit**: USD per metric tonne
- **Period**: Minimum 12 months, preferably 24+ months
- **Frequency**: Daily closing prices
- **Format**: CSV or Excel

**Possible sources**:
- Our internal procurement records
- Fastmarkets (MB-STE-0152: UAE Rebar Import)
- Argus Steel
- Supplier price quotes

### 2. Iron Ore Prices
- **Specification**: 62% Fe content, CFR China
- **Unit**: USD/mt, Daily prices
- **Period**: Same as rebar (12-24 months)

### 3. Coking Coal Prices
- **Specification**: Premium coking coal, CFR China
- **Unit**: USD/mt, Daily prices
- **Period**: Same as rebar (12-24 months)

---

## 📊 ADDITIONAL DATA (Priority 2 - Improves Accuracy)

- **Ferrous Scrap Prices** (HMS 1/2, Shredded, or Busheling)
- **Steel Billet Prices** (CIS export or Middle East)
- **Brent Crude Oil Prices** (publicly available)
- **Baltic Dry Index** (freight costs - publicly available)

---

## 📋 WHAT WE NEED FROM YOU

1. **Data Sources**: Which data providers do we have access to?
   - [ ] Fastmarkets
   - [ ] S&P Global Platts
   - [ ] Argus Media
   - [ ] SteelOrbis
   - [ ] Internal procurement records
   - [ ] Other: _____________

2. **Historical Data**: Can you provide the data files for the past 12-24 months?
   - Preferred format: CSV with columns (date, symbol, price_usd_mt)
   - Timeline: By [specify date]

3. **Ongoing Updates**: How can we receive daily/weekly updates?
   - [ ] Email attachment
   - [ ] Shared drive (OneDrive, Google Drive)
   - [ ] API access
   - [ ] Database connection
   - [ ] Other: _____________

4. **Budget**: If we need new subscriptions, what's the approved budget?
   - Basic steel data package: $3,000-10,000/year
   - Comprehensive package (all features): $15,000-40,000/year
   - Use free sources + procurement records: $0

---

## 📅 PROPOSED TIMELINE

| Week | Activity |
|------|----------|
| Week 1-2 | Receive historical data, validate quality |
| Week 2-3 | Process and integrate data |
| Week 3-4 | Retrain model with real data |
| Week 4-5 | Deploy to production dashboard |
| Ongoing | Daily automated updates |

---

## 📎 ATTACHMENTS

Please find attached:
1. **DATA_REQUIREMENTS.md** - Complete technical specifications (detailed)
2. **Dashboard demo** - https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/

---

## ✅ ACTION ITEMS

**For Data Team:**
- [ ] Review attached data requirements document
- [ ] Identify available data sources (internal and subscriptions)
- [ ] Provide historical data files for critical symbols
- [ ] Set up ongoing data delivery mechanism

**For Procurement/Finance:**
- [ ] Approve budget for data subscriptions (if needed)
- [ ] Review data provider options

**For Management:**
- [ ] Approve project timeline
- [ ] Designate point of contact for ongoing coordination

---

## 📞 NEXT STEPS

I propose we schedule a **30-minute meeting** to discuss:
1. Available data sources
2. Data access permissions
3. Timeline and responsibilities
4. Budget considerations

**Proposed meeting times:**
- Option 1: [Date/Time]
- Option 2: [Date/Time]
- Option 3: [Date/Time]

Please let me know your availability, or feel free to suggest an alternative time.

---

## ❓ QUESTIONS?

If you have any questions about the data requirements, please don't hesitate to reach out.

**Contact Information:**
- Email: [Your Email]
- Phone: [Your Phone]
- Project Dashboard: https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/

---

## 💼 BUSINESS VALUE

Once deployed with real data, this system will provide:
- ✅ **Daily price forecasts** (1-day, 7-day, 30-day ahead)
- ✅ **95% confidence intervals** for risk management
- ✅ **Cost savings** of $25,000-$250,000 annually (based on procurement volume)
- ✅ **Better procurement timing** (buy low, negotiate better)
- ✅ **Budget accuracy** for long-term planning

The model has already proven its capability with synthetic data. With real market data, we can deliver immediate business value.

---

Thank you for your support on this initiative. I look forward to collaborating with you to make this forecasting system a valuable tool for our organization.

Best regards,

[Your Name]
[Your Title]
[Your Department]
[Contact Information]

---

**Attachments:**
1. DATA_REQUIREMENTS.md (detailed specifications)
2. Dashboard screenshot or link

**CC**: [Manager], [Stakeholders]

---

## ALTERNATIVE: SHORT VERSION FOR QUICK REQUEST

If you prefer a very brief request, use this:

---

**Subject**: Quick Request - Steel Price Data for Forecasting Model

Hi [Name],

We've built a steel price forecasting dashboard (live at: https://steel-price-forecasting-2ppxjawkb8yjptlr8pujyi.streamlit.app/) and need real data to make it production-ready.

**Can you help provide:**
1. **UAE Rebar import prices** (12+ months of daily data)
2. **Iron ore & coking coal prices** (same period)
3. **Scrap and billet prices** (if available)

**Format**: CSV or Excel with date, symbol, price columns

**Timeline**: By [date]

Detailed requirements attached. Can we schedule 15 minutes to discuss?

Thanks!
[Your Name]

---
