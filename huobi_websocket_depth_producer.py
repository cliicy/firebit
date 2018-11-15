# -*- coding: utf-8 -*-
from websocket import create_connection
import gzip
import time
import json
import sys,os,csv,threading
#from send_mail import *
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

def save_to_csv(json_result):
    try:
        data_folder = '/yanjiuyuan/data'
        today_date = time.strftime("%Y%m%d")
        file_path = os.path.join(data_folder, today_date, "huobi", "depth")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            csv_name = file_path + '/' + "depth" + '_' + today_date + '.csv'
            with open(csv_name, "a", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(
                    ['symbol', 'ts', 'depth', 'sell_price', 'sell_amt', 'buy_price', 'buy_amt'])

        file_name = file_path + '/' + "depth" + '_' + today_date + '.txt'
        # print (file_name)
        with open(file_name, 'a') as fw:
            fw.write(result + '\n')
        csv_name = file_path + '/' + "depth" + '_' + today_date + '.csv'
        # 转化为标准币对形式保存在csv
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,json_result["ch"].split('.')[1])
        ts = json_result['ts']
        write_lines = []
        bids = json_result['tick']['bids']
        # print (len(bids))
        asks = json_result['tick']['asks']
        # print(len(asks))
        small_len = len(bids)
        if small_len > len(asks):
            small_len = len(asks)
        for i in range(small_len):
            depth = i + 1
            sell_price = asks[i][0]
            sell_amt = asks[i][1]
            buy_price = bids[i][0]
            buy_amt = bids[i][1]
            line = [symbol, ts, depth, sell_price, sell_amt, buy_price, buy_amt]
            write_lines.append(line)
        if len(bids) > small_len:
            for j in range(small_len, len(bids)):
                depth = j + 1
                buy_price = bids[j][0]
                buy_amt = bids[j][1]
                line = [symbol, ts, depth, '', '', buy_price, buy_amt]
                write_lines.append(line)
        if len(asks) > small_len:
            for k in range(small_len, len(asks)):
                depth = k + 1
                sell_price = asks[k][0]
                sell_amt = asks[k][1]
                line = [symbol, ts, depth, sell_price, sell_amt, '', '']
                write_lines.append(line)

        with open(csv_name, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for write_line in write_lines:
                csv_writer.writerow(write_line)

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    sender = MqSender("huobi", "depth")

    while(1):
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    #tradeStr="""{"sub": "market.ethusdt.kline.1min","id": "id10"}"""

    #请求 KLine 数据
    #tradeStr="""{"req": "market.ethusdt.kline.15min","id": "id10"}"""
    #tradeStr = """{"req": "market.ethusdt.kline.1min","id": "id10"}"""
    #订阅 Market Depth 数据
    ethusdtStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""
    btcusdtStr="""{"sub": "market.btcusdt.depth.step5","id": "id10"}"""
    bchusdtStr="""{"sub": "market.bchusdt.depth.step5","id": "id10"}"""
    ltcusdtStr="""{"sub": "market.ltcusdt.depth.step5","id": "id10"}"""
    eosusdtStr="""{"sub": "market.eosusdt.depth.step5","id": "id10"}"""
    ethbtcStr="""{"sub": "market.ethbtc.depth.step5","id": "id10"}"""
    eosbtcStr="""{"sub": "market.eosbtc.depth.step5","id": "id10"}"""
    xrpusdtStr="""{"sub": "market.xrpusdt.depth.step5","id": "id10"}"""
    #请求 Market Depth 数据
    #tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

    #订阅 Trade Detail 数据
    #tradeStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Trade Detail 数据
    # tradeStr="""{"req": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Market Detail 数据
    #tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""
    depth_topic = [ethusdtStr,btcusdtStr,bchusdtStr,ltcusdtStr,eosusdtStr,ethbtcStr,eosbtcStr,xrpusdtStr]
    for topic in depth_topic:
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
                    if hasattr(sender,"s_conn"):
                        sender.send(str(json_result))
                    # 多线程处理，发送到mq 和 存储到txt，csv 流程并行执行
                    #threading.Thread(target=send_to_mq, args=([json_result])).start()
                    #threading.Thread(target=save_to_csv, args=([json_result])).start()
                    save_to_csv(json_result)


        except Exception as e:
            print(e)
            sender.close()
            time.sleep(5)
            #send_mail( "market_depth program error" + str(e))
            ws = create_connection("wss://api.huobipro.com/ws")
            for topic in depth_topic:
                print(topic)
                ws.send(topic)

