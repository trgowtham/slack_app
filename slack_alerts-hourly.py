import logging
import sys

from logging.config import fileConfig
from slackclient import SlackClient
from utils import get_vr_price_live, StockInfo
from time import sleep
from decimal import Decimal
from datetime import datetime
from pytz import timezone


def alert_below_percentage(percentage):
    '''
    :param percentage: how much lower the value has gone
    :return: list of StockInfo objects
    '''
    logging.debug(f' Getting stocks below {percentage} %')
    result = []
    # get live prices
    vr_live_prices = get_vr_price_live()
    #logging.debug(f'{vr_live_prices}')
    for stock in vr_live_prices[:]:
        #logging.debug(f'{stock.name}: {stock.pChange}')
        if abs(stock.pChange) > percentage:
            #print(stock.name)
            logging.debug(f'{stock.name}: {stock.pChange}')
            result.append(stock)
    logging.debug(f'{result}')
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
    fileConfig('logging.ini')
    logger = logging.getLogger()
    lhStdout = logger.handlers[0]

    fileHandler = logging.FileHandler('slack_hourly.log')
    logger.addHandler(fileHandler)
    logger.removeHandler(lhStdout)
    tz    = timezone('Asia/Calcutta')
    current_time = datetime.now(tz)

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
                print(f'Adding {stock.name} to alert_tracking')
            else:
                # if the stock fall 3 % more (i.e 6% now)
                # then send the alert again
                old_pchange = Decimal(alert_tracking[stock.symbol].pChange)
                new_pchange = Decimal(stock.pChange)
                diff_pchange = new_pchange - old_pchange

                if abs(diff_pchange) >  abs(old_pchange):
                    logging.debug(f'pChange {stock.name} to alert_tracking')
                    logging.debug(f'Adding {stock.name} to alert_tracking')
                    new_alert_stock.append(stock)
        print(new_alert_stock)
        response = format_alert(new_alert_stock)
        #slack_message(response, 'stock-alerts')
        slack_message(response, 'testing')
        logging.debug(f'Sleep for 20 min')
        sleep(60*20)