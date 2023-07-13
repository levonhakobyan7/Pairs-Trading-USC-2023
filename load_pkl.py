import pandas as pd
from config import PKL_FILE_NAME
from request_api import StockApi
import pickle


def get_data(stocks: list, headers: list):
    with open(PKL_FILE_NAME, 'rb') as f:
        loaded_data = pickle.load(f)

    valid_stock, re_request_stocks = [], []
    stock_symbols = loaded_data.columns.get_level_values(1).unique()

    for i in stocks:
        if i in stock_symbols:
            valid_stock.append(i)
        else:
            re_request_stocks.append(i)

    jointed_data = loaded_data.loc[:, (headers, valid_stock)]

    # re-request
    # check valid
    api = StockApi()
    # v_stocks = api.get_tickers_detail(re_request_stocks)
    v_stocks = []
    for stock in re_request_stocks:
        v_stocks.append({'symbol': stock, 'cap':-1})
    data = api.get_candles(v_stocks, store=False)
    v_jointed_data = data[(headers)]
    concat_data = jointed_data.join(v_jointed_data)
    f.close()
    return concat_data


if __name__ == "__main__":
    stock_list = ["AAPL", 'META', "SPY", "QQQ"]
    headers = ['Adj Close', 'Close']
    date = get_data(stock_list, headers)
    print(date)
