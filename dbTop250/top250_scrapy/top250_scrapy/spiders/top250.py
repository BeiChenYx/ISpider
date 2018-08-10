# -*- coding: utf-8 -*-
import scrapy


class Top250Spider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['book.douban.com/top250']
    start_urls = ['http://book.douban.com/top250/']

    def parse(self, response):
        pass
