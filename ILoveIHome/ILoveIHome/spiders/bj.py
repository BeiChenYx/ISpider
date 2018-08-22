# -*- coding: utf-8 -*-
"""
使用基础爬虫先爬取信息，之后再用crawlspider横纵爬取，
完成这些后再用分布式爬取
"""
import scrapy

from ILoveIHome.items import IloveihomeItem, NextHomeItem


class BjSpider(scrapy.Spider):
    """
    分别要进行横纵爬取
    """
    name = 'bj'
    allowed_domains = ['fang.5i5j.com']
    start_urls = ['https://fang.5i5j.com/bj/loupan/']
    # start_urls = ['https://www.baidu.com']

    def parse(self, response):
        print('response len: ', len(response.body))
        # print(response.body)
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

                item['name'] = home.xpath(name_xpath)
                item['covered'] = ' '.join([covered.strip() for covered in home.xpath(covered_xpath)])
                item['addr'] = ' '.join([addr.strip() for addr in home.xpath(addr_xpath)])
                item['time'] = ' '.join([time.strip() for time in home.xpath(time_xpath)])
                item['type_home'] = ' '.join([ty.strip() for ty in home.xpath(type_xpath)])
                item['price'] = ' '.join([price.strip() for price in home.xpath(price_xpath)])
                yield item
            except Exception as err:
                print(str(err))

        # 再获取下一页的url地址
        next_url = response.selector.xpath('//div[@class="pagination blue"]/ul/li[last()]/a/@href').extract_first()
        if not next_url:
            yield scrapy.Request(next_url, callback=self.parse)
