"""
公用信息
"""

# 访问的请求头
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    'referer': 'https://www.zhihu.com/topics',
    'origin': 'https://www.zhihu.com',
}

# 域名
domain_name = 'https://www.zhihu.com'

def get(url, json=False):
    """
    获取url的页面
    """
    rst = requests.get(url, headers=header)
    print('rst.status_code: ', rst.status_code)
    if rst.status_code == 200:
        if json:
            return rst.json
        else:
            return rst.text
    return ''