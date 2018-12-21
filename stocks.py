import csv
import logging
import shutil

from logging.config import fileConfig
from functools import wraps
from time import time
from collections import  namedtuple

Stock = namedtuple('Stock', 'name type symbol reco_date reco_date_price stock_id')

VR_CSV_FILE = 'vr_stock_db.csv'
# Dictionary to hold all VR stocks namedtuple
VR_STOCKS = None

def all_vr_stocks():
    '''
     Read vr_stock_db.csv and return a list of tuples, (stock, namedtuple)

    :return:
    '''

    with open(VR_CSV_FILE, mode='r') as csv_file:
        # Filter lines which starts with comments
        csv_reader = csv.DictReader(filter(lambda row: row[0]!= '#', csv_file))
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
    stock_obj = None
    global VR_STOCKS
    if not VR_STOCKS:
        VR_STOCKS = all_vr_stocks()

    if symbol in VR_STOCKS:
        stock_obj = VR_STOCKS[symbol]

    return stock_obj

def add_recos(new_reco):

    # Temp file to write to.
    TEMP_CSV = 'vr_stock_db_temp.csv'
    #create a dummy file with all existing reco and then add the new objects
    recos = all_vr_stocks()

    # add the new recos to VR_STOCKS.
    # This is to make a single data point to write back to file.
    for stock in new_reco:
        recos[stock.symbol] = stock

    # write to a dummy file
    with open(TEMP_CSV, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=Stock._fields)
        writer.writeheader()
        for d in recos.items():
            # import pdb;pdb.set_trace()
            writer.writerow(d[1]._asdict())

    # move temp file to original db csv file
    shutil.move(TEMP_CSV, VR_CSV_FILE)


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

