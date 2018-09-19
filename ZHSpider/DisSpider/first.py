"""
获取话题所有一级类别data-id
"""
from pyquery import PyQuery as pq

from common import get
from cache_handler import RedisHandler


class First(RedisHandler):
    """
    封装一级类别获取和保存，继承Redis操作
    """
    def __init__(self):
        RedisHandler.__init__(self)

    def save_result(self, data):
        """
        保存结果到Redis中去
        """
        # [self.push_onetopic(val) for val in data]
        for val in data:
            print('val: ', val)
            self.push_onetopic(val)

    def parse_page(self, html):
        """
        :html 需要解析的数据
        """
        assert html, 'html 不能为空'

        result = list()
        if html:
            rst = pq(html)
            lis = rst('li.zm-topic-cat-item')
            for li in lis.items():
                data_id = li.attr('data-id')
                # name = li('a').text()
                # print('data_id: ', data_id)
                result.append(data_id)
        return result


    def get_page(self, url):
        """
        :url 需要爬取的地址
        """
        return get(url)

    def main(self):
        """
        目标地址: https://www.zhihu.com/topics
        """
        url = 'https://www.zhihu.com/topics'
        html = self.get_page(url)
        info = self.parse_page(html)
        self.save_result(info) 
        # return info


if __name__ == '__main__':
    first = First()
    first.main()
