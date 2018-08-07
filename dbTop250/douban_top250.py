"""
爬取豆瓣网图书Top250的信息
"""
# coding: utf-8
import json
import time
import requests
from lxml import etree


__headers__ = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0"}
__file_path__ = './top250.json'

def get_page(url) -> str:
    """
    获取url指定的页面
    :url 要访问的地址
    :return 返回响应的内容字符串，失败返回空字符串
    """
    # result = requests.get(url, headers=__headers__)
    result = requests.get(url)
    if result.status_code == 200:
        return result.text
    return ''

def parse_page(html) -> dict:
    """
    解析html，获取目标数据
    :html 需要解析的字符串数据
    :return 返回一个字典
    """
    # 使用 Xpath 解析数据
    result = etree.HTML(html)
    title_rst = result.xpath('//div[@class="pl2"]/a/text()')
    # auth publisher time price出版信息
    publish_all_rst = result.xpath('//p[@class="pl"]/text()')
    score_rst = result.xpath('//span[@class="rating_nums"]/text()')
    comments_rst = result.xpath('//span[@class="pl"]/text()')
    len_title = len(title_rst)
    print('len_title: ', len_title)
    print('title: ', [title.strip() for title in title_rst])
    # for index in range(len_title):
    #     try:
    #         title = title_rst[index]
    #         publish_info = publish_all_rst[index].split('/')
    #         price = publish_info.pop()
    #         timed = publish_info.pop()
    #         publisher = publish_info.pop()
    #         author = '/'.join(publish_info)
    #         score = score_rst[index]
    #         comments, = comments_rst[index]
    #         rst = {
    #             'title': title,
    #             'author': author,
    #             'publisher': publisher,
    #             'time': timed,
    #             'price': price,
    #             'score': score,
    #             'comments': comments,
    #         }
    #         print('index: ', index)
    #         print('title: ', title)
    #         yield rst
    #     except Exception as err:
    #         print(str(err))


def save_data(data) -> bool:
    """
    将数据保存到__file_path__指定的json文件中去
    :data 要保存的数据
    :return True / False
    """
    # print('data: ', data)
    try:
        with open(__file_path__, 'w', encoding='utf-8') as handler:
            json.dump(data, handler, ensure_ascii=False, indent=4)
        return True
    except json.JSONDecodeError as err:
        print(str(err))
        return False

def main():
    """
    主调度函数
    """
    origin_url = 'https://book.douban.com/top250?start='
    aim_url = [origin_url + str(i * 25) for i in range(10)]
    success_url = list()
    failed_url = list()
    result_info = list()
    for url in aim_url:
        html = get_page(url)
        if html:
            result = parse_page(html)
            success_url.append(url)
            result_info.append(result)
        else:
            failed_url.append(url)
        time.sleep(1)
    save_data(result_info)
    print('sucess process page: ', len(success_url))
    print('failed process page: ', len(failed_url))


if __name__ == '__main__':
    main()
