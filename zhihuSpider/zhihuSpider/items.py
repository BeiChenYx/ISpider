# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topicCategory = scrapy.Field()         # 话题总类别
    topicLink = scrapy.Field()


class ZhihuspiderArticleOrQuestionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章所属的话题类别
    TopicCategory = scrapy.Field()
    # 文章名字
    ArticleName = scrapy.Field()
    # 文章点赞数
    ArticleLikenum = scrapy.Field()
    # 文章评论数
    ArticleCommentnum = scrapy.Field()
    # 文章连接
    ArticleLink = scrapy.Field()
    # 是文章还是问答
    IsArticle = scrapy.Field()
    # 创建时间
    Created = scrapy.Field()
