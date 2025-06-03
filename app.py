import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🔍 Stock Data Debugger")

ticker = st.text_input("Enter stock ticker (e.g., AAPL):", value="AAPL")

if ticker:
    data = yf.download(ticker, period="5y")
    
    if data.empty:
        st.error("❌ No data returned. Check the ticker.")
    else:
        st.success("✅ Data received.")
        st.write("### Raw Data:")
        st.write(data.head())

        st.write("### Columns:")
        st.write(data.columns.tolist())
