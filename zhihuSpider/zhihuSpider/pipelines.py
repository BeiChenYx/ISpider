# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .spiders.sqlOpertion import MysqlOperation


class ZhihuspiderPipeline(object):
    def process_item(self, item, spider):
        if str(item.__class__) == "<class 'zhihuSpider.items.ZhihuspiderItem'>":
            # print("识别到了话题items，马上插入数据库...")
            # print(item)
            self.processZhihuspiderItem(item)
        elif str(item.__class__) == "<class 'zhihuSpider.items.ZhihuspiderArticleOrQuestionItem'>":
            print(item['TopicCategory'])
            print(item['ArticleName'])
            print(item['ArticleLikenum'])
            print(item['ArticleCommentnum'])
            print(item['ArticleLink'])
            print(item['IsArticle'])
            print(item['Created'])
        else:
            print('没有检测到任何items...')
        return item

    def processZhihuspiderItem(self, item):
        '''处理ZhihuspiderItem的入库问题'''
        self.sql = MysqlOperation()
        self.sql.connectDB()
        sql = 'insert into topic_info(topicCategory, topicLink) values("%s", "%s");' % (item['topicCategory'], item['topicLink'])
        self.sql.execute(sql)
        self.sql.closeDB()
        # print(sql + ' 完成入库....')
