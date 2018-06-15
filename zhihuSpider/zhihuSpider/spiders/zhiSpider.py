# -*- coding: utf-8 -*-
import re
import json
from lxml import etree

import requests
import urllib.parse
import scrapy
from scrapy.http import Request

from .sqlOpertion import MysqlOperation
from zhihuSpider.items import ZhihuspiderItem


class ZhispiderSpider(scrapy.Spider):
    name = 'zhiSpider'
    allowed_domains = ['zhihu.com']

    def __init__(self):
        self.myurl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
        self.header = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;\
            q=0.3,en;q=0.2',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) \
            Gecko/20100101 Firefox/57.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
            */*;q=0.8',
        }

    def start_requests(self):
        return [Request('https://www.zhihu.com/topics', headers=self.header,
                callback=self.parseTopics)]

    def parseTopics(self, response):
        '''开始分析话题'''
        topicsList = response.xpath('//li[@class="zm-topic-cat-item"]/a/text()').extract()
        topicDataId = response.xpath('//li[@class="zm-topic-cat-item"]/@data-id').extract()
        params = '{"topic_id": %d,"offset": %d,"hash_id": ""}'
        urlNext = []
        for index in range(0, 1):  # 获取所有的一级话题len(topicsList)
            for i in range(0, 1):  # 最多获取50个二级话题
                try:
                    data_id = int(topicDataId[index])
                    postData = {'method': 'next', 'params': params % (data_id, i * 20)}
                    rst = requests.post(url=self.myurl, data=postData, headers=self.header)
                    if len(rst.text) <= 20:
                        break
                    # 提取话题数据
                    rst = rst.json()
                    for msgIndex in range(0, len(rst['msg'])):
                        selector = etree.HTML(rst['msg'][msgIndex])
                        topicName = selector.xpath('//div[@class="blk"]/a[@target="_blank"]/strong/text()')
                        topicLink = selector.xpath('//div[@class="blk"]/a[@target="_blank"]/@href')
                        item = ZhihuspiderItem()
                        if (len(topicName) == 0 or len(topicsList[index]) == 0
                                or len(topicLink) == 0):
                            item['topicCategory'] = 'not-found'
                            item['topicLink'] = 'not-found'
                        else:
                            item['topicCategory'] = topicsList[index] + '/' + topicName[0]
                            item['topicLink'] = 'https://www.zhihu.com' + topicLink[0] + '/hot'
                        # 去处理每个单独页面
                        urlNext.append(item['topicLink'])
                        yield item
                except Exception as e:
                    print('parseTopics: ' + str(e))
        for indexUrl in urlNext:
            try:
                rstTopic = requests.get(url=indexUrl, headers=self.header)
                # print(rstTopic.text.encode(rstTopic.encoding).decode('utf-8'))
                self.parseArticle(urllib.parse.unquote(rstTopic.text), item['topicLink'], item['topicCategory'])
            except Exception as e:
                print('line 74 :' + str(e))


    def parseArticle(self, response, referUrl, topicCategory):
        '''提取二级类别下面的所有文章或者问题的url并去解析数据'''
        parNextUrl = '(http://www.zhihu.com/api/v[0-9]/topics/[0-9]+/feeds/top_activity)\?include=(.*?)\&amp;limit=(.*?)\&amp;'\
                     'after_id=([0-9.]+)'
        nextUrl = re.compile(parNextUrl).findall(response)
        print('nextUrl:  ' + str(nextUrl))
        header = self.header
        try:
            header['authorization'] = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
            thisUrl = re.sub('http', 'https', nextUrl[0][0])
            include = nextUrl[0][1]
            limit = nextUrl[0][2]
            after_id = nextUrl[0][3]
            rstNext = requests.get(url=thisUrl, headers=header, params={
                'include': include,
                'limit': limit,
                'after_id': after_id})
            nextData = json.loads(rstNext.text)
            self.parseData(thisData=nextData, Category=topicCategory)
            # 提取二级类别下面的所有数据，通过接口循环访问所有的api
            nextPageUrl = nextData['paging']['next']
            # 每次访问读取五个文章或者问题
            nextPageTotals = int(nextData['paging']['totals']) // 5
            nextPageUrlList = [nextPageUrl, ]
            for j in range(0, nextPageTotals):
                # print(nextPageUrlList[j])
                rstNextPage = requests.get(url=nextPageUrlList[j], headers=header)
                nextPageData = json.loads(rstNextPage.text)
                nextPageUrlList.append(nextPageData['paging']['next'])
                self.parseData(thisData=nextPageData, Category=topicCategory)
        except Exception as e:
            print('parseArticle :  ' + str(e))

    def parseData(self, thisData, Category):
        print('数据个数为： ' + str(len(thisData['data'])))
        sqlOperation = MysqlOperation()
        sqlOperation.connectDB()
        for i in range(0, len(thisData['data'])):
            try:
                sqlStr = ''
                if 'question' in thisData['data'][i]['target'].keys():
                    questionId = thisData['data'][i]['target']['question']['id']
                    link = r'https://www.zhihu.com/question/%s/answer/%s' % (
                        questionId, thisData['data'][i]['target']['id']
                    )
                    sqlStr = 'insert into QuestionDec(topicCategory, '\
                             'ArticleName, ArticleLikenum, ArticleCommentnum, '\
                             'ArticleLink, IsArticle, Created) '\
                             'values(\"%s\", \"%s\", \"%d\", \"%d\"'\
                             ', \"%s\", \"%s\", "%s\");' % (
                        Category,
                        thisData['data'][i]['target']['question']['title'],
                        thisData['data'][i]['target']['voteup_count'],
                        thisData['data'][i]['target']['comment_count'],
                        link,
                        thisData['data'][i]['target']['question']['type'],
                        thisData['data'][i]['target']['question']['created'])
                    # 处理问答数据
                    self.processQuestion(link, questionId)
                else:
                    targetUrl = thisData['data'][i]['target']['url']
                    sqlStr = 'insert into ArticleDec(topicCategory, '\
                             'ArticleName, ArticleLikenum, ArticleCommentnum,'\
                             ' ArticleLink, Created) '\
                             'values(\"%s\", \"%s\", \"%d\", \"%d\"'\
                             ', \"%s\", \"%s\");' % (
                        Category,
                        thisData['data'][i]['target']['title'],
                        thisData['data'][i]['target']['voteup_count'],
                        thisData['data'][i]['target']['comment_count'],
                        targetUrl,
                        thisData['data'][i]['target']['created']
                    )
                    sqlOperation.execute(self.processArticale(targetUrl))
                # 入库\
                sqlOperation.execute(sqlStr)
                # print(sqlStr)
            except Exception as e:
                print('json解析出错' + str(e))
        sqlOperation.closeDB()

    def processQuestion(self, questionUrl, questionId):
        ''' 提取问题的标题，问题内容，答案作者，答案内容 '''
        sqlOperation = MysqlOperation()
        sqlOperation.connectDB()
        rstQuestion = requests.get(url=questionUrl, headers=self.header)
        selector = etree.HTML(rstQuestion.text)
        questionName = selector.xpath('//h1[@class="QuestionHeader-title"]/text()')
        questionInfo = selector.xpath('//span[@class="RichText"]/text()')
        answer = selector.xpath('//div[@id="null-toggle"]/a[@class="UserLink-link"]/text()')
        answerContent = selector.xpath('//div[@class="RichContent-inner"]')[0]
        answerContentInfo = answerContent.xpath('string(.)')

        # 初次加载的会出现三个评论, 使用循环处理可以避免列表越界问题
        for i in range(0, len(answer)):
            sqlStr = 'insert into AnswerInfo(questionName, '\
                     'questionInfo, answer, answerContentInfo) '\
                     'values(\"%s\", \"%s\", \"%s\", \"%s\");' % (
                     questionName[i], questionInfo[i],
                     answer[i], answerContentInfo[i])
            sqlOperation.execute(sqlStr)
            print(sqlStr)

        firstCommentUrl = r'https://www.zhihu.com/api/v4/questions/%s/answers' % questionId
        include = 'data[*].is_normal,admin_closed_comment,reward_info,'\
                   'is_collapsed,annotation_action,annotation_detail,'\
                   'collapse_reason,is_sticky,collapsed_by,suggest_edit,'\
                   'comment_count,can_comment,content,editable_content,'\
                   'voteup_count,reshipment_settings,comment_permission,'\
                   'created_time,updated_time,review_info,relevant_info,'\
                   'question,excerpt,relationship.is_authorized,is_author,'\
                   'voting,is_thanked,is_nothelp,upvoted_followees;data[*].'\
                   'mark_infos[*].url;data[*].author.follower_count,'\
                   'badge[?(type=best_answerer)].topics'
        # offset = ''
        limit = 3
        sort_by = 'default'
        header = self.header
        header['authorization'] = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
        rstNext = requests.get(url=firstCommentUrl, headers=header, params={
            'include': include, 'limit': limit, 'sort_by': sort_by})
        nextData = json.loads(rstNext.text)
        totals = 0
        for dataIndex in range(0, len(nextData['data'])):
            try:
                authorAnserName = nextData['data'][dataIndex]['author']['name']
                anserComment = nextData['data'][dataIndex]['content']
                # 获取总数
                totals = int(nextData['paging']['totals'])
                # 获取第一批评论
                sqlStr = 'insert into AnswerInfo(questionName,\
                          questionInfo, answer, answerContentInfo)\
                          values(\"%s\", \"%s\", \"%s\", \"%s\");\
                          ' % (questionName, questionInfo,
                               authorAnserName, anserComment)
                sqlOperation.execute(sqlStr)
                print(authorAnserName)
            except Exception as e:
                print(e)
        # 根据上面获取的总数，去请求剩下的评论
        for i in range(0, totals):
            try:
                rstNext = requests.get(url=firstCommentUrl, headers=header,
                                       params={'include': include,
                                               'limit': limit,
                                               'offset': 3 * i,
                                               'sort_by': sort_by})
                thisData = json.loads(rstNext.text)
                for dataIndex in range(0, len(thisData['data'])):
                    try:
                        authorAnserName = thisData['data'][dataIndex]['author']['name']
                        anserComment = thisData['data'][dataIndex]['content']
                        print(authorAnserName)
                        # 入库
                        sqlStr = 'insert into AnswerInfo(questionName,\
                                  questionInfo, answer, answerContentInfo)\
                                  values(\"%s\", \"%s\", \"%s\", \"%s\");' % (
                                  questionName, questionInfo,
                                  authorAnserName, anserComment)
                        sqlOperation.execute(sqlStr)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

        sqlOperation.closeDB()

    def processArticale(self, ArticleUrl):
        ''' 提取文章的数据 '''
        # 'https://zhuanlan.zhihu.com/api/posts/33240331/comments?limit=10&offset=0'
        # 'https://zhuanlan.zhihu.com/p/33240331'
        # targetId = re.split(r'/', ArticleUrl)[-1]
        rstArticale = requests.get(url=ArticleUrl, headers=self.header)
        selector = etree.HTML(rstArticale.text)
        articleName = selector.xpath('//h1[@class="PostIndex-title av-paddingSide av-titleFont"]/text()')
        # print(articleName)
        articleAthor = selector.xpath('//a[@class="PostIndex-authorName"]/text()')
        # print(articleAthor)
        articleContent = selector.xpath('//div[@class="RichText PostIndex-content av-paddingSide av-card"]')[0]
        articleContentInfo = articleContent.xpath('string(.)')
        # print(articleContentInfo)
        sqlStr = 'insert into ArticleDetailInfo(title,'\
                 'author, content)'\
                 'values(\"%s\", \"%s\", \"%s\");' % (articleName,
                                                articleAthor,
                                                articleContentInfo)
        return sqlStr
