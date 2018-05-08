import nsepy
import logging

from datetime import date
from stocks import get_stocks
from db_utils import MyZODB
from dateutil import parser
from collections import namedtuple

StockInfo = namedtuple('StockInfo','name lastPrice pChange dayLow dayHigh open')

def check_vr_reco(symbol):
    '''
    Check whether a stock is VR recommended or not
    :param symbol:
    :return:
        If symbol is VR recommended, return Stock object else None
    '''
    stock = None
    mydb = MyZODB()
    if symbol in mydb.dbroot.stocks:
        stock = mydb.dbroot.stocks[symbol]
    mydb.close()
    return stock

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
    # open the DB

    mydb = MyZODB()
    # check symbol is in db or not
    if symbol in mydb.dbroot.stocks:
        stock_obj = mydb.dbroot.stocks[symbol]
        dt = parser.parse(stock_obj.reco_date)
        min, max = get_min_max(symbol, dt.date(), date.today())
        str = '{:<10};{:<10};{:<15};{:<10};{:<10}'.format(symbol, stock_obj.reco_date, stock_obj.reco_date_price,
                                                          min, max)
        result.append(str)
    elif not symbol:
        # symbol is None
        for stock_symbol, stock_obj in mydb.dbroot.stocks.items():
            dt = parser.parse(stock_obj.reco_date)
            min, max = get_min_max(stock_symbol, dt.date(), date.today())
            str = '{:<10};{:<10};{:<15};{:<10};{:<10}'.format(stock_symbol, stock_obj.reco_date, stock_obj.reco_date_price,
                                                          min, max)
            result.append(str)
    mydb.close()
    return result


def get_live_price(symbol):
    '''

    :param symbol:
    :return:  StockInfo object
    '''
    try:
        info = nsepy.live.get_quote(symbol)
        stock_info = StockInfo(info['companyName'], info['lastPrice'],
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

    mydb = MyZODB()
    result = []
    multiplier = (100 - percentage)/100
    for stock_symbol, stock in mydb.dbroot.stocks.items():
        live_price = get_live_price(stock_symbol).lastPrice
        reco_price = float(stock.reco_date_price.replace(',', ''))
        logging.debug(f'{stock_symbol} live: {live_price} reco_price: {reco_price}')
        if live_price < (multiplier * reco_price):
            logging.debug(f'Appending : {stock_symbol}:  {live_price}')
            result.append('{:<10};{:<10};{:<10}'.format(stock_symbol, reco_price, live_price))

    mydb.close()
    return result

def reco_percent(percent, dir):
    '''
    :param percentage: input percentage
    :param dir: '<' or '>'
    :return: list of qualified stock in tuples (symbol, current_price, % from reco_price)
    '''
    result = []
    result.append(str)
    # open the DB

    mydb = MyZODB()
    # check symbol is in db or not
    for symbol in mydb.dbroot.stocks.items():
        stock = mydb.dbroot.stocks[symbol]
    return None


if __name__ == '__main__':
    #data = min_max_reco_date()
    #for line in data:
    #    print(line)
    result = alert_below_percentage(10)
    print(result)
