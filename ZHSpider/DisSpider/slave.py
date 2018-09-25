"""
slave
"""
from multiprocessing import Process

from first import First
from second import Second
from title_filter import TitleFilter
from artical import Artical
from question import Question


def main():
    # first = First()
    second = Second()
    title_filter = TitleFilter()
    artical = Artical()
    question = Question()
    objects = [second, title_filter, artical, question]

    tasks = list()
    for obj in objects:
        task = Process(target=obj.main) 
        tasks.append(task)

    for pro in tasks:
        pro.start()

    for pro in tasks:
        pro.join()


if __name__ == "__main__":
    main()
