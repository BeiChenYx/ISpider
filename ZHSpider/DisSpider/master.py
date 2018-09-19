"""
主要功能模块，负责启动项目访问知乎一级类别
并将数据存储到Redis缓存中去
"""
from first import First


def main():
    first = First()
    first.main()


if __name__ == "__main__":
    main()
