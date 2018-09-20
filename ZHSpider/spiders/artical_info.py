"""
从artical_url.txt中获取文章详细信息的url
然后访问地址，获取文章和评论信息
文章需要提取的信息:
    文章名字
    文章作者
    文章作者的主页地址
    文章点赞数量
    文章地址
    文章评论数量

评论需要提取的信息:
    评论者名字
    评论者的url_token(定位到评论者)
    评论创建的时间
    评论点赞数量
"""
import time

from lxml import etree

import common


def save_artical_comment(artical, comment):
    """
    保存文章信息和评论信息
    :artical 文章信息，字典格式
    :comment 评论信息，字典列表格式
    """
    with open('./doc/artical_info.txt', 'a', encoding='utf-8') as fi:
        fi.write(
            ','.join([str(value) for _, value in artical.items()])
        ) 
        fi.write('\n')

    with open('./doc/artical_comment_info.txt', 'a', encoding='utf-8') as fi:
        for com in comment:
            info = [str(value) for _, value in com.items()]
            info.insert(0, artical['url'])
            fi.write(','.join(info))
            fi.write('\n')

def parse_artical_info(html):
    """
    提取文章信息
    :html 为访问的文章详情信息
    """
    rst = etree.HTML(html)
    # 文章名字
    name = rst.xpath('//h1[@class="Post-Title"]/text()')[0]
    # 作者名字
    author = rst.xpath(
            '//div[@class="AuthorInfo-content"]/div/span/\
            div/div/a[@class="UserLink-link"]/text()' 
    )[0]
    # 作者主页地址
    author_url = rst.xpath(
            '//div[@class="AuthorInfo-content"]/div/span/\
            div/div/a[@class="UserLink-link"]/@href' 
    )[0]
    # 点赞数
    likenum = rst.xpath('//span[@class="Voters"]/button/text()')[0]
    
    return {'name': name, 'author': author, 
            'author_url': 'http:' + author_url, 'likenum': likenum}

def parse_comment_info(data):
    ""
    提取评论信息
    """
    # 评论总数
    common_counts = data['common_counts']
    commons = list()
    rst = data['data']
    for comment in rst:
        # 作者名字
        author = comment['author']['member']['name']
        # 作者的url_token 
        url_token = comment['author']['member']['url_token']
        # 评论创建时间
        create_time = comment['created_time']
        # 评论的点赞数
        vote_count = comment['vote_count']
        info = {
                'author': author,
                'url_token': url_token,
                'create_time': create_time,
                'vote_count': vote_count
        }
        commons.append(info)
    return commons, common_counts, data['paging']['is_end']


def get_artical_info(url):
    """
    访问url获取到文章详细信息页面
    """
    return common.get(url)

def get_comment_info(artical_id, offset=0, limit=20, referer=None):
    """
    获取评论信息
    """
    host = 'https://www.zhihu.com/api/v4/articles/'
    url = (host + artical_id + '/comments?include='
            'data%5B*%5D.author%2Ccollapsed%2Creply_to_author'
            '%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count'
            '%2Cis_parent_author%2Cis_author%2Calgorithm_right'
            '&order=normal&limit=' + str(limit) + '&offset='
            + str(offset) + '&status=open')
    header = None
    if not referer:
        header = common.Iheader
        header['referer'] = referer
        header['origin'] = 'https://zhuanlan.zhihu.com'
        
    return common.get(url, True, header)

def get_artical_info_url():
    """
    获取artical_url.txt文件中的url
    """
    with open('./doc/artical_url.txt', 'r', encoding='utf-8') as fi:
        for line in fi:
            yield line.strip()

def main():
    artical_urls = get_artical_info_url()
    for url in artical_urls:
        try:
            print('新的文章请求:', url)
            html = get_artical_info(url)
            if not html:
                print('html: ', html)
                continue

            artical_info = parse_artical_info(html)
            artical_id = url.split('/')[-1]
            rst = get_comment_info(artical_id, referer=url)
            # print('rst: ', rst)
            comment_info = parse_comment_info(rst)
            artical_info['common_counts'] = comment_info[1]
            artical_info['url'] = url
            comments = list()
            comments.extend(comment_info[0])
            if not comment_info[-1]:
                offset = 0
                while True:
                    offset = offset + 20
                    rstjson = get_comment_info(
                        artical_id, offset=offset, referer=url
                    )
                    info = parse_comment_info(rstjson)
                    comments.extend(info[0])
                    if info[-1]:
                        print('完成一个文章的信息抓取...')
                        break
                    time.sleep(1)
            else:
                print('一次完成一个文章的信息抓取...')

            save_artical_comment(artical_info, comments)
            time.sleep(2)
        except Exception as err:
            print(str(err))


if __name__ == '__main__':
    starting = time.time()
    with open('./doc/artical_info.log', 'a', encoding='utf-8') as fi:
        fi.write('starting: ' + str(starting) + '\n')
    main()
    ending = time.time()
    with open('./doc/artical_info.log', 'a', encoding='utf-8') as fi:
        fi.write('ending: ' + str(ending) + '\n')
        fi.write('任务耗时: ' + str((ending - starting) / 60) + 'min\n')
