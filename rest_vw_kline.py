# -*- coding: utf-8 -*-

import time
from Utils import *
from config.settings import symbol_list
from common.enums import HUOBI_PERIOD_LIST
from common.enums import Symbol, Platform
from config.settings import sdb, mdb


def trigger():
    for sy in symbol_list:
        try:
            CandleApp().run(sy, HUOBI_PERIOD_LIST[0])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[1])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[2])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[3])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[4])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[5])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[6])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[7])
            CandleApp().run(sy, HUOBI_PERIOD_LIST[8])
        except Exception as e:
            print(e)


class CandleApp:

    def run(self, *args):
        while True:
            self.sync_kline(*args)
            time.sleep(60)

    # 获取KLine
    def sync_kline(self, symbol, period, size=2000):
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
        try:
            ret = http_get_request(url, params)
            if ret["status"] == "ok":
                json_ret = ret["data"]
                for line in json_ret:
                    sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI, symbol)
                    # 把 下面的实时数据写入 Mongodb中
                    # 'high' 最高价
                    # 'low' 最低价
                    # open 开盘价
                    # close 收盘价
                    # count
                    # base_vol 基准货币成交量
                    # quote_vol 计价货币成交量
                    # 货币对
                    ybdd = {}
                    ybdd['sym'] = sym
                    ybdd['ts'] = line["id"] * 1000
                    # 间隔时间
                    ybdd['interval'] = period
                    # 开盘价格
                    ybdd['open'] = line['open']
                    # 最高价格
                    ybdd['high'] = line['high']
                    # 最低价
                    ybdd['low'] = line['low']
                    # close
                    ybdd['close'] = line['close']
                    # count
                    ybdd['count'] = line['count']
                    # quote_vol 计价货币成交量
                    ybdd['quote_vol'] = round(line['vol'], 2)
                    ybdd['exchange'] = 'huobi'
                    ybdd['api'] = 'kline'
                    inter_p = Symbol.convert_to_standard_interval(Platform.PLATFORM_HUOBI, period)
                    coll = sdb[mdb[inter_p]]
                    coll.update({'sym': ybdd['sym'], 'ts': ybdd['ts'], 'interval': ybdd['interval']},
                                {'$set': {'Open': ybdd['open'], 'High': ybdd['high'],
                                          'Low': ybdd['low'], 'Close': ybdd['close'], 'Count': ybdd['count'],
                                          'Quote_vol': ybdd['quote_vol'], 'exchange': ybdd['exchange'],
                                          'api': ybdd['api']}}, True)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    trigger()




