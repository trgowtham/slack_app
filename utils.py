import nsepy
import logging

from logging.config import fileConfig
from datetime import date
from stocks import get_vr_stocks, check_stock_in_db, StockCache
from dateutil import parser
from collections import namedtuple
from multiprocessing import Pool

# Adding stock symbol to this for easy access.
StockInfo = namedtuple('StockInfo','name symbol lastPrice pChange dayLow dayHigh open')

cache_live = {}
CACHE_EXPIRY = 600
PARALLEL = 5 # parallel threads

def run_parallel(func, arg_list):
    '''

    :param func:  func to run in parallel
    :param arg_list: arg_list to func
    :return:  list of results
    '''
    with Pool(PARALLEL) as process:
        result = process.map(func, arg_list)
    return result

def check_vr_reco(symbol):
    '''
    Check whether a stock is VR recommended or not
    :param symbol:
    :return:
        If symbol is VR recommended, return Stock object else None
    '''
    return check_stock_in_db(symbol)

def get_min_max(stock, start_date, end_date):
    '''

    :param stock:
    :param start_date:
    :param end_date:
    :return:
    '''
    data = nsepy.get_history(symbol=stock, start=start_date, end=end_date)
    min = data['Low'].min()
    max = data['High'].max()
    logging.debug(f'for {stock} return values ({min},{max})')
    return (min, max)


def min_max_reco_date(symbol=None):
    '''

    :return: returns a list of string objects in format :
    (Symbol'; 'Reco-date'; 'Reco-date-price'; 'Min';'Max')

    '''
    result = []
    str = '{:<10};{:<10};{:<15};{:<10};{:<10}'.format('Symbol', 'Reco-date', 'Reco-date-price', 'Min',
                                                      'Max')
    result.append(str)

    if not symbol:
        # provide info for all stocks
        for stock_symbol, stock_obj in get_vr_stocks():
            dt = parser.parse(stock_obj.reco_date)
            min, max = get_min_max(stock_symbol, dt.date(), date.today())
            str = '{:<10};{:<10};{:<15};{:<10};{:<10}'.format(stock_symbol, stock_obj.reco_date, stock_obj.reco_date_price,
                                                          min, max)
            result.append(str)
    else:
        stock_obj = check_stock_in_db(symbol)
        if stock_obj:
            dt = parser.parse(stock_obj.reco_date)
            min, max = get_min_max(symbol, dt.date(), date.today())
            str = '{:<10};{:<10};{:<15};{:<10};{:<10}'.format(symbol, stock_obj.reco_date, stock_obj.reco_date_price,
                                                          min, max)
            result.append(str)
    logging.debug(f'return: {result}')
    return result

@StockCache(cache_live, CACHE_EXPIRY)
def get_live_price(symbol):
    '''

    :param symbol:
    :return:  StockInfo object
    '''
    try:
        logging.debug(f'get live price for {symbol}')
        info = nsepy.live.get_quote(symbol)
        stock_info = StockInfo(info['companyName'], symbol,
                               info['lastPrice'],
                               info['pChange'], info['dayLow'],
                               info['dayHigh'],info['open'])
        return stock_info
    except IndexError as err:
        logging.error('get_live_price: %s', str(err))
        raise err



def alert_below_percentage(percentage):
    '''

    :param percentage: how much lower the value has gone
    :return: list of semicolon separated strings in order:
            STOCK_SYMBOL ; RECO PRICE ; LIVE_PRICE
    '''
    logging.debug(f' Getting stocks below {percentage} %')
    result = []
    multiplier = (100 - percentage)/100

    # create a list of vr recommended stock symbols
    vr_stocks = get_vr_stocks()
    stock_list = [symbol for symbol, _ in vr_stocks]

    # get live prices
    vr_live_prices = run_parallel(get_live_price, stock_list)
    logging.debug(f'{vr_live_prices}')
    for info_obj in vr_live_prices:
        stock = check_stock_in_db(info_obj.symbol)
        reco_price = float(stock.reco_date_price.replace(',', ''))
        logging.debug(f'{info_obj.symbol} live: {info_obj.lastPrice} reco_price: {reco_price}')
        if info_obj.lastPrice < (multiplier * reco_price):
            logging.debug(f'Appending : {info_obj.symbol}:  {info_obj.lastPrice}')
            result.append('{:<10};{:<10};{:<10}'.format(info_obj.symbol, reco_price, info_obj.lastPrice))

    return result


if __name__ == '__main__':
    fileConfig('logging.ini', disable_existing_loggers=True)
    logger = logging.getLogger()
    result = alert_below_percentage(10)
    logging.debug(f'result of alert_below_percentage(10):  {result}')
    logging.debug(f'cache: {cache_live}')

