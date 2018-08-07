# -*- coding: utf-8 -*-
import scrapy


class DbbookSpider(scrapy.Spider):
    name = 'dbbook'
    allowed_domains = ['book.douban.com']
    start_urls = ['http://book.douban.com/']

    def parse(self, response):
        print("read: ", len(response.text))
