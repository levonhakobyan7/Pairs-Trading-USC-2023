from load_pkl import get_data

if __name__ == "__main__":
    # a list of stock symbols that you want, if the symbol is invalid, the system will ignore
    stock_list = ["AAPL", 'META', "SPY", "BTC-USD", "ETH-USD"]
    # choice of headers from ['Adj Close', 'Close', 'Open', 'Volume', 'Low', 'High']
    headers = ['Adj Close', 'Close']
    stock_data = get_data(stock_list, headers)
    print(stock_data)
    print(stock_data.columns)
