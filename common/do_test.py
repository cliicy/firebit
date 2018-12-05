import json
import ujson
from bs4 import BeautifulSoup
import requests
import time
import gevent
from gevent import monkey, pool
monkey.patch_all()
from threading import Thread


def monkey_patch_json():
    json.__name__ = 'ujson'
    json.dumps = ujson.dumps
    json.loads = ujson.loads


def do_debug():
    pass


def get_links(url):
    # time.sleep(2)
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        links = soup.find_all('a')
        print(links)


def start_process():
    time.sleep(2)
    jobs = []
    links = []
    p = pool.Pool(10)
    urls = [
        'http://www.baidu.com',
    ]
    for url in urls:
        jobs.append(p.spawn(get_links, url))
    gevent.joinall(jobs)


def invoke_test():
    t = Thread(target=start_process, )
    t.start()
    t.join()


def do_trace():
    a = 1
    b = 10
    from ipdb import set_trace
    set_trace()
    c = b/a
    print(c)


if __name__ == '__main__':
    # test monkey path start
    # monkey_patch_json()
    # print('main.py', json.__name__)
    # import sub
    # test monkey path end


    pass
