import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("📈 Stock Price Trend Predictor")

# Sidebar input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA):", value="AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if start_date >= end_date:
    st.error("End date must be after start date.")
    st.stop()

# Fetch data
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No data found. Please check the ticker and date range.")
    st.stop()

# Check for 'Adj Close', else use 'Close'
if 'Adj Close' in data.columns:
    price_column = 'Adj Close'
elif 'Close' in data.columns:
    price_column = 'Close'
else:
    st.error("Expected 'Adj Close' or 'Close' column in data.")
    st.stop()

data['Return'] = data[price_column].pct_change()
data = data.dropna()

# Prepare data for prediction
data['Day'] = np.arange(len(data)).reshape(-1, 1)
X = data['Day'].values.reshape(-1, 1)
y = data[price_column].values

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict future price
future_days = st.slider("Days into the future to predict", 1, 30, 7)
future_index = np.array([[len(data) + future_days]])
predicted_price = model.predict(future_index)[0]

# Display
st.subheader(f"Predicted Price for {ticker.upper()} after {future_days} days:")
st.success(f"${predicted_price:.2f}")

# Plot
st.line_chart(data[price_column])
