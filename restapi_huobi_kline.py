# -*- coding: utf-8 -*-

import time,json,os,csv
from Utils import *
import datetime
from enums import PlatformDataType, Symbol, Platform



def job():
    print("I'm working...")

# 获取KLine
def get_kline(symbol, period='1min', size=2000):
    """
    :param symbol
    :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: 可选值： [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)



def save_to_csv(symbol):
    # 今天日期
    today = datetime.date.today()
    #print(today)
    # 昨天时间
    yesterday = today - datetime.timedelta(days=1)
    #print(yesterday.strftime("%Y%m%d"))

    # 昨天开始时间戳
    yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
    #print(yesterday_start_time)
    # 昨天结束时间戳
    yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
    #print(yesterday_end_time)

    data_folder = '/yanjiuyuan/code/huobi/kline_data'

    yesterday_date = yesterday.strftime("%Y%m%d")
    file_path = os.path.join(data_folder, yesterday_date, "huobi", "kline")
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        csv_name = file_path + '/' + "kline" + '_' + yesterday_date + '.csv'
        with open(csv_name, "a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(
                ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol',
                 'count'])

    r_lest = []
    try:
        result = get_kline(symbol)

        if result["status"] == "ok":
            json_result = result["data"]

            for item in json_result:
                if item["id"] >= yesterday_start_time and item["id"] <= yesterday_end_time:
                    #print(item)
                    r_lest.append((item))

            #
    except Exception as e:
        print(str(e))


    print(len(r_lest))
    csv_name = file_path + '/' + "kline" + '_' + yesterday_date + '.csv'
    #print(csv_name)
    with open(csv_name, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for line in r_lest:
            writ_line = [Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,symbol),
                         line["id"] * 1000,
                         '1m',
                         line['id'] * 1000,
                         line['open'],
                         line['close'],
                         line['low'],
                         line['high'],
                         line['amount'],
                         line['vol'],
                         line['count']
                         ]
            csv_writer.writerow(writ_line)

def get_symbols_kline():
    symbol_list = ['ethusdt',
                   'btcusdt',
                   'bchusdt',
                   'ltcusdt',
                   'eosusdt',
                   'ethbtc',
                   'eosbtc',
                   'xrpusdt']
    for symbol in symbol_list:
        save_to_csv(symbol)

if __name__ == '__main__':
    #print(get_kline("eosbtc", "1min", size=2000))
    get_symbols_kline()
    



