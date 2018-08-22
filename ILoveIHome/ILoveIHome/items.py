# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IloveihomeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    covered = scrapy.Field()
    addr = scrapy.Field()
    time = scrapy.Field()
    type_home = scrapy.Field()
    price = scrapy.Field()

class NextHomeItem(scrapy.Item):
    """
    分页的url地址
    """
    url = scrapy.Field()
