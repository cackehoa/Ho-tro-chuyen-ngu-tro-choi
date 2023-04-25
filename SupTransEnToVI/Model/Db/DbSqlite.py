'''Sqlite.py
Quản lý việc kết nối với Sqlite
'''
import os
import sqlite3
from datetime import datetime

class DbSqlite:
    def __init__(self, fileDatabase):
        isFile = os.path.exists(fileDatabase) and os.path.isfile(fileDatabase)
        self.conSqlite = sqlite3.connect(fileDatabase, check_same_thread = False)
        self.cursor = self.conSqlite.cursor()
        if not isFile:
            self.create_table()

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
                WHERE eng LIKE ?
                ORDER BY length(eng), eng
                LIMIT ?, ?
                '''
            self.cursor.execute(sql_select, (f'%{key}%', startRow, maxRow))
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

    #Lấy theo eng
    def get_eng(self, eng):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng=?
            '''
        self.cursor.execute(sql_select, (eng,))
        result = self.cursor.fetchone()
        return result

    #Lấy câu gần đúng ngắn nhất
    def get_like_eng(self, eng):
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng LIKE ?
            ORDER BY length(eng), eng
            '''
        self.cursor.execute(sql_select, (f'%{eng}%',))
        result = self.cursor.fetchone()
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
        WHERE  id = ? '''
        self.cursor.execute(sql_delete, (id_,))

    #Thật sự lưu dữ liệu xuống tiệp tin database
    def save_database(self):
        self.conSqlite.commit()

    #Đóng database an toàn
    def __del__(self):
        self.conSqlite.close()