# know_quiz

## 使用说明

```
$ python setup.py install

$ spider.py -h |　--help
Usage: spider.py -u url [-d deep | -f logfile | -l level | -t number]
spider man for know inc. quiz
Options:
  -h, --help            show this help message and exit
  -u verbose, --url=verbose
                        the url of scraping
  -d DEGREE, --degree=DEGREE
                        deep or simple, default is simple
  -f FILE, --logfile=FILE
                        write logging to file, default: /var/log/spider.log
  -k KEYWORD, --keyword=KEYWORD
                        scraping keywords
  -b FILE, --dbfile=FILE
                        write data to file, default: /tmp/spider.db
  -l DEBUG_LEVEL, --debug_level=DEBUG_LEVEL
                        debug level to write range 1 to 5, default: 1
  -t THREAD_NUM, --thread_num=THREAD_NUM
                        debug level to write, default is 10


# 简单用法
$ spider.py -u http://www.coyote.hk -k coyote

# 复杂用法
$ spider.py -u http://www.coyote.hk -k coyote -t 5 -l 5 -d deep -l /var/log/spider.log -b /tmp/spider.db
```

## 题目内容

```
spider.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5”


参数说明：

-u 指定爬虫开始地址

-d 指定爬虫深度

--thread 指定线程池大小，多线程爬取页面，可选参数，默认10

--dbfile 存放结果数据到指定的数据库（sqlite）文件中

--key 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面

-l 日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认spider.log

--testself 程序自测，可选参数

 

功能描述：

1、指定网站爬取指定深度的页面，将包含指定关键词的页面内容存放到sqlite3数据库文件中

2、程序每隔10秒在屏幕上打印进度信息

3、支持线程池机制，并发爬取网页

4、代码需要详尽的注释，自己需要深刻理解该程序所涉及到的各类知识点

5、需要自己实现线程池

 

提示1：使用re  urllib/urllib2  beautifulsoup/lxml2  threading optparse Queue  sqlite3 logger  doctest等模块

提示2：注意是“线程池”而不仅仅是多线程

提示3：爬取sina.com.cn两级深度要能正常结束

 

建议程序可分阶段，逐步完成编写，例如：

版本1:Spider1.py -u url -d deep

版本2：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself

版本3：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number

版本4：剩下所有功能
```

## 思维过程

![know_quiz](http://coyote.qiniudn.com/freemind.jpeg)



## TimeLine

- 150317 初建项目
- 150317 添加解析参数功能和核心线程池
- 150319 添加数据模块和爬虫模板, 但是未完善
    - 添加两个文件, 以及设想框架
- 150325 添加数据库操作核心功能以及爬虫功能
    - 完善data.py中的功能, 添加增删改查的sql语句
- 150326 最后完善
    - log 中文化
    - data.py 推翻之前写的代码, 结构化从新设计
    - modules.py 中的功能完善
    - tpool.py 中加入写数据库的线程

## 程序缺陷

- modules.py 
    - 爬虫功能只进行了关键字匹配, 存储的结果是 是否包含关键字的Bool值
    - 功能简单, 定制化不够强
    - 不易扩展, 应当抽象为class
    - 对重复的url没有进行校验
- data.py
    - 只包含了add_data方法, 创建表字段简单, 并且没有主键
    - 由于没有主键, 同一个url被多次存储
    - spiderdata的类功能不完善
- tpool.py
    - 没有经过详细的数据流设计, 传递参数比较混乱
    - 稳定性和执行效率测试没有做
    - 可能会出现部分raise error 没有捕获, 导致线程退出
- spider.py
    - 没有用argparse, 并且帮助信息不够详细
    - logging没有单独提取出来
- 其他
    - 整体上 tpool 相对比较完善
    - data 因为有些没有用到的功能, 所以部分没用的代码被删除掉了
    - modules 因为爬虫之前没有接触过, 只是单纯的做了简单功能. 后续需要继续学习
    - 对爬虫没有整体的把握和接触.
    - 当然还有很多没有写进去的, 但是存在的问题.

## 反思

拿到题目, 打开freemind整理一下信息, 然后开始搭建框架, 一点点充实代码.
- 过程中遇到的问题
    - 爬虫实在是接触的少. 所以不太会结合`re` `urllib/urllib2` `BeautifulSoup`
    - 数据库设计的时候一开始设想的比较复杂, 导致后期写数据库的时候造成麻烦
    - 多线程中, 写数据库只能在同一个线程操作数据库, 这个确实之前没有遇到过

## 邮件
```
>> * SpiderData类中property 用法有些问题。  变量名和被装饰方法名一样?

这点确实自己没有注意, 不过周四自己翻译了一篇underscore的用法之后有了一些认识
内部变量和 property的名称 用underscore区分是否是合理的呢?
http://www.coyote.hk/pythonzhong-de-xia-hua-xian.html

>> * debug_level这个命令行选项，只是影响日志格式。 并没有进行日志级别过滤？
​
一开始自己看题目的时候, 题目中写道

日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认spider.log
参数 -l loglevel(1-5)

​当时认为就是level过滤的是日志级别, 后来仔细读题, 数字越大越详细, 那么所谓的详细可能就是日志的内容?
我打开logging查看了几个参数:
In [1]: import logging

In [2]: logging.INFO

Out[2]: 20

In [3]: logging.DEBUG

Out[3]: 10

In [4]: logging.ERROR

Out[4]: 40

数值越大, 记录的级别越高, 反而越不详细, 过滤掉一些没用的log, 所以就采用了内容详细程度过滤.

不过个人认为, 题目应当表达的时过滤级别, 而不是内容吧


>> * URL处理部分太过简单， 应该允许用户输入 www.baidu.com

url处理这一块我是秉承自己的代码习惯,
习惯先能够把流程调通, 功能的核心部分先实现, 细节上慢慢完善, 比如字符处理, 错误捕获

当然在之前的开发过程中,我也不清楚这样做是否恰当

>> * OptionParser中的选项对应help建议写明确一些。

;-P 英文水平读和看应该还可以, 但是自己编写帮助信息的英文水平, 着实还需要继续锻炼

>> * py文件头 建议加上 #/bin/env python

这个的确是我忘记了. 但是应该只在spider.py中加吧, 其他的作为package中的py, 应该没必要加吧?

>> * 我看部分核心功能并没有实现，但是README里面都没有体现？

README最后才写是我的一个坏毛病! 我改!!!

>> 建议： 好好梳理一下README，这样能够直观的了解程序开发进度。
OK
 
 
>> 陈伟晴，代码初步看下了，先简单邮件回复你下：

>> 按严格的工具、类库方式来说明：
>> * 版本控制的 commit log 可以更规范些，比如：这次提交做了哪些事情？不是 add two files 这种宽泛的没有太多实际意义的日志信息

严重表示同意! 我坏毛病就是自己写的工具的时候自己一般都不太认真写commit log, 但是工作中还是会认真对待的.
以后工作和自己都认真对待!!

>> * 可以写个简单的 setup.py 方便别人安装，或者完善下 README，方便别人立马能使用你写的程序

这个确实是我自己考虑中的一个欠缺! README 同上!! 我改!!

>> * 建议：optparse 可以替换成 Python 2.7 开始更推荐的 argparse 了

我out了..虽然之前用过argparse 但是还真没注意是推荐用法

>> * class ThreadPool 是忘记用新的类方式？ThreadPool(object)

No, No, No  这个是粘贴时候的一个失误, 因为这个threadPool我之前写过一个, 名字不叫这个, 改名字的时候给误删了
不过话说, py3以后就没有什么新类和旧类了吧

* 可以的话，写点必要的测试代码，如果觉得有需要的话

测试代码肯定是要写的, 不过我没有按照TDD开发的话, 是不是应该最后在写? 而且时间不是很充裕:-(

* 有些冗余的 pass 函数或方法实现完了，应该就可以去掉了吧？

好的, 个人习惯是最后检查代码的时候再删掉, 保留着在检查代码的时候会再看到pass的时候再回想一下当时的功能是否完全实现

* 大量出现的 degree 这个变量是深度的意思？

这个东西我还没想好怎么用,因为还没有写爬取内容的代码, 在写scraping功能的时候再考虑如何使用

* modules 和 data 两个 py 还没用到？

没写完ToT

* 判断 URL 那是否合法那，只判断一个 http 开头可能不够严谨，比如：http.example.com

这个的确是考虑欠佳

* python spider.py -d 1 -u http://www.baidu.com -t 3 貌似结束不了？

好像是可以的, 就是最后有个延迟, 因为我在主进程里面有个检查线程是否全部退出的一个功能, 但是我考虑如果频率太高检查的话会造成资源浪费, 后来写了个sleep(5)也就是两次检查之间有个5秒的延迟, 过一会就退出了, 我这里是没问题的,或许有未知的bug?

* -d -k -f 这几个参数还没实现哈?

嘿嘿, 似的
```
