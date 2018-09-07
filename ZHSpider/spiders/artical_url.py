"""
获取文章url地址
"""
import re
import time
from xml import etree

import common


def get_artical_url(url):
    """
    通过翻页的方式获取下一个动态加载的文章url
    """
    rst = common.get(url, isjson=True)
    urls = list()
    for line in rst['data']:
        url = line['url']
        urls.append(url)
    return urls, rst['paging']['next'], rst['paging']['is_end']
    

def save_title_url(url):
    """
    保存文章详细信息的地址
    """
    with open('title_url.txt', 'a', encoding='utf-8') as fi:
        for line in url:
            print(line)
            fi.write(line)

def parse_first_url(html):
    """
    从第一次访问的内容中解析出下一批文章的地址，
    以供翻页使用
    """
    rst = etree.HTML(html) 
    title_url = rst.xpath('//h2[@class="ContentItem-title"]/a/@href')
    next_url = re.findall(
        ('http://www.zhihu.com/api/v[0-9]/topics/[0-9]+/feeds/top_activity\?'
        'include=.*?\&amp;limit=.*?\&amp;after_id=[0-9.]+'),
        html
    )
    return title_url, next_url[0]

def get_second_info(url):
    """
    访问二级类别的详细页面，获取初次加载的文章url以及
    后续文章url的请求地址
    """
    html = common.get(url)
    return html

def get_second_type(path):
    """
    从path中读取所有的二级类别中的文章列表地址
    """
    with open(path, 'r', encoding='utf-8') as fi:
        lines = fi.readlines()
        return lines

def main():
    lines = get_second_type('./secondType.txt')
    for line in lines:
        html = get_second_info(common.domain_name + line)
        if not html:
            continue
        title_url, next_url = parse_first_url(html)
        save_title_url(title_url)

        task_url = [next_url, ]
        while True:
            if len(task_url) == 0:
                break
            url = task_url.pop()
            artical_url, next_request_url, is_end = get_artical_url(url)
            save_title_url(artical_url)
            if is_end:
                break
            task_url.insert(0, next_request_url)
            time.sleep(1)

        time.sleep(2)
        

if __name__ == '__main__':
    main()