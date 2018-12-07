# -*- coding: utf-8 -*-

from Utils import *
from config.settings import symbol_list


def get_detail(symbol):
    """
    :param symbol
    :return:
    """
    params = {'symbol': symbol}
    url = "https://api.huobi.pro" + '/v1/account/accounts'
    return http_get_request(url, params)


def save_to_mongodb(sym):
    print(sym)
    pass
        
            
if __name__ == '__main__':
    for symbol in symbol_list:
        save_to_mongodb(symbol)

