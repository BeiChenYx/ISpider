"""
从question_url.txt中提取问答的url地址，然后访问
提取问答数据和评论数据
问答需要提取的信息:
    问题标题
    评论数量
    关注者数量
    被浏览数量
    问题创建时间

评论需要提取的信息:
    回答者名字
    回答者url_token
    创建时间
    赞同数量
    评论数量
"""
import time

from lxml import etree

import common


def save_question_comment(question, comment):
    """
    保存问答信息和评论信息
    """
    with open('./doc/question_info.txt', 'a', encoding='utf-8') as fi:
        fi.write(
            ','.join([str(value) for _, value in question.items()])
        ) 
        fi.write('\n')

    with open('./doc/question_comment_info.txt', 'a', encoding='utf-8') as fi:
        for com in comment:
            info = [str(value) for _, value in com.items()]
            info.insert(0, question['url'])
            fi.write(','.join(info))
            fi.write('\n')

def parse_comment_info(data):
    """
    提取评论信息
    """
    rst = data['data']
    comments = list()
    for comment in rst:
        # 回答者名字
        name = comment['author']['name']
        # 回答者url_token
        url_token = comment['author']['url_token']
        # 创建时间
        create_date = comment['created_time']
        # 赞同数量
        voteup_count = comment['voteup_count']
        # 评论数量
        comment_count = comment['comment_count']
        info = {
                'name': name,
                'url_token': url_token,
                'create_date': create_date,
                'voteup_count': voteup_count,
                'comment_count': comment_count
        }
        comments.append(info)
    return comments, data['paging']['is_end']

def parse_question_info(html):
    """
    提取问答信息
    """
    rst = etree.HTML(html)
    page = '//div[@class="QuestionPage"]'
    # page = rst.xpath('//div[@class="QuestionPage"]')
    # 问题标题
    title = rst.xpath(page + '/meta[@itemprop="name"]/@content')[0]
    # 评论数量
    comment_count = rst.xpath(page
            + '/meta[@itemprop="commentCount"]/@content')[0]
    # 关注者数量
    follower_count= rst.xpath(page
            + '/meta[@itemprop="zhihu:followerCount"]/@content')[0]
    # 问题创建时间
    date_created= rst.xpath(page
            + '/meta[@itemprop="dateCreated"]/@content')[0]

    # 被浏览数量
    visits_count = rst.xpath(
            '//strong[@class="NumberBoard-itemValue"]/@title')[1]
    
    return {'title': title, 'comment_count': comment_count,
            'follower_count': follower_count,
            'date_created': date_created,
            'visits_count': visits_count}

def get_question_info(url):
    """
    获取问答的详情页面
    """
    return common.get(url)

def get_comment_info(question_id, offset=0, limit=5, referer=None):
    """
    获取评论信息
    """
    url = ('https://www.zhihu.com/api/v4/questions/%s/answers?'
            'include=data[*].is_normal,admin_closed_comment,'
            'reward_info,is_collapsed,annotation_action,annotation'
            '_detail,collapse_reason,is_sticky,collapsed_by,'
            'suggest_edit,comment_count,can_comment,content,'
            'editable_content,voteup_count,reshipment_settings,'
            'comment_permission,created_time,updated_time,review_'
            'info,relevant_info,question,excerpt,relationship.'
            'is_authorized,is_author,voting,is_thanked,is_nothelp;'
            'data[*].mark_infos[*].url;data[*].author.follower_'
            'count,badge[*].topics&offset=%s&limit=%s&sort_by='
            'default') % (
               str(question_id), str(limit), str(offset)
           )
    header = None
    if not referer:
        header = common.Iheader
        header['referer'] = referer
        header['x-requested-with'] = 'fetch'
        header['x-udid'] = 'AGDmMwbDMQ6PTgvzf0j8efogt4vh5K_aSXk='
    print(url)
    return common.get(url, True, header)

def get_question_info_url():
    """
    获取artical_url.txt文件中的url
    """
    with open('./doc/question_url.txt', 'r', encoding='utf-8') as fi:
        for line in fi:
            yield line.strip()

def main():
    question_urls = get_question_info_url()
    for url in question_urls:
        try:
            print('新的文章请求:', url)
            html = get_question_info(url)
            if not html:
                print('html: ', html)
                continue
            question_info = parse_question_info(html)
            question_info['url'] = url
            question_id = url.split('/')[-3]
            rst = get_comment_info(question_id, referer=url)
            if not len(rst):
                print('rst: ', rst)
                continue
            comment_info = parse_comment_info(rst)
            comments = list()
            comments.extend(comment_info[0])
            if not comment_info[-1]:
                offset = 0
                while True:
                    offset = offset + 5
                    rstjson = get_comment_info(
                        question_id, offset=offset, referer=url
                    )
                    info = parse_comment_info(rstjson)
                    comments.extend(info[0])
                    if info[-1]:
                        print('完成一个文章的信息抓取...')
                        break
                    time.sleep(1)
            else:
                print('一次完成一个文章的信息抓取...')

            save_question_comment(question_info, comments)
            time.sleep(2)
        except Exception as err:
            print(str(err))


if __name__ == "__main__":
    starting = time.time()
    with open('./doc/question_info.log', 'a', encoding='utf-8') as fi:
        fi.write('starting: ' + str(starting) + '\n')
    main()
    ending = time.time()
    with open('./doc/question_info.log', 'a', encoding='utf-8') as fi:
        fi.write('ending: ' + str(ending) + '\n')
        fi.write('任务耗时: ' + str((ending - starting) / 60) + 'min\n')
