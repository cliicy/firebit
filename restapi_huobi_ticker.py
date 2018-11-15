# -*- coding: utf-8 -*-

import time
from Utils import *
import os,time,sys,csv
import threading
from enums import PlatformDataType, Symbol, Platform
from sender import MqSender
# 获取 Market Detail 24小时成交量数据
def get_detail(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}

    url = "https://api.huobi.pro" + '/market/detail'
    return http_get_request(url, params)


def save_ticker_data(symbol,sender):
    
    try:
        data_folder = '/yanjiuyuan/data'
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


        json_result = get_detail(symbol=symbol)
        #print(json_result)
        if json_result and json_result['status'] == 'ok':

            if hasattr(sender,"s_conn"):
                sender.send(str(json_result))

            file_name = file_path + '/' + "ticker" + '_' + today_date + '.txt'
            # print (file_name)
            with open(file_name, 'a') as fw:
                fw.write(str(json_result) + '\n')

            csv_name = file_path + '/' + "ticker" + '_' + today_date + '.csv'
                #symbol = json_result["ch"].split('.')[1]
                # 转化为标准币对形式保存在csv
            symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,json_result["ch"].split('.')[1])
                #print(symbol)
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
        print(e)
        
            


if __name__ == '__main__':
    sender = MqSender("huobi", "ticker")
    symbol_list = ['ethusdt','btcusdt','bchusdt','ltcusdt','eosusdt','ethbtc','eosbtc','xrpusdt']
    #print (type())
    for symbol in symbol_list:
        save_ticker_data(symbol,sender)
        #print(get_detail(symbol))

