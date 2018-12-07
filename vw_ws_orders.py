# -*- coding: utf-8 -*-
from websocket import create_connection
import gzip
import time
import json
from common.enums import Symbol, Platform
from config.settings import detail_coll

ws_url = "wss://api.huobipro.com/ws/v1"
# ws_url = "wss://api.huobipro.com/ws"


def save_to_mongodb(data):
    print('save to mongodb: ', data)
    return
    try:
        # 把 下面的实时数据写入 Mongodb中
        # "amount": 24小时成交量,
        # "open": 前推24小时成交价,
        # "close": 当前成交价,
        # "high": 近24小时最高价,
        # "low": 近24小时最低价,
        # "count": 近24小时累积成交数,
        # "vol": 近24小时累积成交额, 即
        # sum(每一笔成交价 * 该笔的成交量)
        # sym ts, amount, open, close, high, low, count, vol, amount
        ybdd = {}
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,
                                                   json_result["ch"].split('.')[1])
        tdata = json_result['tick']
        amount = tdata['amount']
        open = tdata['open']
        price = tdata['close']   # "close": 当前成交价 也就是最新价
        high = tdata['high']
        low = tdata['low']
        vol = tdata['vol']
        # 涨跌幅 最新成交价 - 24小时前成交价 / 24小时前成交价
        ff = (price - open) / open * 100
        delta = ('%.2f' % ff)
        ybdd['Change'] = '{0}{1}'.format(delta, '%')
        ybdd['sym'] = symbol
        ybdd['amount'] = amount
        ybdd['Price'] = price
        ybdd['High'] = high
        ybdd['Low'] = low
        ybdd['Volume'] = vol
        ybdd['api'] = 'ticker'
        ybdd['exchange'] = 'huobi'
        detail_coll.update({'sym': ybdd['sym'], 'exchange': ybdd['exchange']},
                           {'$set': {'Change': ybdd['Change'], 'Volume': ybdd['Volume'],
                                     'amount': ybdd['amount'], 'Price': ybdd['Price'],
                                     'High': ybdd['High'], 'Low': ybdd['Low'], 'api': 'ticker'}}, True)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(ws_url)
            break
        except Exception as e:
            print('connect ws error,retry...', e)
            time.sleep(5)
    # btcusdtStr = """{"sub": "orders.btcusdt"}"""
    btcusdtStr = """{"op": "sub" ,"topic": "orders.btcusdt"}"""
    # btcusdtStr = """{"op": "req" ,  "cid": "40sG903yz86oDFWr", "topic": "accounts.list"}"""
    # btcusdtStr = """{"op": "sub" ,  "cid": "40sG903yz86oDFWr", "topic": "orders.htusdt"}"""
    # ethusdtStr = """{"sub": "market.ethusdt.detail", "id8": "id10"}"""
    # btcusdtStr = """{"sub": "market.btcusdt.detail","id8": "id10"}"""
    # etcusdtStr = """{"sub": "market.etcusdt.detail","id8": "id10"}"""
    # bchusdtStr = """{"sub": "market.bchusdt.detail","id8": "id10"}"""
    # ltcusdtStr = """{"sub": "market.ltcusdt.detail","id8": "id10"}"""
    # eosusdtStr = """{"sub": "market.eosusdt.detail","id8": "id10"}"""
    # ethbtcStr = """{"sub": "market.ethbtc.detail","id8": "id10"}"""
    # eosbtcStr = """{"sub": "market.eosbtc.detail","id8": "id10"}"""
    # xrpusdtStr = """{"sub": "market.xrpusdt.detail","id8": "id10"}"""

    detail_topic = [btcusdtStr]

    # detail_topic = [ethusdtStr, btcusdtStr, etcusdtStr, bchusdtStr, ltcusdtStr, eosusdtStr, ethbtcStr,
    #                 eosbtcStr, xrpusdtStr]

    for topic in detail_topic:
        # print(topic)
        ws.send(topic)
        # print("sub success!")

    while True:
        try:
            compressData=ws.recv()
        # 判断字符串类型如果是str 则转换成 bytes
            if isinstance(compressData, str):
                compressData = compressData.encode(encoding="utf-8")
            result = gzip.decompress(compressData).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":'+ts+'}'
                ws.send(pong)
            else:
                if len(result) == 0:
                    continue
                ret = json.loads(result)
                print(ret)
                if 'status' in ret:
                    continue
                else:
                    save_to_mongodb(ret)
        except Exception as e:
            print(e)
            time.sleep(5)
            ws = create_connection(ws_url)
            for topic in detail_topic:
                print(topic)
                ws.send(topic)

