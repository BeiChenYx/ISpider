# -*- coding: utf-8 -*-
import time


import requests
from concurrent.futures import ThreadPoolExecutor


def return_future(msg):
    # time.sleep(1)
    print('return_future: ', msg)
    return msg


pool = ThreadPoolExecutor(max_workers=2)

f1 = pool.submit(return_future, 'hello')
f2 = pool.submit(return_future, 'world')

time.sleep(3)
# 执行完成了就返回True, 取消或者没有完成就返回False
print(f1.done())
print(f2.done())

print(f1.result)
print(f2.result)


# 使用map的方式


urls = [
    'http://www.baidu.com',
    'http://qq.com',
    'http://sina.com'
]


def task(url, timeout=10):
    print('task : ', url)
    time.sleep(10)
    return requests.get(url, timeout=timeout)


pool = ThreadPoolExecutor(max_workers=3)
results = pool.map(task, urls)

for ret in results:
    print('%s, %s' % (ret.url, len(ret.content)))
