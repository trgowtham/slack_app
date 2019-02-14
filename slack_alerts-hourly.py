import logging
import os
import sys
from nsetools import Nse
from logging.config import fileConfig
from slackclient import SlackClient
from utils import get_vr_price_live, StockInfo
from time import sleep
from decimal import Decimal
from datetime import datetime
from pytz import timezone


NIFTY = 'NIFTY 50'

def dict_to_stock_info(stock_dict):
    '''
    Convert dictionary returned from Nse to StockInfo object
    to make it compatible with existing tools
    :param stock_dict:
    :return:  StockInfo
    '''
    logging.debug(f'Nse dict: {stock_dict}')
    #pChange = Decimal(stock_dict["pChange"])
    pChange = -6.0
    stock_info = StockInfo(stock_dict['name'], NIFTY, stock_dict["lastPrice"], pChange, -1, -1, -1)
    logging.debug(f' Equivalent StockInfo: {stock_info}')
    return stock_info


def alert_below_percentage(percentage):
    '''
    :param percentage: how much lower the value has gone
    :return: list of StockInfo objects
    '''
    logging.debug(f' Getting stocks below {percentage} %')
    result = []
    # get live prices of VR stocks
    vr_live_prices = get_vr_price_live()
    #logging.debug(f'{vr_live_prices}')
    for stock in vr_live_prices[:]:
        #logging.debug(f'{stock.name}: {stock.pChange}')
        if abs(stock.pChange) > percentage:
            #print(stock.name)
            logging.debug(f'{stock.name}: {stock.pChange}')
            result.append(stock)
    logging.debug(f'VR results : {result}')

    # check 'NIFTY 50'
    nse = Nse()
    nifty_q = dict_to_stock_info(nse.get_index_quote(NIFTY))
    #StockInfo = namedtuple('StockInfo', 'name symbol lastPrice pChange dayLow dayHigh open')
    if abs(nifty_q.pChange) > percentage:
        logging.debug(f'Adding {nifty_q.name}: {nifty_q.pChange}')
        result.append(nifty_q)
    else:
        logging.debug(f'NIFTY change : {nifty_q.pChange}')

    return result

token_pre = 'xoxb-356641465604'
#Append the above to the below variable. Masking the token so that it does not get disabled.
token = token_pre + '-CDXc8LeJUx9woOaSrUY5ByCJ'

slack_client = SlackClient(token)
# Dictionary to keep track of alerts sent. If stock further drops drastically(drop of 3% more
# then we will send alert again else ignore the stock
alert_tracking = {}

def slack_message(message, channel):
    # Sends the direct response back to the channel
    slack_client.api_call('chat.postMessage', channel=channel,
                text=message, username="botuser",
                icon_emoji=':robot_face:')

def format_alert(stock_list):
    response = []
    for stock in stock_list:
        response.append(f'{"Symbol:":<15}{stock.name:<25}')
        response.append(f'{"Live price:":<15}{stock.lastPrice:<5}{"( ":<2}{stock.pChange:<1}{"%)":<2}')
    return '\n'.join(response)

if __name__ == "__main__":

    # create the logging instance for logging to file only
    logger = logging.getLogger('')

    # create the handler for the main logger
    file_logger = logging.FileHandler('slack_hourly.log')
    NEW_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
    file_logger_format = logging.Formatter(NEW_FORMAT)

    # tell the handler to use the above format
    file_logger.setFormatter(file_logger_format)

    # finally, add the handler to the base logger
    logger.addHandler(file_logger)

    # remember that by default, logging will start at 'warning' unless
    # we set it manually
    logger.setLevel(logging.DEBUG)


    tz    = timezone('Asia/Calcutta')
    current_time = datetime.now(tz)

    # This is just for testing
    prev_response = ''
    # Get stock which went up/down by 3%
    while True:
        current_time = datetime.now(tz)

        # Exit the script @ 4PM
        if current_time.hour > 15:
            sys.exit(0)

        stock_list = alert_below_percentage(3)
        new_alert_stock = []
        for stock in stock_list:
            #import pdb;pdb.set_trace()
            if stock.symbol not in alert_tracking.keys():
                new_alert_stock.append(stock)
                alert_tracking[stock.symbol] = stock
                #logging.debug(f'Adding {stock.name} to alert_tracking')
                logging.debug(f'Adding {stock.name} to alert_tracking')
            else:
                # if the stock fall 3 % more (i.e 6% now)
                # then send the alert again
                old_pchange = Decimal(alert_tracking[stock.symbol].pChange)
                new_pchange = Decimal(stock.pChange)
                diff_pchange = new_pchange - old_pchange

                #if abs(diff_pchange) >  abs(old_pchange):
                # if the stock has further fallen more than 2 % report.
                if abs(diff_pchange) > 2 :
                    logging.debug(f'pChange {stock.name} to alert_tracking')
                    logging.debug(f'Adding {stock.name} to alert_tracking')
                    new_alert_stock.append(stock)
        response = format_alert(new_alert_stock)
        logging.debug(f'Prev Alert was  : {prev_response}')
        logging.debug(f'New Alert which will  : {response}')
        prev_response = response
        if new_alert_stock:
            #slack_message(response, 'stock-alerts')
            logging.debug(f'response: {response}')
            slack_message(response, 'testing')

        logging.debug(f'Sleep for 15 min')
        sleep(60*15)
