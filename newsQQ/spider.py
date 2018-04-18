import urllib.request
import time

class NewsSpider(object):
    """
    request news
    """

    def __init__(self):
        # self.aim_url = 'http://news.qq.com/'
        self.aim_url = 'https://blog.csdn.net/'
        # headers = (
        #     "User-Agent",
        #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"
        # )
        # opener = urllib.request.build_opener()
        # opener.addheaders = [headers]
        # # 安装为全局
        # urllib.request.install_opener(opener)

    def first_request(self):
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
        print(r.text)
        print(len(r.text))


if __name__ == '__main__':
    news = NewsSpider()
    # news.first_request()
    news.first_requestsLib_request()