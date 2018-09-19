"""
主要功能模块，负责启动项目访问知乎一级类别
并将数据存储到Redis缓存中去
"""
from first import First


def main():
    # 创建Redis对象，并连接Redis
    # iredis = RedisHandler(host='120.79.7.88', port=6378)

    # 执行第一个类别请求
    # first_result = first.main()
    # print(first_result)
    # for value in first_result:
        # iredis.push_onetopic(value)
        # print(value)
    first = First()
    first.main()


if __name__ == "__main__":
    main()
