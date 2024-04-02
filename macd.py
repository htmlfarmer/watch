import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Define the ticker symbol
ticker_symbol = 'PBR'

# Define the start and end dates for historical data
start_date = '2020-01-01'
end_date = '2024-04-01'

# Fetch historical data from Yahoo Finance
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Calculate the MACD (12-day EMA - 26-day EMA)
ema12 = data['Close'].ewm(span=12, min_periods=0, adjust=False).mean().values
ema26 = data['Close'].ewm(span=26, min_periods=0, adjust=False).mean().values
macd = ema12 - ema26

# Calculate the Signal Line (9-day EMA of MACD)
signal_line = pd.Series(macd).ewm(span=9, min_periods=0, adjust=False).mean().values

# Plot the MACD and Signal Line
plt.figure(figsize=(12,6))
plt.plot(data.index.to_numpy(), macd, label='MACD', color='blue')
plt.plot(data.index.to_numpy(), signal_line, label='Signal Line', color='red')
plt.title('MACD Analysis for {}'.format(ticker_symbol))
plt.xlabel('Date')
plt.ylabel('MACD')
plt.legend()
plt.show()
