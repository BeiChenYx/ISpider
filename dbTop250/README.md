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

```text
榜单信息都分布在在 <table with="100%"> 中，每页有25个；
每个table 中有一个 tr, tr下面两个td, 第二个td为所要的数据位置
xpath:
 tds: '//table[@width="100%"]/tr/td[2]'

```