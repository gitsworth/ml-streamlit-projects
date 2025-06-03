import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("📈 Stock Price Trend Predictor")

# Inputs
ticker = st.text_input("Enter Stock Ticker Symbol", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))

if ticker and start_date < end_date:
    data = yf.download(ticker, start=start_date, end=end_date)

    # Handle MultiIndex column issue
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if 'Adj Close' not in data.columns:
        st.error("'Adj Close' column not found in data. Please try a different ticker.")
    elif data.empty:
        st.error("No data found. Please try a different ticker or date range.")
    else:
        st.subheader("Raw Stock Data")
        st.write(data.tail())

        # Calculate return and fit trend
        data['Return'] = data['Adj Close'].pct_change()
        data.dropna(inplace=True)
        data['Day'] = np.arange(len(data))

        model = LinearRegression()
        model.fit(data[['Day']], data['Return'])
        next_day = np.array([[len(data)]])
        predicted_return = model.predict(next_day)[0]

        st.subheader("📊 Predicted Next Day Return")
        st.write(f"{predicted_return*100:.4f} %")

        if predicted_return > 0:
            st.success("📈 Positive trend: stock may go up.")
        else:
            st.error("📉 Negative trend: stock may go down.")
else:
    st.info("Enter valid inputs to see predictions.")
