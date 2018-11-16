#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Utils import *
import os, time, sys, csv
import threading
from sender import MqSender
from common.enums import PlatformDataType, Symbol, Platform

# 获取 Market Detail 24小时成交量数据
def get_detail(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)



#将消息发送到mq
# def send_to_mq(msg):
#     try:
#         #print("send_to_mq start time: ")
#         #print(time.strftime("%Y%m%d %H:%M:%S"))
#         sender.send(str(msg))
#         #print("ok")
#
#     except Exception as e:
#         print(str(e))

def save_to_csv(json_result):
    try:
        data_folder = 'D:\\huobi_download'
        today_date = time.strftime("%Y%m%d")
        file_path = os.path.join(data_folder, today_date, "huobi", "ticker")

        if not os.path.exists(file_path):
            os.makedirs(file_path)
            csv_name = file_path + '/' + "ticker" + '_' + today_date + '.csv'
            with open(csv_name, "a", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['symbol',
                                     'ts',
                                     'latest_price',
                                     'latest_amount',
                                     'max_buy1_price',
                                     'max_buy1_amt',
                                     'min_sell1_price',
                                     'min_sell1_amt',
                                     'pre_24h_price',
                                     'pre_24h_price_max',
                                     'pre_24h_price_min',
                                     'pre_24h_bt_finish_amt',
                                     'pre_24h_usd_finish_amt'])
        file_name = file_path + '/' + "ticker" + '_' + today_date + '.txt'
        # print (file_name)
        with open(file_name, 'a') as fw:
            fw.write(str(json_result) + '\n')

        csv_name = file_path + '/' + "ticker" + '_' + today_date + '.csv'
        # 转化为标准币对形式保存在csv
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,json_result["ch"].split('.')[1])
        print(symbol)
        ts = json_result['ts']
        with open(csv_name, "a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([symbol,
                                 ts,
                                 '',
                                 '',
                                 '',
                                 '',
                                 '',
                                 '',
                                 json_result['tick']['open'],
                                 json_result['tick']['high'],
                                 json_result['tick']['low'],
                                 json_result['tick']['amount'],
                                 json_result['tick']['vol']])

    except Exception as e:
        print(str(e))


def save_ticker_data(symbol,):
    while True:
        try:

            json_result = get_detail(symbol=symbol)

            if json_result and json_result['status'] == 'ok':
                #sender.send(str(json_result))
                print(json_result)
                # 多线程处理，发送到mq 和 存储到txt，csv 流程并行执行
                #threading.Thread(target=send_to_mq, args=([json_result])).start()
                threading.Thread(target=save_to_csv, args=([json_result])).start()
                save_to_csv(json_result)

        except Exception as e:
            print(e)
            #sender.close()
            continue


if __name__ == '__main__':
    # kline
    # print (get_kline(symbol='btcusdt',period='1min',size=10))
    # market detail merged
    # print(get_ticker(symbol='btcusdt'))
    # market ticker
    # print(get_market_ticker())
    # market depth
    # print(get_depth(symbol='btcusdt',type='step5'))
    # market trade
    # print(get_trade(symbol='btcusdt'))
    # 获取 Market Detail 24小时成交量数据

    #sender = MqSender("huobi", "ticker")
    symbol_list = ['ethusdt',
                   'btcusdt',
                   'bchusdt',
                   'ltcusdt',
                   'eosusdt',
                   'ethbtc',
                   'eosbtc']

    # print (type())
    for symbol in symbol_list:
        threading.Thread(target=save_ticker_data, args=(symbol,)).start()

