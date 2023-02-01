#TepTin.py
#Quản lý xuất nhập tệp tin

import os
import re
import csv
import json
import shutil
import gzip
from ..HamChung import Chuyen_Doi_Ky_Tu_Dat_Biet

class TepTin:
    '''Quản lý vấn đề xuất nhập tệp tin'''
    def __init__(self):
        self.tep_khong_chuyen_ngu = os.path.join(os.getcwd(), 'khong_chuyen_ngu.txt')
        
    def Kiem_Tra_Tep_Ton_Tai(self, ten_tep):
        '''Kiểm tra tệp có tồn tại và thật sự là tệp tin chứ không phải thư mục
        Trả về:
            ket_qua: boolean
        '''
        return ten_tep != '' and os.path.exists(ten_tep) and os.path.isfile(ten_tep)
        
    def Ghi_Khong_Chuyen_Ngu(self, du_lieu):
        '''Ghi ra tệp tep_khong_chuyen_ngu những câu chưa chuyển ngữ
        Đầu vào:
            du_lieu: list (đơn)
        Xuất ra:
            self.tep_khong_chuyen_ngu: tệp kiểu Csv
        '''
        with open(self.tep_khong_chuyen_ngu, 'w', encoding = 'utf-8', newline = '') as ghi_tep:
            ghi_csv = csv.writer(ghi_tep, delimiter = ',')
            #Ghi tiêu đề
            ghi_csv.writerow(['STT', 'Chưa chuyển ngữ'])
            #Duyệt ghi dữ liệu
            dem = 1
            for dong in du_lieu:
                if len(dong) > 0:
                    ghi_csv.writerow([dem, dong])
                    dem +=1
        
    def Doc_XUnity(self, ten_tep):
        '''Đọc tệp kiểu txt có định dạng XUnity
        Định dạng kiểu: tiếng_Anh=tiếng_việt
        Đầu vào
            ten_tep: string #Đường dẫn tệp
        Đầu ra:
            ket_qua: list [(eng, vie)]
        '''
        ket_qua = []
        #Nếu tệp tồn tại thì đọc từng dòng
        def Chuyen_Ky_Tu(chuoi):
            ky_tus = {'\n' : '\\n', '\t' : '\\t', '\r' : '\\r','\\' : '\\\\'}
            ket_qua = chuoi
            for khoa in ky_tus:
                ket_qua = khoa.join(ket_qua.split(ky_tus[khoa]))
            return ket_qua
        with open(ten_tep, 'r', encoding = 'utf-8') as doc_tep:
            for dong in doc_tep:
                tach = []
                if len(dong) > 1:
                    #tach = dong[:-1].split('=') #Bỏ ký tự \n ở cuối và tách chuỗi
                    tach = dong.split('=')
                #Nếu chí có khóa và ngôn ngữ
                so_luong = len(tach)
                if so_luong == 1:
                    eng = Chuyen_Ky_Tu(tach[0])
                    ket_qua.append((eng, ''))
                elif so_luong > 1:
                    eng = Chuyen_Ky_Tu(tach[0])
                    vie = Chuyen_Ky_Tu(tach[1])
                    ket_qua.append((eng, vie))
        return ket_qua
        
    def Ghi_XUnity(self, ten_tep, du_lieu):
        '''Ghi dữ liệu theo định dạng XUnity
        Đầu vào:
            ten_tep: string #Đường dẫn tệp
            du_lieu: list (eng, vie)
        Đầu ra:
            Đổ dữ liệu ra tiệp có tên: ten_tep '''
        with open(ten_tep, 'w', encoding = 'utf-8') as ghi_tep:
            for dong in du_lieu:
                #Loại bỏ ký tự xuống dòng '\n'
                eng = Chuyen_Doi_Ky_Tu_Dat_Biet(dong[0])
                vie = Chuyen_Doi_Ky_Tu_Dat_Biet(dong[1])
                ghi_tep.write(f'{eng}={vie}\n')
        
    def Doc_Json(self, ten_tep):
        '''Đọc tệp có định dạng Json
        Đầu vào:
            ten_tep: string #Đường dẫn tệp
        Đầu ra:
            ket_qua: Json
        '''
        ket_qua = []
        with open(ten_tep, "r", encoding = 'utf-8') as doc_tep:
            try:
                ket_qua = json.loads(doc_tep.read())
            except ValueError as ex:
                print(f'Gặp lỗi khi đọc tệp kiểu Json.\nTên tệp: {ten_tep}.\nThông điệp báo lỗi: {ex}')
        return ket_qua
        
    def Ghi_Json(self, ten_tep, du_lieu):
        '''Ghi tệp có định dạng Json
        Đầu vào:
            ten_tep: string #Đường dẫn tệp
            du_lieu: Json
        '''
        with open(ten_tep, 'w', encoding = 'utf-8') as ghi_tep:
            json.dump(du_lieu, ghi_tep, ensure_ascii=False, indent=4)

    def Doc_Csv(self, ten_tep, dau_phan_cach = ','):
        '''Đọc toàn bộ dữ liệu trong tệp Csv
        Đầu vào:
            ten_tep: string #Đường dẫn tệp
        Trả về
            {'tieu_de' : list, 'du_lieu' : list}
        '''
        du_lieu = []
        tieu_de = []
        with open(ten_tep, "r", encoding = 'utf-8') as doc_tep:
            doc_csv = csv.reader(doc_tep, delimiter = dau_phan_cach)
            tieu_de = next(doc_csv)
            for dong in doc_csv:
                    du_lieu.append(dong)
        return {'tieu_de' : tieu_de, 'du_lieu' : du_lieu}
        
    def Doc_Cot_Csv(self, du_lieu = []):
        '''Đọc 2 cột dữ liệu tệp trong cùng 1 tiệp Csv
        Đầu vào du_lieu với các khóa:
            tep_eng: string #đường dẫn tệp
            cot_eng, cot_vie: int #Cột chỉ định câu eng/vie
        Trả về:
            ket_qua: list [('dữ liệu cot_eng', 'dữ liệu cot_vie')]
        '''
        ket_qua = []
        #return ket_qua
        with open(du_lieu['tep_eng'], "r", encoding = 'utf-8') as doc_tep:
            doc_csv = csv.reader(doc_tep, delimiter = du_lieu['dau_phan_cach'])
            tieu_de = next(doc_csv) #Bỏ qua tiêu đề
            for dong in doc_csv:
                so_cot = len(dong)
                #Cột eng không tồn tại
                if du_lieu['cot_eng'] >= so_cot:
                    continue
                if len(dong[du_lieu['cot_eng']]) != 0:
                    #Cột vie không tồn tại lấy cột cuối cùng
                    if du_lieu['cot_vie'] < so_cot:
                        ket_qua.append((dong[du_lieu['cot_eng']], dong[du_lieu['cot_vie']]))
                    else:
                        ket_qua.append((dong[du_lieu['cot_eng']], dong[so_cot - 1]))
        return ket_qua
        
    def Doc_Cot_2_Csv(self, du_lieu = []):
        '''Đọc 2 cột dữ liệu tệp từ 2 tiệp Csv tương ứng
        Đầu vào du_lieu với các khóa:
            tep_eng, tep_vie: string #đường dẫn tệp
            cot_eng, cot_vie: int #Cột chỉ định câu eng/vie
            cot_khoa_eng, cot_khoa_vie: int #Cột chỉ định khóa tương ứng
        Trả về:
            ket_qua: list [('dữ liệu cot_eng', 'dữ liệu cot_vie')]
        '''
        du_lieu_eng = {}
        ket_qua = []
        #Đọc dữ liệu từ tệp tep_eng
        with open(du_lieu['tep_eng'], "r", encoding = 'utf-8') as doc_tep_eng:
            doc_csv_eng = csv.reader(doc_tep_eng, delimiter = du_lieu['dau_phan_cach'])
            tieu_de = next(doc_csv_eng) #Bỏ qua tiêu đề
            for dong in doc_csv_eng:
                so_cot = len(dong)
                #Cột khóa eng hoặc cột eng không tồn tại
                if du_lieu['cot_khoa_eng']  >= so_cot or du_lieu['cot_eng'] >= so_cot:
                    continue
                if len(dong[du_lieu['cot_khoa_eng']]) != 0 and len(dong[du_lieu['cot_eng']]) != 0:
                    du_lieu_eng[dong[du_lieu['cot_khoa_eng']]] = dong[du_lieu['cot_eng']]
        #Đọc dữ liệu từ tệp tep_vie
        with open(du_lieu['tep_vie'], "r", encoding = 'utf-8') as doc_tep_vie:
            doc_csv_vie = csv.reader(doc_tep_vie, delimiter = du_lieu['dau_phan_cach'])
            tieu_de = next(doc_csv_vie) #Bỏ qua tiêu đề
            for dong in doc_csv_vie:
                so_cot = len(dong)
                #Cột khóa vie không tồn tại
                if du_lieu['cot_khoa_vie'] >= so_cot:
                    continue
                if dong[du_lieu['cot_khoa_vie']] in du_lieu_eng:
                    #Cột vie không tồn tại lấy cột cuối cùng
                    if du_lieu['cot_vie'] < so_cot:
                        ket_qua.append((du_lieu_eng[dong[du_lieu['cot_khoa_vie']]], dong[du_lieu['cot_vie']]))
                    else:
                        ket_qua.append((du_lieu_eng[dong[du_lieu['cot_khoa_vie']]], dong[so_cot - 1]))
        return ket_qua
        
    def Ghi_Csv(self, ten_tep, du_lieu = [], dau_phan_cach = ','):
        '''Lưu dữ liệu Csv ra tệp tin
        Đầu vào:
            ten_tep: string #Tên tệp lưu
            du_lieu: list['tieu_de', 'du_lieu']
                tieu_de: list #Tiêu đề
                du_lieu: list #Dữ liệu
        '''
        with open(ten_tep, 'w', encoding = 'utf-8', newline = '') as ghi_tep:
            ghi_csv = csv.writer(ghi_tep, delimiter = dau_phan_cach)
            #Ghi tiêu đề
            ghi_csv.writerow(du_lieu['tieu_de'])
            #Ghi nhiều hàng dữ liệu
            ghi_csv.writerows(du_lieu['du_lieu'])
        
    def Doc_Ini(self, ten_tep):
        '''Đọc đọc dữ liệu kiệu Ini từ tệp tin
        Đầu vào:
            ten_tep: string #Tên tệp
        Đầu ra:
            ket_qua: list[(khoa_id, [(khoa,gia_tri)])]
        '''
        danh_sach_dong = []
        with open(ten_tep, "r", encoding = 'utf-8') as doc_tep:
            danh_sach_dong = doc_tep.readlines()
        khoa_id = ('default', [])
        ket_qua = []
        ket_qua.append(khoa_id)
        for dong_l in danh_sach_dong:
            dong = dong_l.strip()
            #Bỏ qua dòng rỗng
            if len(dong) == 0:
                continue
            #Bỏ qua chú thích
            if dong[:1] == ';':
                continue
            #Kiểm tra có phải id không
            loc = re.findall(r'^\[([^\[]+)\]$', dong)
            if len(loc) == 1:
                khoa_id = (loc[0], [])
                ket_qua.append(khoa_id)
                continue
            tach_chuoi = dong.split('=')
            if len(tach_chuoi) == 2: #Bình thường
                khoa_id[1].append((tach_chuoi[0], tach_chuoi[1]))
            elif len(tach_chuoi) == 1: #Lỗi mới xảy ra
                khoa_id[1].append((tach_chuoi[0], ''))
            else: #Có vấn đề gì đó với dấu bằng (=)
                khoa_id[1].append((tach_chuoi[0], '='.join(tach_chuoi[1:])))
        #Xóa bỏ default nếu không tồn tại
        if len(ket_qua) > 0:
            if len(ket_qua[0][1]) == 0:
                return ket_qua[1:]
        return ket_qua
        
    def Ghi_Ini(self, ten_tep, du_lieu):
        '''Ghi dữ liệu kiểu Ini ra tệp tin
        Đầu vào:
            ten_tep: string #Tên tệp
            du_lieu: ket_qua: list[(khoa_id, [(khoa,gia_tri)])] #Dữ liệu cần ghi
        '''
        with open(ten_tep, 'w', encoding = 'utf-8') as ghi_tep:
            for khoa_id in du_lieu:
                ghi_tep.write(f'[{khoa_id[0]}]\n')
                for gia_tri in khoa_id[1]:
                    ghi_tep.write(f'{gia_tri[0]}={Chuyen_Doi_Ky_Tu_Dat_Biet(gia_tri[1])}\n')
                ghi_tep.write('\n')
        
    def Nen_Tep_Gzip(self, tep_nguon, tep_dich):
        '''Đọc tệp nguồn nén thành tệp đích
        Đầu vào:
            tep_nguon: string #Tên tệp cần nén
            tep_dich: string #Tên tệp nén
        '''
        with open(tep_nguon, 'rb') as doc_tep:
            with gzip.open(tep_dich, 'wb') as ghi_tep:
                shutil.copyfileobj(doc_tep, ghi_tep)