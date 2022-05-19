#CoSoDuLieu.py
#Quản lý xuất nhập cơ sở dữ liệu
import os
import sqlite3
from datetime import datetime

class CoSoDuLieu:
    '''Quản lý xuất nhập cơ sở dữ liệu'''
    def __init__(self, tep_csdl):
        '''Hàm khởi tạo kết nối đến cơ sở dữ liệu mặc định database.db'''
        self.Ket_Noi(tep_csdl)
        
    def Ket_Noi(self, tep_csdl):
        '''Kết nối đến tệp tep_csdl'''
        tep_ton_tai = os.path.exists(tep_csdl) and os.path.isfile(tep_csdl)
        self.ket_noi_sqlite = sqlite3.connect(tep_csdl)
        self.con_tro = self.ket_noi_sqlite.cursor()
        #Nếu tep_csdl không tồn tại thì tạo bảng tương ứng
        if not tep_ton_tai:
            self.Tao_Bang()
        
    def Danh_Sach_Bang(self):
        '''Lấy danh sách tên bảng có trong csdl
        Đầu ra:
            ket_qua: danh sách tên bảng
        '''
        sql = '''SELECT name
            FROM sqlite_schema
            WHERE type ='table' AND name NOT LIKE 'sqlite_%';'''
        ket_qua_sql = self.ket_noi_sqlite.execute(sql)
        ket_qua = []
        for hang in ket_qua_sql:
            ket_qua.append(hang[0])
        return ket_qua;
        
    def Tao_Bang(self):
        '''Tạo bảng tương ứng'''
        sql_create = '''CREATE TABLE CAU_GOC (
        id INTEGER  PRIMARY KEY AUTOINCREMENT,
        eng TEXT NOT NULL,
        vie TEXT DEFAULT '',
        ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
        ngay_sua DATETIME DEFAULT CURRENT_TIMESTAMP
        );'''
        self.ket_noi_sqlite.execute(sql_create)
        print('Tạo bảng CAU_GOC thành công')
        
    def Danh_Sach_Loc(self, bat_dau, so_dong, tu_khoa):
        if tu_khoa == '':
            sql_select = '''SELECT id, eng, vie
                FROM CAU_GOC
                ORDER BY eng
                LIMIT ?, ? '''
            self.con_tro.execute(sql_select, (bat_dau, so_dong))
        else:
            sql_select = '''SELECT id, eng, vie
                FROM CAU_GOC
                WHERE eng LIKE ?
                ORDER BY eng
                LIMIT ?, ? '''
            self.con_tro.execute(sql_select, (f'%{tu_khoa}%', bat_dau, so_dong))
        ket_qua = self.con_tro.fetchall()
        return ket_qua
    
    def Lay_Eng(self, eng):
        '''Tìm câu tiếng anh tương ứng có trong csdl
        Đầu vào:
            eng: string
        '''
        sql_select = '''SELECT *
            FROM CAU_GOC
            WHERE eng=? '''
        self.con_tro.execute(sql_select, (eng,))
        ket_qua = self.con_tro.fetchall()
        return ket_qua
    
    def Lay_Id(self, id):
        '''Tìm id tương ứng có trong csdl
        Đầu vào:
            id: int
        '''
        sql_select = '''SELECT *
            FROM CAU_GOC
            WHERE id=? '''
        self.con_tro.execute(sql_select, (id,))
        ket_qua = self.con_tro.fetchall()
        return ket_qua
        
    def Nhap_Cau_Goc(self, eng, vie):
        '''Hàm nhập câu gốc đơn
        Đầu vào:
            eng: string
            vie: string
        Trả về
            id được tạo ra cuối cùng: int
        '''
        sql_insert = '''INSERT INTO CAU_GOC(eng, vie)
            VALUES(?,?) '''
        self.con_tro.execute(sql_insert, (eng, vie))
        return self.con_tro.lastrowid
        
    def Cap_Nhat_Vie(self, id, vie):
        '''Cập nhật tiếng Việt của id
        Đầu vào:
            id: int
            vie: string
        '''
        sql_update = '''UPDATE CAU_GOC
            SET vie = ?, ngay_sua = ?
            WHERE  id = ? '''
        self.con_tro.execute(sql_update, (vie, datetime.now(), id))
        
    def Cap_Nhat_Cau_Goc(self, id, eng, vie):
        '''Hàm cập nhật câu gốc
        Đầu vào:
            id: int
            eng: string
            vie: string '''
        sql_update = '''UPDATE CAU_GOC
            SET eng= ?,
                vie = ?,
                ngay_sua = ?
            WHERE  id = ? '''
        self.con_tro.execute(sql_update, (eng, vie, datetime.now(), id))
        
    def Xoa_Cau_Goc(self, id):
        '''Xóa câu gốc có id
        Đầu vào:
            id: int
        '''
        sql_delete = '''DELETE FROM CAU_GOC
        WHERE  id = ? '''
        self.con_tro.execute(sql_delete, (id,))
        
    def __del__(self):
        '''Hàm hủy dùng để ngắt kết nối đến cơ sở dữ liệu '''
        self.ket_noi_sqlite.commit() #Lưu dữ liệu
        self.ket_noi_sqlite.close()
