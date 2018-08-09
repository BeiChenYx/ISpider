# 爬取指定关键词的百度图片

## 网站分析

``` text
搜索请求:

初始请求:

https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word=%E6%B5%B7

初始请求中有个 thumbURL 字段为初始请求的图片url地址
thumbURL: "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2929358115,620586623&fm=27&gp=0.jpg

滚动鼠标触发请求:
https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B5%B7&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%B5%B7&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=30&rn=30&gsm=1e&1533794293319=

https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B5%B7&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%B5%B7&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=60&rn=30&gsm=3c&1533794293803=


https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B5%B7&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%B5%B7&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1533796404816=

https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B5%B7&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%B5%B7&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=120&rn=30&gsm=78&1533796405044=

对比发现：
pn: 30递增到60， ==> 测试 pn=0 ==> 结果返回一致，第一个 thumbURL的值获取的图片和初始请求中的一样；
gsm: 不一样， ==> 测试去掉gsm参数 ==> 结果不影响访问, 但1e, 3c 对应的十进制刚好是 30, 60
最后一个数字1533794293803= 不一样，目测是时间搓 ==> 测试去掉这个参数 ==> 不影响访问;

总结规律：
直接访问滚动鼠标的发送请求地址，pn 从 0 开始，30间距递增， gsm 为 pn 的十六进制数, 最后一个值使用时间搓；
每次滚动请求间隔2-3秒左右；

爬取完一个请求，获取thumbURL的值，该值为图片的地址，直接下载，建议每次下载完30个，暂停2-3秒;
```