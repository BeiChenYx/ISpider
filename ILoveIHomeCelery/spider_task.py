"""
Celery任务模块，实际执行网页爬取的模块
"""
import requests
from celery import Celery
from lxml import etree


# 这里定义了broker和backend
app = Celery(
    'spider_task',
    broker='amqp://guest@localhost/',
    backend='amqp'
)

@app.task
def crawl(url):
    """
    app.task装饰器使得,crawl成为一个celery的任务,
    该任务主要负责爬取url指定的网页
    :url 需要跑去的地址
    """
    print('crawl aim url: ', url)
    result = requests.get(
            url, headers={'Connection':'close'}
    )
    if result.status_code == 200:
        print('--'*30)
        print('rsponse len: ', len(result.text))
        print('--'*30)
        return result.text
    return ''

