# -*- coding: utf-8 -*-
'''
__auth__ = coyote
'''

from optparse import OptionParser
from tpool import ThreadPool
import logging
import sys
import time
import os

logger = logging.getLogger("spider")


def handler_logger(level, logfile, screen=True):
    level_map = {
        1: "%(message)s",
        2: "%(asctime)s - %(message)s",
        3: "%(asctime)s - %(name)s - %(message)s",
        4: "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        5: "%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s"
    }
    fhandler = logging.FileHandler(logfile)
    logger.setLevel(logging.INFO)
    fhandler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        level_map[level]
    )
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    if screen:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)


class Spider(object):

    def __init__(self, thread_num, logfile, debug_level,
                 dbfile, keyword, degree):
        self.urls = []
        self.logfile = logfile
        self.debug_level = debug_level
        self.dbfile = dbfile
        self.thread_num = thread_num
        self.keyword = keyword
        self.degree = degree

    def run(self, urls):
        logger.info("start run spider process")
        self.thread_pool = ThreadPool(self.thread_num)
        for url in urls:
            logger.info("add url %s to queue" % url)
            self.thread_pool.add_job(url, self.keyword, self.degree)
        while self.thread_pool.check_job() > 0:
            try:
                logger.info("%d job is working" % self.thread_pool.check_job())
                time.sleep(5)
            except KeyboardInterrupt:
                self.thread_pool.stop_job()

    def quit(self):
        logger.warn("quit all thread")
        self.thread_pool.stop_all()


def scraping(argv):
    usage = 'usage: %prog -u url [-d deep | -f logfile | -l level | -t number]'
    parser = OptionParser(
        usage=usage, description='spider man for know inc. quiz'
    )
    parser.add_option(
        "-u", "--url", dest="url",
        help="the url of scraping", metavar="verbose"
    )
    parser.add_option(
        "-d", "--degree", dest="degree", default="simple",
        help="deep or simple"
    )
    parser.add_option(
        "-f", "--logfile", dest="logfile", default="spider.log",
        help="write logging to file", metavar="FILE"
    )
    parser.add_option(
        "-k", "--keyword", dest="keyword", type="str", default="",
        help="scraping keywords"
    )
    parser.add_option(
        "-b", "--dbfile", dest="dbfile", default="spider.db",
        help="write data to file", metavar="FILE"
    )
    parser.add_option(
        "-l", "--debug_level", dest="debug_level", type="int", default=1,
        help="debug level to write"
    )
    parser.add_option(
        "-t", "--thread_num", dest="thread_num", type="int", default=10,
        help="debug level to write"
    )

    if len(argv) < 1:
        parser.print_help()
        return
    options, args = parser.parse_args(argv)

    # 解析debug等级, 1-5之间
    debug_level = 0
    if options.debug_level in range(1, 6):
        debug_level = options.debug_level
    # 解析日志文件, 如果存在, 追加写, 如果不存在, 直接写
    logfile = ""
    if os.path.exists(options.logfile):
        logfile = options.logfile

    # 处理日志级别
    handler_logger(debug_level, options.logfile)

    # 解析深度参数, 只能是deep和simple
    degree = ""
    if options.degree in ["deep", "simple"]:
        degree = options.degree

    # 解析爬取关键字
    keyword = ""
    if isinstance(options.keyword, str):
        keyword = options.keyword

    # 解析数据库文件
    dbfile = options.dbfile

    # 解析线程池大小
    thread_num = 0
    if isinstance(options.thread_num, int):
        thread_num = options.thread_num

    spider = Spider(thread_num, logfile, debug_level, dbfile, keyword, degree)

    # 解析url, 可以使用逗号分割多个url
    urls = []
    if options.url:
        for u in options.url.split(","):
            if u.startswith("http"):
                urls.append(u)
            else:
                logger.error("%s is illegal url" % u)
    if not urls:
        logger.error("no url to scraping, exit")
        return 
    spider.run(urls)

if __name__ == "__main__":
    scraping(sys.argv[1:])
