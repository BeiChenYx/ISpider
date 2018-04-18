'''
获取豆瓣出版社的名字
'''

import urllib.request
import re 


url = 'https://read.douban.com/provider/all'
pageData = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
# print(len(pageData))
pat = '<div class="name">(.*?)</div>'
rst_list = re.compile(pat).findall(pageData)
for rst in rst_list:
    print(rst)

