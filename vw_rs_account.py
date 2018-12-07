# -*- coding: utf-8 -*-

import time
from Utils import *
from config.settings import acc_coll, balance_coll
TRADE_SYMBOL_LIST = ['btc', 'bch', 'eth', 'ltc', 'eos', 'eth', 'xrp', 'usdt', 'btc', 'usd']

key_info = []
acc_info = acc_coll.find_one({"exchange": 'huobi', 'api': 'key'})
key_info = get_apikeys(acc_info)
platform = 'huobi'


class BalanceApp:
    def run(self, *args):
        while True:
            self.sync_accts_detail(*args)
            time.sleep(3600)

    @staticmethod
    def sync_accts_detail():
        acc_ret = None
        try:
            # acc_id = acc_coll.find({"exchange": platform, "api": 'accounts', 'state': 'working', 'type': 'spot'})
            acc_info = acc_coll.find({"exchange": platform, "api": 'accounts'})
            for one in acc_info:
                acc_id = one['id']
                acc_ret = HuobiUtil().get_account_balance(key_info, acc_id)
                # 获取此账户及其下各个子账户中的所有拥有此币种的所有余额信息
                # print('账户信息：', acc_ret)
                # 账户信息： [{'status': 'ok', 'data': {'id': 5632276, 'type': 'spot', 'state': 'working',
                #                                  'list': [{'currency': 'hb10', 'type': 'trade', 'balance': '0'}
                if len(acc_ret) > 0:
                    for acc in acc_ret:
                        rdata = acc['data']
                        data_list = rdata['list']
                        for one in data_list:
                            if one['currency'] in TRADE_SYMBOL_LIST:
                                print('----', one)
                                ybdd = {}
                                ybdd['acc_id'] = rdata['id']
                                ybdd['acc_type'] = rdata['type']
                                ybdd['acc_state'] = rdata['state']
                                ybdd['sym'] = one['currency']
                                ybdd['type'] = one['type']
                                ybdd['balance'] = one['balance']
                                balance_coll.update({'exchange': platform, 'api': 'balance', 'acc_id': ybdd['acc_id'],
                                                     'acc_type': ybdd['acc_type'], 'acc_state': ybdd['acc_state'],
                                                     'sym': ybdd['sym'], 'type': ybdd['type']},
                                                    {'$set': {'balance': ybdd['balance']}}, True)
        except Exception as e:
            acc_ret = e
        finally:
            return acc_ret


class AccountApp:

    def run(self, *args):
        while True:
            self.sync_account(*args)
            time.sleep(3600)

    # 获取account
    def sync_account(self):
        """
        :param symbol
        :return:
        """
        params = {}
        params.update({'ACCESS_KEY': key_info[0], 'SECRET_KEY': key_info[1]})
        try:
            url, params, headers_post = HuobiUtil().api_key_get_params_prepare(params, ACCOUNT_URL)
            ret = http_get_request(url, params)
            # {'status': 'ok', 'data': [{'id': 5632276, 'type': 'spot', 'subtype': '', 'state': 'working'}]}
            # print("获取到的账户信息：{}".format(ret))
            if ret["status"] == "ok":
                retd = ret["data"]
                for one in retd:
                    ybdd = {}
                    ybdd['id'] = one['id']
                    ybdd['type'] = one['type']
                    ybdd['state'] = one['state']
                    acc_coll.update({'exchange': platform, 'api': 'accounts'},
                                    {'$set': {'id': ybdd['id'], 'type': ybdd['type'], 'state': ybdd['state']}}, True)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    # AccountApp().run()
    BalanceApp().run()



