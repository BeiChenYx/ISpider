# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree

from master.items import BookUrlItem

class DbbooksSpider(scrapy.Spider):
    name = 'dbBooks'
    allowed_domains = ['book.douban.com']
    # start_urls = ['http://book.douban.com/tag']

    def start_requests(self):
        """
        请求所有标签页，获取所有类别的地址
        单页面请求，使用requests来完成
        """
        origin_url = 'https://book.douban.com/tag/'
        result = requests.get(origin_url)
        if result.status_code == 200:
            html = etree.HTML(result.text)
            type_urls = html.xpath('//td/a/@href')
            for url in type_urls:
                aim_url = 'https://book.douban.com' + url
                yield scrapy.Request(aim_url, callback=self.parse)
        else:
            raise scrapy.exceptions.CloseSpider('初始分类标签页面出错!')

    def parse(self, response):
        """
        获取各个分类的第一页，获取书的详情url
        """
        book_urls = response.xpath('//div[@class="info"]/a/@href')
        for url in book_urls:
            book_url_item = BookUrlItem()
            book_url_item['book_url'] = url
            yield book_url_item
