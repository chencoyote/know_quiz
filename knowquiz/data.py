# -*- coding: utf-8 -*-
'''
data

数据库操作模板, 表结构初始化等相关操作
'''

import sqlite3
import logging
import os

logger = logging.getLogger("spider.data")


class SpiderData(object):

    sql_create_table = '''CREATE TABLE spider(
        url VARCHAR(32),
        keyword VARCHAR(32),
        matched BOOL
        )'''

    ERROR_TABLE_EXIST = "table spider already exists"

    def __init__(self, dbfile="./spider.db"):
        self.dbfile = dbfile
        self.conn = self._connect()
        self.cur = self.conn.cursor()

    def _connect(self):
        '''
        连接数据库, 如果数据库文件不存在,
        创建数据库文件, 并且建立数据表
        '''
        if not os.path.isfile(self.dbfile):
            conn = sqlite3.connect(self.dbfile)
            cur = conn.cursor()
            try:
                cur.execute(self.sql_create_table)
            except sqlite3.OperationalError, e:
                # import pdb
                # pdb.set_trace()
                if str(e) != self.ERROR_TABLE_EXIST:
                    logger.error("创建数据库表<<spider>>失败" + "\n" + str(e))
            except sqlite3.Error, e:
                logger.error("操作数据库失败:" + "\n" + e.args[0])
            conn.commit()
            conn.close()
        return sqlite3.connect(self.dbfile)

    def _select(self, sql):
        '''
        查询数据库, 执行查询语句
        参数: sql语句
        '''
        try:
            self.cur.execute(sql)
        except sqlite3.Error as e:
            logger.error("执行sql语句发生错误: %s" % str(e))
        for row in self.cur:
            result = {}
            for i, j in enumerate(self.cur.description):
                result[j[0]] = row[i]
            yield result

    def _execute(self, sql):
        '''
        数据库执行插入, 修改等操作
        参数: sql语句
        '''
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in e.message:
                return False
        return True

    def add_data(self, data):
        '''
        向数据库中插入抓取数据
        '''
        sqlline = "INSERT INTO spider (url, keyword, matched) VALUES ('%(url)s', '%(keyword)s', '%(matched)s')"
        sqlline = sqlline % data
        r = self._execute(sqlline)
        return r

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    sd = SpiderData()
    data = {"url": "1",
            "keyword": "keyword",
            "matched": "html"}
    sd.add_data(data)
