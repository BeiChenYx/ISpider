"""
获取zh:twotopic中的二级类别下面的文章或问答的url地址
然后保存到Redis中去
"""
import re
import time

from lxml import etree

import common
from cache_handler import RedisHandler


class TitleFilter(RedisHandler):
    """
    获取二级类别下面的文章或问答的url地址
    """
    def __init__(self):
        RedisHandler.__init__(self)
        self.referer = 'https://www.zhihu.com/topics'

    def read_second_url(self):
        """
        读取Redis中的二级类别的url
        """
        while True:
            line = self.get_twotopic()
            if line == None:
                break
            yield common.domain_name + line + '/hot'

    def get_second_info(self, url):
        """
        访问二级类别的详细页面，获取初次加载的文章url以及
        后续文章url的请求地址
        """
        print('title_filter url is: ', url)
        header = common.Iheader
        header['referer'] = self.referer
        header['Connection'] = 'keep-alive'
        header['Host'] = 'www.zhihu.com'
        header['Upgrade-Insecure-Requests'] = '1'
        html = common.get(url, header=header)

        return html

    def parse_first_url(self, html):
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
                artical_url = item.xpath(
                    './div/h2[@class="ContentItem-title"]/a/@href'
                )
                artical_list.append('http:' + artical_url[0])
                print('parse_first_url artical_url is: ', 
                       artical_url[0])
            else:
                # 内容为问题
                question_url = item.xpath('./div/h2/div/a/@href')
                print(question_url)
                question_list.append(
                        common.domain_name + question_url[0]
                )
                print('parse_first_url question_url is: ', 
                       question_url[0])

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

    def get_paging_url(self, url, referer):
        """
        获取url指定的信息，然后通过翻页的方
        式获取下一个动态加载的文章url
        :url 需要访问的接口
        :referer 二级话题的url
        """
        header = common.Iheader
        header['referer'] = referer
        rst = common.get(url, isjson=True, header=header)
        if rst == '':
            return None
        # 数据中有两种数据，分别是问答和文章两种，需要分开处理
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
                print('get_artical_url question_url is: ', 
                       question_url)
            elif data['target']['type'] == 'article':
                artical_url =  data['target']['url']
                artical_list.append(artical_url)
                print('get_artical_url artical_url is: ',
                       artical_url)
            else:
                print('检测到异常类型....')
        next_url = rst['paging']['next']
        is_end = rst['paging']['is_end']
        return artical_list, question_list, next_url, is_end

    def save_result(self, artical, question):
        """
        将结果保存到Redis中去
        """
        for val in artical:
            self.push_articalurl(val)
            print('save artical: ', val)

        for val in question:
            self.push_questionurl(val)
            print('save question: ', val)

    def main(self):
        urls = self.read_second_url()
        for line in urls:
            try:
                html = self.get_second_info(line)
                if not html:
                    continue
                info_first = self.parse_first_url(html) 
                self.save_result(info_first[0], info_first[1])
                
                task_url = [info_first[-1], ]
                while True:
                    if len(task_url) == 0:
                        break
                    url = task_url.pop()
                    info_paging = self.get_paging_url(url, line)
                    if not info_paging:
                        continue
                    self.save_result(info_paging[0], info_paging[1])
                    if info_paging[-1]:
                        break
                    task_url.insert(0, info_paging[-2])
                    time.sleep(2)

                time.sleep(1)
            except Exception as err:
                print(str(err))


if __name__ == "__main__":
    title = TitleFilter()
    title.main()
