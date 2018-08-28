# -*- coding: utf-8 -*-
import scrapy

from scrapy_redis.spiders import RedisSpider

from ILoveIHomeSlave.items import IloveihomeslaveItem

class BjSpider(RedisSpider):
    name = 'bj'
    # allowed_domains = ['fang.5i5j.com']
    # start_urls = ['http://fang.5i5j.com/']
    redis_key = 'bjurl:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(BjSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        #print(response.status)
        print('=='*30)
        print('bjurl: ', response.url)
        print('=='*30)
        try:
            item = IloveihomeslaveItem()
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
