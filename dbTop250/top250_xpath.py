"""
爬取豆瓣网图书Top250的信息
"""
# coding: utf-8
import json
import requests
from lxml import etree


__headers__ = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
}
__file_path__ = './top250.json'

def get_page(url) -> str:
    """
    获取url指定的页面
    :url 要访问的地址
    :return 返回响应的内容字符串，失败返回空字符串
    """
    result = requests.get(url, headers=__headers__)
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
    tds = result.xpath('//table[@width="100%"]/tr/td[2]')
    for td in tds:
        publisher = td.xpath('./p[@class="pl"]/text()')[0].split('/')
        yield {
            'title': td.xpath('./div[@class="pl2"]/a/@title')[0],
            'price': publisher.pop(),
            'time': publisher.pop(),
            'publisher': publisher.pop(),
            'author': '/'.join(publisher),
            'score': td.xpath('./div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0],
            'comments': td.xpath('./div[@class="star clearfix"]/span[@class="pl"]/text()')[0],
        }

def save_data(data) -> bool:
    """
    将数据保存到__file_path__指定的json文件中去
    :data 要保存的数据
    :return True / False
    """
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
            for rst in result:
                result_info.append(rst)
            success_url.append(url)
            print('result_info len: ', len(result_info))
        else:
            failed_url.append(url)
    save_data(result_info)
    print('sucess process page: ', len(success_url))
    print('failed process page: ', len(failed_url))


if __name__ == '__main__':
    main()
