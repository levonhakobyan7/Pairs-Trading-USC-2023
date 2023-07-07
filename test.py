import yfinance as yf

data = yf.download("SPY AAPL", start="2013-01-01", end="2023-04-30")

print(data.keys())
print(data)