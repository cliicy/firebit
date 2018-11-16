# -*- coding: utf-8 -*-
from websocket import create_connection
import gzip
import time
import json,csv
import sys, os
import threading
from sender import MqSender
import operator as op
from common.enums import PlatformDataType, Symbol, Platform
#from send_mail import *

#将消息发送到mq
def send_to_mq(msg):
    try:
        #print("send_to_mq start time: ")
        #print(time.strftime("%Y%m%d %H:%M:%S"))
        sender.send(str(msg))
        #print("ok")

    except Exception as e:
        print(str(e))

def save_to_csv(json_result):
    try:
        data_folder = '/yanjiuyuan/data'
        today_date = time.strftime("%Y%m%d")
        file_path = os.path.join(data_folder, today_date, "huobi", "kline")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            csv_name = file_path + '/' + "kline" + '_' + today_date + '.csv'
            with open(csv_name, "a", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(
                    ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'hight', 'amount', 'vol',
                     'count'])

        file_name = file_path + '/' + "kline" + '_' + today_date + '.txt'
        # print (file_name)
        with open(file_name, 'a') as fw:
            fw.write(str(json_result) + '\n')
        # 转化为标准币对形式保存在csv
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,json_result["ch"].split('.')[1])

        line = [symbol,
                json_result['ts'],
                '1m',
                json_result['tick']['id'],
                json_result['tick']['open'],
                json_result['tick']['close'],
                json_result['tick']['low'],
                json_result['tick']['high'],
                json_result['tick']['amount'],
                json_result['tick']['vol'],
                json_result['tick']['count']
                ]

        # 如果 dict 为空 则插入
        if not write_dict:
            write_dict[symbol] = line

        if symbol not in write_dict:
            write_dict[symbol] = line

        else:
            # 如果symbol 在 dict 中 比较 新来的数据 id 与字典中的 id是否相同 相同则更新字典中的key，如果不同的话 将字典中的key数据 写入到CSV，最新的数据更新字典中的key，继续比较。
            if op.eq(line[3], write_dict[symbol][3]):
                write_dict[symbol] = line

            if op.gt(line[3], write_dict[symbol][3]):
                csv_name = file_path + '/' + "kline" + '_' + today_date + '.csv'
                with open(csv_name, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(write_dict[symbol])
                write_dict[symbol] = line


    except Exception as e:
        print(str(e))
if __name__ == '__main__':


    sender = MqSender("1","kline")

    # 订阅 ethusdt KLine 数据
    ethusdtStr = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""
    # 订阅 btcusdt Kline 数据
    btcusdtStr = """{"sub": "market.btcusdt.kline.1min","id": "id10"}"""
    # 订阅 bchusdt Kline 数据
    bchusdtStr = """{"sub": "market.bchusdt.kline.1min","id": "id10"}"""
    # 订阅 ltcusdt Kline 数据
    ltcusdtStr = """{"sub": "market.ltcusdt.kline.1min","id": "id10"}"""
    # 订阅 eosusdt Kline 数据
    eosusdtStr = """{"sub": "market.eosusdt.kline.1min","id": "id10"}"""
    # 订阅 ethbtc Kline 数据
    ethbtcStr = """{"sub": "market.ethbtc.kline.1min","id": "id10"}"""
    # 订阅 eosbtc Kline 数据
    eosbtcStr = """{"sub": "market.eosbtc.kline.1min","id": "id10"}"""

    xrpusdtStr = """{"sub": "market.xrpusdt.kline.1min","id": "id10"}"""

    kline_topic = [ethusdtStr,btcusdtStr,bchusdtStr,ltcusdtStr,eosusdtStr,ethbtcStr,eosbtcStr,xrpusdtStr]
    #kline_topic = [btcusdtStr]
    write_dict = {}


    while (1):
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    for sub_str in kline_topic:
        ws.send(sub_str)
        print(sub_str)
        print("sub success!")

    while (1):
        try:
            compressData = ws.recv()
            # 判断字符串类型如果是str 则转换成 bytes
            if isinstance(compressData, str):
                compressData = compressData.encode(encoding="utf-8")

            result = gzip.decompress(compressData).decode('utf-8')
            # print(result)
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":' + ts + '}'
                ws.send(pong)
            # ws.send(tradeStr)
            else:
                if len(result) == 0:
                    continue
                # print(result)
                json_result = json.loads(result)
                if 'status' in json_result:
                    continue
                else:
                    # 多线程处理，发送到mq 和 存储到txt，csv 流程并行执行
                    #threading.Thread(target=send_to_mq, args=([json_result])).start()
                    #threading.Thread(target=save_to_csv, args=([json_result])).start()
                    if hasattr(sender,"s_conn"):
                        sender.send(str(json_result))
                    save_to_csv(json_result)






        except Exception as e:
            print(e)
            # send_mail("market_kline program error" + str(e))
            sender.close()
            time.sleep(5)
            write_dict = {}

            ws = create_connection("wss://api.huobipro.com/ws")
            for sub_str in kline_topic:
                ws.send(sub_str)
                print(sub_str)
                print("sub success!")


