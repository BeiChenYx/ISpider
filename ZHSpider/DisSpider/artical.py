"""
访问文章详情信息，并获取评论
将信息保存到redis中去
"""
import time
import json

from lxml import etree

import common
from cache_handler import RedisHandler


class Artical(RedisHandler):
    """
    处理文章详情和评论
    """
    def __init__(self):
        RedisHandler.__init__(self)

    def read_artical_url(self):
        """
        读取Redis中的文章url
        """
        while True:
            url = self.get_articalurl()
            if url == None:
                time.sleep(3)
                continue
            yield url

    def get_artical_info(self, url):
        """
        获取文章详情页面
        """
        return common.get(url)

    def get_comment_info(self, artical_id, offset=0, 
                         limit=20, referer=None):
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

    def parse_comment_info(self, data):
        """
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

    def parse_artical_info(self, html):
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
        likenum = rst.xpath(
                '//span[@class="Voters"]/button/text()')[0]
        
        return {'name': name, 'author': author, 
                'author_url': 'http:' + author_url,
                'likenum': likenum}

    def save_result(self, artical=None, comment=None):
        if artical:
            self.push_articalinfo(json.dumps(artical))
            print('artical: ', json.dumps(artical))

        if comment:
            for val in comment:
                self.push_articalcomment(json.dumps(val))
                print('comment: ', json.dumps(val))

    def main(self):
        urls = self.read_artical_url()
        for url in urls:
            try:
                html = self.get_artical_info(url)
                if not html:
                    print('artical info: ', html)
                    continue
                artical_info = self.parse_artical_info(html)
                artical_id = url.split('/')[-1]
                rst = self.get_comment_info(
                        artical_id, referer=url
                )
                comment_info = self.parse_comment_info(rst)
                artical_info['common_counts'] = comment_info[1]
                artical_info['url'] = url
                self.save_result(artical=artical_info)
                if not comment_info[-1]:
                    offset = 0
                    count = 0
                    while True:
                        offset = offset + 20
                        rstjson = self.get_comment_info(
                            artical_id, offset=offset, referer=url
                        )
                        info = self.parse_comment_info(rstjson)
                        if info[-1]:
                            print('完成一个文章的信息抓取...')
                            break
                        count += 1
                        print('%s 完成了%d次评论请求' % (
                              artical_id, count)
                        )
                        self.save_result(comment=info[0])
                        time.sleep(1)
                else:
                    print('一次完成一个文章的信息抓取...')

                time.sleep(2)
            except Exception as err:
                print(str(err) + ': error in ' + str(__file__))


if __name__ == "__main__":
    print(__file__)
    artical = Artical()
    artical.main()
