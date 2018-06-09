import os
import ZODB, ZODB.FileStorage
import BTrees.OOBTree
import transaction
import logging
from logging.config import fileConfig
from stocks import Stock

DB_PATH= os.path.dirname(os.path.realpath(__file__)) + '/db/mydata.fs'

from ZODB import FileStorage, DB
import transaction


class MyZODB(object):

    # singleton DB instance
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        # return if connection already set
        if  hasattr(self, "connection"):
            logging.debug(f'DB Object already exists. Return')
            return
        logging.debug('Creating a new db instance')
        self.storage = FileStorage.FileStorage(DB_PATH)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

    def close(self):
        self.db.close()

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
    fileConfig('logging.ini', disable_existing_loggers=True)
    logger = logging.getLogger()
    # print all the stocks in DB
    mydb = MyZODB()
    db_stock = mydb.dbroot.stocks
    print(f'items in db {len(mydb.dbroot.stocks.items())}')
    for item in mydb.dbroot.stocks:
        print (item)

    mydb.close()