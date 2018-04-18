'''
初步分析，尝试获取
'''
import urllib.request
from lxml import etree
import time
import json


aimUrl = 'https://blog.csdn.net/'

# 添加浏览器伪装
header = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0')
opener = urllib.request.build_opener()
opener.addheaders = [header]

# urllib.request.urlretrieve(aimUrl, './home.html')
aimData = urllib.request.urlopen(aimUrl).read()
etreeAimData = etree.HTML(aimData.decode('utf-8', 'ignore'))
# 获取文章名字
blogTitleAll = etreeAimData.xpath('//h2[@class="csdn-tracking-statistics"]/a/text()')
# for blogTitle in blogTitleAll:
#     print(blogTitle)

print('All blog is ', len(blogTitleAll))

# 获取博客的所有链接
linkPat = '//h2[@class="csdn-tracking-statistics"]/a/@href'
blogLinkAll = etreeAimData.xpath(linkPat)

for blogLink in blogLinkAll:
    print(blogLink)

print('All blog link\' len is ', len(blogLinkAll))
# time.sleep(2)

# 动态加载后再次获取新的数据 ?type = more & category = home & shown_offset = 1523364890754806
updateUrl = 'https://blog.csdn.net/api/articles?type=more&category=home&shown_offset={}'
for count in range(1, 11):
    print('第', count, '提取')
    nowTimelist = str(time.time()).split('.')
    nowTime = ''.join(nowTimelist)
    updateData = urllib.request.urlopen(updateUrl.format(nowTime)).read().decode('utf-8', 'ignore')
    # print('updateData len is ', len(updateData))

    neadArticlesList = list()
    try:
        updateBlog = json.loads(updateData)
        # with open('blog.json', 'w') as blogFile:
        #     json.dump(updateBlog, blogFile)
        # print('updateBlog type is dict? ', isinstance(updateBlog, dict))
        if isinstance(updateBlog, dict):
            print('提取文章url')
            articlesList = updateBlog['articles']
            # print('articlesList len is ', len(articlesList))

            for article in articlesList:
                neadArticlesList.append(article['url'])
                # print(article['title'], ':', article['url'])

    except Exception as err:
        print(err)

    # 循环获取文章
    i = 0
    for blogLinkVal in neadArticlesList:
        print(str(count * 10 + i), ': ', blogLinkVal)
        urllib.request.urlretrieve(aimUrl, './blog/' + str(count * 10 + i) + '.html')
        i = i + 1
    count = count + 1
