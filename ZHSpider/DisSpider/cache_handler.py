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
        self._host = 'localhost'
        self._port = 6379
        self._password = ''
        self.iredis = redis.Redis(host=self._host, 
                                  port=self._port, 
                                  decode_responses=True)
    
    def __del__(self):
        del self.iredis
