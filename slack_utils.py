'''

Interface which can be called directly by Slack users
Here ideally we should be getting response from functions in utils.py
format them and then return.

'''
import logging

from tabulate import tabulate
from logging.config import fileConfig
from utils import check_vr_reco, min_max_reco_date, get_live_price, alert_below_percentage, get_vr_stocks_live_util

#TODO: use decorator to catch exceptions
def get_quotes(symbol):
    '''

    :param symbol:
    :return:  info about stock symbol
    '''
    #check VR stock or not
    try:
        stock = check_vr_reco(symbol)
        logging.debug(f'{symbol}: stock obj {stock}')
        info = get_live_price(symbol)
        data = [[info.name],
                ["LastPrice:", info.lastPrice, info.pChange],
                ["Day Low:", info.dayLow],
                ["Day High:", info.dayHigh],
                ["Day Open:", info.open],
                ]
        logging.debug(str(data))
        if stock:
            # stock recommended in VR, get reco price and other details
            result = min_max_reco_date(symbol)
            print(result[1])
            _, vr_reco_date, vr_reco_price, vr_min, vr_max = result[1].split(';')
            data.append(["VR Reco Date:", vr_reco_date]),
            data.append(["VR Reco Price:", vr_reco_price])
            data.append(["VR Min:", vr_min])
            data.append(  ["VR Max:", vr_max])
        ret = tabulate(data, tablefmt="simple", headers="firstrow")# numalign="left")
        logging.debug(ret)
        return ret
    except IndexError as err:
        logging.debug(str(err))
        return 'IndexError'

def get_performance(symbol):
    '''

    :param symbol:
    :return: stock parameters from the reco-date
        1. High  it attained
        2. Low it attained
        3. Performance as per current price
    '''
    #TODO should be done by slack.py
    symbol = symbol.upper()
    try:
        if(check_vr_reco(symbol) is None):
            return 'Not a VR recommendation'

        result = min_max_reco_date(symbol)
        info = get_live_price(symbol)
        _, vr_reco_date, vr_reco_price, vr_min, vr_max = result[1].split(';')
        response = [[info.name],
                    ["CurrentPrice:", info.lastPrice, info.pChange],
                    ["Vr Reco Date:", vr_reco_date],
                    ["VR Reco Price:", vr_reco_price],
                    ["VR Max:", vr_max],
                    ["VR Min:", vr_min]
                    ]
        perf = ((info.lastPrice - float(vr_reco_price)) / float(vr_reco_price)) * 100
        response.append(["Performance:",round(perf,2) ])
        ret = tabulate(response, tablefmt="simple", headers="firstrow")
        return ret
    except IndexError:
        return 'TBA'

def get_vr_stocks_below(percentage):
    '''

    :param percentange:
    :return:
       All stocks making loss or profits above percentage provided
    '''
    response = []
    for symbol in alert_below_percentage(int(percentage)):
        slist = symbol.split(';')
        logging.debug(f'{symbol}')
        response.append(f'{"Symbol:":<15}{slist[0]:<25}')
        response.append(f'{"Live price:":<15}{slist[2]:<25}')
        response.append(f'{"Reco price:":<15}{slist[1]:<25}')
        percent = ((float(slist[2]) - float(slist[1])) / float(slist[1])) * 100
        response.append(f'{"% change:":<15}{round(percent, 2):<5}%')
        response.append(f'{""}')
    return '\n'.join(response)

def get_vr_stocks_live():
    '''

    :param percentange:
    :return:
       All stocks making loss or profits above percentage provided
    '''
    data = []
    logging.debug(f'Calling test')
    for symbol in get_vr_stocks_live_util():
        slist = symbol.split(';')
        logging.debug(f'{symbol}')
        data.append([slist[0], "Current:", "{0}({1}%)".format(slist[2].rstrip(), slist[3].rstrip()), "RecoP:", slist[1]])
        #response.append(f'{slist[0]:<25}CurP: {slist[2]:<10}({slist[3]}%) RecoP:  {slist[1]:<25}')
    ret = tabulate(data, tablefmt="simple", numalign="left")# numalign="left")
    logging.debug(ret)
    return ret

if __name__ == '__main__':
    fileConfig('logging.ini', disable_existing_loggers=True)
    logger = logging.getLogger()
    res = get_quotes("INDIGO")
    logging.debug("get quotes %s" % str(res))
