import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.title("Stock Price Trend Predictor 📈")

# User input
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, MSFT):", value="AAPL").upper()

if ticker:
    # Download historical data
    data = yf.download(ticker, period="5y", progress=False)
    
    if data.empty:
        st.error("No data found for this ticker.")
    else:
        st.subheader(f"Showing data for {ticker}")
        st.write(data.tail())

        # Prepare features
        data['Return'] = data['Adj Close'].pct_change()
        data['Target'] = (data['Return'].shift(-1) > 0).astype(int)  # 1 if next day up else 0
        data.dropna(inplace=True)

        features = data[['Return']]
        target = data['Target']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)

        # Train model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        st.write(f"Model Accuracy on test set: {accuracy:.2%}")

        # Predict next day trend using last return
        last_return = features.iloc[-1].values.reshape(1, -1)
        prediction = model.predict(last_return)[0]

        trend = "Up 📈" if prediction == 1 else "Down 📉"
        st.success(f"Predicted next day trend: **{trend}**")
