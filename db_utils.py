import os
import ZODB, ZODB.FileStorage
import BTrees.OOBTree
import transaction

from stocks import Stock

DB_PATH= os.path.dirname(os.path.realpath(__file__)) + '/db/mydata.fs'

from ZODB import FileStorage, DB
import transaction


class MyZODB(object):
    def __init__(self):
        self.storage = FileStorage.FileStorage(DB_PATH)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

    def close(self):
        self.connection.close()
        self.db.close()
        self.storage.close()

def create_db():
    #One time action of creating and DB and other actions
    mydb = MyZODB()
    # create for stocks placeholder for storing all Stock objects
    mydb.dbroot.stocks = BTrees.OOBTree.BTree()
    #TODO create for person
    # commit and close
    transaction.commit()
    mydb.close()

if __name__ == '__main__':
    'create db and check '
    create_db()
    import sys;sys.exit(0)
    # #check and print
    mydb = MyZODB()
    print(mydb.dbroot.items())
    st = Stock('name', 'type', 'symbol', 'reco_date', 'reco_date_price', 'risk_score')
    st1 = Stock('name', 'type', 'symbol1', 'reco_date', 'reco_date_price', 'risk_score')
    db_stock = mydb.dbroot.stocks
    for stock in [st, st1]:
        if stock.symbol not in db_stock:
            db_stock[stock.symbol] = stock
        else:
            print(f'Not adding {st.symbol}')
    transaction.commit()
    print(mydb.dbroot)
    print(type(mydb.dbroot.stocks))
    print(f'items in db {len(mydb.dbroot.stocks.items())}')
    for item in mydb.dbroot.stocks:
        print (item)
    mydb.close()
