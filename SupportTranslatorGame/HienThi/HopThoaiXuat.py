#HopThoaiXuat.py
#Hộp thoại quản lý nhập tệp tin đích và nguồn

from tkinter import ttk, IntVar
from tkinter.simpledialog import Dialog as Hop_thoai

class HopThoaiXuat(Hop_thoai):
    def __init__(self, tk_goc, tieu_de):
        self.tk_goc = tk_goc
        self.tieu_de = tieu_de
        self.co_dich = IntVar()
        self.du_lieu ={'tep_nguon' : '',
            'tep_dich' : '',
            'co_dich' : 0
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
        #Cột tiếng Anh Csv
        if self.tieu_de == 'Csv':
            frame_cot_eng = ttk.Frame(frame_chinh)
            ttk.Label(frame_cot_eng, text='Cột tiếng Anh:').pack(side='left')
            self.entry_cot_eng = ttk.Entry(frame_cot_eng, width=5, justify='center')
            self.du_lieu['cot_eng'] = 1
            self.entry_cot_eng.delete(0, 'end')
            self.entry_cot_eng.insert('end', self.du_lieu['cot_eng'])
            self.entry_cot_eng.pack(side='left')
            frame_cot_eng.pack(side='top', fill='x')
            frame_dau_phan_cach = ttk.Frame(frame_chinh)
            ttk.Label(frame_dau_phan_cach, text='Dấu phân cách:').pack(side='left')
            self.entry_dau_phan_cach = ttk.Entry(frame_dau_phan_cach, width=5, justify='center')
            self.du_lieu['dau_phan_cach'] = ','
            self.entry_dau_phan_cach.delete(0, 'end')
            self.entry_dau_phan_cach.insert('end', self.du_lieu['dau_phan_cach'])
            self.entry_dau_phan_cach.pack(side='left')
            frame_dau_phan_cach.pack(side='top', fill='x')
        #Tệp đích
        ttk.Label(frame_chinh, width=25, text='Tệp đích').pack(side='top', fill='x')
        frame_tep_dich = ttk.Frame(frame_chinh)
        self.entry_tep_dich = ttk.Entry(frame_tep_dich, textvariable='', width=40)
        self.entry_tep_dich.pack(side='left')
        ttk.Button(frame_tep_dich, text='Duyệt...', command=self.Duyet_Tep_Dich).pack(side='left')
        frame_tep_dich.pack(side='top', fill='x')
        #Cột tiếng Việt Csv
        if self.tieu_de == 'Csv':
            frame_cot_vie = ttk.Frame(frame_chinh)
            ttk.Label(frame_cot_vie, text='Cột tiếng Việt:').pack(side='left')
            self.entry_cot_vie = ttk.Entry(frame_cot_vie, width=5, justify='center')
            self.du_lieu['cot_vie'] = 2
            self.entry_cot_vie.delete(0, 'end')
            self.entry_cot_vie.insert('end', self.du_lieu['cot_vie'])
            self.entry_cot_vie.pack(side='left')
            frame_cot_vie.pack(side='top', fill='x')
        ttk.Checkbutton(frame_chinh, text='Cố dịch', variable=self.co_dich, onvalue=1, offvalue=0).pack(side='top', fill='x')
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
        '''Đọc thông tin được nhập vào du_lieu'''
        self.du_lieu['tep_nguon'] = self.entry_tep_nguon.get()
        self.du_lieu['tep_dich'] = self.entry_tep_dich.get()
        try:
            self.du_lieu['co_dich'] = int(self.co_dich.get())
        except:
            pass
        if self.tieu_de == 'Csv':
            self.du_lieu['dau_phan_cach'] = self.entry_dau_phan_cach.get()
            try:
                self.du_lieu['cot_vie'] = int(self.entry_cot_vie.get())
            except:
                pass
            try:
                self.du_lieu['cot_eng'] = int(self.entry_cot_eng.get())
            except:
                pass
        self.destroy()