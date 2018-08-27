# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ILoveIHome.items import IloveihomeItem, NextHomeItem

class BjcSpider(CrawlSpider):
    name = 'bjurl'
    allowed_domains = ['fang.5i5j.com']
    start_urls = ['http://fang.5i5j.com/bj/loupan']

    rules = (
        Rule(LinkExtractor(allow='https://fang.5i5j.com/bj/loupan/n[0-9]+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = NextHomeItem()
        item['url'] = response.url
        return item