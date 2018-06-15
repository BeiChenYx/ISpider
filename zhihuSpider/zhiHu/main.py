# -*- coding: utf-8 -*-
'''本文件为知乎爬虫的主要执行入口
重构之前的scrapy模块的爬虫
任务层级关系：
1.爬取所有的话题(一级话题和二级话题)，入库
2.根据第一步爬取的话题url，去获取话题对应的文章或问题的名称及地址，入库
3.根据第二部的文章或问题的地址，获取详细信息，入库
'''
import topicUrl
import topicDec
from topicModels import TopicModel


if __name__ == '__main__':
    # TODO：myhost 放到配置文件中读取
    myhost = 'mysql+pymysql://root:11223@localhost:3306/testAPI?charset=utf8'
    topicDb = TopicModel(host=myhost, cmdEcho=False)
    topicObject = topicUrl.ZhiHuTopic(topicDb)
    # 话题的名称和URL列表
    topicInfo = topicObject.main()
    # print(topicInfo)
    decObject = topicDec.ArticleQuestion(topicInfo[0][0], topicInfo[0][1])
    decInfo = decObject.main()
