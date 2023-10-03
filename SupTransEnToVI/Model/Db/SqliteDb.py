'''SqliteDb.py
Quản lý việc kết nối với Sqlite
'''
import os
import sqlite3
import re
from datetime import datetime
from .Sqlite import *

class SqliteDb:
    def __init__(self, fileDatabase):
        isFile = os.path.exists(fileDatabase) and os.path.isfile(fileDatabase)
        self.conSqlite = sqlite3.connect(fileDatabase, check_same_thread = False)
        self.cursor = self.conSqlite.cursor()
        # Định nghĩa ký tự thoát (escape)
        self.escapeLike = [('\\', '\\\\'), ('%', '\\%'), ('_', '\\_')]
        if not isFile:
            self.create_table(self.conSqlite)
            self.create_config_default()
        self.get_config()
        self.dbRoot = RootSent(self)
        self.dbCache = CacheSent(self)
        #print('Ngày', self.config['cache_update'])

    def get_db_root(self):
        return self.dbRoot

    def get_db_cache(self):
        return self.dbCache

    # Chèn ký tự thoát (escape)
    def escape_string_like(self, key):
        result = key
        for es in self.escapeLike:
            result = result.replace(es[0], es[1])
        return result

    #Tạo bảng tương ứng trong database mới tạo
    def create_table(self, conSqlite):
        #Tạo bảng cấu hình
        sql_create = '''CREATE TABLE CONFIG_SENT (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            root_update DATETIME DEFAULT CURRENT_TIMESTAMP,
            cache_update DATETIME DEFAULT CURRENT_TIMESTAMP
            );'''
        conSqlite.execute(sql_create)
        print('Tạo bảng CONFIG_SENT thành công')
        #Tạo bảng câu gốc
        sql_create = '''CREATE TABLE ROOT_SENT (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            eng TEXT NOT NULL,
            vie TEXT DEFAULT '',
            day_create DATETIME DEFAULT CURRENT_TIMESTAMP,
            day_update DATETIME DEFAULT CURRENT_TIMESTAMP
            );'''
        conSqlite.execute(sql_create)
        print('Tạo bảng ROOT_SENT thành công')
        #Tạo bảng câu tạm
        sql_create = '''CREATE TABLE CACHE_SENT (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            eng TEXT NOT NULL,
            vie TEXT DEFAULT '',
            escChar TEXT DEFAULT '',
            day_update DATETIME DEFAULT CURRENT_TIMESTAMP,
            retrains INTEGER DEFAULT 0,
            input_source INTEGER DEFAULT 0
            );'''
        conSqlite.execute(sql_create)
        print('Tạo bảng CACHE_SENT thành công')

    #Tạo con trỏ mới (dùng trong Thread)
    def create_new_cursor(self):
        return self.conSqlite.cursor()

    #Lấy con trỏ của luồng chính
    def get_cursor(self):
        return self.cursor

    
    '''--------------------------------------------------------------------------------
    Đây là phần code cho bảng cấu hình (CONFIG_SENT)
    Lưu lại thông tin cấu hình xuống cơ sở dữ liệu
    - root_update: ngày cập nhật thay đổi cũ nhất
    --------------------------------------------------------------------------------'''

    #Tạo dữ liệu cấu hình mặc định
    def create_config_default(self):
        sql_insert = '''INSERT INTO CONFIG_SENT(root_update)
            VALUES(?)
            '''
        time_default = datetime.now()
        self.cursor.execute(sql_insert, (time_default,))
        self.config['cache_update'] = time_default
        self.config['root_update'] = time_default
        return self.cursor.lastrowid

    #Lấy ngày cập nhật cũ nhất
    def get_config(self):
        #Lấy dữ liệu đầu tiên
        sql_select = '''SELECT id, cache_update,root_update
            FROM CONFIG_SENT
            ORDER BY id
            '''
        self.cursor.execute(sql_select)
        config = self.cursor.fetchone()
        self.config = {}
        #Thường sẽ không xảy ra nhưng cứ kiểm tra cho chắc
        if config is None:
            self.create_config_default()
            return
        self.config['cache_update'] = config[1]
        self.config['root_update'] = config[2]

    #Lưu ngày cập nhật hiện tại
    def set_config_root_update(self):
        sql_update = '''UPDATE CONFIG_SENT
            SET root_update = ?
            '''
        self.cursor.execute(sql_update, (datetime.now(),))

    #Thật sự lưu dữ liệu xuống tiệp tin database
    def save_database(self):
        self.conSqlite.commit()
    
    #Đóng database an toàn
    def __del__(self):
        self.cursor.close()
        self.conSqlite.close()