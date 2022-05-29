#TepTin.py
#Quản lý xuất nhập tệp tin

import os
import json
import csv

class TepTin:
    '''Quản lý vấn đề xuất nhập tệp tin'''
    def __init__(self):
        pass
        
    def Kiem_Tra_Tep_Ton_Tai(self, ten_tep):
        '''Kiểm tra tệp có tồn tại và thật sự là tệp tin chứ không phải thư mục
        Trả về:
            ket_qua: boolean
        '''
        return os.path.exists(ten_tep) and os.path.isfile(ten_tep)
        
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
        with open(ten_tep, 'r', encoding = 'utf-8') as doc_tep:
            for dong in doc_tep:
                tach = []
                if len(dong) > 1:
                    #tach = dong[:-1].split('=') #Bỏ ký tự \n ở cuối và tách chuỗi
                    tach = dong.split('=')
                #Nếu chí có khóa và ngôn ngữ
                so_luong = len(tach)
                if so_luong == 1:
                    ket_qua.append((tach[0], ''))
                elif len(tach) > 1:
                    ket_qua.append((tach[0], tach[1]))
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
                vie = '\\n'.join(dong[1].split('\n'))
                ghi_tep.write(f'{dong[0]}={vie}\n')
        
    def Doc_Json(self, ten_tep):
        '''Đọc tệp có định dạng Json
        Đầu vào:
            ten_tep: string #Đường dẫn tệp
        Đầu ra:
            ket_qua: Json
        '''
        ket_qua = []
        with open(ten_tep, "r", encoding = 'utf-8') as doc_tep:
            ket_qua = json.loads(doc_tep.read())
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
                if len(dong[du_lieu['cot_eng']]) != 0:
                    ket_qua.append((dong[du_lieu['cot_eng']], dong[du_lieu['cot_vie']]))
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
                if len(dong[du_lieu['cot_khoa_eng']]) != 0 and len(dong[du_lieu['cot_eng']]) != 0:
                    du_lieu_eng[dong[du_lieu['cot_khoa_eng']]] = dong[du_lieu['cot_eng']]
        #Đọc dữ liệu từ tệp tep_vie
        with open(du_lieu['tep_vie'], "r", encoding = 'utf-8') as doc_tep_vie:
            doc_csv_vie = csv.reader(doc_tep_vie, delimiter = du_lieu['dau_phan_cach'])
            tieu_de = next(doc_csv_vie) #Bỏ qua tiêu đề
            for dong in doc_csv_vie:
                if dong[du_lieu['cot_khoa_vie']] in du_lieu_eng:
                    ket_qua.append((du_lieu_eng[dong[du_lieu['cot_khoa_vie']]], dong[du_lieu['cot_vie']]))
        return ket_qua
        
    def Ghi_Csv(self, ten_tep, du_lieu = [], dau_phan_cach = ','):
        with open(ten_tep, 'w', encoding = 'utf-8', newline = '') as ghi_tep:
            ghi_csv = csv.writer(ghi_tep, delimiter = dau_phan_cach)
            #Ghi tiêu đề
            ghi_csv.writerow(du_lieu['tieu_de'])
            #Ghi nhiều hàng dữ liệu
            ghi_csv.writerows(du_lieu['du_lieu'])
        