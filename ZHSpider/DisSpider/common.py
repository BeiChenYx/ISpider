"""
公用信息
"""
import requests

# 访问的请求头
Iheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #'Host': 'www.zhihu.com',
    #'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'
}

# 域名
domain_name = 'https://www.zhihu.com'

def get(url, isjson=False, header=None):
    """
    获取url的页面
    """
    # print('get url: ', url)
    if header:
        rst = requests.get(url, headers=header, timeout=15)
    else:
        rst = requests.get(url, headers=Iheader, timeout=15)
    print('rst.status_code: ', rst.status_code)
    if rst.status_code == 200:
        if isjson:
            return rst.json()
        else:
            return rst.text
    return ''

def post(url, formdata, isjson=False):
    """
    post方式访问
    :url 需要访问的地址
    :formdata 需要提交的数据, 字典格式
    """
    # print('url: ', url)
    # print('formdata: ', formdata)
    rst = requests.post(url, data=formdata,headers=Iheader)
    print('rst.status_code: ', rst.status_code)
    if rst.status_code == 200:
        if isjson:
            return rst.json()
        else:
            return rst.text
    return ''
