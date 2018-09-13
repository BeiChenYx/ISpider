"""
主文件：用来启动所有任务
"""
import os

import first_type
import second_type
import artical_url
import artical_info
import question_info

if __name__ == "__main__":
    if not os.path.exists('./doc'):
        os.mkdir('./doc')
        print('创建./doc文件夹')

    first_type.main()
    second_type.main()
    artical_url.main()
    artical_info.main()
    question_info.main()
