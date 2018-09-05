"""
获取话题所有一级类别data-id
将类别名字和url地址存入json文件
"""
import json

import requests
from pyquery import PyQuery as pq

__headers__ = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
}

def save_result(data):
    """
    :data 需要保存的数据
    """
    info = {
        'info': data,
    }
    with open('./firstType.json', 'w', encoding='utf-8') as fi:
        json.dump(info, fi, ensure_ascii=False, indent=4)

def parse_page(html):
    """
    :html 需要解析的数据
    """
    result = list()
    if html:
        rst = pq(html)
        lis = rst('li.zm-topic-cat-item')
        for li in lis.items():
            data_id = li.attr('data-id')
            name = li('a').text()
            info = {
                'name': name,
                'data-id': data_id,
            }
            print('info: ', info)
            result.append(info)
    return result


def get_page(url):
    """
    :url 需要爬取的地址
    """
    rst = requests.get(url, headers=__headers__)
    print('rst.status_code: ', rst.status_code)
    if rst.status_code == 200:
        return rst.text
    return ''

def main():
    """
    目标地址: https://www.zhihu.com/topics
    """
    url = 'https://www.zhihu.com/topics'
    html = get_page(url)
    info = parse_page(html)
    save_result(info)

if __name__ == '__main__':
    main()