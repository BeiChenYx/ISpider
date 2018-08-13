# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymysql

class MysqlTop250ScrapyPipeline(object):
    """
    连接数据库，将数据写入数据库中
    """
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASS"),
            port=crawler.settings.get("MYSQL_PORT")
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(
            self.host,
            self.user,
            self.password,
            self.database,
            charset='utf8',
            port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        sql = ("insert into db_top250(title,price,time,publisher,author,score,comments)"
               "values('%s','%s','%s','%s','%s','%s', '%s')" % (
                   item['title'],
                   item['price'],
                   item['time'],
                   item['publisher'],
                   item['author'],
                   item['score'],
                   item['comments']))
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()

class DuplicatesTop250Pipeline(object):
    """
    过滤去重
    """

    def __init__(self):
        self.title_seen = set()

    def process_item(self, item, spider):
        """
        根据title来过滤
        """
        # 输出爬虫的名字
        print('spider is: ', spider.name)
        if item['title'] in self.title_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.title_seen.add(item['title'])
            return item
