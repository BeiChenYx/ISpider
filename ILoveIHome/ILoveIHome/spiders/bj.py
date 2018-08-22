# -*- coding: utf-8 -*-
import scrapy

from ILoveIHome.items import IloveihomeItem


class BjSpider(scrapy.Spider):
    name = 'bj'
    allowed_domains = ['fang.5i5j.com']
    start_urls = ['https://fang.5i5j.com/bj/loupan/']

    def parse(self, response):
        print(response.body)
        print(len(response.body))
