"""
将Redis中的数据存入mysql数据库
"""
import pymysql
import redis


class Imysql(object):
    """
    操作mysql
    """
    def __init__(self):
        self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='yang1xing2',
                db='site_spider',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
        )

    def exec(self, sql):
        """
        执行sql
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            self.connection.commit()
        finally:
            self.connection.close()


class Iredis(object):
    """
    操作Redis
    """
    pass


