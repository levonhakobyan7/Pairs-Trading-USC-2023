import os
from data_load.config import STOCK_NUM
from data_load.request_api import StockApi
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

if __name__ == "__main__":
    # load data
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'data/')):
        os.mkdir(os.path.join(os.path.dirname(__file__), 'data/'))

    api = StockApi()
    market_tickers = api.get_tickers([])
    logging.info(f"Start Loading Stock Data.")
    ticker_details = api.get_tickers_detail(market_tickers)
    best_500_stocks = sorted(ticker_details, key=lambda d: d['cap'], reverse=True)[:STOCK_NUM]
    data = api.get_candles(best_500_stocks)
    logging.info(f"Stock Data Saved.")