#TepTin.py
#Quản lý xuất nhập tệp tin

import os
import json

class TepTin:
    '''Quản lý vấn đề xuất nhập tệp tin'''
    def __init__(self):
        pass
        
    def Kiem_Tra_Tep_Ton_Tai(self, ten_tep):
        '''Kiểm tra tệp có tồn tại và thật sự là tệp tin chứ không phải thư mục'''
        return os.path.exists(ten_tep) and os.path.isfile(ten_tep)
        
    def Doc_XUnity(self, ten_tep):
        '''Đọc tệp kiểu txt có định dạng XUnity
        Định dạng kiểu: tiếng_Anh=tiếng_việt
        Đầu vào
            ten_tep: đường dẫn tệp
        Đầu ra:
            ket_qua: danh sách kiểu (eng, vie)
        '''
        ket_qua = []
        #Nếu tệp tồn tại thì đọc từng dòng
        with open(ten_tep, 'r', encoding='utf-8') as doc_tep:
            for dong in doc_tep:
                #Bỏ ký tự \n ở cuối và tách chuỗi
                tach = []
                if len(dong) > 1:
                    tach = dong[:-1].split('=')
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
            ten_tep: đường dẫn tệp
            du_lieu: có định dạng (eng, vie)
        Đầu ra:
            Đổ dữ liệu ra tiệp có tên: ten_tep '''
        with open(ten_tep, 'w', encoding='utf-8') as ghi_tep:
            for dong in du_lieu:
                ghi_tep.write(f'{dong[0]}={dong[1]}\n')
        
    def Doc_Json(self, ten_tep):
        '''Đọc tệp có định dạng Json
        Đầu vào:
            ten_tep: đường dẫn tệp
        Đầu ra:
            du_lieu: Json '''
        du_lieu = []
        with open(ten_tep, "r", encoding='utf-8') as doctep:
            du_lieu = json.loads(doctep.read())
        return du_lieu
        
    def Ghi_Json(self, ten_tep, du_lieu):
        pass