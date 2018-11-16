##
火币 kline 前端要从后台获取数据时，要传给后端当前时间，后端就把距离当前时间的前2000条数据返回
如果用gevent+rest的方式去获取多个货币对的kline行情数据，会报429的错误
Receiving a status 429 is not an error, it is the other server "kindly" asking you to please stop spamming requests.
 Obviously, your rate of requests has been too high and the server is not willing to accept this
 所以vwallet_huobi_worker.py暂时不用
 直接运行rest_vw_kline.py去获取行情数据



