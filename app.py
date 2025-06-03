import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.title("📈 Stock Price Trend Predictor")

ticker = st.text_input("Enter Stock Ticker Symbol", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))

if ticker and start_date < end_date:
    try:
        # Use yf.Ticker for more consistent results
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)

        # Fallback if 'Adj Close' is missing
        if 'Adj Close' in data.columns:
            close_col = 'Adj Close'
        elif 'Close' in data.columns:
            close_col = 'Close'
        else:
            st.error("No closing price data found.")
            st.stop()

        st.subheader("📋 Data Preview")
        st.write(data[[close_col]].tail())

        # Calculate returns
        data['Return'] = data[close_col].pct_change()
        data.dropna(inplace=True)
        data['Day'] = np.arange(len(data))

        # Train linear regression model
        model = LinearRegression()
        model.fit(data[['Day']], data['Return'])
        next_day = np.array([[len(data)]])
        predicted_return = model.predict(next_day)[0]

        st.subheader("📊 Predicted Next Day Return")
        st.write(f"{predicted_return * 100:.4f} %")

        if predicted_return > 0:
            st.success("📈 Positive trend: stock may go up.")
        else:
            st.error("📉 Negative trend: stock may go down.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
