#MoHinh.py
#Model: Quản lý việc xuất nhập dữ liệu

from .TepTin import TepTin
from .CoSoDuLieu import CoSoDuLieu

class MoHinh:
    def __init__(self, tep_csdl):
        '''Hàm khởi tạo'''
        self.tep_tin = TepTin()
        self.csdl = CoSoDuLieu(tep_csdl)
        
    def Lay_Tep(self):
        return self.tep_tin
    
    def Lay_Csdl(self):
        return self.csdl
    