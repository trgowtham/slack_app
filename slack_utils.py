'''

Interface which can be called directly by Slack users
Here ideally we should be getting response from functions in utils.py
format them and then return.

'''
import logging
from logging.config import fileConfig
from utils import check_vr_reco, min_max_reco_date, get_live_price, reco_percent, alert_below_percentage

#TODO use a separate formatting class to do formatting takes a list as input and gives
# proper formatted output
#TODO: use decorator to catch exceptions

def get_quotes(symbol):
    '''

    :param symbol:
    :return:  info about stock symbol
    '''
    #check VR stock or not
    try:
        stock = check_vr_reco(symbol)
        info = get_live_price(symbol)
        response = []
        response.append(f'{info.name:^}')
        response.append(f'{"LastPrice:":<25}{str(info.lastPrice).strip():<25}')#({info.pChange:<12}%)')
        response.append(f'{"Day Low:":<24} {str(info.dayLow).strip():<24}')
        response.append(f'{"Day High:":<24} {info.dayHigh:<24}')
        response.append(f'{"Day Open:":<25}{info.open:<25}')
        if stock:
            # stock recommended in VR, get reco price and other details
            result = min_max_reco_date(symbol)
            print(result[1])
            _ , vr_reco_date, vr_reco_price, vr_min, vr_max = result[1].split(';')
            response.append(f'{"Vr Reco Date:":<25}{vr_reco_date:<25}')
            response.append(f'{"VR Reco Price:":<25}{vr_reco_price:<25}')
            response.append(f'{"VR Min:":<25}{vr_min:<25}')
        return '\n'.join(response)
    except IndexError as err:
        return 'IndexError'

def get_performance(symbol):
    '''

    :param symbol:
    :return: stock parameters from the reco-date
        1. High  it attained
        2. Low it attained
        3. Performance as per current price
    '''
    try:
        if(check_vr_reco(symbol) is None):
            return 'Not a VR recommendation'

        result = min_max_reco_date(symbol)
        info = get_live_price(symbol)
        response = []
        response.append(f'{info.name:^}')
        response.append(f'{"CurrentPrice:":<25}{str(info.lastPrice).strip():<25}({info.pChange:<12}%)')
        print(result[1])
        _ , vr_reco_date, vr_reco_price, vr_min, vr_max = result[1].split(';')
        response.append(f'{"Vr Reco Date:":<25}{vr_reco_date:<25}')
        response.append(f'{"VR Reco Price:":<25}{vr_reco_price:<25}')
        response.append(f'{"VR Max:":<25}{vr_max:<25}')
        response.append(f'{"VR Min:":<25}{vr_min:<25}')
        perf = ((info.lastPrice - float(vr_reco_price)) / float(vr_reco_price)) * 100
        print(perf)
        response.append(f'{"Performance:":<25}{round(perf,2):<5}%')
        return '\n'.join(response)

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


if __name__ == '__main__':
    fileConfig('logging.ini', disable_existing_loggers=True)
    logger = logging.getLogger()
    res = get_quotes("INDIGO")
    logging.debug("get quotes %s" % str(res))
