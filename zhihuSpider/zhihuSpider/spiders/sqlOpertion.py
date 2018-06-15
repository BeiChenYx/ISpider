# -*- coding: utf-8 -*-
import pymysql.cursors


class MysqlOperation(object):
    '''封装pymysql操作'''
    def connectDB(self,
                  host='127.0.0.1',
                  user='root',
                  password='11223',
                  mysqldb='testAPI',
                  dbport=3306):
        try:
            self.db = pymysql.connect(host=host,
                                      user=user,
                                      password=password,
                                      db=mysqldb,
                                      port=dbport,
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
            self.cur = self.db.cursor()
            # print('连接数据库完成了....')
        except Exception as e:
            print(e)

    def closeDB(self):
        self.db.close()
        # print('断开数据库...')

    def execute(self, sql):
        try:
            print(sql)
            self.cur.execute(sql)
            self.db.commit()
            print('........execute sql end........')
        except Exception as e:
            self.db.rollback()
            print(e)
