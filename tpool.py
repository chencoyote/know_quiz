# -*- coding: utf-8 -*-
'''
__auth__ = coyote
'''
import threading
import time
import logging
from Queue import Queue

logger = logging.getLogger("spider")


class SpiderWorker(threading.Thread):

    def __init__(self, tid, work_q, result_q, event):
        threading.Thread.__init__(self)
        self.work_queue = work_q
        self.result_queue = result_q
        self.timeout = 10
        self.event = event
        self.tid = tid
        self.setDaemon(True)
        pass

    def run(self):
        logger.info("thread number %s is start" % self.tid)
        while not self.event.isSet():
            if not self.work_queue.empty():
                url, keyword, degree = self.work_queue.get(self.timeout)
                # print url, keyword, degree
                # logger.debug(
                #     "start scraping url is %s " % url
                # )
                logger.info("start scraping 100")
                # self.worker(url, keyword)
            else:
                time.sleep(1)
        logger.warn("线程已停止")

    def worker(self, url, keyword):
        print "aaaa"


class ThreadPool:

    def __init__(self, max_pool=10):
        self.work_queue = Queue()
        self.res_queue = Queue()
        self.max_pool = max_pool
        self.event = threading.Event()
        self.pool = []
        self._recruit_threads()

    def _recruit_threads(self):
        for i in range(self.max_pool):
            logger.info("thread number %d is create" % i)
            aw = SpiderWorker(
                i, self.work_queue, self.res_queue, self.event
            )
            self.pool.append(aw)
        for thread in self.pool:
            thread.start()
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

    def add_job(self, url, keywords, degree):
        self.work_queue.put((url, keywords, degree))
