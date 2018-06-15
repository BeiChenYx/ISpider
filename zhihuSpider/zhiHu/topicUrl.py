# -*- coding: utf-8 -*-
'''
此模块为获取知乎的一级二级话题的信息
'''
from concurrent.futures import ThreadPoolExecutor as Pool

import requests
from lxml import etree

import helpFunction
from topicModels import TopicModel


class ZhiHuTopic(object):
    '''获取知乎话题信息'''
    def __init__(self, topicModel):
        self.start_url = 'https://www.zhihu.com/topics'
        self.aim_url = 'https://www.zhihu.com'
        self.topicModel = topicModel

    def start_requests(self):
        '''获取初次话题的页面'''
        return requests.get(self.start_url, headers=helpFunction.getHeader())

    def parseStartRequests(self, response):
        '''
        解析start_requests响应的数据并获取一级话题的URL列表
        :param response: start_requests请求的响应
        :return: 返回一级话题名称和一级话题的id
        '''
        print('请求 ' + str(response.url) + ' 完成')
        # 一级话题xpath表达式
        firstTopicXpath = '//li[@class="zm-topic-cat-item"]/a/text()'
        # 一级话题id的xpath表达式
        firstTopicIdXpath = '//li[@class="zm-topic-cat-item"]/@data-id'
        selector = etree.HTML(response.text)
        # 提取一级话题和话题ID
        firstTopic = selector.xpath(firstTopicXpath)
        firstTopic = firstTopic if firstTopic else ['null']
        firstTopicId = selector.xpath(firstTopicIdXpath)
        firstTopicId = firstTopicId if firstTopicId else ['null']
        return (firstTopic, firstTopicId)

    def secondTopicUrl_requests(self, firstTopicName, firstTopicId):
        '''
        获取所有的二级话题的URL及名称
        param: firstTopicId 一级话题的id列表
        param: firstTopicName 一级话题的名字列表
        return: 话题的名称和URL列表
        '''
        def _parseMsg(firstTopicName, msg):
            '''
            提取每个二级话题的名字和URL地址
            话题的名字和URL地址在此存储
            return: 返回单个话题的Name(拼接了一级话题和二级话题)和URL
            '''
            selector = etree.HTML(msg)
            secondName = selector.xpath('//div[@class="blk"]/'
                                        'a[@target="_blank"]'
                                        '/strong/text()')
            secondName = secondName if secondName else ['null']
            secondLink = selector.xpath('//div[@class="blk"]'
                                        '/a[@target="_blank"]/@href')
            secondLink = secondLink if secondLink else ['null']
            topicName = firstTopicName + '/' + secondName[0]
            topicLink = self.aim_url + secondLink[0] + '/hot'
            print(topicName, ': ', topicLink)
            return (topicName, topicLink)

        def _requestPost(parms):
            firstTopicName = parms['firstTopicName']
            del parms['firstTopicName']
            secondUrl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
            rst = requests.post(url=secondUrl, data=parms,
                                headers=helpFunction.getHeader())
            if rst.status_code != 200:
                return ([], [])
            if len(rst.text) <= 20:
                # Requests的响应内容小于20个长度表明已经没有二级话题了
                print('error: ', secondUrl, str(parms))
                return ([], [])
            rst = rst.json()
            topicNameList = []
            topicUrlList = []
            for msg in rst['msg']:
                msgRst = _parseMsg(firstTopicName, msg)
                topicNameList.append(msgRst[0])
                topicUrlList.append(msgRst[1])
            return (topicNameList, topicUrlList)

        topicUrl = []
        parmsAll = []
        # 测试循环一次， 正式使用len(firstTopicId)
        for index in range(1):
            # 测试循环一次，正式使用50
            for i in range(1):
                topic_id = int(firstTopicId[index])
                parms = '{"topic_id": %d,"offset": %d,"hash_id": ""}'
                urlParms = {
                    'method': 'next',
                    'params': parms % (topic_id, i * 20),
                    'firstTopicName': firstTopicName[index]
                }
                parmsAll.append(urlParms)

        pool = Pool(max_workers=10)
        results = pool.map(_requestPost, parmsAll)
        for rst in results:
            if not rst[0] or not rst[1]:
                continue
            self.topicModel.insertTopicInfo(rst[0], rst[1])
            topicUrl.append((rst[0], rst[1]))
        return topicUrl

    def main(self):
        '''
        此类的入口函数，获取话题的名字和URL地址
        return: 话题的名称和URL列表
        '''
        topicInfo = []
        try:
            rst = self.start_requests()
            firstTopicInfo = self.parseStartRequests(rst)
            topicInfo = self.secondTopicUrl_requests(*firstTopicInfo)
        except Exception as e:
            print(e)
        finally:
            return topicInfo


if __name__ == '__main__':
    myhost = 'mysql+pymysql://root:11223@localhost:3306/testAPI?charset=utf8'
    topicDb = TopicModel(host=myhost, cmdEcho=False)
    topicObject = ZhiHuTopic(topicDb)
    topicInfo = topicObject.main()
