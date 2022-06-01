#https://pypi.org/project/yahooquery/2.2.5/
from yahooquery import Ticker
import requests
import json

def GetSingleStock(tickerString):
    tickers = Ticker(tickerString)
    return tickers
def GetAllStocks(tickerString):
    tickers = Ticker(tickerString)
    return tickers


def get_symbol_list(symbol):
    url = "https://query1.finance.yahoo.com/v1/finance/search?q={}".format(symbol)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    result = result.content.decode()
    print(result)
    return json.loads(result)['quotes']


get_symbol_list("Micro")
