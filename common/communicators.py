#  -*- coding:utf-8 -*-
import requests


class HttpCommunicator:
    """
    http通信器
    """

    def http_get(self, url, params, headers):

        """
         http通信器get请求方法

        :param url: 请求接口地址 字符串类型 例如：'https://api.huobi.pro/market/history/kline'
        :param params: 请求参数  字典类型  例如：{'symbol': 'btcusdt', 'period': '1min', 'size': 150}
        :param headers: 请求头信息  字典类型 例如：{'Content-type': 'application/x-www-form-urlencoded',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        :return: 返回json格式数据
        """
        headers = headers
        postdata = params
        # print("%s,%s,%s" % (url, params, headers))
        response = requests.get(url, postdata, headers=headers, timeout=5)
        ret = None
        try:

            if response.status_code == 200:
                # print("response:%s" % (response.json()))
                ret = response.json()
                # return response.json()
            else:
                print("response:%s" % response.status_code)
                ret = response
        except Exception as e:
            print(e)
            ret = e
        finally:
            return ret

    def http_post(self, url, params, headers, content_type=None, timeout=10):

        """
        http通信器post请求方法

        :param url: 请求接口地址 字符串类型 例如：'https://api.huobi.pro/market/history/kline'
        :param params: 请求参数  字典类型  例如：{'symbol': 'btcusdt', 'period': '1min', 'size': 150}
        :param headers: 请求头信息  字典类型 例如：{'Content-type': 'application/x-www-form-urlencoded',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        :return: 返回json格式数据
        """

        headers = headers
        postdata = params
        if content_type is not None:
            print("url:%s,postdata:%s,timeout:%s" % (url, postdata, timeout))
            response = requests.post(url, None, postdata, headers=headers, timeout=timeout)
        else:
            print("url:%s,postdata:%s,timeout:%s" % (url, postdata, timeout))
            response = requests.post(url, postdata, headers=headers, timeout=timeout)
        try:
            if response.status_code == 200:
                print("response:%s" % (response.json()))
                return response.json()
            else:
                return
        except Exception as e:
            print(e)
            return


class SocketCommunicator:
    """
    socket通信器
    """
    # TODO 待开发


if __name__ == '__main__':
    pass
