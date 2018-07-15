import BTrees.OOBTree
import logging
import os
import subprocess

import transaction
from ZODB import DB
from ZEO.ClientStorage import ClientStorage

from logging.config import fileConfig


DB_PATH= os.path.dirname(os.path.realpath(__file__)) + '/db/mydata.fs'

DB_PORT = 5555
SERVER = 'localhost'


def start_server():
    # use zeoctl
    zeo_cmd = f'runzeo -a {SERVER}:{DB_PORT} -f {DB_PATH}'
    status_cmd = ['zeoctl', '-p', zeo_cmd ,'status']
    start_cmd = ['zeoctl', '-p', zeo_cmd ,'start']
    logging.debug(f'Checking zeoctl status')
    if subprocess.run(status_cmd).returncode:
        # start the process
        logging.debug(f'Starting zeoctl process')
        if subprocess.run(start_cmd).returncode:
            raise Exception('Unable to start ZEO server')
        logging.debug(f'Successfully started zeoctl')

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

        # start the server if not started already
        start_server()

        server_and_port = (SERVER, DB_PORT)
        self.storage = ClientStorage(server_and_port)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()
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

    fileConfig('logging.ini', disable_existing_loggers=True)
    logger = logging.getLogger()
    # print all the stocks in DB
    mydb = MyZODB()
    db_stock = mydb.dbroot.stocks
    print(f'items in db {len(mydb.dbroot.stocks.items())}')
    for item in mydb.dbroot.stocks:
        print (item)

    mydb.close()