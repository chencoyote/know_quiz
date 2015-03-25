# -*- coding: utf-8 -*-
'''
__auth__ = coyote
'''
import threading
import time
import logging
from Queue import Queue
from data import SpiderData

logger = logging.getLogger("spider")


class SpiderWorker(threading.Thread):

    def __init__(self, tid, work_q, event):
        threading.Thread.__init__(self)
        self.work_queue = work_q
        self.timeout = 10
        self.event = event
        self.tid = tid
        self.setDaemon(True)
        pass

    def run(self):
        logger.info("thread number %s is start" % self.tid)
        while not self.event.isSet():
            if not self.work_queue.empty():
                callable, args = self.work_queue.get(self.timeout)
                logger.info("start scraping use %s" % callable.__name__)
                result = callable(*args)
                print result
                if result["deep_url"]:
                    for url in result["deep_url"]:
                        self.work_queue.put(
                            (callable, (url, result["keyword"], "simple"))
                        )
                        self.sd.add(
                            result["url"], result["keyword"], result["html"]
                        )
                else:
                    self.sd.add(
                        result["url"], result["keyword"], result["html"]
                    )
                self.sd.close_all()
            else:
                time.sleep(1)
        logger.warn("线程已停止")

    '''
    暂时取消下列方法, 把爬虫功能提取到modules.py中
    '''
    # def worker(self, url, keyword, degree):
    #     if degree is "simple":
    #         '''
    #         ## 功能说明
    #         - urllib 获取url的html, re匹配keyword
    #         - 获取到的信息, 使用DB模块API 进行存储
    #             + 字段: 时间, url, keyword, html, keyword个数
    #         '''
    #         # TODO -- 以上
    #         pass
    #     elif degree is "deep":
    #         '''
    #         ## 功能说明
    #         - urllib 获取url的html, re匹配keyword
    #         - beautifulSoup加载html为dom, 寻找所有的<a>标签, 获取url
    #         - 将url添加到work_queue中
    #             + 如果需要无限深度挖掘, 则 degree 继续为 deep
    #             + 如果只需要2级, 则在 put到queue时候改为 simple
    #         '''
    #         # TODO -- 以上
    #         pass


class ThreadPool:

    def __init__(self, dbfile, max_pool=10):
        self.work_queue = Queue()
        self.res_queue = Queue()
        self.max_pool = max_pool
        self.event = threading.Event()
        self.pool = []
        self.sd = SpiderData()
        self.sd.dbfile = dbfile
        self._recruit_threads()

    def _recruit_threads(self):
        for i in range(self.max_pool):
            logger.info("thread number %d is create" % i)
            aw = SpiderWorker(
                i, self.work_queue, self.res_queue, self.event, self.sd
            )
            # TODO -- 数据库只能由一个线程操作, 单独创建一个线程进行存储数据
            aw.start()
            self.pool.append(aw)
        self.event.clear()
        while True:
            try:
                alive = False
                for thread in self.pool:
                    alive = alive or thread.isAlive()
                if not alive:
                    break
            except KeyboardInterrupt:
                logger.warn("用户强制停止线程池")
                self.event.set()
            finally:
                break

    def add_job(self, callable, args):
        self.work_queue.put((callable, args))

    def check_job(self):
        check = [1 for thread in self.pool if thread.isAlive()]
        return len(check)

    def stop_job(self):
        logger.warn("用户强制停止线程池")
        self.event.set()
