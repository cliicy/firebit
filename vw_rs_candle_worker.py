from gevent import monkey

monkey.patch_all()
import gevent
from vw_rs_kline import CandleApp
from config.settings import symbol_list
from common.enums import HUOBI_PERIOD_LIST


def run_task():
    greenlets = []
    for sy in symbol_list:
        try:
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[0]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[1]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[2]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[3]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[4]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[5]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[6]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[7]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[8]))
            greenlets.append(gevent.spawn(CandleApp().run, sy, HUOBI_PERIOD_LIST[9]))
        except Exception as e:
            print(e)
    gevent.joinall(greenlets)


if __name__ == '__main__':
    # print(sys.argv[0])
    run_task()
