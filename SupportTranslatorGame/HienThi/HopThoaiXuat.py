#HopThoaiXuat.py
#Hộp thoại quản lý nhập tệp tin đích và nguồn

from tkinter import ttk
from tkinter.simpledialog import Dialog as Hop_thoai

class HopThoaiXuat(Hop_thoai):
    def __init__(self, tk_goc, tieu_de):
        self.tk_goc = tk_goc
        self.tieu_de = tieu_de
        self.du_lieu ={'tep_nguon' : '',
            'tep_dich' : ''
            }
        super().__init__(tk_goc, 'Xuất ' + tieu_de)
        
    def body(self, frame_chinh):
        '''Thân hộp thoại'''
        #Tệp nguồn
        ttk.Label(frame_chinh, width=25, text='Tệp nguồn').pack(side='top', fill='x')
        frame_tep_nguon = ttk.Frame(frame_chinh)
        self.entry_tep_nguon = ttk.Entry(frame_tep_nguon, textvariable='', width=40)
        self.entry_tep_nguon.pack(side='left')
        ttk.Button(frame_tep_nguon, text='Duyệt...', command=self.Duyet_Tep_Nguon).pack(side='left')
        frame_tep_nguon.pack(side='top', fill='x')
        #Tệp đích
        ttk.Label(frame_chinh, width=25, text='Tệp đích').pack(side='top', fill='x')
        frame_tep_dich = ttk.Frame(frame_chinh)
        self.entry_tep_dich = ttk.Entry(frame_tep_dich, textvariable='', width=40)
        self.entry_tep_dich.pack(side='left')
        ttk.Button(frame_tep_dich, text='Duyệt...', command=self.Duyet_Tep_Dich).pack(side='left')
        frame_tep_dich.pack(side='top', fill='x')
        return frame_chinh
        
    def buttonbox(self):
        '''Nút bấm hộp thoại'''
        frame_box = ttk.Frame(self)
        ttk.Button(frame_box, text='Xuất', command=self.Button_Xuat).pack(side='left')
        ttk.Button(frame_box, text='Hủy', command=self.destroy).pack(side='left')
        frame_box.pack()
        self.bind('<Escape>', lambda event: self.destroy())
        self.bind('<Return>', lambda event: self.Button_Xuat())
        
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
        self.du_lieu['tep_nguon'] = self.entry_tep_nguon.get()
        self.du_lieu['tep_dich'] = self.entry_tep_dich.get()
        self.destroy()