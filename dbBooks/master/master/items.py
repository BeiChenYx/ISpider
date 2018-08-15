# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MasterItem(scrapy.Item):
    """
    需要获取的数据
    """
    # define the fields for your item here like:
    book_id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    origin_author = scrapy.Field()
    translator = scrapy.Field()
    publish_time = scrapy.Field()
    page_num = scrapy.Field()
    price = scrapy.Field()
    hardback = scrapy.Field()
    series = scrapy.Field()
    isbn = scrapy.Field()
    scroe = scrapy.Field()
    scroes_num = scrapy.Field()


class TypeUrlItem(scrapy.Item):
    """
    所有图书标签的url
    """
    url = scrapy.Field()


class BookUrlItem(scrapy.Item):
    """
    图书的详细地址
    """
    book_url = scrapy.Field()
