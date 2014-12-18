import datetime
import mbtcapi
import time
from pymongo import MongoClient

CACHE_TIME = 61
QUOTES_COLLECTION = 'quotes'
TRADES_COLLECTION = 'trades'
COIN = 'btc'


def process_book(db):
    quotes = db[QUOTES_COLLECTION]
    book = mbtcapi.getOrderBook(COIN)
    book['ts'] = datetime.datetime.utcnow()
    quotes.insert(book)


def process_trades(db):
    trades_col = db[TRADES_COLLECTION]
    trades = mbtcapi.getTrades(COIN)
    for trade in trades:
        trades_col.update({'tid':trade['tid']}, trade, upsert=True)


def main():
    client = MongoClient()
    db = client['MBTC']

    while True:
        process_book(db)
        process_trades(db)
        time.sleep(CACHE_TIME)


if __name__ == "__main__":
    main()
