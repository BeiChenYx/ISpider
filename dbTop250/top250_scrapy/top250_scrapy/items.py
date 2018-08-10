# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Top250ScrapyItem(scrapy.Item):
    """
    Top250需要的数据
    """
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    time = scrapy.Field()
    publisher = scrapy.Field()
    author = scrapy.Field()
    score = scrapy.Field()
    comments = scrapy.Field()
