import logging
import persistent
from logging.config import fileConfig

from db_utils import MyZODB

#TODO find better place to open 1 db instance shared across methods
# subclass of Persistent to save in DB

class Stock(persistent.Persistent):

    def __init__(self, name, type, symbol, reco_date, reco_date_price, stock_id):
        '''

        :param name: name of stockl
        :param type:  Timely or All weather
        :param symbol:  NSE symbol
        :param reco_date:  Date of recommendation
        :param reco_date_price:  Price of recommendation date
        :param stock_id : VR stock id for lookup
        '''
        self.name = name
        self.type = type
        self.symbol = symbol
        self.reco_date = reco_date
        self.reco_date_price = reco_date_price
        self.stock_id = stock_id


#TODO: Change it to accept what type of stock we want timely or all-weather
def get_vr_stocks():
    '''
    return all timely or all-weather stocks
    :param type:
    :return: list of tuples (symbol, stock_object)
    '''

    mydb = MyZODB()
    logging.debug(f"Total Recommended stocks : {len(mydb.dbroot.stocks)}")

    return mydb.dbroot.stocks.items()

def check_stock_in_db(symbol):
    '''

    :param symbol:
    :return:  stock object or None
    '''
    stock_obj = None
    mydb = MyZODB()
    if symbol in mydb.dbroot.stocks:
        stock_obj = mydb.dbroot.stocks[symbol]

    return stock_obj

if __name__ == '__main__':
    fileConfig('logging.ini',disable_existing_loggers=True)
    logger = logging.getLogger()
    res = get_vr_stocks()
    logging.debug("get stocks: stored in %s" % type(res))

    symbol = 'LT'
    stock_obj = check_stock_in_db(symbol)
    logging.debug(f'{symbol} : {stock_obj.type}')
