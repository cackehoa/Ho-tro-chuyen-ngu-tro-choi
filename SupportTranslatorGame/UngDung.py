#UngDung.py
#App: Lớp trung gian nhằm kết nối MVC

import tkinter as tk
from .HienThi import HienThi
from .DieuKhien import DieuKhien
from .MoHinh import MoHinh

class UngDung(tk.Tk):
    '''Khởi tạo ứng dụng thừa kế tkinter
    Có  nhiệm vụ kết nối mô hình - hiển thị - điều khiển với nhau'''
    def __init__(self, tep_csdl):
        super().__init__()
        #Tiêu đề
        self.title('Hỗ trợ chuyển ngữ trò chơi')
        #Kích thước GUI
        #self.geometry('485x495')
        self.resizable(False, False)
        hien_thi = HienThi(self)
        mo_hinh = MoHinh(tep_csdl)
        dieu_khien = DieuKhien(mo_hinh, hien_thi)
        hien_thi.Nhap_Dieu_Khien(dieu_khien)
