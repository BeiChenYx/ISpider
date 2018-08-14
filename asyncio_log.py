# IPython log file

get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('logstop', './text.py')
get_ipython().run_line_magic('logstart', './text.py')
get_ipython().run_line_magic('logstop', '')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('logstart', './asyncio_log.py')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('pwd', '')
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 ok'
        
def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER]Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()
    
c = consumer()
produce(c)
import asyncio
async def hello():
    print('Hello world!')
    r = yield from asyncio.sleep(1)
@asyncio.coroutine
def hello():
    print('Hello world!')
    r = yield from asyncio.sleep(1)
    print('Hello again!')
    
loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()

import threading

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    r = yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())
    
loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
