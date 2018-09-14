"""
主要功能模块，负责启动项目访问知乎一级类别
并将数据存储到Redis缓存中去
"""
import common
import first

def main():
    # 目标地址
    url = 'https://www.zhihu.com/topics'
    html = common.get(url)
    first_result = first.parse_page(html)
    print(first_result)




if __name__ == "__main__":
    main()
