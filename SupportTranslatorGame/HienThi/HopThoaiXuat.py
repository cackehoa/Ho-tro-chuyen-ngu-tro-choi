#HopThoaiXuat.py
#Hộp thoại quản lý nhập tệp tin đích và nguồn

from tkinter import ttk
from tkinter.simpledialog import Dialog as Hop_thoai

class HopThoaiXuat(Hop_thoai):
    def __init__(self, tk_goc, tieu_de):
        self.tk_goc = tk_goc
        self.tieu_de = tieu_de
        self.tep_nguon = '' #Tên tệp nguồn
        self.tep_dich = '' #Tên tệp đích
        super().__init__(tk_goc, 'Xuất ' + tieu_de)
        
    def body(self, frame_chinh):
        '''Thân hộp thoại'''
        self.label_tep_nguon = ttk.Label(frame_chinh, width=25, text='Tệp nguồn')
        self.label_tep_nguon.pack(side='top', fill='x')
        self.frame_tep_nguon = ttk.Frame(frame_chinh)
        self.entry_tep_nguon = ttk.Entry(self.frame_tep_nguon, textvariable='', width=40)
        self.entry_tep_nguon.pack(side='left')
        self.button_tep_nguon = ttk.Button(self.frame_tep_nguon, text='Duyệt...', command=self.Duyet_Tep_Nguon)
        self.button_tep_nguon.pack(side='left')
        self.frame_tep_nguon.pack(side='top', fill='x')
        self.label_tep_dich = ttk.Label(frame_chinh, width=25, text='Tệp đích')
        self.label_tep_dich.pack(side='top', fill='x')
        self.frame_tep_dich = ttk.Frame(frame_chinh)
        self.entry_tep_dich = ttk.Entry(self.frame_tep_dich, textvariable='', width=40)
        self.entry_tep_dich.pack(side='left')
        self.button_tep_dich = ttk.Button(self.frame_tep_dich, text='Duyệt...', command=self.Duyet_Tep_Dich)
        self.button_tep_dich.pack(side='left')
        self.frame_tep_dich.pack(side='top', fill='x')
        return frame_chinh
        
    def buttonbox(self):
        '''Nút bấm hộp thoại'''
        self.frame_box = ttk.Frame(self)
        self.button_xuat = ttk.Button(self.frame_box, text='Xuất', command=self.Button_Xuat)
        self.button_xuat.pack(side='left')
        self.button_huy = ttk.Button(self.frame_box, text='Hủy', command=self.destroy)
        self.button_huy.pack(side='left')
        self.frame_box.pack()
        self.bind('<Escape>', lambda event: self.destroy())
        
    def Duyet_Tep_Nguon(self):
        '''Lấy đường dẫn tệp nguồn'''
        ten_tep = self.tk_goc.Hop_Thoai_Mo_Tep(self.tieu_de)
        if len(ten_tep) > 0:
            self.entry_tep_nguon.delete(0, 'end')
            self.entry_tep_nguon.insert('end', ten_tep)
        
    def Duyet_Tep_Dich(self):
        '''Lấy đường dẫn tệp đích'''
        ten_tep = self.tk_goc.Hop_Thoai_Luu_Tep(self.tieu_de)
        if len(ten_tep) > 0:
            self.entry_tep_dich.delete(0, 'end')
            self.entry_tep_dich.insert('end', ten_tep)
            
    def Button_Xuat(self):
        '''Trả lại kết quả'''
        self.tep_nguon = self.entry_tep_nguon.get()
        self.tep_dich = self.entry_tep_dich.get()
        self.destroy()