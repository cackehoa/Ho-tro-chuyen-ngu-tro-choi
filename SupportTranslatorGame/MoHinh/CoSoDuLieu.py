#CoSoDuLieu.py
#Quản lý xuất nhập cơ sở dữ liệu
import threading
import sqlite3
import time
import os
import re
from datetime import datetime
from ..HamChung import Loc_Khoang_Trang

class CoSoDuLieu:
    '''Quản lý xuất nhập cơ sở dữ liệu'''
    def __init__(self, tep_csdl):
        self.tep_csdl = tep_csdl
        '''Hàm khởi tạo kết nối đến cơ sở dữ liệu mặc định database.db'''
        self.Ket_Noi(tep_csdl)
        
    def Loc_Khoang_Trang(self, chuoi):
        '''Bỏ khoảng trắng thừa và ký tự đặt biệt đầu và cuối chuỗi
        Giữ lại ký tự xuống dòng '\n'
        '''
        cat_dau_duoi = chuoi.strip()
        doan_vans = cat_dau_duoi.split('\n')
        loc_khoan_trang = []
        for doan in doan_vans:
            loc_khoan_trang.append(' '.join(doan.split()))
        ket_qua = '\n'.join(loc_khoan_trang)
        return ket_qua
        
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
        return self.Lay_Eng_Thread(eng, self.con_tro)
    
    def Lay_Eng_Thread(self, eng, con_tro):
        '''Tìm câu tiếng anh tương ứng có trong csdl
        Dành cho chạy đa luồng
        Đầu vào:
            eng: string
        '''
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE eng=?
            '''
        con_tro.execute(sql_select, (eng,))
        ket_qua = con_tro.fetchone()
        return ket_qua
        
    def Lay_Id(self, id_):
        '''Tìm id tương ứng có trong csdl
        Đầu vào:
            id_: int
        '''
        sql_select = '''SELECT id, eng, vie
            FROM CAU_GOC
            WHERE id=?
            '''
        self.con_tro.execute(sql_select, (id_,))
        ket_qua = self.con_tro.fetchone()
        return ket_qua
        
    def Nhap_Cau_Goc(self, eng, vie):
        '''Hàm nhập câu gốc đơn
        Đầu vào:
            eng: string
            vie: string
        Trả về
            id_: int #được tạo ra cuối cùng: int
        '''
        sql_insert = '''INSERT INTO CAU_GOC(eng, vie)
            VALUES(?,?)
            '''
        self.con_tro.execute(sql_insert, (eng, vie))
        return self.con_tro.lastrowid
        
    def Cap_Nhat_Vie(self, id_, vie):
        '''Cập nhật tiếng Việt của id
        Đầu vào:
            id_: int
            vie: string
        '''
        sql_update = '''UPDATE CAU_GOC
            SET vie = ?, ngay_sua = ?
            WHERE  id = ?
            '''
        self.con_tro.execute(sql_update, (vie, datetime.now(), id_))
        
    def Cap_Nhat_Cau_Goc(self, id_, eng, vie):
        '''Hàm cập nhật câu gốc
        Đầu vào:
            id_: int
            eng: string
            vie: string '''
        sql_update = '''UPDATE CAU_GOC
            SET eng= ?,
                vie = ?,
                ngay_sua = ?
            WHERE  id = ?
            '''
        self.con_tro.execute(sql_update, (eng, vie, datetime.now(), id_))
        
    def Xoa_Cau_Goc(self, id_):
        '''Xóa câu gốc có id
        Đầu vào:
            id_: int
        '''
        sql_delete = '''DELETE FROM CAU_GOC
        WHERE  id = ? '''
        self.con_tro.execute(sql_delete, (id_,))
    
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
        Dành cho luồng chính
        Đầu vào:
            eng: string #Câu tiếng Anh
            co_dich: int #Cố dịch = 1
        Đầu ra:
            vie: string #Câu tiếng Việt hoặc eng
        '''
        return self.Chuyen_Ngu_Thread(eng, co_dich, self.con_tro)
        
    def Chuyen_Ngu_Thread(self, eng, co_dich, con_tro):
        '''Cố chuyển câu tiếng Anh sang tiếng Việt nhiều nhất có thể
        Dành cho đa luồng
        Đầu vào:
            eng: string #Câu tiếng Anh
            co_dich: int #Cố dịch = 1
            con_tro: point #con trỏ sqlite3
        Đầu ra:
            vie: string #Câu tiếng Việt hoặc eng
        '''
        cau_eng = self.Lay_Eng_Thread(eng, con_tro)
        if cau_eng is not None:
            return cau_eng[2]
        #Tách nhỏ câu ra để dịch
        if co_dich == 1:
            def Chia_Nho_Cau(van_ban, dieu_kien_chia, con_tro):
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
                    cau_chuyen_ngu.append(self.Chuyen_Ngu_Thread(cau.strip(), 1, con_tro))
                return dieu_kien_chia.join(cau_chuyen_ngu)
                
            def Boc_Dau_Cuoi(van_ban, dau_boc_dau, dau_boc_cuoi, con_tro):
                '''Bọc đầu - cuối để tìm kết quả tương ứng trong csdl
                Đầu vào:
                    van_ban: string
                    dau_boc_dau: char
                    dau_boc_cuoi: char
                Đầu ra:
                    vie: string #rỗng nếu không dịch được
                '''
                cau_eng = self.Lay_Eng_Thread(dau_boc_dau + van_ban + dau_boc_cuoi, con_tro)
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
            #Kiểm tra nếu là số thì bỏ qua    
            mau_tach_so = '^([\-\+]{0,1}[\s%\$]*[0-9]+[0-9\.\,]*[\s%\$MKmkBb]*)$'
            chuoi_tach = re.findall(mau_tach_so, eng)
            if len(chuoi_tach) > 0:
                return eng
            #Phân tách câu dạng: number + string
            #VD: +1 day
            mau_tach_so_dau = '^([\-\+]{0,1}[\s%\$]*[0-9]+[0-9\.\,]*[\s%\$]*)([\S\s]+)$'
            chuoi_tach = re.findall(mau_tach_so_dau, eng)
            if len(chuoi_tach) > 0:
                return chuoi_tach[0][0] + self.Chuyen_Ngu_Thread(chuoi_tach[0][1], 1, con_tro)
            #Phân tách câu dạng: string + number
            #VD: day + 1
            mau_tach_so_cuoi = '^([\s%\$]*[0-9\.\,]*[0-9]+[\s%\$]*[\-\+]{0,1}[\s]*)([\S\s]+)$'
            chuoi_tach = re.findall(mau_tach_so_cuoi, eng[::-1])
            if len(chuoi_tach) > 0:
                vie = chuoi_tach[0][1]
                so_cuoi = chuoi_tach[0][0]
                return self.Chuyen_Ngu_Thread(vie[::-1], 1, con_tro) + so_cuoi[::-1]
            #Bỏ rác đầu chuỗi
            mau_rac = '^([\-\+\*\$\?\s\^\.\\\\,&#!…%@=:;_~`“”\"\'\{\}\[\]\|\(\)]+)([\S\s]+)$'
            chuoi_tach = re.findall(mau_rac, eng)
            if len(chuoi_tach) > 0:
                return chuoi_tach[0][0] + self.Chuyen_Ngu_Thread(chuoi_tach[0][1], 1, con_tro)
            #Bỏ rác cuối chuỗi
            chuoi_tach = re.findall(mau_rac, eng[::-1])
            if len(chuoi_tach) > 0:
                chuoi_nguoc = chuoi_tach[0][1]
                rac_nguoc = chuoi_tach[0][0]
                return self.Chuyen_Ngu_Thread(chuoi_nguoc[::-1], 1, con_tro) + rac_nguoc[::-1]
            #Bọc câu bằng dấu bọc dau_boc để hy vọng tìm được giá trị tương ứng trong csdl
            #Xử lý hết các trường hợp chậm: chỉ xử lý 3 trường hợp cơ bản
            #1/ Dấu bọc đặt biệt '“', '”'
            vie = Boc_Dau_Cuoi(eng, '“', '”', con_tro)
            if vie is not None:
                return vie
            #2/ Dấu bọc thường
            dau_bocs = ['"', '“', '”', '\'', '…', '...']
            for dau_boc in dau_bocs:
                vie = Boc_Dau_Cuoi(eng, dau_boc, dau_boc, con_tro)
                if vie  is not None:
                    return vie
                #Bọc đầu
                cau_eng = self.Lay_Eng_Thread(dau_boc + eng, con_tro)
                if cau_eng is not None:
                    vie = cau_eng[2]
                    if vie[:len(dau_boc)] == dau_boc:
                        return vie[len(dau_boc):]
                    return vie
                #Bọc cuối
                cau_eng = self.Lay_Eng_Thread(eng + dau_boc, con_tro)
                if cau_eng is not None:
                    vie = cau_eng[2]
                    if vie[-len(dau_boc):] == dau_boc:
                        return vie[:-len(dau_boc)]
                    return vie
            #3/ Dấu bọc đặt biệt ngược '”', '“'
            vie = Boc_Dau_Cuoi(eng, '”', '“', con_tro)
            if vie  is not None:
                return vie
            #Chia nhỏ câu theo dấu câu
            dau_caus = ['\n', '\\n', '.', '!', '?', ';', '…', ':'] #Điểm tách là dấu câu
            for dau_cau in dau_caus:
                #Thêm dấu câu dau_cau cuối câu hy vọng tìm giá trị tương ứng có csdl
                cau_eng = self.Lay_Eng_Thread(eng + dau_cau, con_tro)
                if cau_eng is not None:
                    vie = cau_eng[2]
                    #Xóa dấu câu tránh gấp đôi
                    if vie[-len(dau_cau):] == dau_cau:
                        return vie[:-len(dau_cau)]
                    return vie
                #Chia nhỏ câu tại điểm tách và 1 ký tự rỗng theo sau
                if eng.find(dau_cau + ' ') != -1:
                    return Chia_Nho_Cau(eng, dau_cau + ' ', con_tro)
                #Chia nhỏ câu tại điểm tách
                if eng.find(dau_cau) != -1:
                    return Chia_Nho_Cau(eng, dau_cau, con_tro)
            #Chia nhỏ câu theo thẻ html
            mau_html = '(<[\S\s]+>)'
            chuoi_tach = re.findall(mau_html, eng)
            for chuoi in chuoi_tach:
                return Chia_Nho_Cau(eng, chuoi, con_tro)
            #Chia nhỏ câu câu theo dấu câu để cố dịch thử
            #-- Nhiều khả năng xuất hiện kết quả đã kiểm thử ở trên
            #-- Tìm cách giảm (nếu có thể) giúp tăng tốc
            dau_tachs = ['"', '“', '”', '-', '*', '#', ',', '\'', '@']
            for dau_tach in dau_tachs:
                if eng.find(' ' + dau_tach + ' ') != -1:
                    return Chia_Nho_Cau(eng, ' ' + dau_tach + ' ', con_tro)
                if eng.find(dau_tach + ' ') != -1:
                    return Chia_Nho_Cau(eng, dau_tach + ' ', con_tro)
                if eng.find(' ' + dau_tach) != -1:
                    return Chia_Nho_Cau(eng, ' ' + dau_tach, con_tro)
                if eng.find(dau_tach) != -1:
                    return Chia_Nho_Cau(eng, dau_tach, con_tro)
        return eng #Trả lại câu tiếng Anh
    
    def Chuyen_Ngu_XUnity(self, du_lieu, co_dich, kq_du_lieu, khong_chuyen_ngu):
        '''Hàm giúp chuyển ngữ loại XUnity
        Áp dụng phươn đa luồng nhằm tăng tốc
        Đầu vào:
            du_lieu: list #Dữ liệu cần chuyển ngữ
            co_dich: int(0,1) #Cố dịch
        Đầu ra:
            kq_du_lieu: list #Dữ liệu sau khi chuyển  ngữ
            khong_chuyen_ngu: list #Dữ liệu không chuyển ngữ dạng (STT,Chưa chuyển ngữ)
        '''
        def Duyet_Du_Lieu_XUnity(du_lieu, co_dich, kq_du_lieu, khong_chuyen_ngu):
            #Tạo con trỏ mới đến csdl
            ket_noi_sqlite = sqlite3.connect(self.tep_csdl)
            con_tro = ket_noi_sqlite.cursor()
            for dong in du_lieu:
                cau_eng = Loc_Khoang_Trang(dong[0])
                if len(cau_eng) < 2:
                    kq_du_lieu.append((dong[0], cau_eng))
                    continue #Bỏ qua câu ngắn hơn 2
                cau_vie = Loc_Khoang_Trang(dong[1])
                vie = self.Chuyen_Ngu_Thread(cau_eng, co_dich, con_tro)
                #Nếu không dịch được thì trả lại kết quả cũ hoặc chính câu tiếng Anh
                if vie == cau_eng:
                    if len(cau_vie) == 0:
                        kq_du_lieu.append((dong[0], vie))
                    else:
                        kq_du_lieu.append((dong[0], cau_vie))
                    if dong[0] not in khong_chuyen_ngu:
                        khong_chuyen_ngu.append(dong[0])
                else:
                    if len(vie) == 0:
                        kq_du_lieu.append((dong[0], cau_vie))
                        if dong[0] not in khong_chuyen_ngu:
                            khong_chuyen_ngu.append(dong[0])
                    else:
                        kq_du_lieu.append((dong[0], vie))
            #Đóng csdl
            ket_noi_sqlite.close()
        #Tạo số luồng bằng số CPU đang có
        so_thread = os.cpu_count()
        danh_sach_thread = []
        ket_qua_luong = []
        ket_qua_kocn = []
        so_dong = len(du_lieu)
        #Hạn chế tạo nhiều luồng khi số lượng dữ liệu nhỏ
        if so_dong <= so_thread:
            so_thread = 1
        #Khởi chạy so_thread luồng
        for cpu in range(so_thread):
            ket_qua_luong.append([])
            ket_qua_kocn.append([])
            luong = threading.Thread(target=Duyet_Du_Lieu_XUnity, args=(du_lieu[(so_dong*cpu)//so_thread:(so_dong*(cpu+1))//so_thread], co_dich, ket_qua_luong[cpu], ket_qua_kocn[cpu]))
            luong.start()
            danh_sach_thread.append(luong)
        #Đợi các luồng kết thúc
        for luong in danh_sach_thread:
            luong.join()
        #Nối các kết quả lại với nhau
        for ket_qua in ket_qua_luong:
            kq_du_lieu.extend(ket_qua)
        for ket_qua in ket_qua_kocn:
            khong_chuyen_ngu.extend(ket_qua)
        
    def Chuyen_Ngu_Csv(self, du_lieu_csv, cot_eng, cot_vie, co_dich, kq_du_lieu, khong_chuyen_ngu):
        '''Hàm giúp chuyển ngữ loại csv
        Áp dụng phươn đa luồng nhằm tăng tốc
        Đầu vào:
            du_lieu_csv: list #Dữ liệu cần chuyển ngữ
            cot_eng: int #Cột tiếng Anh
            cot_vie: int #Cột xuất tiếng Việt
            co_dich: int(0,1) #Cố dịch
        Đầu ra:
            kq_du_lieu: list #Dữ liệu sau khi chuyển  ngữ
            khong_chuyen_ngu: list #Dữ liệu không chuyển ngữ dạng (STT,Chưa chuyển ngữ)
        '''
        def Duyet_Du_Lieu_Csv(du_lieu_csv, cot_eng, cot_vie, co_dich, kq_du_lieu, khong_chuyen_ngu):
            '''Duyệt dữ liệu Csv và chuyển ngữ'''
            #Tạo con trỏ mới đến csdl
            ket_noi_sqlite = sqlite3.connect(self.tep_csdl)
            con_tro = ket_noi_sqlite.cursor()
            for dong in du_lieu_csv:
                so_dong = len(dong)
                #Cột tiếng Anh không tồn tại
                #Gặp một số tệp Csv không tiêu chuẩn
                if cot_eng >= so_dong:
                    kq_du_lieu.append(dong)
                    continue
                cau_eng = Loc_Khoang_Trang(dong[cot_eng])
                #Câu tiếng Anh quá ngắn < 2
                if len(cau_eng) < 2:
                    if cot_vie < so_dong:
                        dong[cot_vie] = cau_eng
                    else:
                        dong.append(cau_eng)
                    kq_du_lieu.append(dong)
                    continue
                vie = self.Chuyen_Ngu_Thread(cau_eng, co_dich, con_tro)
                if cau_eng == vie:
                    if cot_vie < so_dong and len(dong[cot_vie]) != 0:
                        vie = dong[cot_vie]
                    if dong[cot_eng] not in khong_chuyen_ngu:
                        khong_chuyen_ngu.append(dong[cot_eng])
                #Nếu cột Việt không tồn tại thì thêm vào cuối
                if cot_vie < so_dong:
                    dong[cot_vie] = vie
                else:
                    dong.append(vie)
                kq_du_lieu.append(dong)
            #Đóng csdl
            ket_noi_sqlite.close()
        #Tạo số luồng bằng số CPU đang có
        so_thread = os.cpu_count()
        danh_sach_thread = []
        ket_qua_luong = []
        ket_qua_kocn = []
        so_dong = len(du_lieu_csv)
        #Hạn chế tạo nhiều luồng khi số lượng dữ liệu nhỏ
        if so_dong <= so_thread:
            so_thread = 1
        #Khởi chạy so_thread luồng
        for cpu in range(so_thread):
            ket_qua_luong.append([])
            ket_qua_kocn.append([])
            luong = threading.Thread(target=Duyet_Du_Lieu_Csv, args=(du_lieu_csv[(so_dong*cpu)//so_thread:(so_dong*(cpu+1))//so_thread], cot_eng, cot_vie, co_dich, ket_qua_luong[cpu], ket_qua_kocn[cpu]))
            luong.start()
            danh_sach_thread.append(luong)
        #Đợi các luồng kết thúc
        for luong in danh_sach_thread:
            luong.join()
        #Nối các kết quả lại với nhau
        for ket_qua in ket_qua_luong:
            kq_du_lieu.extend(ket_qua)
        for ket_qua in ket_qua_kocn:
            khong_chuyen_ngu.extend(ket_qua)
    
    def Chuyen_Ngu_Json(self, du_lieu, co_dich, kq_du_lieu, khong_chuyen_ngu):
        '''Hàm giúp chuyển ngữ loại json
        Áp dụng phươn đa luồng nhằm tăng tốc
        Đầu vào:
            du_lieu: dict #Dữ liệu cần chuyển ngữ
            co_dich: int(0,1) #Cố dịch
        Đầu ra:
            kq_du_lieu: dict #Dữ liệu sau khi chuyển  ngữ
            khong_chuyen_ngu: list #Dữ liệu không chuyển ngữ dạng (STT,Chưa chuyển ngữ)
        '''
        def Duyet_Du_Lieu_Json(du_lieu, co_dich, khong_chuyen_ngu, con_tro):
            '''Hàm đệ quy duyệt dữ liệu dict và chuyển ngữ'''
            for khoa_chung in du_lieu:
                keu_du_lieu = type(du_lieu[khoa_chung])
                if keu_du_lieu is dict:
                    #Đệ quy
                    du_lieu[khoa_chung] = Duyet_Du_Lieu_Json(du_lieu[khoa_chung], co_dich, khong_chuyen_ngu, con_tro)
                elif keu_du_lieu is list or keu_du_lieu is tuple:
                    for dong  in range(du_lieu[khoa_chung]):
                        cau_eng = Loc_Khoang_Trang(du_lieu[khoa_chung][dong])
                        if len(cau_eng) > 1:
                            vie = self.Chuyen_Ngu_Thread(cau_eng, co_dich, con_tro)
                            if cau_eng == vie and du_lieu[khoa_chung][dong] not in khong_chuyen_ngu:
                                    khong_chuyen_ngu.append(du_lieu[khoa_chung][dong])
                            du_lieu[khoa_chung][dong] = vie
                        else:
                            du_lieu[khoa_chung][dong] = cau_eng
                else:
                    cau_eng = Loc_Khoang_Trang(du_lieu[khoa_chung])
                    if len(cau_eng) > 1:
                        vie = self.Chuyen_Ngu_Thread(cau_eng, co_dich, con_tro)
                        if cau_eng == vie and du_lieu[khoa_chung] not in khong_chuyen_ngu:
                                khong_chuyen_ngu.append(du_lieu[khoa_chung])
                        du_lieu[khoa_chung] = vie
                    else:
                        du_lieu[khoa_chung] = cau_eng
            return du_lieu
        def Thread_Json(du_lieu, co_dich, ket_qua, khong_chuyen_ngu):
            '''Hàm khởi tạo kết nối sqlite3 trước khi duyệt'''
            #Tạo con trỏ mới đến csdl
            ket_noi_sqlite = sqlite3.connect(self.tep_csdl)
            con_tro = ket_noi_sqlite.cursor()
            ket_qua.update(Duyet_Du_Lieu_Json(du_lieu, co_dich, khong_chuyen_ngu, con_tro))
            #Đóng csdl
            ket_noi_sqlite.close()
        #Tạo số luồng bằng số CPU đang có
        so_thread = os.cpu_count()
        danh_sach_thread = []
        ket_qua_luong = []
        ket_qua_kocn = []
        so_dong = len(du_lieu)
        #Hạn chế tạo nhiều luồng khi số lượng dữ liệu nhỏ
        if so_dong <= so_thread:
            so_thread = 1
        #Khởi chạy so_thread luồng
        for cpu in range(so_thread):
            ket_qua_luong.append({})
            ket_qua_kocn.append([])
            luong = threading.Thread(target=Thread_Json, args=(dict(list(du_lieu.items())[(so_dong*cpu)//so_thread:(so_dong*(cpu+1))//so_thread]), co_dich, ket_qua_luong[cpu], ket_qua_kocn[cpu]))
            luong.start()
            danh_sach_thread.append(luong)
        #Đợi các luồng kết thúc
        for luong in danh_sach_thread:
            luong.join()
        #Nối các kết quả lại với nhau
        for ket_qua in ket_qua_luong:
            kq_du_lieu.update(ket_qua)
        for ket_qua in ket_qua_kocn:
            khong_chuyen_ngu.extend(ket_qua)
    
    def __del__(self):
        '''Hàm hủy dùng để ngắt kết nối đến cơ sở dữ liệu '''
        #Lưu dữ liệu đã thay đổi
        self.ket_noi_sqlite.commit()
        #Đóng csdl
        self.ket_noi_sqlite.close()
