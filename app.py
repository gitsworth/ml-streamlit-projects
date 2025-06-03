import streamlit as st
import yfinance as yf
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go

st.set_page_config(page_title="Stock Forecast", layout="centered")
st.title("📈 Stock Price Forecast App (Prophet Model)")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA):", value="AAPL")
n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, period="5y", progress=False)
    if data.empty:
        return None
    data.reset_index(inplace=True)
    return data

if ticker:
    data_load_state = st.text("Loading data...")
    data = load_data(ticker.upper())
    if data is None:
        st.error("❌ No data found. Please check the stock ticker symbol.")
        st.stop()
    data_load_state.text("✅ Data loaded!")

    st.subheader("✅ Columns Found:")
    st.write(data.columns.tolist())

    if 'Close' not in data.columns:
        st.error("❌ 'Close' column not found in the data. Try a different stock.")
        st.stop()

    # Plot raw data
    st.subheader("📊 Historical Closing Prices")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
    fig1.update_layout(title="Stock Price History", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig1)

    # Forecasting
    df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet(daily_seasonality=True)
    model.fit(df_train)
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)

    st.subheader(f"📉 Forecast for next {n_years} years")
    fig2 = plot_plotly(model, forecast)
    st.plotly_chart(fig2)

    st.subheader("🔍 Forecast data (tail):")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
