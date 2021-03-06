# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree

from master.items import MasterItem


class DbbooksSpider(scrapy.Spider):
    name = 'dbBooks'
    allowed_domains = ['book.douban.com']
    # start_urls = ['http://http://book.douban.com/']

    def start_requests(self):
        """
        请求所有标签页，获取所有类别的地址
        单页面请求，使用requests来完成
        """
        print('---'*20)
        origin_url = 'https://book.douban.com/tag/'
        header = {
            'User_Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64;'
                           ' rv:61.0) Gecko/20100101 Firefox/61.0'),
        }
        result = requests.get(origin_url, headers=header)
        print('result.status_code: ', result.status_code)
        print('result.text: ', result.text)
        if result.status_code == 200:
            html = etree.HTML(result.text)
            type_urls = html.xpath('//td/a/@href')
            print('type_urls: ', type_urls)
            for url in type_urls:
                aim_url = 'https://book.douban.com' + url
                print("aim_url: ", aim_url)
                print('---'*20)
                yield scrapy.Request(aim_url, callback=self.parse)
        else:
            raise scrapy.exceptions.CloseSpider('初始分类标签页面出错!')

    def parse(self, response):
        book_urls = response.xpath('//div[@class="info"]/a/@href')
        for url in book_urls:
            book_url_item = MasterItem()
            book_url_item['book_url'] = url
            print('book_url: ', url)
            print('==='*20)
            yield book_url_item
