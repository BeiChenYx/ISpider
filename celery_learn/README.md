# Celery框架官方学习笔记

```
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