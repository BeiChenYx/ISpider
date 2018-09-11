"""
从artical_url.txt中获取文章详细信息的url
然后访问地址，获取文章和评论信息
文章需要提取的信息:
    文章名字
    文章作者
    文章作者的主页地址
    文章点赞数量
    文章地址
    文章评论数量

评论需要提取的信息:
    评论者名字
    评论者的url_token(定位到评论者)
    评论创建的时间
    评论点赞数量
    评论内容
"""
import common


def get_artical_info(url):
    """
    访问url获取到文章详细信息页面
    """
    common.get(url)

def get_artical_info_url():
    """
    获取artical_url.txt文件中的url
    """
    with open('./artical_url.txt', 'r', encoding='utf-8') as fi:
        for line in fi:
            yield line.strip()

def main():
    artical_urls = get_artical_info_url()
    for url in artical_urls:
        print(url)


if __name__ == '__main__':
    main()
