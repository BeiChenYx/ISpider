"""
爬取豆瓣网图书Top250的信息
"""
# coding: utf-8
import requests
from lxml import etree


__headers__ = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0"}

def get_page(url) -> str:
    """
    获取url指定的页面
    :url 要访问的地址
    :return 返回响应的内容字符串，失败返回空字符串
    """
    result = requests.get(url, header=__headers__)
    if result.status_code == 200:
        return result.text
    return ''

def parse_page(html) -> dict:
    """
    解析html，获取目标数据
    :html 需要解析的字符串数据
    :return 返回一个字典
        {
            'title': '',
            'author': '',
            'publisher': '',
            'time': '',
            'price': '',
            'score': '',
            'comments': '',
        }
    """
    # 使用 Xpath 解析数据
    result = etree.HTML(html)
    title = result.xpath('//div[@class="pl2"]/a/text()')
    # auth publisher time price出版信息
    publish_all = result.xpath('//p[@class="pl"/text()')
    score = result.xpath('//span[@class="rating_nums"]/text()')
    title = result.xpath('')


def main():
    """
    主调度函数
    """
    url = 'https://book.douban.com/top250?start=0'


if __name__ == '__main__':
    main()
