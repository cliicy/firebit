#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests
from cryptography.fernet import Fernet
from common.communicators import HttpCommunicator
# 此处填写APIKEY

ACCESS_KEY = ""
SECRET_KEY = ""


# API 请求地址
MARKET_URL = "https://api.huobi.pro"
TRADE_URL = "https://api.huobi.pro"
ACCOUNT_URL = '/v1/account/accounts'
# 首次运行可通过get_accounts()获取acct_id,然后直接赋值,减少重复获取。
ACCOUNT_ID = 0

# 火币配置信息
huobi_setting = {
    # API 请求地址
    'MARKET_URL' : "https://api.huobi.pro",
    'TRADE_URL' : "https://api.huobi.pro",
    # REST API GET请求 header信息
    'GET_HEADERS' : {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.71 Safari/537.36',
    },
    # REST API POST请求 header信息
    'POST_HEADERS' : {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    },
    'ORDER_PLACE_URL': '/v1/order/orders/place',
}


def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    response = requests.get(url, postdata, headers=headers, timeout=5) 
    try:
        
        if response.status_code == 200:
            return response.json()
        else:
            print('http error: ', response.status_code)
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" %(response.text,e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    response = requests.post(url, postdata, headers=headers, timeout=10)
    try:
        
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" %(response.text,e))
        return


def api_key_get(params, request_path):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)

    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature


class CryptoConfig(object):
    account_cipher_key = "PJ7TgEt2PmiUCxUlAdmEld2iCPauEy66iAoP0gB0DD4="


class JwtConfig(object):
    SECRET_KEY = "dfyg"


class CryptoUtil(object):
    @staticmethod
    def encrypt(text):
        cipher_key = CryptoConfig.account_cipher_key.encode('utf-8')
        cipher = Fernet(cipher_key)
        return str(cipher.encrypt(text.encode(encoding='utf-8')), 'utf-8')

    @staticmethod
    def decrypt(text):
        cipher_key = CryptoConfig.account_cipher_key.encode('utf-8')
        cipher = Fernet(cipher_key)
        return str(cipher.decrypt(text.encode(encoding='utf-8')), 'utf-8')

    @staticmethod
    def md5_encrypt(text):
        m = hashlib.md5()
        bytes = text.encode(encoding='utf-8')
        m.update(bytes)
        return m.hexdigest()

    @staticmethod
    def base64_encrypt(text):
        encrypt_str = base64.b64encode(text.encode('utf-8'))
        return str(encrypt_str, 'utf-8')

    @staticmethod
    def base64_decrypt(text):
        decode_str = base64.b64decode(text.encode('utf-8'))
        return str(decode_str, 'utf-8')


def get_apikeys(info):
    access = info['access']
    secret = info['secret']
    tt = CryptoUtil().base64_decrypt(access)
    api = CryptoUtil().decrypt(tt)
    tts = CryptoUtil().base64_decrypt(secret)
    secret = CryptoUtil().decrypt(tts)
    return [api, secret]


class SignatureUtil:
    """
    签名工具类
    """
    # 公钥字符串
    public_key = None
    # 私钥字符串
    private_key = None
    # 私钥文件
    public_key_file = None
    # 公钥文件
    private_key_file = None
    # 输入字符串
    input_text = None
    # 输出字符串
    output_text = None
    # 验签结果
    verify_result = False
    """
    签名工具类
    """

    def sign(self, *args):
        """
        签名
        :return:
        """
        pass

    def verify(self, *args):
        """
        验证签名
        :return:
        """
        pass


class HuobiUtil(SignatureUtil):
    """
    火币工具类
    """

    def sign(self, *args):
        """
        签名
        :return:
        """
        pass

    def verify(self, *args):
        """
        验证签名
        :return:
        """
        pass

    def api_key_get_params_prepare(self, params, request_path):

        """
            必须需要签名认证的get请求参数整理

        :param params: 请求参数  字典类型
        :param request_path: get请求接口路径 字符串类型
        :return:
            url：实际get请求地址 字符串类型
            params：整理之后的get请求参数 字典类型
            headers_get : get请求headers信息 字典类型
        """
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': params['ACCESS_KEY'],
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})
        host_url = huobi_setting['TRADE_URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = createSign(params, method, host_name, request_path,
                                                   params['SECRET_KEY'])
        url = host_url + request_path
        headers_get = huobi_setting['GET_HEADERS']
        return url, params, headers_get

    def api_key_post_params_prepare(self, params, request_path):

        """
        必须需要签名认证的post请求参数整理

        :param params: 请求参数  字典类型
        :param request_path: post请求接口路径 字符串类型
        :return:
            url：实际post请求地址 字符串类型
            params：整理之后的post请求参数 字典类型
            headers_post : post请求headers信息 字典类型
        """
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': params['ACCESS_KEY'],
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}
        host_url = huobi_setting['TRADE_URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path,
                                                           params['SECRET_KEY'])

        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        headers_post = huobi_setting['POST_HEADERS']

        return url, json.dumps(params), headers_post

    def createSign(self, pParams, method, host_url, request_path, secret_key):

        """
        签名生成方法
        """
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    def get_accounts(self, acc_info):
        """
        :return:
        """
        path = "/v1/account/accounts"
        params = {}
        params.update({'ACCESS_KEY': acc_info[0], 'SECRET_KEY': acc_info[1]})
        url, params, headers_post = HuobiUtil().api_key_get_params_prepare(params, path)
        return HttpCommunicator().http_get(url=url, params=params, headers=headers_post)

    def get_account_balance(self, keys_info, acc_id):
        """
        :param keys_info:
        :param acc_id:
        :return:
        """
        ret_bal = []
        try:
            path = '{0}/{1}/{2}'.format("/v1/account/accounts", acc_id, "balance")
            params = {}
            params.update({'ACCESS_KEY': keys_info[0], 'SECRET_KEY': keys_info[1]})
            url, params, headers_post = HuobiUtil().api_key_get_params_prepare(params, path)
            # print('要查询账户余额信息的参数：', params)
            rdata = HttpCommunicator().http_get(url=url, params=params, headers=headers_post)
            # print('获取到的账户[{0}]余额信息：{1}'.format(acc_id, rdata))
            ret_bal.append(rdata)
        except Exception as e:
            print(e)
            ret_bal.append(e)
        finally:
            return ret_bal

    # def get_orders(self, keys_info, order_id):
    def get_orders(self, **kargs):
        """
        :param keys_info:
        :param order_id:
        :return:
        """
        params = {}
        path = "/v1/order/orders"
        if "order_id" in kargs:
            path = '{0}/{1}'.format(path, kargs['order_id'])
        if "symbol" in kargs:
            params.update({'symbol': kargs['symbol']})
        if "states" in kargs:
            params.update({'states': kargs['states']})
        if "access_key" in kargs:
            params.update({'ACCESS_KEY': kargs['access_key']})
        if "secret_key" in kargs:
            params.update({'SECRET_KEY': kargs['secret_key']})
        rdata = None
        try:
            # print('查询订单的参数：', params)
            url, params, headers_post = HuobiUtil().api_key_get_params_prepare(params, path)
            # print('要查询账户余额信息的参数：', params)
            rdata = HttpCommunicator().http_get(url=url, params=params, headers=headers_post)
            # print('获取到的账户[{0}]余额信息：{1}'.format(acc_id, rdata))
        except Exception as e:
            print(e)
            rdata = e
        finally:
            return rdata