# ZHSpider

spiders目录为单个任务的方式，使用文件来保存结果；
DisSpider目录是在spiders目录基础上改用Redis进行分布式开发;

## 问题描述

基础要求：把知乎的所有话题、各话题内的文章、问答爬下来（至少爬10万条数据，不设上限），把数据存储到数据库中，手段不限（可以使用Scrapy也可以使用Urllib,具体技术不做限制）。

## 项目具体要求

1. 把知乎所有话题爬下来存入数据库中(数据库建议使用mysql);
2. 根据各话题信息，构造各话题的文章列表，把所有文章名、文章链接等信息爬到数据库中。（考虑到时间问题，可以不用爬完，至少总文章数据爬10万条，不设上限）
3. 把文章具体信息（如果是专栏文章需要爬包括文章标题、作者、文章内容，如果是问答内容需要爬包括问题标题，问题描述，答案内容，答案作者等信息）爬下来存储到数据库中，问答类信息与文章类信息存储到不同数据库中。
4. 有能力可以采用分布式爬虫架构。

## 爬虫分析

本着大问题分割成小问题的原则，可以分成以下模块:

所有分类地址: https://www.zhihu.com/topics

* 获取所有的一级类别;
* 获取一级类别下面所有二级类别;
* 获取二级类别下面的文章列表;
* 从详细页面中抽取文章数据和评论数据;

### 获取所有的一级类别

初始地址 https://www.zhihu.com/topics 中有个结构

```html
<ul class="zm-topic-cat-main clearfix">
<li class="zm-topic-cat-item" data-id="1761"><a href="#生活方式">生活方式</a></li>
<li class="zm-topic-cat-item" data-id="3324"><a href="#经济学">经济学</a></li>
<li class="zm-topic-cat-item" data-id="833"><a href="#运动">运动</a></li>
<li class="zm-topic-cat-item" data-id="99"><a href="#互联网">互联网</a></li>
...
</ul>
```

抓包发现点击每个一级类别的时候都有一个请求: https://www.zhihu.com/node/TopicsPlazzaListV2
为Post方式:

* method:next
* params:{"topic_id":1761,"offset":0,"hash_id":""}

因此通过Post方式请求上面的地址，用data-id的数据填充topic_id就可以获取所有的一级类别

### 获取所有的二级类别

获取一级类别的Post请求中的offset=20则获取了下一页的内容，浏览器表现为点击更多
Post方式请求响应为一个json:

```json
{r:0, msg:[
    "<div class="item"><div class="blk">↵<a target="_blank" href="/topic/19560170">"
   ...
]}
```

其中href中就有二级类别的地址

### 获取二级类别下面的文章列表地址

在二级类别的地址中追加 /hot ，就是默认话题列表的地址，和正常访问一样；初始访问会有默认加载5个文章，
之后每次下拉会自动加载新的文章, 在初始页面中有如下一个页面地址 在next参数中

https://www.zhihu.com/api/v4/topics/19555513/feeds/top_activity

此请求回应一个json数据，里面有10个文章数据，并且有下一个页面的地址，有开始和结束标志字段，有总数字段;

### 获取文章详细页面的数据

访问文章详细页面地址会响应文章数据以及前面几个答案数据，继续点击更多答案则通过json加载新的数据

https://www.zhihu.com/api/v4/questions/21499964/answers

