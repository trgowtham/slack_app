import persistent

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



def get_stocks():
    '''
    return all timely or all-weather stocks
    :param type:
    :return:
    '''
    from db_utils import MyZODB
    mydb = MyZODB()
    print(f"Total Recommended stocks : {len(mydb.dbroot.stocks)}")
    for stock in mydb.dbroot.stocks:
        print(repr(stock))

    return mydb.dbroot.stocks


if __name__ == '__main__':
    get_stocks()