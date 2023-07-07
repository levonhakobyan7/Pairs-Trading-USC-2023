import yfinance as yf
import pickle

# get 100 stocks with largest market cap
stock_list = ["SPY", "AAPL"]

# download the data of the 100 stocks
def get_data(stock_list, start_date="2013-01-01", end_date="2023-04-30", output_file="stock_data.pkl"):
    stocks = ' '.join(stock_list)
    data = yf.download(stocks, start=start_date, end=end_date)
    with open(output_file, 'wb') as f:
        pickle.dump(data, f)

get_data(stock_list, output_file="top_100.pkl")


# TODO: load pickle file
# with open('top_100.pkl', 'rb') as f:
#     loaded_data = pickle.load(f)
# # print(loaded_data)
# apple_adj_close = loaded_data[('Adj Close', 'AAPL')]
# print(len(apple_adj_close))
