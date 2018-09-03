# Celery框架官方学习笔记

```text
版本信息: Celery 4.2.0
```

## Configuration

Celery配置方法

直接使用配置值进行配置

```python
app.conf.enable_utc = True
```

也可以使用update配置多个变量

```python
app.conf.update(
    enable_utr=True,
    timezone='Asia/Shanghai',
)
```

使用配置模块文件的方式

```python
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig')
```

对于Celery配置模块文件一般使用celeryconfig.py名称:
```python
enable_utc = True
timezone = 'Asia/Shanghai'
```
* 此方法为比较常用的配置方式

也可以使用配置类:
```python
import celery import Celery

app = Celery()

class Config:
    enable_utc = True
    timezone = 'Asia/Shanghai'

app.config_from_object(Config)
```

Celery的应用实例是惰性的，在创建实例时只操作四个方面：
1. 创建一个逻辑时钟实例，用于事件。
2. 创建任务注册表。
3. 将自身设置为当前应用程序。
4. 调用app.oninit()回调(默认情况下什么都不做)。

当app创建出来后，需要在其他地方被使用，建议使用参数传递:
```python
class Scheduler(object):
    
    def __init__(self, app):
        self.app = app
```

## Tasks

每个任务类都有一个唯一的名称，此名称在消息中引用，以便工作者能够找到要执行的正确函数

在worker确认任务消息之前，不会将任务消息从队列中删除。一个worker可以预先保留许多信息，即使该worker因停电或其他原因而死亡，该消息也将被重新传递给另一个worker。

无限期阻塞的任务可能最终会阻止Worker实例执行任何其他工作.
比如爬取网页，应该添加一个超时:
```python
import requests
connect_timeout, read_timeout = 5.0, 30.0
response = requests.get(URL, timeout=(connect_timeout, read_timeout))
```

### Basics

通过使用Task()装饰器，可以轻松地从任何可调用的任务创建任务：

```python
from .models import User

@app.task
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

还可以为任务设置许多选项，这些选项可以指定为装饰器的参数:

```python
@app.task(serializer='json')
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

### Names

如果没有提供显式名称，任务装饰器将为您生成一个名称，并且该名称将基于1)定义任务的模块. 2)任务函数的名称.
也可以指定名字

```python
@app.task(name='sum-of-two-numbers')
def add(x, y):
    return x + y
```

### Task Request

Request有以下属性:

| 属性 | 描述 |
| -- | -- |
id| The unique id of the executing task.
group| The unique id of the task’s group, if this task is a member.
chord| The unique id of the chord this task belongs to (if the task is part of the header).
correlation_id| Custom ID used for things like de-duplication.
args| Positional arguments.
kwargs| Keyword arguments.
origin| Name of host that sent this task.
retries| How many times the current task has been retried. An integer starting at 0.
is_eager| Set to True if the task is executed locally in the client, not by a worker.
eta| The original ETA of the task (if any). This is in UTC time (depending on the enable_utc setting).
expires| The original expiry time of the task (if any). This is in UTC time (depending on the enable_utc setting).
hostname| Node name of the worker instance executing the task.
delivery_info| Additional message delivery information. This is a mapping containing the exchange and routing key used to deliver this task. Used by for example app.Task.retry() to resend the task to the same destination queue. Availability of keys in this dict depends on the message broker used.
reply-to| Name of queue to send replies back to (used with RPC result backend for example).
called_directly| This flag is set to true if the task wasn’t executed by the worker.
timelimit| A tuple of the current (soft, hard) time limits active for this task (if any).
callbacks| A list of signatures to be called if this task returns successfully.
errback| A list of signatures to be called if this task fails.
utc| Set to true the caller has UTC enabled (enable_utc).

New in version 3.1.
| 属性 | 描述 |
| -- | -- |
headers| Mapping of message headers sent with this task message (may be None).
reply_to| Where to send reply to (queue name).
correlation_id| Usually the same as the task id, often used in amqp to keep track of what a reply is for.

New in version 4.0.
| 属性 | 描述 |
| -- | -- |
root_id| The unique id of the first task in the workflow this task is part of (if any).
parent_id| The unique id of the task that called this task (if any).
chain| Reversed list of tasks that form a chain (if any). The last item in this list will be the next task to succeed the current task. If using version one of the task protocol the chain tasks will be in request.callbacks instead.

### Logging

工作人员将自动为您设置日志记录，或者您可以手动配置日志记录.

最佳实践是为模块顶部的所有任务创建一个通用记录器.

```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y
```

### Retrying

retry()可用于重新执行任务，例如在发生可恢复错误时。

当您调用retry时，它将使用相同的任务id发送一条新消息，并将注意确保消息与原始任务被传递到同一个队列。

当任务被重试时，这也会被记录为任务状态，这样您就可以使用结果实例来跟踪任务的进度(请参阅状态)。

```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```

如果要为内部retry()调用指定自定义参数，请将retry_kwargs参数传递给Task()装饰器

```python
# 重试最多5次
@app.task(autoretry_for=(FailWhaleError,),
          retry_kwargs={'max_retries': 5})
def refresh_timeline(user):
    return twitter.refresh_timeline(user)

@app.task
def refresh_timeline(user):
    try:
        twitter.refresh_timeline(user)
    except FailWhaleError as exc:
        raise div.retry(exc=exc, max_retries=5)
```

### Avoid launching synchronous subtasks

让任务等待另一个任务的结果是非常低效的，甚至可能在员工池耗尽时导致死锁.

```python
# 正确的方式

def update_page_info(url):
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain()

@app.task()
def fetch_page(url):
    return myhttplib.get(url)

@app.task()
def parse_page(page):
    return myparser.parse_document(page)

@app.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)
```

### Granularity

任务粒度是每个子任务所需的计算量。一般来说，最好把问题分成许多小任务，而不是有几个长时间运行的任务。对于较小的任务，您可以并行处理更多的任务，并且这些任务不会运行足够长的时间来阻止工作人员处理其他等待任务。但是，执行任务确实有开销。需要发送消息，数据可能不是本地的，等等。因此，如果任务粒度太细，所增加的开销可能会消除任何好处。

## Calling Tasks

本文档描述了任务实例和画布使用的芹菜统一的“调用API”。API定义了一组标准的执行选项，以及三种方法:

* apply_async(args[, kwargs[, …]])

    Sends a task message.

* delay(*args, **kwargs)

    Shortcut to send a task message, but doesn’t support execution options.

* calling (__call__)

    Applying an object supporting the calling API (e.g., add(2, 2)) means that the task will not be executed by a worker, but in the current process instead (a message won’t be sent).