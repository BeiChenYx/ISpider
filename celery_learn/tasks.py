# coding: utf-8
"""
学习celery使用
"""
from celery import Celery

app = Celery('tasks',backend='amqp', broker='amqp://guest@localhost//')

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CLEARY_ACCEPT_CONTENT=['json'],
    CLEARY_RESULT_SERIALIZER='json',
    CLEARY_TIMEZONE='Asia/Shanghai',
    CLEARY_ENABLE_UTC=True,
)

@app.task
def add(x, y):
    return x + y
