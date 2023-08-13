import requests
import json
import hmac
import hashlib
import time
import urllib.parse as urlparse
from urllib.parse import urlencode

#https://api.binance.com/api/v3/exchangeInfo

class BinanceData():

    def __init__(self, api_key: str = '', api_secret: str = ''):
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            'X-MBX-APIKEY': self.api_key
        }
        self.host_trade = 'https://fapi.binance.com'

    def __make_request(self, method, prx):
        try:
            url = self.host_trade + prx
            response = requests.request(method=method, url=url, headers=self.headers)
            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            else: return False
        except Exception as ex:
            return False 
            
    def get_prices(self, symbol: str = ''):
        prx = '/fapi/v1/ticker/price?symbol=%s' % symbol
        data = self.__make_request('GET', prx)
        return data

    def get_exchange_info(self):
        prx = '/fapi/v1/exchangeInfo'
        data = self.__make_request('GET', prx)
        return data
    
    def get_order_book(self, symbol: str):
        prx = '/fapi/v1/depth'
        data = self.__make_request('GET', prx)
        return data
    
    def get_recent_trades_list(self, symbol: str):
        prx = '/fapi/v1/trades'
        data = self.__make_request('GET', prx)
        return data

    def get_old_trades_lookup(self, symbol: str):
        prx = '/fapi/v1/historicalTrades'
        data = self.__make_request('GET', prx)
        return data

    def get_klines_data(self, symbol: str, interval: str):
        prx = '/fapi/v1/klines'
        data = self.__make_request('GET', prx)
        return data

    def get_continuous_contract_kline(self, symbol: str, contractType: str, interval: str):
        prx = '/fapi/v1/continuousKlines'
        data = self.__make_request('GET', prx)
        return data

    def get_index_price_kline(self, symbol: str, interval: str):
        prx = '/fapi/v1/indexPriceKlines'
        data = self.__make_request('GET', prx)
        return data

    def get_mark_price_kline(self, symbol: str, interval: str):
        prx = '/fapi/v1/markPriceKlines'
        data = self.__make_request('GET', prx)
        return data

    def get_mark_price(self, symbol: str = ''):
        prx = '/fapi/v1/premiumIndex'
        data = self.__make_request('GET', prx)
        return data

    def get_funding_rate_history(self, symbol: str = ''):
        prx = '/fapi/v1/fundingRate'
        data = self.__make_request('GET', prx)
        return data

    def get_24hr_ticker_price_change_statistics(self, symbol: str = ''):
        prx = '/fapi/v1/ticker/24hr'
        data = self.__make_request('GET', prx)
        return data

    def get_symbol_price_ticker(self, symbol: str = ''):
        prx = '/fapi/v1/ticker/price'
        data = self.__make_request('GET', prx)
        return data

    def get_symbol_order_book_ticker(self, symbol: str = ''):
        prx = '/fapi/v1/ticker/bookTicker'
        data = self.__make_request('GET', prx)
        return data

    def get_open_interest(self, symbol: str):
        prx = '/fapi/v1/openInterest'
        data = self.__make_request('GET', prx)
        return data

    def get_open_interest_statistic(self, symbol: str, period: str, limit = 500):
        prx = '/futures/data/openInterestHist'
        data = self.__make_request('GET', prx)
        return data

    def get_long_short_ratio(self, symbol: str, period: str, limit = 500):
        prx = '/futures/data/globalLongShortAccountRatio'
        data = self.__make_request('GET', prx)
        return data

    def get_taker_buy_sell_volume(self, symbol: str, period: str, limit = 500):
        prx = '/futures/data/takerlongshortRatio'
        data = self.__make_request('GET', prx)
        return data
    

# data = BinanceData().get_prices('ETHUSDT')
# print(type(data))
