# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import time

import redis

class IloveihomePipeline(object):

    def __init__(self,host,port, password):
        #连接redis数据库
        print('redis info: ', host, port, password)
        self.r = redis.Redis(
            str(host),
            int(port),
            password=str(password),
        )

    @classmethod
    def from_crawler(cls, crawler):
        '''
        注入实例化对象（传入参数）
        '''
        return cls(
            host=crawler.settings.get("REDIS_HOST"),
            port=crawler.settings.get("REDIS_PORT"),
            password=crawler.settings.get('REDIS_PASS')
        )

    def process_item(self, item, spider):
        if re.search('/bj/loupan/', item['url']):
            self.r.lpush('bjurl:start_urls', item['url'])
        else:
            self.r.lpush('bjurl:no_urls', item['url'])
        return item
