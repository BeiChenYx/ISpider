"""
Redis缓存操作

队列定义:
    1. 一级类别结果存储队列：
        ZH:OneTopic
    2. 二级类别结果存储队列:
        ZH:TwoTopic
    3. 文章详情页面url地址队列:
        ZH:ArticalUrl
    4. 问答详情页面url地址队列:
        ZH:QuestionUrl
    5. 文章详情数据存储:
        ZH:ArticalInfo
    6. 问答详情数据存储:
        ZH:QuestionInfo
"""
import redis


class RedisHandler(object):
    """
    处理Redis操作的类
    连接，断开，写入，读取的封装
    """
    def __init__(self):
        self._host = 'localhost'
        self._port = 6379
        self._password = ''
        self.iredis = redis.Redis(host=self._host, 
                                  port=self._port, 
                                  decode_responses=True)
    
    def __del__(self):
        del self.iredis

