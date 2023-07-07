'''SqliteDb.py
Quản lý việc kết nối với Sqlite
'''
import os
import sqlite3
import re
from datetime import datetime

class SqliteDb:
    def __init__(self, fileDatabase):
        isFile = os.path.exists(fileDatabase) and os.path.isfile(fileDatabase)
        self.conSqlite = sqlite3.connect(fileDatabase, check_same_thread = False)
        self.cursor = self.conSqlite.cursor()
        # Định nghĩa ký tự thoát (escape)
        self.escapeLike = [('\\', '\\\\'), ('%', '\\%'), ('_', '\\_')]
        if not isFile:
            self.create_table()

    # Chèn ký tự thoát (escape)
    def escape_string_like(self, key):
        result = key
        for es in self.escapeLike:
            result = result.replace(es[0], es[1])
        return result

    #Tạo bảng tương ứng trong database mới tạo
    def create_table(self):
        sql_create = '''CREATE TABLE CAU_GOC (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            eng TEXT NOT NULL,
            vie TEXT DEFAULT '',
            ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
            ngay_sua DATETIME DEFAULT CURRENT_TIMESTAMP
            );'''
        self.conSqlite.execute(sql_create)
        print('Tạo bảng CAU_GOC thành công')

    #Tạo con trỏ mới (dùng trong Thread)
    def create_new_cursor(self):
        return self.conSqlite.cursor()

    #Lấy tất cả từ khóa theo từng trang
    def get_allkeys(self, key, page):
        maxRow = 10
        startRow = (page-1)*maxRow
        if key == '':
            sql_select = '''SELECT id, eng, vie
                FROM CAU_GOC
                ORDER BY eng
                LIMIT ?, ?
                '''
            self.cursor.execute(sql_select, (startRow, maxRow))
        else:
            sql_select = '''SELECT id, eng, vie
                FROM CAU_GOC
                WHERE eng LIKE ? ESCAPE '\\'
                ORDER BY length(eng), eng DESC
                LIMIT ?, ?
                '''
            self.cursor.execute(sql_select, (f'%{self.escape_string_like(key)}%', startRow, maxRow))
        result = self.cursor.fetchall()
        return result

    #Lấy theo id_
    def get_id(self, id_):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE id=?
            '''
        self.cursor.execute(sql_select, (id_,))
        result = self.cursor.fetchone()
        return result

    #Tìm chính xác theo câu eng
    def get_eng(self, eng):
        return self.get_eng_thread(eng, self.cursor)

    #Tìm chính xác theo câu eng (Thread)
    def get_eng_thread(self, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng=?
            '''
        cursor.execute(sql_select, (eng,))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng ngắn nhất
    def get_like_eng(self, eng):
        return self.get_like_eng_thread(eng, self.cursor)

    #Lấy câu gần đúng ngắn nhất (Thread)
    def get_like_eng_thread(self, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'%{self.escape_string_like(eng)}%',))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng ngắn nhất (Thread)
    def get_glob_eng_thread(self, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng GLOB ?
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'*{eng}*',))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng phía trước ngắn nhất (Thread)
    def get_like_front_eng_thread(self, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'%{self.escape_string_like(eng)}',))
        result = cursor.fetchone()
        return result

    
    #Lấy câu gần đúng ở giữa ngắn nhất (Thread)
    def get_like_middle_eng_thread(self, eng1, eng2, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'{self.escape_string_like(eng1)}%{self.escape_string_like(eng2)}%',))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng phía sau ngắn nhất (Thread)
    def get_like_rear_eng_thread(self, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'{self.escape_string_like(eng)}%',))
        result = cursor.fetchone()
        return result

    #Thêm row mới vào database
    def new_row(self, eng, vie):
        sql_insert = '''INSERT INTO CAU_GOC(eng, vie)
            VALUES(?,?)
            '''
        self.cursor.execute(sql_insert, (eng, vie))
        return self.cursor.lastrowid

    #Cập nhật row vào database
    def update_row(self, id_, eng, vie):
        sql_update = '''UPDATE CAU_GOC
            SET eng= ?,
                vie = ?,
                ngay_sua = ?
            WHERE  id = ?
            '''
        self.cursor.execute(sql_update, (eng, vie, datetime.now(), id_))

    #Xóa row khỏi database
    def delete_row(self, id_):
        sql_delete = '''DELETE FROM CAU_GOC
        WHERE  id = ?
        '''
        self.cursor.execute(sql_delete, (id_,))

    #Thật sự lưu dữ liệu xuống tiệp tin database
    def save_database(self):
        self.conSqlite.commit()

    #Đóng database an toàn
    def __del__(self):
        self.cursor.close()
        self.conSqlite.close()