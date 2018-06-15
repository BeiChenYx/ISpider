# -*- coding: utf-8 -*-
'''
本模块为辅助模块
'''
import random


def getHeader():
    '''
    获取浏览器User-Agent
    return: 随机获取浏览器User-Agent
    '''
    userAgentList = [
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
            '537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/'
            '20100101 Firefox/46.0'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, '
            'like Gecko) Version/5.1.7 Safari/534.57.2'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML'
            ', like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'),
        ('Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like '
            'Gecko'),
        ('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; '
            'Trident/6.0)'),
        ('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; '
            'Trident/5.0)'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400QQ'
            'Browser/9.4.7658.400'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER '),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
            'Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7')
    ]

    header = {
        'Accept-Language': ('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;'
                            'q=0.3,en;q=0.2'),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': random.choice(userAgentList),
        'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                   '*/*;q=0.8'),
    }
    return header
