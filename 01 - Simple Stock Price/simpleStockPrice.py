import yfinance as yf
import streamlit as st

st.write("""
    # Simple Stock Price App
    This app allows you to get the current stock price of any company listed on Yahoo Finance.
""")

tickerSymble = 'XPML11.SA'
tickerData = yf.Ticker(tickerSymble)
tickerDf = tickerData.history(period='1d', start='2010-01-01', end='2024-02-17')

# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
st.line_chart(tickerDf.Dividends)