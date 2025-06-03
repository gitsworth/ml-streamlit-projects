import streamlit as st
import yfinance as yf
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go

st.title("📈 Stock Price Forecast App (Prophet Model)")

# User inputs
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA):", value="AAPL")
n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, period="5y")
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Loading data...")
data = load_data(ticker)
data_load_state.text("✅ Data loaded successfully!")

# Plot raw data
st.subheader("📊 Raw Stock Data")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Stock Price"))
fig.layout.update(title_text="Time Series Plot", xaxis_rangeslider_visible=True)
st.plotly_chart(fig)

# Forecasting with Prophet
df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

m = Prophet(daily_seasonality=True)
m.fit(df_train)

future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader(f"📈 Forecast for {ticker.upper()} ({n_years} years)")
fig_forecast = plot_plotly(m, forecast)
st.plotly_chart(fig_forecast)

st.subheader("Forecast Data")
st.write(forecast.tail())
