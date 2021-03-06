from pymongo import MongoClient
symbol_list = ['ethusdt', 'btcusdt', 'bchusdt', 'ltcusdt', 'eosusdt', 'ethbtc', 'eosbtc', 'xrpusdt']
period = ['1min', '5min', '15min', '30min', '60min', '4hour', '1day', '1week', '1mon']
orders_list = ['submitted', 'partial-filled', 'partial-canceled', 'filled', 'canceled']

mdb = {
    "host": '172.24.132.208',
    # "host": '51facai.51vip.biz',
    "user": 'data',
    "password": 'data123',
    "db": 'invest',
    "port": '27017',
    # "port": '16538',
    "marketP1": 'dw_market',
    "M5": 'dw_M5',
    "M15": 'dw_M15',
    "M30": 'dw_M30',
    "D1": 'dw_D1',
    "H1": 'dw_H1',
    "H4": 'dw_H4',
    "W1": 'dw_W1',
    "M1": 'dw_M1',
    "Y1": 'dw_Y1',
    "MON1": 'dw_MON1',
    "depth": 'dw_depth',
    "acc": 'accounts',
    "bal": 'balance',
    "orders": 'orders',
    "market_detail": 'dw_ticker_detail',
    "future": 'ok_future'
}

mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
ticker_coll = sdb[mdb["marketP1"]]
dwM1_coll = sdb[mdb["M1"]]
dwM5_coll = sdb[mdb["M5"]]
dwD1_coll = sdb[mdb["D1"]]
dwH1_coll = sdb[mdb["H1"]]
dwW1_coll = sdb[mdb["W1"]]
future_kline_coll = sdb[mdb["future"]]
depth_coll = sdb[mdb["depth"]]
detail_coll = sdb[mdb["market_detail"]]
acc_coll = sdb[mdb["acc"]]
balance_coll = sdb[mdb["bal"]]
orders_coll = sdb[mdb["orders"]]

