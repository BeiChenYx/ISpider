"""
Redis缓存操作
"""
import redis


class RedisHandler(object):
    """
    处理Redis操作的类
    连接，断开，写入，读取的封装
    """
    def __init__(self):
        """
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
        self._host = 'localhost'
        self._port = 6379
        self._password = ''
        self.iredis = redis.Redis(host=self._host, 
                                  port=self._port, 
                                  decode_responses=True)

        self.one_topic = 'zh:onetopic'
        self.twotopic = 'zh:twotopic'
        self.articalurl = 'zh:articalurl'
        self.questionurl = 'zh:questionurl'
        self.articalinfo = 'zh:articalinfo'
        self.questioninfo = 'zh:questioninfo'
    
    # def __del__(self):
        # redis对象在离开作用域会自动析构
        # del self.iredis

    def _set_queue(data, queue_name):
        """
        将数据写进Redis队列中去
        :data  需要写入的数据
        :queue_name 需要写入的队列名称
        """
        pass

    def _get_queue(queue_name):
        """
        从指定的Redis队列中读取数据
        :queue_name 需要读取的队列名字
        """
        pass
