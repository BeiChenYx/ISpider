"""
主要功能模块，负责启动项目访问知乎一级类别
并将数据存储到Redis缓存中去
"""
from multiprocessing import Process

from first import First
from second import Second
from title_filter import TitleFilter
from artical import Artical
from question import Question


def main():
    first = First()
    second = Second()
    title_filter = TitleFilter()
    artical = Artical()
    question = Question()
    objects = [first, second, title_filter, artical, question]

    tasks = list()
    for obj in objects:
        task = Process(target=obj.main) 

    for pro in tasks:
        pro.start()

    for pro in tasks:
        pro.join()


if __name__ == "__main__":
    main()
