# -*- coding: utf-8 -*-
'''
获取二级话题下面的文章或者问答的URL等信息
'''
import re
import sys
import os
import json
import html
import urllib.parse
from concurrent.futures import ThreadPoolExecutor as Pool

import requests
from lxml import etree

import helpFunction
import topicModels


class ArticleQuestion(object):
    '''
    请求二级话题的URL获取话题下面的文章或问答的URL等信息
    '''
    def __init__(self, topicNames, topicUrls):
        self.urls = topicUrls
        self.names = topicNames

    def getAllUrl(self):
        '''
        获取所有话题url的初次访问的结果，在结果中找到获取所有文章
        和问答的翻页请求地址的参数，根据这个结果可以请求到所有的
        文章和问答的简单描述信息以及具体内容的URL
        return: url的参数, 格式如下:
        [('19672708',
        'data[?(target.type....target.comment_count',
        '5',
        '4093.73878'), (...), ]
        '''
        def _getSecondApi(url):
            '''
            访问二级话题的URL获得话题的API地址
            '''
            rst = requests.get(url, headers=helpFunction.getHeader())
            # 将结果中的数据都进行解码
            rstDecode = urllib.parse.unquote(rst.text)
            # 将结果中的html标签和字符实体等进行解码
            # 完成后赋值个rst，这样就促使解析器回收之前的对象
            rst = html.unescape(rstDecode)
            # 二级话题下面的文章或问答信息URL参数
            patParms = ('http://.*?/topics/([0-9]+)/.*?/top_activity\?'
                        'include=(.*?)\&limit=([0-9]+)\&after_id=([0-9.]+)')
            # 获取到文章或者问答的URL参数
            parms = re.compile(patParms).findall(rst)
            return parms
        rst = Pool(max_workers=10).map(_getSecondApi, self.urls)
        return [item[0] for item in rst if item]

    def _parseData(self, data):
        '''
        解析具体的单个文章或问答的描述信息
        return: 详细网页的的URL类别和URL
        '''
        print('--------_parseData---------')
        if 'question' in data['target'].keys():
            questionId = data['target']['target']['question']['id']
            link = r'https://www.zhihu.com/question/%s/answer/%s' % (
                questionId, data['target']['target']['id']
            )
            questionName = data['target']['question']['title']
            questionLikenum = data['target']['voteup_count']
            questionCommentnum = data['target']['comment_count']
            questionLink = link
            questionCreated = data['target']['question']['created']
            # 查找页面总数
            # 入库， 简述信息太多，批量插入会大量消耗内存
            self.topicDb.insertQuestionDec(
                questionName, questionLikenum, questionCommentnum,
                questionLink, questionCreated)
            print('question', questionLink)
            return ('question', questionLink)
        else:
            articleName = data['target']['title']
            articleLikenum = data['target']['voteup_count']
            articleCommentnum = data['target']['comment_count']
            articleLink = data['target']['url']
            articleCreated = data['target']['created']
            self.topicDb.insertArticleDec(
                articleName, articleLikenum, articleCommentnum,
                articleLink, articleCreated)
            print('article', articleLink)
            return ('article', articleLink)

    def _parseRequestPage(self, response):
        '''
        解析单个_requestPage的结果
        return: 下一页URL， 总页面个数， 详情URL信息
        '''
        print('-------_parseRequestPage------')
        try:
            # 将结果中的数据都进行解码
            rstDecode = urllib.parse.unquote(response)
            #将结果中的html标签和字符实体等进行解码
            # 完成后赋值个rst，这样就促使解析器回收之前的对象
            rst = html.unescape(rstDecode)
            rst = json.loads(rst)
            print(type(rst), ' : ', rst)
            nextPageUrl = rst['paging']['next']
            pageTotals = int(rst['paging']['totals']) // 5
            descrition = map(self._parseData, rst['data'])
            return (nextPageUrl, pageTotals, descrition)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return '', 0, ''

    def _requestPage(self, getData):
        '''
        此方法模拟单个话题的翻页功能，从而获取到文章和问答的描述信息
        '''
        print('-----requestGetAllUrl ---> _requestPage-----')
        try:
            thisurl = (r'https://www.zhihu.com/api/v4/topics/%s/feeds'
                       '/top_activity' % getData[0])
            header = helpFunction.getHeader()
            # print('header is : ' + str(header))
            header['authorization'] = ('oauth c3cef7c6'
                                       '6a1843f8b3a9e6a1e3160e20')
            rst = requests.get(url=thisurl, headers=header, params={
                               'include': getData[1],
                               'limit': getData[2],
                               'after_id': getData[3]})
            rstInfo = []
            # 拿到了第一页数据，以及页面总数
            nextPageUrl, pageTotals, rstNext = self._parseRequestPage(rst.text)
            rstInfo.append(rstNext)
            # 循环获取单个话题的所有数据
            pageUrl = [nextPageUrl, ]
            for i in range(0, pageTotals):
                try:
                    print('pageUrl is :', pageUrl[i])
                    rstNextPage = requests.get(url=pageUrl[i],
                                               headers=helpFunction.getHeader())
                    if len(rstNextPage.text) < 200:
                        continue
                    else:
                        nextPageUrl, _, rstNext = self._parseRequestPage(rstNextPage.text)
                        pageUrl.append(nextPageUrl)
                        rstInfo.append(rstNext)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
            return rstInfo
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return []

    def requestGetAllUrl(self, getParams):
        '''
        通过翻页来获取所有的文章和问答描述信息
        return: 文章或话题的名称和文章或话题URL列表
        '''
        return Pool(max_workers=10).map(self._requestPage, getParams)

    def main(self):
        '''
        此类的入口函数，获取问题或文章的描述信息
        return: 文章或话题的名称及文章或话题的详情URL
        '''
        myhost = 'mysql+pymysql://root:11223@localhost:3306/testAPI?charset=utf8'
        self.topicDb = topicModels.TopicModel(host=myhost, cmdEcho=False)
        decInfo = []
        try:
            params = self.getAllUrl()
            # print('main: ' + str(params))
            decInfo.append(self.requestGetAllUrl(params))
        except Exception as e:
            print(e)
        finally:
            return decInfo
