"""
获取文章url地址
"""
import re
import time
from lxml import etree

import common


def get_artical_url(url):
    """
    通过翻页的方式获取下一个动态加载的文章url
    """
    rst = common.get(url, isjson=True)
    if rst == '':
        return None
    # 数据中有两种数据，分别是问答和文章两种，需要分开处理
    urls = list()
    artical_list = list()
    question_list = list()
    for data in rst['data']:
        if data['target']['type'] == 'answer':
            question_id = data['target']['question']['id']
            answser_id = data['target']['id']
            question_url = '%s/question/%d/answer/%d' % (
                    common.domain_name, question_id, answser_id
            )
            question_list.append(question_url)
            print('get_artical_url question_url is: ', question_url)
        elif data['target']['type'] == 'article':
            artical_url =  data['target']['url']
            artical_list.append(artical_url)
            print('get_artical_url artical_url is: ', artical_url)
        else:
            print('检测到异常类型....')
    next_url = rst['paging']['next']
    is_end = rst['paging']['is_end']
    return artical_list, question_list, next_url, is_end

def save_title_url(artical, question):
    """
    保存文章详细信息的地址
    """
    with open('artical_url.txt', 'a', encoding='utf-8') as fi:
        for line in artical:
            print(line)
            fi.write(line + '\n')
    with open('question_url.txt', 'a', encoding='utf-8') as fi:
        for line in question:
            print(line)
            fi.write(line + '\n')

def parse_first_url(html):
    """
    从第一次访问的内容中解析出下一批文章的地址，
    以供翻页使用
    """
    # 提取当前加载页的数据，数据分文章和问答两类
    artical_list = list()
    question_list = list()
    rst = etree.HTML(html) 
    items = rst.xpath('//div[@class="List-item TopicFeedItem"]')
    for item in items:
        type_text = item.xpath('./div/@class')[0]
        print('type_text: ', type_text)
        if type_text == 'ContentItem ArticleItem':
            # 内容为文章
            artical_url = item.xpath('./div/h2[@class="ContentItem-title"]/a/@href')
            artical_list.append('http:' + artical_url[0])
            print('parse_first_url artical_url is: ', artical_url[0])
        else:
            # 内容为问题
            question_url = item.xpath('./div/h2/div/a/@href')
            print(question_url)
            question_list.append(common.domain_name + question_url[0])
            print('parse_first_url question_url is: ', question_url[0])

    # 查找下一页的url地址
    part = ('(http://www.zhihu.com/api/v4/topics/[0-9]+'
            '/feeds/top_activity)\?include=(.*?)&amp;'
            'limit=([0-9]+)&amp;after_id=([0-9.]+)')
    rst = re.findall(part, html, re.I)
    if len(rst) == 0:
        return '', ''
    next_url = (rst[0][0] + '?include=' + rst[0][1]
            + '&limit=' + rst[0][2] + '&after_id=' + rst[0][3])

    return artical_list, question_list, next_url

def get_second_info(url):
    """
    访问二级类别的详细页面，获取初次加载的文章url以及
    后续文章url的请求地址
    """
    print('get_second_info url is: ', url)
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
    for line in lines[:1]:
        html = get_second_info(common.domain_name + line.strip())
        if not html:
            continue
        info_first = parse_first_url(html)
        save_title_url(info_first[0], info_first[1])

        task_url = [info_first[-1], ]
        while True:
            if len(task_url) == 0:
                break
            url = task_url.pop()
            info_paging = get_artical_url(url)
            if not info_paging:
                continue
            save_title_url(info_paging[0], info_paging[1])
            if info_paging[-1]:
                break
            task_url.insert(0, info_paging[-2])
            time.sleep(1)

        time.sleep(2)


if __name__ == '__main__':
    starting = time.time()
    with open('./artical_url.log', 'a', encoding='utf-8') as fi:
        fi.write('starting: ' + str(starting) + '\n')
    main()
    ending = time.time()
    with open('./artical_url.log', 'a', encoding='utf-8') as fi:
        fi.write('ending' + str(ending) + '\n')
        fi.write('任务耗时: ' + str((ending - starting) / 60 + 'min\n'))
