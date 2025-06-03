import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("Stock Price Trend Predictor")

# User inputs the stock ticker and date range
ticker = st.text_input("Enter Stock Ticker", "AAPL")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

if ticker and start_date < end_date:
    data = yf.download(ticker, start=start_date, end=end_date)

    # Fix for multi-level columns (sometimes yfinance returns MultiIndex columns)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    if data.empty:
        st.error("No data found for this ticker and date range.")
    else:
        # Show the raw data
        st.subheader("Stock Data")
        st.write(data.tail())

        # Calculate daily returns (percentage change)
        data['Return'] = data['Adj Close'].pct_change()

        # Prepare data for trend prediction
        data = data.dropna(subset=['Return'])
        data['Day'] = np.arange(len(data)).reshape(-1, 1)

        # Fit linear regression to predict return trend
        model = LinearRegression()
        model.fit(data[['Day']], data['Return'])

        # Predict returns trend (next day)
        next_day = np.array([[len(data)]])
        predicted_return = model.predict(next_day)[0]

        st.subheader("Predicted Next Day Return")
        st.write(f"{predicted_return*100:.4f} %")

        # Show trend interpretation
        if predicted_return > 0:
            st.success("Trend looks positive! The stock price might go up tomorrow.")
        else:
            st.error("Trend looks negative! The stock price might go down tomorrow.")
else:
    st.info("Please enter a valid ticker and date range.")
