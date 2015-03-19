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

    sql_create_table = '''CREATE TABLE {table_name}(
        url VARCHAR(32) PRIMARY KEY,
        keyword VARCHAR(32),
        html VARCHAR(255)
        )'''
    # 删除表目前没啥用
    # sql_delete_table = '''DROP TABLE IF EXISTS {table_name}'''
    sql_insert_data = '''INSERT INTO {table_name} VALUE({url}, {keyword}, {html})'''
    sql_select_data = '''SELECT {colume} from {table_name} WHERE url = {url}'''
    sql_update_data = '''UPDATE student SET url = ? WHERE ID = ?'''

    def __init__(self, dbfile):
        self.dbfile = "spider.db"
        pass

    @property
    def dbfile(self):
        return self.dbfile

    @property
    def connect(self):
        '''
        获取数据库连接对象
        '''
        try:
            if os.path.exists(self.dbfile) and os.path.isfile(self.dbfile):
                return sqlite3.connect(self.dbfile)
            else:
                return sqlite3.connect(":memory:")
        except sqlite3.Error, e:
            logger.error("连接sqlite3数据库失败", "\n", e.args[0])
            return

    @property
    def cursor(self):
        '''
        获取数据库的游标对象
        '''
        return self.connect.cursor()

    def dataexec(self, func):
        def per_exec(*args):
            connect = self.connect
            cursor = self.cursor
            sqlline = func(*args)
            cursor.execute(sqlline)
            connect.commit()
            self.close_all()
        return per_exec

    def close_all(self):
        if self.connect:
            self.connect.close()
        if self.cursor():
            self.cursor.close()

    @dataexec
    def add(self, url, keyword, html):
        return self.sql_insert_data.format()
        pass