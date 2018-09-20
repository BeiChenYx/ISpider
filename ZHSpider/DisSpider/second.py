"""
从缓存中获取一级类别，然后访问，获取二级类别
"""
import time
import re

from lxml import etree

import common
from cache_handler import RedisHandler


class Second(RedisHandler):
    """
    从一级类别中获取二级类别
    """
    def __init__(self):
        RedisHandler.__init__(self)

    def read_data_id(self):
        """
        获取一级类别
        """
        while True:
            data_id = self.get_onetopic()
            if data_id == None:
                break
            yield data_id

    def get_second(self, data_id, offset):
        """
        获取二级类别的地址
        """
        url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
        params = '{"topic_id": %d,"offset": %d,"hash_id": ""}'
        postData = {
                'method': 'next',
                'params': params % (int(data_id), int(offset))
        }
        rst = common.post(url, isjson=True, formdata=postData)
        if rst:
            return rst['msg']
        else:
            return ''

    def parse_result(self, data):
        """
        提取二级类别的地址
        """
        urls = list()
        for msg in data:
            url = re.findall(
                    '<a target="_blank" href="(.*?)">',
                    msg
            )
            urls.append(url[0])
        return urls

    def save_result(self, data):
        """
        保存结果到Redis中去
        """
        for val in data:
            print('second val: ', val)
            self.push_twotopic(val)

    def main(self):
        topic_ids = self.read_data_id()
        for topic_id in topic_ids:
            offset = 0
            print('topic_id strart: ', topic_id)
            while True:
                msg = self.get_second(topic_id, offset)
                if not len(msg):
                    break
                offset += 20
                urls = self.parse_result(msg)
                self.save_result(urls)
                time.sleep(3)
        

if __name__ == '__main__':
    second = Second()
    second.main()
