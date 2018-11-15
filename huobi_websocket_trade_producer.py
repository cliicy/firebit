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
from enums import PlatformDataType, Symbol, Platform
#将消息发送到mq
def send_to_mq(msg):
    try:
        #print("send_to_mq start time: ")
        #print(time.strftime("%Y%m%d %H:%M:%S"))
        sender.send(str(msg))
        #print("ok")

    except Exception as e:
        print(str(e))

#将消息解析保存到txt，csv
def save_to_csv(json_result):
    try:
        #print("save_to_csv start time: ")
        #print(time.strftime("%Y%m%d %H:%M:%S"))
        #json_result = eval(json_result)
        data_folder = '/yanjiuyuan/data'
        today_date = time.strftime("%Y%m%d")
        file_path = os.path.join(data_folder, today_date, "huobi", "trader")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            csv_name = file_path + '/' + "trader" + '_' + today_date + '.csv'
            with open(csv_name, "a", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['symbol', 'id', 'ts', 'direction', 'amount', 'price'])

        file_name = file_path + '/' + "trader" + '_' + today_date + '.txt'
        # print (file_name)
        with open(file_name, 'a') as fw:
            fw.write(result + '\n')
        csv_name = file_path + '/' + "trader" + '_' + today_date + '.csv'
        # 转化为标准币对形式保存在csv
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,json_result["ch"].split('.')[1])
        # print(symbol)
        tick_data = json_result['tick']['data']
        write_lines = []
        for trade in tick_data:
            write_lines.append([
                symbol,
                trade['id'],
                trade['ts'],
                trade['direction'],
                trade['amount'],
                trade['price']
            ])

        with open(csv_name, "a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for line in write_lines:
                csv_writer.writerow(line)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    sender = MqSender("huobi", "trade")
    while(1):
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    ethusdtStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""
    btcusdtStr="""{"sub": "market.btcusdt.trade.detail","id": "id10"}"""
    bchusdtStr="""{"sub": "market.bchusdt.trade.detail","id": "id10"}"""
    ltcusdtStr="""{"sub": "market.ltcusdt.trade.detail","id": "id10"}"""
    eosusdtStr="""{"sub": "market.eosusdt.trade.detail","id": "id10"}"""
    ethbtcStr="""{"sub": "market.ethbtc.trade.detail","id": "id10"}"""
    eosbtcStr="""{"sub": "market.eosbtc.trade.detail","id": "id10"}"""
    xrpusdtStr="""{"sub": "market.xrpusdt.trade.detail","id": "id10"}"""
    #订阅 Trade Detail 数据
    #tradeStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Trade Detail 数据
    # tradeStr="""{"req": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Market Detail 数据
    #tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""
    trade_topic = [ethusdtStr,btcusdtStr,bchusdtStr,ltcusdtStr,eosusdtStr,ethbtcStr,eosbtcStr,xrpusdtStr]
    for topic in trade_topic:
        print(topic)
        ws.send(topic)
        print("sub success!")

    while (1):
        try:
            compressData=ws.recv()
        #判断字符串类型如果是str 则转换成 bytes
            if isinstance(compressData,str):
                compressData=compressData.encode(encoding="utf-8")

            result=gzip.decompress(compressData).decode('utf-8')
            #print(result)
            if result[:7] == '{"ping"':
                ts=result[8:21]
                pong='{"pong":'+ts+'}'
                ws.send(pong)
            #ws.send(tradeStr)
            else:
                if len(result) == 0:
                    continue
                #print(result)
                json_result=json.loads(result)
                if 'status' in json_result:
                    continue
                else:
                    #print(json_result)
                    #send_to_mq(json_result)
                    #多线程处理，发送到mq 和 存储到txt，csv 流程并行执行
                    #threading.Thread(target=send_to_mq, args=([json_result])).start()
                    #threading.Thread(target=save_to_csv, args=([json_result])).start()
                    
                    if hasattr(sender,"s_conn"):
                        sender.send(str(json_result))
                    save_to_csv(json_result)

        except Exception as e:
            print(e)
            sender.close()
            #send_mail( "market_kline program error" + str(e))
            time.sleep(5)
            ws = create_connection("wss://api.huobipro.com/ws")
            for topic in trade_topic:
                print(topic)
                ws.send(topic)

