# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ILoveIHome.items import IloveihomeItem, NextHomeItem

class BjcSpider(CrawlSpider):
    name = 'bjc'
    allowed_domains = ['fang.5i5j.com']
    start_urls = ['http://fang.5i5j.com/bj/loupan']

    rules = (
        Rule(LinkExtractor(allow='https://fang.5i5j.com/bj/loupan/n[0-9]+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('response len: ', len(response.body))
        # 先获取爬取的页面中的房屋信息
        homes = response.selector.xpath('//div[@class="houseList_list"]')
        for home in homes:
            try:
                item = IloveihomeItem()
                txt_xpath = './div[@class="houseList_list_txt fl"]'
                name_xpath = txt_xpath + '/div[@class="txt1 style"]/h3/a/text()'
                covered_xpath = txt_xpath + '/div[@class="style"]//span/text()'
                addr_xpath = txt_xpath + '/div[@class="style address"]//span/text()'
                time_xpath = txt_xpath + '/div[@class="style"][2]//span/text()'
                type_xpath = txt_xpath + '/div[@class="title"]//span/text()'
                price_xpath = ('./div[@class="price fontS16"]/text() | '
                               './div[@class="price fontS16"]/i/text()')

                item['name'] = home.xpath(name_xpath).extract_first().strip()
                item['covered'] = ' '.join([covered.strip() for covered in home.xpath(covered_xpath).extract()])
                item['addr'] = ' '.join([addr.strip() for addr in home.xpath(addr_xpath).extract()])
                item['time'] = ' '.join([time.strip() for time in home.xpath(time_xpath).extract()])
                item['type_home'] = ' '.join([ty.strip() for ty in home.xpath(type_xpath).extract()])
                item['price'] = ' '.join([price.strip() for price in home.xpath(price_xpath).extract()])
                yield item
            except Exception as err:
                print(str(err))
