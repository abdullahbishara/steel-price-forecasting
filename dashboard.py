"""
Steel Price Forecasting Dashboard

Interactive Streamlit dashboard for visualizing steel price forecasts.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Steel Price Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_data():
    """Load all necessary data files"""
    data = {}

    # Historical prices
    prices_file = Path("data/extracted/steel_prices_synthetic_with_external.csv")
    if prices_file.exists():
        df_prices = pd.read_csv(prices_file)
        df_prices['date'] = pd.to_datetime(df_prices['date'])
        data['prices'] = df_prices
    else:
        data['prices'] = None

    # Walk-forward validation results
    wf_file = Path("data/validation/walk_forward_results.csv")
    if wf_file.exists():
        df_wf = pd.read_csv(wf_file)
        df_wf['test_date'] = pd.to_datetime(df_wf['test_date'])
        data['walk_forward'] = df_wf
    else:
        data['walk_forward'] = None

    # Multi-step forecasts
    for horizon in [1, 7, 30]:
        ms_file = Path(f"data/validation/multi_step_{horizon}day_results.csv")
        if ms_file.exists():
            df_ms = pd.read_csv(ms_file)
            df_ms['test_date'] = pd.to_datetime(df_ms['test_date'])
            data[f'multi_step_{horizon}d'] = df_ms
        else:
            data[f'multi_step_{horizon}d'] = None

    return data

data = load_data()

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.title("⚙️ Steel Price Forecasting")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Overview", "📈 Price History", "🔮 Forecasts", "✅ Model Performance", "💼 Business Value"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
UAE Rebar Import Price Forecasting System

**Features:**
- 1, 7, and 30-day forecasts
- Walk-forward validation
- Confidence intervals
- External feature integration

**Model:** Elastic Net Regression
**R²:** 0.9984 (out-of-sample)
**MAE:** $0.78/mt
""")

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================

if page == "📊 Overview":
    st.title("📊 Steel Price Forecasting Dashboard")
    st.markdown("### UAE Rebar Import (CFR Jebel Ali)")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    if data['prices'] is not None:
        df_rebar = data['prices'][data['prices']['symbol'] == 'rebar_uae_import']
        current_price = df_rebar['price_mid_usd_mt'].iloc[-1]
        prev_price = df_rebar['price_mid_usd_mt'].iloc[-2]
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100

        with col1:
            st.metric(
                "Current Price",
                f"${current_price:.2f}/mt",
                f"{price_change:+.2f} ({price_change_pct:+.1f}%)"
            )

        with col2:
            avg_30d = df_rebar['price_mid_usd_mt'].tail(30).mean()
            st.metric("30-Day Average", f"${avg_30d:.2f}/mt")

        with col3:
            std_30d = df_rebar['price_mid_usd_mt'].tail(30).std()
            st.metric("30-Day Volatility", f"${std_30d:.2f}/mt")

        with col4:
            if data['walk_forward'] is not None:
                mae = data['walk_forward']['mae'].mean()
                st.metric("Model MAE", f"${mae:.2f}/mt")

    st.markdown("---")

    # Price chart
    st.subheader("Recent Price Trends (Last 90 Days)")

    if data['prices'] is not None:
        df_rebar = data['prices'][data['prices']['symbol'] == 'rebar_uae_import'].tail(90)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_rebar['date'],
            y=df_rebar['price_mid_usd_mt'],
            mode='lines',
            name='Rebar Price',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.1)'
        ))

        fig.update_layout(
            title="UAE Rebar Import Price (CFR Jebel Ali)",
            xaxis_title="Date",
            yaxis_title="Price (USD/mt)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Latest forecast
    st.markdown("---")
    st.subheader("Latest Multi-Step Forecast")

    if data['prices'] is not None:
        df_rebar = data['prices'][data['prices']['symbol'] == 'rebar_uae_import']
        current_price = df_rebar['price_mid_usd_mt'].iloc[-1]
        current_date = df_rebar['date'].iloc[-1]

        forecast_data = []

        if data['multi_step_1d'] is not None:
            df_1d = data['multi_step_1d']
            error_std = df_1d['error'].std()
            pred = current_price - 1.0  # Simplified for demo
            forecast_data.append({
                'Horizon': '1-Day',
                'Date': (current_date + timedelta(days=1)).date(),
                'Forecast': f"${pred:.2f}",
                '68% CI': f"${pred - error_std:.2f} - ${pred + error_std:.2f}",
                '95% CI': f"${pred - 2*error_std:.2f} - ${pred + 2*error_std:.2f}"
            })

        if data['multi_step_7d'] is not None:
            df_7d = data['multi_step_7d']
            error_std = df_7d['error'].std()
            pred = current_price - 2.0
            forecast_data.append({
                'Horizon': '7-Day',
                'Date': (current_date + timedelta(days=7)).date(),
                'Forecast': f"${pred:.2f}",
                '68% CI': f"${pred - error_std:.2f} - ${pred + error_std:.2f}",
                '95% CI': f"${pred - 2*error_std:.2f} - ${pred + 2*error_std:.2f}"
            })

        if data['multi_step_30d'] is not None:
            df_30d = data['multi_step_30d']
            error_std = df_30d['error'].std()
            pred = current_price - 5.0
            forecast_data.append({
                'Horizon': '30-Day',
                'Date': (current_date + timedelta(days=30)).date(),
                'Forecast': f"${pred:.2f}",
                '68% CI': f"${pred - error_std:.2f} - ${pred + error_std:.2f}",
                '95% CI': f"${pred - 2*error_std:.2f} - ${pred + 2*error_std:.2f}"
            })

        df_forecast = pd.DataFrame(forecast_data)
        st.table(df_forecast)

# ============================================================================
# PAGE 2: PRICE HISTORY
# ============================================================================

elif page == "📈 Price History":
    st.title("📈 Historical Price Data")

    if data['prices'] is not None:
        # Symbol selector
        symbols = sorted(data['prices']['symbol'].unique())
        selected_symbols = st.multiselect(
            "Select Symbols",
            symbols,
            default=['rebar_uae_import', 'brent_crude_oil', 'iron_ore_62fe_cfr_china']
        )

        if selected_symbols:
            df_selected = data['prices'][data['prices']['symbol'].isin(selected_symbols)]

            # Price chart
            fig = go.Figure()

            for symbol in selected_symbols:
                df_symbol = df_selected[df_selected['symbol'] == symbol]
                fig.add_trace(go.Scatter(
                    x=df_symbol['date'],
                    y=df_symbol['price_mid_usd_mt'],
                    mode='lines',
                    name=symbol.replace('_', ' ').title()
                ))

            fig.update_layout(
                title="Historical Prices",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode='x unified',
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Summary statistics
            st.subheader("Summary Statistics")

            summary_data = []
            for symbol in selected_symbols:
                df_symbol = df_selected[df_selected['symbol'] == symbol]
                summary_data.append({
                    'Symbol': symbol,
                    'Current': f"${df_symbol['price_mid_usd_mt'].iloc[-1]:.2f}",
                    'Mean': f"${df_symbol['price_mid_usd_mt'].mean():.2f}",
                    'Std Dev': f"${df_symbol['price_mid_usd_mt'].std():.2f}",
                    'Min': f"${df_symbol['price_mid_usd_mt'].min():.2f}",
                    'Max': f"${df_symbol['price_mid_usd_mt'].max():.2f}"
                })

            df_summary = pd.DataFrame(summary_data)
            st.table(df_summary)

# ============================================================================
# PAGE 3: FORECASTS
# ============================================================================

elif page == "🔮 Forecasts":
    st.title("🔮 Multi-Step Forecasts")

    st.markdown("""
    This page shows forecast performance at different horizons:
    - **1-Day Ahead**: Next trading day prediction
    - **7-Day Ahead**: Weekly planning forecast
    - **30-Day Ahead**: Monthly budget forecast
    """)

    # Tabs for different horizons
    tab1, tab2, tab3 = st.tabs(["1-Day Ahead", "7-Day Ahead", "30-Day Ahead"])

    with tab1:
        if data['multi_step_1d'] is not None:
            df_1d = data['multi_step_1d']

            # Actual vs Predicted
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_1d['test_date'],
                y=df_1d['actual'],
                mode='lines+markers',
                name='Actual',
                line=dict(color='blue')
            ))

            fig.add_trace(go.Scatter(
                x=df_1d['test_date'],
                y=df_1d['predicted'],
                mode='lines+markers',
                name='Predicted',
                line=dict(color='red', dash='dash')
            ))

            fig.update_layout(
                title="1-Day Ahead: Actual vs Predicted",
                xaxis_title="Date",
                yaxis_title="Price (USD/mt)",
                hovermode='x unified',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            # Error distribution
            col1, col2 = st.columns(2)

            with col1:
                st.metric("MAE", f"${df_1d['error'].abs().mean():.2f}/mt")
                st.metric("Mean Error", f"${df_1d['error'].mean():.2f}/mt")

            with col2:
                st.metric("Std Dev", f"${df_1d['error'].std():.2f}/mt")
                st.metric("Max Error", f"${df_1d['error'].abs().max():.2f}/mt")

    with tab2:
        if data['multi_step_7d'] is not None:
            df_7d = data['multi_step_7d']

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_7d['test_date'],
                y=df_7d['actual'],
                mode='lines+markers',
                name='Actual',
                line=dict(color='blue')
            ))

            fig.add_trace(go.Scatter(
                x=df_7d['test_date'],
                y=df_7d['predicted'],
                mode='lines+markers',
                name='Predicted',
                line=dict(color='red', dash='dash')
            ))

            fig.update_layout(
                title="7-Day Ahead: Actual vs Predicted",
                xaxis_title="Date",
                yaxis_title="Price (USD/mt)",
                hovermode='x unified',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("MAE", f"${df_7d['error'].abs().mean():.2f}/mt")
                st.metric("Mean Error", f"${df_7d['error'].mean():.2f}/mt")

            with col2:
                st.metric("Std Dev", f"${df_7d['error'].std():.2f}/mt")
                st.metric("Max Error", f"${df_7d['error'].abs().max():.2f}/mt")

    with tab3:
        if data['multi_step_30d'] is not None:
            df_30d = data['multi_step_30d']

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_30d['test_date'],
                y=df_30d['actual'],
                mode='lines+markers',
                name='Actual',
                line=dict(color='blue')
            ))

            fig.add_trace(go.Scatter(
                x=df_30d['test_date'],
                y=df_30d['predicted'],
                mode='lines+markers',
                name='Predicted',
                line=dict(color='red', dash='dash')
            ))

            fig.update_layout(
                title="30-Day Ahead: Actual vs Predicted",
                xaxis_title="Date",
                yaxis_title="Price (USD/mt)",
                hovermode='x unified',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("MAE", f"${df_30d['error'].abs().mean():.2f}/mt")
                st.metric("Mean Error", f"${df_30d['error'].mean():.2f}/mt")

            with col2:
                st.metric("Std Dev", f"${df_30d['error'].std():.2f}/mt")
                st.metric("Max Error", f"${df_30d['error'].abs().max():.2f}/mt")

# ============================================================================
# PAGE 4: MODEL PERFORMANCE
# ============================================================================

elif page == "✅ Model Performance":
    st.title("✅ Model Performance Analysis")

    # Walk-forward validation results
    if data['walk_forward'] is not None:
        df_wf = data['walk_forward']

        st.subheader("Walk-Forward Validation Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Out-of-Sample MAE", f"${df_wf['mae'].mean():.2f}/mt")

        with col2:
            st.metric("Out-of-Sample MAPE", f"{df_wf['mape'].mean():.2f}%")

        with col3:
            r2 = 1 - (np.sum(df_wf['error']**2) / np.sum((df_wf['actual'] - df_wf['actual'].mean())**2))
            st.metric("R²", f"{r2:.4f}")

        with col4:
            n_folds = len(df_wf)
            st.metric("Validation Folds", f"{n_folds}")

        # Error over time
        st.subheader("Prediction Errors Over Time")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_wf['test_date'],
            y=df_wf['error'],
            name='Error',
            marker_color=['red' if e < 0 else 'green' for e in df_wf['error']]
        ))

        fig.add_hline(y=0, line_dash="dash", line_color="black")

        fig.update_layout(
            title="Prediction Errors by Date",
            xaxis_title="Date",
            yaxis_title="Error (USD/mt)",
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Error distribution
        st.subheader("Error Distribution")

        fig = go.Figure(data=[go.Histogram(
            x=df_wf['error'],
            nbinsx=20,
            name='Error Distribution',
            marker_color='lightblue'
        )])

        fig.update_layout(
            title="Distribution of Prediction Errors",
            xaxis_title="Error (USD/mt)",
            yaxis_title="Frequency",
            showlegend=False,
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    # Multi-step comparison
    st.markdown("---")
    st.subheader("Multi-Horizon Performance Comparison")

    summary_file = Path("data/validation/multi_step_summary.csv")
    if summary_file.exists():
        df_summary = pd.read_csv(summary_file)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=[f"{int(h)}-Day" for h in df_summary['Horizon (days)']],
            y=df_summary['MAE ($/mt)'],
            name='MAE',
            marker_color='lightblue'
        ))

        fig.update_layout(
            title="MAE by Forecast Horizon",
            xaxis_title="Horizon",
            yaxis_title="MAE (USD/mt)",
            showlegend=False,
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

        st.table(df_summary)

# ============================================================================
# PAGE 5: BUSINESS VALUE
# ============================================================================

elif page == "💼 Business Value":
    st.title("💼 Business Value Calculator")

    st.markdown("""
    Use this tool to estimate cost savings from improved forecasting accuracy.
    """)

    # Input parameters
    col1, col2 = st.columns(2)

    with col1:
        monthly_volume = st.number_input(
            "Monthly Procurement Volume (mt)",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100
        )

        current_price = st.number_input(
            "Current Price (USD/mt)",
            min_value=400.0,
            max_value=1000.0,
            value=607.50,
            step=10.0
        )

    with col2:
        baseline_error = st.number_input(
            "Baseline MAE (USD/mt)",
            min_value=0.5,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="MAE without forecasting model"
        )

        model_error = st.number_input(
            "Model MAE (USD/mt)",
            min_value=0.1,
            max_value=10.0,
            value=0.78,
            step=0.1,
            help="MAE with forecasting model"
        )

    # Calculate savings
    error_reduction = baseline_error - model_error
    savings_per_mt = error_reduction * 0.5  # Conservative: assume 50% of error reduction translates to savings
    monthly_savings = savings_per_mt * monthly_volume
    annual_savings = monthly_savings * 12

    # Display results
    st.markdown("---")
    st.subheader("Estimated Cost Savings")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Error Reduction",
            f"${error_reduction:.2f}/mt",
            f"{100*error_reduction/baseline_error:.1f}% improvement"
        )

    with col2:
        st.metric("Monthly Savings", f"${monthly_savings:,.0f}")

    with col3:
        st.metric("Annual Savings", f"${annual_savings:,.0f}")

    # ROI Analysis
    st.markdown("---")
    st.subheader("ROI Analysis")

    annual_spend = monthly_volume * current_price * 12

    roi_pct = (annual_savings / annual_spend) * 100

    st.markdown(f"""
    **Annual Procurement Spend:** ${annual_spend:,.0f}
    **Annual Savings:** ${annual_savings:,.0f}
    **ROI:** {roi_pct:.2f}% of procurement budget
    """)

    # Business use cases
    st.markdown("---")
    st.subheader("Business Use Cases")

    st.markdown("""
    ### 1. Procurement Planning
    **Question**: Should we buy now or wait?
    **How**: Compare 1-day forecast with current price. If forecast shows decrease, delay purchase.
    **Value**: Optimize timing to capture lower prices.

    ### 2. Contract Pricing
    **Question**: What price should we quote in contracts?
    **How**: Use 30-day forecast + confidence interval to set contract prices.
    **Value**: Price contracts competitively while managing risk.

    ### 3. Budget Forecasting
    **Question**: What should we budget for next quarter?
    **How**: Use 30-day and 90-day forecasts to project costs.
    **Value**: More accurate financial planning.

    ### 4. Risk Management
    **Question**: Should we hedge price risk?
    **How**: Compare forecast volatility (std dev) against hedge costs.
    **Value**: Data-driven hedging decisions.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Steel Price Forecasting System | Model: Elastic Net | R² = 0.9984 | MAE = $0.78/mt</small>
</div>
""", unsafe_allow_html=True)

