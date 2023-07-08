from polygon import RESTClient
from config import POLYGON_API_KEY, MAX_THREAD_NUM, STOCK_NUM, PKL_FILE_NAME
import yfinance as yf
import time
from multiprocessing.pool import ThreadPool as Pool
import pickle
import logging
from datetime import datetime
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class StockApi:
    def __init__(self):
        self.polygonClient = RESTClient(POLYGON_API_KEY)
        self.yahooClient = yf
        self.market = 'stocks'

    def get_tickers(self, symbols: list) -> list:
        tickers = []
        start = time.time()

        for t in self.polygonClient.list_tickers(market=self.market, active=True, limit=1000):
            ticker = {}
            ticker['name'] = t.__getattribute__('name')
            ticker['exchange'] = t.__getattribute__('primary_exchange')
            ticker['symbol'] = t.__getattribute__('ticker')
            # print(ticker)
            tickers.append(ticker)
        return tickers

    def get_tickers_detail(self, symbols: list) -> list:
        def get_tickers_loop(symbol):
            try:
                detail = self.polygonClient.get_ticker_details(symbol)
                ticker_detail = None
                if detail.__getattribute__('market_cap'):
                    ticker_detail = {
                            "symbol":symbol,
                            'cap':detail.__getattribute__('market_cap')
                    }
                else:
                    ticker_detail = {
                        "symbol": symbol,
                        'cap': -1
                    }
                logging.info(f"Load Data for {ticker_detail['symbol']}")
                return ticker_detail
            except:
                return {}

        res = []
        start = time.time()
        pool = Pool(MAX_THREAD_NUM)
        for each_t in symbols:
            if type(each_t) == dict:
                res.append(pool.apply_async(get_tickers_loop, (each_t['symbol'],)))
            elif type(each_t) == str:
                res.append(pool.apply_async(get_tickers_loop, (each_t,)))


        pool.close()
        pool.join()
        ticker_details = [res.get() for res in res if res.get() != {}]
        return ticker_details


    def get_candles(self, symbols:list, store=True):
        stock_list = [item['symbol'] for item in symbols]
        stocks = ' '.join(stock_list)
        data = yf.download(stocks, start="1990-01-01", end=datetime.today().strftime('%Y-%m-%d'))
        if store:
            self.store(data)
        return data

    def store(self, data):
        with open(PKL_FILE_NAME, 'wb') as f:
            pickle.dump(data, f)

    def get_ticker_detail(self, symbol:str) -> dict:
        try:
            detail = self.polygonClient.get_ticker_details(symbol)
            print(detail)
            ticker_detail = {
                "symbol": symbol,
                'cap': detail.__getattribute__('market_cap')
            }
            return {
                'status':200,
                'data':ticker_detail,
                'msg': ''
            }
        except Exception as e:
            return {
                'status': 404,
                'data': {},
                'msg': 'Not Found.'
            }



if __name__ == "__main__":
    # api = StockApi()
    # market_tickers = api.get_tickers([])
    # ticker_details = api.get_tickers_detail(market_tickers)
    # best_500_stocks = sorted(ticker_details, key=lambda d: d['cap'], reverse=True)[:STOCK_NUM+1]
    # data = api.get_candles(best_500_stocks)
    api = StockApi()
    # print(api.get_ticker_detail('asdasdasd'))
    # print(api.get_tickers_detail(["AAPL", 'sadkhksjgd']))


