# -*- coding: utf-8 -*-
import scrapy

from top250_scrapy.items import Top250ScrapyItem


class Top250Spider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['book.douban.com/top250']

    def start_requests(self):
        origin_url = 'https://book.douban.com/top250?start='
        aim_url = [origin_url + str(i * 25) for i in range(10)]

        for url in aim_url:
            # yield scrapy.FormRequest(url, callback=self.parse)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        tds = response.selector.xpath('//table[@width="100%"]/tr/td[2]')
        for td in tds:
            publisher = td.xpath('./p[@class="pl"]/text()').extract_first().split('/')
            item = Top250ScrapyItem()
            item['title'] = td.xpath('./div[@class="pl2"]/a/@title').extract_first()
            item['price'] = publisher.pop()
            item['time'] = publisher.pop()
            item['publisher'] = publisher.pop()
            item['author'] = '/'.join(publisher)
            item['score'] = td.xpath('./div[@class="star clearfix"]/'
                                     'span[@class="rating_nums"]/text()').extract_first()
            item['comments'] = td.xpath('./div[@class="star clearfix"]'
                                        '/span[@class="pl"]/text()').extract_first()
            yield item
