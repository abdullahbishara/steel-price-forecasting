# Steel Price Forecasting Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

An interactive dashboard for forecasting UAE Rebar import prices using Elastic Net regression with external market indicators.

## 🎯 Features

- **📊 Real-time Price Monitoring**: Track current rebar prices with 24-hour changes
- **🔮 Multi-Step Forecasting**: 1-day, 7-day, and 30-day ahead predictions
- **📈 Price History**: Compare rebar with raw materials (iron ore, coal, scrap, oil)
- **✅ Model Performance**: Walk-forward validation with out-of-sample testing
- **💼 Business ROI Calculator**: Interactive tool to estimate cost savings

## 🚀 Live Demo

**Dashboard URL**: [Your App URL Here]

## 📊 Model Performance

- **Out-of-Sample MAE**: $0.78/mt
- **Out-of-Sample R²**: 0.9984
- **1-Day Forecast MAE**: $0.74/mt
- **7-Day Forecast MAE**: $1.00/mt
- **30-Day Forecast MAE**: $0.82/mt

## 🗂️ Project Structure

```
steel_price_forecasting/
├── dashboard.py                    # Main Streamlit dashboard
├── requirements.txt                # Python dependencies
├── data/
│   ├── extracted/
│   │   └── steel_prices_synthetic_with_external.csv  # 17 symbols × 365 days
│   ├── features/
│   │   └── steel_features_with_external.csv          # 294 samples × 591 features
│   └── validation/
│       ├── walk_forward_results.csv                  # Out-of-sample validation
│       └── multi_step_*_results.csv                  # Multi-horizon forecasts
└── scripts/
    ├── generate_synthetic_data_with_external.py      # Data generation
    ├── improve_model_r2_with_external.py             # Model training
    ├── walk_forward_validation.py                    # Validation testing
    └── multi_step_forecasting.py                     # Forecast generation
```

## 💻 Local Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/steel_price_forecasting.git
cd steel_price_forecasting
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run dashboard.py
```

4. Open your browser to `http://localhost:8501`

## 🔧 Technology Stack

- **Framework**: Streamlit
- **ML Model**: Scikit-learn Elastic Net Regression
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy

## 📈 Data & Features

### Price Symbols (17 total):
- **Steel Products**: UAE Rebar import price (target)
- **Raw Materials**: Iron ore 62% Fe, coking coal, metallurgical coal, steam coal
- **Ferrous Scrap**: HMS 1/2, shredded, busheling
- **Semi-finished**: Steel billet
- **Energy**: Brent crude oil, natural gas (TTF, Henry Hub)
- **Freight**: Baltic Dry Index
- **FX**: USD/AED exchange rate
- **Macro**: China Manufacturing PMI

### Feature Engineering (589 features):
- Lag features (1, 5, 10, 20, 30 days)
- Rolling statistics (5, 20, 30-day windows)
- Momentum indicators
- Price spreads and ratios
- RSI (Relative Strength Index)

## 🎯 Model Details

### Algorithm: Elastic Net Regression
- **Alpha**: 0.01
- **L1 Ratio**: 0.5
- **Active Features**: 19 out of 589
- **Regularization**: L1 (Lasso) + L2 (Ridge)

### Validation Methodology:
- **Walk-Forward Validation**: Rolling window with 17 folds
- **Initial Training**: 180 days
- **Step Size**: 7 days
- **Test Size**: 7 days per fold

## 📊 Dashboard Pages

### 1. Overview
- Current price and key metrics
- 90-day price chart
- Latest multi-step forecasts with confidence intervals

### 2. Price History
- Multi-symbol comparison charts
- Interactive Plotly visualizations
- Summary statistics table

### 3. Forecasts
- Actual vs Predicted charts for 1/7/30-day horizons
- Error metrics (MAE, MAPE, R², Directional Accuracy)
- Recent forecast results

### 4. Model Performance
- Walk-forward validation results
- Error distribution histograms
- Multi-horizon performance comparison

### 5. Business Value
- Interactive ROI calculator
- Monthly/annual savings projections
- Use case examples

## 🚀 Deployment on Streamlit Cloud

This dashboard is deployed on Streamlit Community Cloud (free tier).

### Deploy Your Own:
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and `dashboard.py`
6. Click "Deploy"

## 📝 Data Updates

To update with new data:

1. Generate new synthetic data:
```bash
python generate_synthetic_data_with_external.py
```

2. Train model:
```bash
python improve_model_r2_with_external.py
```

3. Run validations:
```bash
python walk_forward_validation.py
python multi_step_forecasting.py
```

4. Dashboard will automatically load new data files

## 🔐 Data Privacy

**Note**: This project uses synthetic data generated via Geometric Brownian Motion for demonstration purposes. No real proprietary pricing data is included in this repository.

For production use with real data:
- Store sensitive data in private repositories
- Use Streamlit secrets management for API keys
- Implement user authentication if needed

## 📚 Documentation

- [DASHBOARD_README.md](DASHBOARD_README.md) - Complete dashboard usage guide
- [EXTERNAL_FEATURES_RESULTS.md](EXTERNAL_FEATURES_RESULTS.md) - Model analysis
- [SESSION_COMPLETE_SUMMARY.md](SESSION_COMPLETE_SUMMARY.md) - Project summary

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.

## 🙏 Acknowledgments

- Built with Streamlit framework
- Scikit-learn for machine learning
- Plotly for interactive visualizations

---

**⭐ If you find this project useful, please consider giving it a star!**
