# Steel Price Forecasting Dashboard

## Quick Start

### 1. Install Dashboard Dependencies

```bash
pip install -r requirements_dashboard.txt
```

This will install:
- `streamlit` - Web dashboard framework
- `plotly` - Interactive charts
- `pandas` - Data manipulation
- `numpy` - Numerical computing

### 2. Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## Dashboard Features

### 📊 Overview Page
- **Current Price**: Latest rebar price with 24-hour change
- **30-Day Average & Volatility**: Market statistics
- **Model MAE**: Current prediction accuracy
- **Price Chart**: Last 90 days of price history
- **Latest Forecast**: Multi-step predictions with confidence intervals

### 📈 Price History Page
- **Multi-Symbol Charts**: Compare rebar with raw materials, oil, etc.
- **Symbol Selector**: Choose which prices to display
- **Summary Statistics**: Mean, std dev, min/max for each symbol

### 🔮 Forecasts Page
- **1-Day Ahead**: Daily prediction performance
- **7-Day Ahead**: Weekly forecast accuracy
- **30-Day Ahead**: Monthly planning forecasts
- **Actual vs Predicted Charts**: Visual comparison
- **Error Metrics**: MAE, mean error, std dev, max error

### ✅ Model Performance Page
- **Walk-Forward Validation**: Out-of-sample test results
- **Error Over Time**: Prediction errors by date
- **Error Distribution**: Histogram of forecast errors
- **Multi-Horizon Comparison**: Performance across 1, 7, 30-day forecasts

### 💼 Business Value Page
- **Cost Savings Calculator**: Interactive ROI estimator
- **Input Parameters**: Monthly volume, current price, error rates
- **Savings Projection**: Monthly and annual savings estimates
- **ROI Analysis**: Return on investment calculation
- **Business Use Cases**: Procurement, contracts, budgeting, risk management

---

## Dashboard Screenshots

### Overview
- Displays current price: **$607.50/mt**
- Shows model MAE: **$0.78/mt**
- Interactive line chart with hover details

### Forecasts
- **1-Day**: MAE $0.74/mt
- **7-Day**: MAE $1.00/mt
- **30-Day**: MAE $0.82/mt

### Business Calculator
- Input: 1,000 mt/month procurement
- Output: $180,000 annual savings estimate

---

## Customization

### Update Data
To refresh the dashboard with new data:

1. Generate new synthetic data:
   ```bash
   python generate_synthetic_data_with_external.py
   ```

2. Train models:
   ```bash
   python improve_model_r2_with_external.py
   ```

3. Run validations:
   ```bash
   python walk_forward_validation.py
   python multi_step_forecasting.py
   ```

4. Refresh dashboard (it will auto-detect new data files)

### Modify Charts
Edit `dashboard.py` to customize:
- Chart colors: Modify `line=dict(color='...')` in Plotly traces
- Layout: Change `st.columns()` configuration
- Metrics: Add new `st.metric()` displays

### Add New Pages
Add a new page by:
1. Adding option to `st.sidebar.radio()`
2. Creating new `elif page == "New Page":` block
3. Adding content with Streamlit components

---

## Production Deployment

### Option 1: Streamlit Cloud (Easiest)
1. Push code to GitHub repository
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repo
4. Deploy (free tier available)

### Option 2: Docker Container
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements_dashboard.txt
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t steel-dashboard .
docker run -p 8501:8501 steel-dashboard
```

### Option 3: Cloud VM (AWS/Azure/GCP)
1. Launch Ubuntu VM
2. Install Python 3.10+
3. Clone repository
4. Install dependencies: `pip install -r requirements_dashboard.txt`
5. Run with systemd service for auto-restart
6. Use nginx as reverse proxy
7. Enable HTTPS with Let's Encrypt

---

## Automated Daily Updates

### Windows Task Scheduler
Create `run_daily_update.bat`:
```batch
@echo off
cd C:\Users\abdul\steel_price_forecasting
python generate_synthetic_data_with_external.py
python improve_model_r2_with_external.py
python walk_forward_validation.py
python multi_step_forecasting.py
echo Update complete at %date% %time% >> update_log.txt
```

Schedule in Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 6:00 AM
4. Action: Start Program -> `run_daily_update.bat`

### Linux Cron
Add to crontab:
```bash
0 6 * * * cd /path/to/steel_price_forecasting && python generate_synthetic_data_with_external.py && python improve_model_r2_with_external.py && python walk_forward_validation.py && python multi_step_forecasting.py
```

---

## Troubleshooting

### Dashboard won't start
**Error**: `ModuleNotFoundError: No module named 'streamlit'`
**Fix**: Install requirements: `pip install -r requirements_dashboard.txt`

### Charts not showing
**Error**: Blank charts or "No data available"
**Fix**: Ensure validation files exist:
- `data/validation/walk_forward_results.csv`
- `data/validation/multi_step_*_results.csv`

Run validation scripts if missing:
```bash
python walk_forward_validation.py
python multi_step_forecasting.py
```

### Port already in use
**Error**: `Address already in use`
**Fix**: Use different port: `streamlit run dashboard.py --server.port=8502`

### Performance issues
**Symptom**: Dashboard loads slowly
**Fix**:
1. Reduce data size: Use `.tail(90)` for charts
2. Enable caching: Already implemented with `@st.cache_data`
3. Increase memory: Set `--server.maxUploadSize=1000`

---

## Integration with Real Data

When you receive real data from your team:

1. **Replace synthetic data file**:
   ```python
   # In dashboard.py, change:
   prices_file = Path("data/extracted/steel_prices_all_sources_normalized.csv")
   ```

2. **Update feature engineering**:
   - Run `improve_model_r2_with_external.py` with real data
   - Retrain model parameters

3. **Recalculate metrics**:
   - Re-run walk-forward validation
   - Update multi-step forecasts

4. **Adjust confidence intervals**:
   - Real data will have different error distributions
   - Update CI calculations in `multi_step_forecasting.py`

---

## API Integration (Future)

To integrate with live data APIs:

### Add API connector
```python
# api_connector.py
import requests

def fetch_fastmarkets_data():
    """Fetch latest prices from Fastmarkets API"""
    response = requests.get(
        "https://api.fastmarkets.com/v1/prices",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    return response.json()
```

### Schedule API calls
```python
# In dashboard.py
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_live_data():
    return fetch_fastmarkets_data()
```

---

## Support & Maintenance

### Logs
Check Streamlit logs for errors:
- Windows: `%USERPROFILE%\.streamlit\logs\`
- Linux: `~/.streamlit/logs/`

### Updates
Keep dependencies updated:
```bash
pip install --upgrade streamlit plotly pandas numpy
```

### Backup
Backup critical files:
- `data/validation/*.csv` - Validation results
- `dashboard.py` - Dashboard code
- Model weights (if saved separately)

---

## Next Enhancements

### Short-term
- [ ] Add email alerts for large price movements
- [ ] Export forecasts to Excel/PDF
- [ ] Add user authentication
- [ ] Mobile-responsive design

### Medium-term
- [ ] Real-time data integration
- [ ] Multiple commodity support (HRC, billet, etc.)
- [ ] Advanced charting (candlestick, OHLC)
- [ ] Custom date range selection

### Long-term
- [ ] Machine learning model comparison (XGBoost vs Elastic Net)
- [ ] Ensemble forecasting (combine multiple models)
- [ ] Automated alert system (SMS/email/Slack)
- [ ] Multi-user dashboard with permissions
- [ ] Integration with procurement systems (SAP, Oracle)

---

## License & Credits

**Model**: Elastic Net Regression
**Data**: Synthetic (for demonstration)
**Framework**: Streamlit + Plotly
**Created**: 2025-12-30
**Author**: Steel Price Forecasting Team

---

## Contact

For questions or issues:
- Check `EXTERNAL_FEATURES_RESULTS.md` for model details
- Review `walk_forward_validation.py` for out-of-sample testing
- See `multi_step_forecasting.py` for forecast methodology

---

**Dashboard Version**: 1.0
**Last Updated**: 2025-12-30
