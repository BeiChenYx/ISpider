"""
公用信息
"""
import requests

# 访问的请求头
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    'referer': 'https://www.zhihu.com/topics',
    'origin': 'https://www.zhihu.com',
}

# 域名
domain_name = 'https://www.zhihu.com'


def get(url, isjson=False):
    """
    获取url的页面
    """
    rst = requests.get(url, headers=header)
    print(url)
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
    rst = requests.post(url, data=formdata,headers=header )
    print('rst.status_code: ', rst.status_code)
    if rst.status_code == 200:
        if isjson:
            return rst.json()
        else:
            return rst.text
    return ''