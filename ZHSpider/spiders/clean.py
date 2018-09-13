"""
清理执行结果
"""
import os

def clear_dir(path):
    """
    清空指定目录下的文件和指定的目录
    """
    if os.path.exists(path):
        files = os.listdir(path)
        for fi in files:
            os.remove(path + '/' + fi)
        print('delete %s file' % (path + '/' + fi))
        os.rmdir(path)
        print('delete %s dir' % path)

if __name__ == "__main__":
    clear_dir('./doc')
    clear_dir('./__pycache__')
