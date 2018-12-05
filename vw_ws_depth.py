# -*- coding: utf-8 -*-
from websocket import create_connection
import gzip
import time
import json
from common.enums import Symbol, Platform
from config.settings import depth_coll


def save_to_mongodb(data):
    try:
        # 把 下面的实时数据写入 Mongodb中
        # sym ts, depth, sell_price, sell_amt, buy_price, buy_amt
        # symbol
        # 货币对
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI, json_result["ch"].split('.')[1])
        ts = data['ts']
        bids = json_result['tick']['bids']
        asks = json_result['tick']['asks']
        ybdd = {}
        ybdd['sym'] = symbol
        small_len = len(bids)
        if small_len > len(asks):
            small_len = len(asks)
        for i in range(small_len):
            depth = i + 1
            sell_price = asks[i][0]
            sell_amt = asks[i][1]
            buy_price = bids[i][0]
            buy_amt = bids[i][1]
        if len(bids) > small_len:
            for j in range(small_len, len(bids)):
                depth = j + 1
                buy_price = bids[j][0]
                buy_amt = bids[j][1]
        if len(asks) > small_len:
            for k in range(small_len, len(asks)):
                depth = k + 1
                sell_price = asks[k][0]
                sell_amt = asks[k][1]
                # line = [symbol, ts, depth, sell_price, sell_amt, '', '']
                # write_lines.append(line)
        ybdd['depth'] = depth
        ybdd['ts'] = ts
        ybdd['buy_price'] = buy_price
        ybdd['buy_amt'] = buy_amt
        ybdd['sell_price'] = sell_price
        ybdd['sell_amt'] = sell_amt
        ybdd['api'] = 'depth'
        ybdd['exchange'] = 'huobi'
        depth_coll.insert(ybdd)
        # depth_coll.update({'sym': ybdd['sym'], 'exchange': ybdd['exchange'], 'depth': ybdd['depth']},
        #                   {'$set': {'buy_price': ybdd['buy_price'], 'buy_amt': ybdd['buy_amt'],
        #                             'sell_price': ybdd['sell_price'], 'sell_amt': ybdd['sell_amt'],
        #                             'sym': ybdd['sym'], 'exchange': ybdd['exchange'], 'api': 'ticker'}}, True)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    while True:
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except Exception as e:
            print('connect ws error,retry...', e)
            time.sleep(5)

    ethusdtStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""
    btcusdtStr="""{"sub": "market.btcusdt.depth.step5","id": "id10"}"""
    bchusdtStr="""{"sub": "market.bchusdt.depth.step5","id": "id10"}"""
    ltcusdtStr="""{"sub": "market.ltcusdt.depth.step5","id": "id10"}"""
    eosusdtStr="""{"sub": "market.eosusdt.depth.step5","id": "id10"}"""
    ethbtcStr="""{"sub": "market.ethbtc.depth.step5","id": "id10"}"""
    eosbtcStr="""{"sub": "market.eosbtc.depth.step5","id": "id10"}"""
    xrpusdtStr="""{"sub": "market.xrpusdt.depth.step5","id": "id10"}"""

    depth_topic = [ethusdtStr, btcusdtStr, bchusdtStr, ltcusdtStr, eosusdtStr, ethbtcStr,
                   eosbtcStr, xrpusdtStr]
    for topic in depth_topic:
        print(topic)
        ws.send(topic)
        print("sub success!")

    while True:
        try:
            compressData=ws.recv()
        # 判断字符串类型如果是str 则转换成 bytes
            if isinstance(compressData, str):
                compressData=compressData.encode(encoding="utf-8")
            result=gzip.decompress(compressData).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":'+ts+'}'
                ws.send(pong)
            else:
                if len(result) == 0:
                    continue
                json_result = json.loads(result)
                if 'status' in json_result:
                    continue
                else:
                    save_to_mongodb(json_result)
        except Exception as e:
            print(e)
            time.sleep(5)
            ws = create_connection("wss://api.huobipro.com/ws")
            for topic in depth_topic:
                print(topic)
                ws.send(topic)

