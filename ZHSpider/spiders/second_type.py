"""
获取所有二级类别信息
"""
import json
import re
import time

import common


def save_result(info):
    """
    保存二级类别
    """
    with open('secondType.txt', 'a', encoding='utf-8') as fi:
        for line in info:
            fi.write(line+'/hot\n')

def parse_result(data):
    """
    提取二级类别的地址
    """
    urls = list()
    for msg in data:
        url = re.findall('<a target="_blank" href="(.*?)">', msg)
        urls.append(url[0])
    return urls

def get_second_type(data_id, offset):
    """
    获取二级类别的地址
    """
    url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
    params = '{"topic_id": %d,"offset": %d,"hash_id": ""}'
    postData = {'method': 'next', 'params': params % (int(data_id), int(offset))}
    rst = common.post(url, isjson=True, formdata=postData)
    if rst:
        return rst['msg']
    else:
        return ''

def get_data_id(path):
    """
    获取二级类别的topic_id
    """
    data = dict()
    with open(path, 'r', encoding='utf-8') as fi:
        info = json.load(fi)
        data.update(info)
    for info in data['info']:
        yield info['data-id']

def main():
    topic_ids = get_data_id('./firstType.json')
    for topic_id in topic_ids:
        offset = 0
        print('topic_id strart: ', topic_id)
        while True:
            msg = get_second_type(topic_id, offset)
            if not len(msg):
                break
            offset += 20
            urls = parse_result(msg)
            save_result(urls)
            time.sleep(3)


if __name__ == '__main__':
    starting = time.time()
    with open('./second_type.log', 'a', encoding='utf-8') as fi:
        fi.write('starting: ' + str(starting) + '\n')
    main()
    ending = time.time()
    with open('./second_type.log', 'a', encoding='utf-8') as fi:
        fi.write('ending' + str(ending) + '\n')
        fi.write('任务耗时: ' + str((ending - starting) / 60 + 'min\n'))
