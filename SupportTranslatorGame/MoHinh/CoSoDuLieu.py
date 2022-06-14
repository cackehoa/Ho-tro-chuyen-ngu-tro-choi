#CoSoDuLieu.py
#Quản lý xuất nhập cơ sở dữ liệu
import os
import sqlite3
import re
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
        '''Tạo bảng tương ứng trong csdl'''
        sql_create = '''CREATE TABLE CAU_GOC (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            eng TEXT NOT NULL,
            vie TEXT DEFAULT '',
            ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
            ngay_sua DATETIME DEFAULT CURRENT_TIMESTAMP
            );'''
        self.ket_noi_sqlite.execute(sql_create)
        print('Tạo bảng CAU_GOC thành công')
        
    def Danh_Sach_Loc(self, bat_dau, so_dong, sap_xep = 'eng', thu_tu = 'ASC', tu_khoa = ''):
        '''Hiển thị danh sách đã được lọc
        Đầu vào:
            bat_dau: int
            so_dong: int
            tu_khoa: string
            sap_xep: id/eng/vie/ngay_tao/ngay_sua
            thu_tu: ASC/DESC
        Trả lại:
            ket_qua: list
        '''
        if tu_khoa == '':
            sql_select = '''SELECT id, eng, vie
                FROM CAU_GOC
                ORDER BY eng
                LIMIT ?, ?
                '''
            self.con_tro.execute(sql_select, (bat_dau, so_dong))
        else:
            sql_select = '''SELECT id, eng, vie
                FROM CAU_GOC
                WHERE eng LIKE ?
                ORDER BY eng
                LIMIT ?, ?
                '''
            self.con_tro.execute(sql_select, (f'%{tu_khoa}%', bat_dau, so_dong))
        ket_qua = self.con_tro.fetchall()
        return ket_qua
    
    def Lay_Eng(self, eng):
        '''Tìm câu tiếng anh tương ứng có trong csdl
        Đầu vào:
            eng: string
        '''
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng=?
            '''
        self.con_tro.execute(sql_select, (eng,))
        ket_qua = self.con_tro.fetchone()
        return ket_qua
    
    def Lay_Id(self, id):
        '''Tìm id tương ứng có trong csdl
        Đầu vào:
            id: int
        '''
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE id=?
            '''
        self.con_tro.execute(sql_select, (id,))
        ket_qua = self.con_tro.fetchone()
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
            VALUES(?,?)
            '''
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
            WHERE  id = ?
            '''
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
            WHERE  id = ?
            '''
        self.con_tro.execute(sql_update, (eng, vie, datetime.now(), id))
        
    def Xoa_Cau_Goc(self, id):
        '''Xóa câu gốc có id
        Đầu vào:
            id: int
        '''
        sql_delete = '''DELETE FROM CAU_GOC
        WHERE  id = ? '''
        self.con_tro.execute(sql_delete, (id,))
    
    def Xoa_Cau_Rac(self):
        '''Xóa câu rác:
        - Có tiếng Anh với tiếng Việt giống nhau
        - Câu tiếng Anh quá ngắn
        - Câu tiếng Việt không giá trị
        '''
        sql_delete = '''DELETE FROM CAU_GOC
        WHERE eng = vie or length(eng) < 2 or length(vie) < 1
        '''
        self.con_tro.execute(sql_delete)
        
    def Chuyen_Ngu(self, eng, co_dich = 0):
        '''Cố chuyển câu tiếng Anh sang tiếng Việt nhiều nhất có thể
        Đầu vào:
            eng: string #Câu tiếng Anh
            co_dich: int #Cố dịch = 1
        Đầu ra:
            vie: string #Câu tiếng Việt hoặc eng
        '''
        if len(eng) > 1:
            cau_eng = self.Lay_Eng(eng)
            if cau_eng is not None:
                return cau_eng[2]
            #Tách nhỏ câu ra để dịch
            if co_dich == 1:
                def Chia_Nho_Cau(van_ban, dieu_kien_chia = '\n'):
                    '''Chia nhỏ câu theo dieu_kien_chia rồi dịch và nối lại
                    Đầu vào:
                        van_ban: string
                        dieu_kien_chia: string
                    Đầu ra:
                        vie: string
                    '''
                    cau_chuyen_ngu = []
                    tach_van_ban = van_ban.split(dieu_kien_chia)
                    for cau in tach_van_ban:
                        cau_chuyen_ngu.append(self.Chuyen_Ngu(cau.strip(), 1))
                    return dieu_kien_chia.join(cau_chuyen_ngu)
                    
                def Boc_Dau_Cuoi(van_ban, dau_boc_dau, dau_boc_cuoi):
                    '''Bọc đầu - cuối để tìm kết quả tương ứng trong csdl
                    Đầu vào:
                        van_ban: string
                        dau_boc_dau: char
                        dau_boc_cuoi: char
                    Đầu ra:
                        vie: string #rỗng nếu không dịch được
                    '''
                    cau_eng = self.Lay_Eng(dau_boc_dau + van_ban + dau_boc_cuoi)
                    if cau_eng is not None:
                        vie = cau_eng[2]
                        if vie[:len(dau_boc_dau)] == dau_boc_dau:
                            if vie[-len(dau_boc_cuoi):] == dau_boc_cuoi:
                                return vie[len(dau_boc_dau):-len(dau_boc_cuoi)]
                            return vie[len(dau_boc_dau):]
                        elif vie[-len(dau_boc_cuoi):] == dau_boc_cuoi:
                            return vie[:-len(dau_boc_cuoi)]
                        return vie
                    return None
                    
                #Phân tách câu dạng: number + string
                #VD: +1 day
                mau_tach = '^([\-\+]{0,1}[\s]*[0-9]+[0-9\.\,]*[\s]*)([\S\s]+)$'
                chuoi_tach = re.findall(mau_tach, eng)
                if len(chuoi_tach) > 0:
                    return chuoi_tach[0][0] + self.Chuyen_Ngu(chuoi_tach[0][1], 1)
                #Bỏ rác đầu chuỗi
                mau_rac = '^([\-\+\*\$\?\s\^\.\\\\,&#!…%@=:;_~`“”\"\'\{\}\[\]\|\(\)]+)([\S\s]+)$'
                chuoi_tach = re.findall(mau_rac, eng)
                if chuoi_tach:
                    return chuoi_tach[0][0] + self.Chuyen_Ngu(chuoi_tach[0][1], 1)
                #Bỏ rác cuối chuỗi
                chuoi_tach = re.findall(mau_rac, eng[::-1])
                if chuoi_tach:
                    chuoi_nguoc = chuoi_tach[0][1]
                    rac_nguoc = chuoi_tach[0][0]
                    return self.Chuyen_Ngu(chuoi_nguoc[::-1], 1) + rac_nguoc[::-1]
                #Bọc câu bằng dấu bọc dau_boc để hy vọng tìm được giá trị tương ứng trong csdl
                #Xử lý hết các trường hợp chậm: chỉ xử lý 3 trường hợp cơ bản
                #1/ Dấu bọc đặt biệt '“', '”'
                vie = Boc_Dau_Cuoi(eng, '“', '”')
                if vie is not None:
                    return vie
                #2/ Dấu bọc thường
                dau_bocs = ['"', '“', '”', '\'', '...']
                for dau_boc in dau_bocs:
                    vie = Boc_Dau_Cuoi(eng, dau_boc, dau_boc)
                    if vie  is not None:
                        return vie
                    #Bọc đầu
                    cau_eng = self.Lay_Eng(dau_boc + eng)
                    if cau_eng is not None:
                        vie = cau_eng[2]
                        if vie[:len(dau_boc)] == dau_boc:
                            return vie[len(dau_boc):]
                        return vie
                    #Bọc cuối
                    cau_eng = self.Lay_Eng(eng + dau_boc)
                    if cau_eng is not None:
                        vie = cau_eng[2]
                        if vie[-len(dau_boc):] == dau_boc:
                            return vie[:-len(dau_boc)]
                        return vie
                #3/ Dấu bọc đặt biệt ngược '”', '“'
                vie = Boc_Dau_Cuoi(eng, '”', '“')
                if vie  is not None:
                    return vie
                #Chia nhỏ câu theo dấu câu
                dau_caus = ['\n', '\\n', '.', '!', '?', ';', '…', ':'] #Điểm tách là dấu câu
                for dau_cau in dau_caus:
                    #Thêm dấu câu dau_cau cuối câu hy vọng tìm giá trị tương ứng có csdl
                    cau_eng = self.Lay_Eng(eng + dau_cau)
                    if cau_eng is not None:
                        vie = cau_eng[2]
                        #Xóa dấu câu tránh gấp đôi
                        if vie[-len(dau_cau):] == dau_cau:
                            return vie[:-len(dau_cau)]
                        return vie
                    #Tách tại điểm tách và 1 ký tự rỗng theo sau
                    if eng.find(dau_cau + ' ') != -1:
                        return Chia_Nho_Cau(eng, dau_cau + ' ')
                    #Tách tại điểm tách
                    if eng.find(dau_cau) != -1:
                        return Chia_Nho_Cau(eng, dau_cau)
                #Tách nhỏ theo thẻ html
                mau_html = '(<[\S\s]+>)'
                chuoi_tach = re.findall(mau_html, eng)
                for chuoi in chuoi_tach:
                    return Chia_Nho_Cau(eng, chuoi)
                #Tách câu theo dấu câu để cố dịch thử
                #-- Nhiều khả năng xuất hiện kết quả đã kiểm thử ở trên
                #-- Tìm cách giảm (nếu có thể) giúp tăng tốc
                dau_tachs = ['"', '“', '”', '-', '*', '#', ',', '\'']
                for dau_tach in dau_tachs:
                    if eng.find(' ' + dau_tach + ' ') != -1:
                        return Chia_Nho_Cau(eng, ' ' + dau_tach + ' ')
                    if eng.find(dau_tach + ' ') != -1:
                        return Chia_Nho_Cau(eng, dau_tach + ' ')
                    if eng.find(' ' + dau_tach) != -1:
                        return Chia_Nho_Cau(eng, ' ' + dau_tach)
                    if eng.find(dau_tach) != -1:
                        return Chia_Nho_Cau(eng, dau_tach)
        return eng #Trả lại câu tiếng Anh
    
    def __del__(self):
        '''Hàm hủy dùng để ngắt kết nối đến cơ sở dữ liệu '''
        self.ket_noi_sqlite.commit() #Lưu dữ liệu
        self.ket_noi_sqlite.close()
