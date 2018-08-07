# 豆瓣网图书Top250信息爬取

## 依赖库

``` text
pip install requests
pip install BeuatifulSoup4
pip install lxml
pip install pyquery
```

## 爬虫要求

1. 使用 Xpath, BeautifulSoup, PyQuery三种方式解析数据;
2. 使用urllib, requests两种方式爬取;
3. 要求实现翻页爬取250条数据;
4. 将爬取的数据写入文件;
5. 需要解析的数据: 书名，作者(包括译者), 出版社, 出版时间, 价钱， 评分， 评价人数;

## 爬虫分析

### url分析

页码 |       URL
---|---
第一页|https://book.douban.com/top250?start=0
第二页|https://book.douban.com/top250?start=25
第三页|  https://book.douban.com/top250?start=50
....  |...
第十页|https://book.douban.com/top250?start=225

> 规律：start 参数控制翻页，每页25个数据.

### 数据解析

字段      | Xpath                   | BeautifulSoup         | PyQuery
----------|:-----------------------:|:----------------------:|--------
tile      |//div[@class="pl2"]/a/text()|'div.pl2 a'|'div.pl2 a'
author      |//p[@class="pl"]/text()|'p.pl'|'p.pl'
publisher |//p[@class="pl"]/text()|'p.pl'|'p.pl'
time      |//p[@class="pl"]/text()|'p.pl'|'p.pl'
price     |//p[@class="pl"]/text()|'p.pl'|'p.pl'
score     |//span[@class="rating_nums"]/text()|'span.rating_nums'|'span.rating_nums'
comments  |//span[@class="pl"]/text()|'span.pl'|'span.pl'

> 其中 auth publisher time price在一个块里面，使用了 / 分开；