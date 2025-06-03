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
    data = yf.download(ticker, start=start_date, end=end_date)

    # Show all columns to debug
    st.subheader("📋 Data Columns")
    st.write(data.columns.tolist())

    # Fix: Flatten MultiIndex if needed
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [' '.join(col).strip() for col in data.columns.values]

    # Debug: Show tail
    st.subheader("📄 Raw Data Preview")
    st.write(data.tail())

    # Check for 'Adj Close'
    if 'Adj Close' not in data.columns:
        st.error("'Adj Close' column not found in data. Please try a different ticker.")
    else:
        # Proceed with analysis
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
