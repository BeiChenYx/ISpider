import urllib.request
# import time
from lxml import etree


class NewsSpider(object):
    """
    request news
    """

    def __init__(self):
        self.aim_url = 'http://news.qq.com/'
        self.news_url = list()
        # self.aim_url = 'https://blog.csdn.net/'


    def first_request(self):
        """
        urllib.request方式请求
        :return:
        """
        # headers = (
        #     "User-Agent",
        #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
        # )
        # opener = urllib.request.build_opener()
        # opener.addheaders = [headers]
        # # 安装为全局
        # urllib.request.install_opener(opener)
        # urllib.request.urlretrieve(self.aim_url, './DOC/first.html')
        req = urllib.request.urlopen(self.aim_url, timeout=30)
        print('first request code is ', req.getcode())
        if req.getcode() == 200:
            data = req.read().decode('UTF-8', 'ignore')
            print(data)
            print(len(data))

    def first_requestsLib_request(self):
        import requests
        r = requests.get(self.aim_url, timeout=30)
        # r.raise_for_status()
        # print(r.text)
        print(len(r.text))
        selector = etree.HTML(r.text)
        url_select = selector.xpath('//div[@class="Q-tpList"]/div/a/@href')
        print('news_url len is ', len(url_select))
        self.news_url.extend(url_select)

        for index in range(0, len(self.news_url)):
            print(self.news_url[index])
            rst = requests.get(self.news_url[index], timeout=30)
            # rst.encoding = 'utf-8'
            with open('./DOC/{}.html'.format(index), 'wb') as file:
                file.write(rst.content)

        # with open('./DOC/first.html', 'w', encoding='utf-8') as file:
        #     file.write(r.text)


if __name__ == '__main__':
    news = NewsSpider()
    # news.first_request()
    news.first_requestsLib_request()