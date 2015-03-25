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
        html VARCHAR(255)
        )'''
    # 删除表目前没啥用
    # sql_delete_table = '''DROP TABLE IF EXISTS {table_name}'''
    sql_insert_data = '''INSERT INTO spider VALUES (?,?,?)'''
    sql_select_data = '''SELECT {colume} from spider WHERE url = {url}'''
    sql_update_data = '''UPDATE spider SET url = ? WHERE ID = ?'''

    ERROR_TABLE_EXIST = "table spider already exists"

    def __init__(self):
        self._dbfile = "./spider.db"
        self.conn = self.connect()
        self.cu = self.conn.cursor()
        self.create_table()
        pass

    @property
    def dbfile(self):
        return self._dbfile

    @dbfile.setter
    def dbfile(self, value):
        self._dbfile = value

    def connect(self):
        '''
        获取数据库连接对象
        '''
        try:
            if os.path.exists(self.dbfile) and os.path.isfile(self.dbfile):
                return sqlite3.connect(self.dbfile)
            else:
                with open(self.dbfile, "w") as f:
                    f.close()
                    return sqlite3.connect(self.dbfile)
        except sqlite3.Error, e:
            logger.error("连接sqlite3数据库失败" + "\n" + e.args[0])
            return

    def close_all(self):
        self.conn.close()

    def create_table(self):
        try:
            self.cu.execute(self.sql_create_table)
        except sqlite3.OperationalError, e:
            # import pdb
            # pdb.set_trace()
            if str(e) == self.ERROR_TABLE_EXIST:
                return
            else:
                logger.error("创建数据库表<<spider>>失败" + "\n" + str(e))
        except sqlite3.Error, e:
            logger.error("操作数据库失败:" + "\n" + e.args[0])
        self.conn.commit()

    def add(self, url, keyword, html):
        '''
        需要后期优化
        '''
        # TODO -- add, update, delete 等方法抽象
        data = (url, keyword, html)
        self.cu.execute(self.sql_insert_data, data)
        self.conn.commit()
        self.cu.close()

if __name__ == "__main__":
    sd = SpiderData()
    sd.add("1", "keyword", "html")
