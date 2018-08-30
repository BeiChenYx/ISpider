"""
我爱我家的celery爬虫的计划任务
"""
from spider_task import crawl

for i in range(1, 54):
    crawl.delay('https://fang.5i5j.com/bj/loupan/n%d' % (i))
