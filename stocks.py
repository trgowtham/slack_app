import csv
import logging
from logging.config import fileConfig
from functools import wraps
from time import time
from collections import  namedtuple

Stock = namedtuple('Stock', 'name type symbol reco_date reco_date_price stock_id')

# Dictionary to hold all VR stocks namedtuple
VR_STOCKS = None

def all_vr_stocks():
    '''
     Read vr_stock_db.csv and return a list of tuples, (stock, namedtuple)

    :return:
    '''

    with open('vr_stock_db.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        stock_list = [Stock(**row) for row in csv_reader]
        logging.debug(f'all_vr_stocks: {stock_list}')
    return {s.symbol: s for s in stock_list}


class StockCache():

    def __init__(self, cache, expiry_time=0):
        self.cache = cache
        self.expiry_time = expiry_time

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args):
            mem_args = args[0]
            if mem_args in self.cache:
                logging.debug(f' {mem_args} found in cache')
                result, timestamp = self.cache[mem_args]
                age = time() - timestamp
                if age < timestamp:
                    return result
                else:
                    logging.debug(f'{mem_args} values in cache expired')

            result = func(*args)
            # cache result as tuple with timestamp
            self.cache[mem_args] = (result, time())
            logging.debug(f'Cache updated for {mem_args}')
            return result
        return wrapped


#TODO: Change it to accept what type of stock we want timely or all-weather
def get_vr_stocks():
    '''
    return all timely or all-weather stocks
    :param type:
    :return: list of tuples (symbol, stock_object)
    '''
    global  VR_STOCKS

    if not VR_STOCKS:
        VR_STOCKS = all_vr_stocks()

    return VR_STOCKS.items()

def check_stock_in_db(symbol):
    '''

    :param symbol:
    :return:  stock object or None
    '''
    global VR_STOCKS
    if not VR_STOCKS:
        VR_STOCKS = all_vr_stocks()

    if symbol in VR_STOCKS:
        stock_obj = VR_STOCKS[symbol]

    return stock_obj


if __name__ == '__main__':
    fileConfig('logging.ini',disable_existing_loggers=True)
    logger = logging.getLogger()

    fileConfig('logging.ini',disable_existing_loggers=True)
    logger = logging.getLogger()
    res = get_vr_stocks()
    logging.debug(f'stocks: {res}')

    symbol = 'LT'
    stock_obj = check_stock_in_db(symbol)
    tuple_dict = {d[0]:None for d in res}
    logging.debug(f'{symbol} : {stock_obj.type}')

