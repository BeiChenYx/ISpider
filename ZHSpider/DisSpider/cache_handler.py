"""
Redis缓存操作
    队列定义:
        1. 一级类别结果存储队列：
            zh:onetopic
        2. 二级类别结果存储队列:
            zh:twotopic
        3. 文章详情页面url地址队列:
            zh:articalurl
        4. 问答详情页面url地址队列:
            zh:questionurl
        5. 文章详情数据存储:
            zh:articalinfo
        6. 问答详情数据存储:
            zh:questioninfo
"""
import configparser

import redis


class RedisHandler(object):
    """
    处理Redis操作的类
    连接，断开，写入，读取的封装
    """
    def __init__(self):
        self._host, self._port = self.read_config()
        assert self._host!='' and self._port!='', \
                '配置文件读取出错'
        self.iredis = redis.Redis(host=self._host, 
                                  port=self._port, 
                                  decode_responses=True)

        self.onetopic = self.read_task('one_topic')
        self.twotopic = self.read_task('two_topic')
        self.articalurl = self.read_task('artical_url')
        self.questionurl = self.read_task('question_url')
        self.articalinfo = self.read_task('artical_info')
        self.questioninfo = self.read_task('question_info')

    def read_config(self):
        """
        读取配置文件
        """
        self.conf = configparser.ConfigParser()
        self.conf.read('./config/config.ini')
        port = self.conf.get('redis', 'port')
        host = self.conf.get('redis', 'host')
        print('read host:port: %s:%s' % (host, port))
        return host, port
    
    def read_task(self, name):
        """
        读取指定队列的值，用于Redis
        """
        self.conf = configparser.ConfigParser()
        self.conf.read('./config/config.ini')
        return self.conf.get('task', name)
    
    # def __del__(self):
        # redis对象在离开作用域会自动析构
        # del self.iredis

    def _set_queue(self, data, queue_name):
        """
        将数据写进Redis队列中去
        :data  需要写入的数据
        :queue_name 需要写入的队列名称
        """
        self.iredis.lpush(queue_name, data)

    def _get_queue(self, queue_name):
        """
        从指定的Redis队列中读取数据
        :queue_name 需要读取的队列名字
        """
        return self.iredis.rpop(queue_name)

    def push_onetopic(self, data):
        self._set_queue(data, self.onetopic)

    def get_onetopic(self):
        return self._get_queue(self.onetopic)

    def push_twotopic(self, data):
        self._set_queue(data, self.twotopic)

    def get_twotopic(self):
        return self._get_queue(self.twotopic)

    def push_articalurl(self, data):
        self._set_queue(data, self.articalurl)

    def get_articalurl(self):
        return self._get_queue(self.articalurl)

    def push_articalinfo(self, data):
        self._set_queue(data, self.articalinfo)

    def get_articalinfo(self):
        return self._get_queue(self.articalinfo)

    def push_questionurl(self, data):
        self._set_queue(data, self.questionurl)

    def get_questionurl(self):
        return self._get_queue(self.questionurl)

    def push_questioninfo(self, data):
        self._set_queue(data, self.questioninfo)

    def get_questioninfo(self):
        return self._get_queue(self.questioninfo)

