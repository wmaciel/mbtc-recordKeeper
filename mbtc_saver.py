import datetime
import mbtcapi
import time
from pymongo import MongoClient

CACHE_TIME = 61

def main():
    client = MongoClient()
    db = client['MBTC']
    quotes = db['quotes']

    last_book = {}

    while True:
        book = mbtcapi.getOrderBook('btc')
        last_book = book
        print book
        book['ts'] = datetime.datetime.utcnow()
        quotes.insert(book)

        time.sleep(CACHE_TIME)

if __name__ == "__main__":
    main()
