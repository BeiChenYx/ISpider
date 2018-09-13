"""
清理执行结果
"""
import os

if __name__ == "__main__":
    files = os.listdir('./doc')
    for fi in files:
        os.remove('./doc/' + fi)
        print('delete %s file' % ('./doc/' + fi))
