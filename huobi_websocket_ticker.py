# -*- coding: utf-8 -*-
from websocket import create_connection
#from send_mail import *
import gzip
import time
import json
import sys,os,csv
import csv
import threading
from sender import MqSender
from common.enums import PlatformDataType, Symbol, Platform

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except Exception as e :
            print('connect ws error,retry...', e)
            time.sleep(5)

    # ethusdtStr="""{"sub": "market.ethusdt.ticker.detail", "id": "id10"}"""
    # btcusdtStr="""{"sub": "market.btcusdt.ticker.detail","id": "id10"}"""
    # bchusdtStr="""{"sub": "market.bchusdt.ticker.detail","id": "id10"}"""
    # ltcusdtStr="""{"sub": "market.ltcusdt.ticker.detail","id": "id10"}"""
    # eosusdtStr="""{"sub": "market.eosusdt.ticker.detail","id": "id10"}"""
    # ethbtcStr="""{"sub": "market.ethbtc.ticker.detail","id": "id10"}"""
    # eosbtcStr="""{"sub": "market.eosbtc.ticker.detail","id": "id10"}"""
    # xrpusdtStr="""{"sub": "market.xrpusdt.ticker.detail","id": "id10"}"""

    ethusdtStr = """{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""
    btcusdtStr = """{"sub": "market.btcusdt.trade.detail","id": "id10"}"""
    bchusdtStr = """{"sub": "market.bchusdt.trade.detail","id": "id10"}"""
    ltcusdtStr = """{"sub": "market.ltcusdt.trade.detail","id": "id10"}"""
    eosusdtStr = """{"sub": "market.eosusdt.trade.detail","id": "id10"}"""
    ethbtcStr = """{"sub": "market.ethbtc.trade.detail","id": "id10"}"""
    eosbtcStr = """{"sub": "market.eosbtc.trade.detail","id": "id10"}"""
    xrpusdtStr = """{"sub": "market.xrpusdt.trade.detail","id": "id10"}"""

    ticker_topic = [ethusdtStr, btcusdtStr, bchusdtStr, ltcusdtStr, eosusdtStr, ethbtcStr,
                    eosbtcStr, xrpusdtStr]
    for topic in ticker_topic:
        print(topic)
        ws.send(topic)
        print("sub success!")

    while 1:
        try:
            compressData=ws.recv()
            # 判断字符串类型如果是str 则转换成 bytes
            if isinstance(compressData,str):
                compressData=compressData.encode(encoding="utf-8")

            result=gzip.decompress(compressData).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":'+ts+'}'
                ws.send(pong)
            else:
                if len(result) == 0:
                    continue
                json_result=json.loads(result)
                if 'status' in json_result:
                    continue
                else:
                    print('返回的数据：', json_result)
                    print(json_result)
                    #send_to_mq(json_result)
                    #多线程处理，发送到mq 和 存储到txt，csv 流程并行执行
                    #threading.Thread(target=send_to_mq, args=([json_result])).start()
                    #threading.Thread(target=save_to_csv, args=([json_result])).start()
                    
                    # if hasattr(sender,"s_conn"):
                    #     sender.send(str(json_result))
                    # save_to_csv(json_result)
        except Exception as e:
            print(e)
            time.sleep(5)
            # ws = create_connection("wss://api.huobipro.com/ws")
            ws = create_connection("wss://api.huobi.br.com/ws")
            for topic in ticker_topic:
                print(topic)
                ws.send(topic)

