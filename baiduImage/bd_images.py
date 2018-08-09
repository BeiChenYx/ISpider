"""
给定关键字，爬取百度图片
"""
# coding: utf-8
import time
import re

import requests
from urllib.parse import quote

__headers__ = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
}

def get_page(url) -> dict:
    """
    获取url指定的页面
    :url 要访问的地址
    :return 返回响应的text内容
    """
    result = requests.get(url, headers=__headers__)
    print('get status_code: ', result.status_code)
    try:
        if result.status_code == 200:
            return result.text
    except ValueError as err:
        print(str(err))
        return ''

def parse_page(data) -> str:
    """
    解析data，获取目标数据
    :data: 需要解析的json
    :return 返回一个url的列表
    """
    if data:
        url_list = re.findall('"thumbURL":"(.*?)"', data)
        for url in url_list:
            if url:
                yield url

def get_images(url_items):
    """
    处理图片下载的方法
    :url_items image url的迭代器
    """
    for url in url_items:
        print('img url: ', url)
        rst = requests.get(url, headers=__headers__)
        # img = Image.open(BytesIO(rst.content))
        img_name = str(time.time()) + '.' + url.split('/')[-1].split('.')[-1]
        # img.save('./images/' +img_name)
        with open('./images/' + img_name, 'wb') as img:
            img.write(rst.content)
            print(img_name)

def main():
    """
    爬虫调度函数
    queryWord为搜索图片的关键字，这里为 '海'
    """
    word = '海'
    page_urls = list()
    # 请求十页，就是10 * 30 张图片
    for i in range(10):
        page_url = ('https://image.baidu.com/search/acjson'
                    '?tn=resultjson_com&ipn=rj&ct=201326592'
                    '&is=&fp=result&queryWord=%s&cl=2'
                    '&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1'
                    '&z=&ic=0&word=%s&s=&se=&tab='
                    '&width=&height=&face=0&istype=2&qc=&nc=1&'
                    'fr=&pn=%s&rn=30&gsm=%s&%s=' % (
                        quote(word), quote(word),
                        str(i), '%x'%i, str(int(time.time()))))
        page_urls.append(page_url)
    for url in page_urls:
        print('now url: ', url)
        data = get_page(url)
        print('data len: ', len(data))
        if data:
            img_url_items = parse_page(data)
            get_images(img_url_items)
        time.sleep(1)

if __name__ == '__main__':
    main()
