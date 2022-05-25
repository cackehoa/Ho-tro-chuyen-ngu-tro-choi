#HopThoaiNhap.py
#Quản lý nhập tiệp tiếng Anh và tiếng Việt

from tkinter import ttk
from tkinter.simpledialog import Dialog as Hop_thoai

class HopThoaiNhap(Hop_thoai):
    def __init__(self, tk_goc, tieu_de):
        self.tk_goc = tk_goc
        self.tieu_de = tieu_de
        self.du_lieu = {'tep_eng' : '',
            'tep_vie' : '',
            'cot_eng' : 1,
            'cot_khoa_eng' : 0,
            'cot_vie' : 2,
            'cot_khoa_vie' : 0
            }
        super().__init__(tk_goc, 'Nhập ' + tieu_de)
        
    def body(self, frame_chinh):
        '''Thân hộp thoại'''
        #Label
        self.label_tep_eng = ttk.Label(frame_chinh, width=25, text='Tệp tiếng Anh:')
        self.label_tep_eng.pack(side='top', fill='x')
        #Frame
        self.frame_tep_eng = ttk.Frame(frame_chinh)
        self.entry_tep_eng = ttk.Entry(self.frame_tep_eng, width=40)
        self.entry_tep_eng.pack(side='left')
        self.button_tep_eng = ttk.Button(self.frame_tep_eng, text='Duyệt...', command=self.Duyet_Tep_Nguon)
        self.button_tep_eng.pack(side='left')
        self.frame_tep_eng.pack(side='top', fill='x')
        #Cột Csv
        if self.tieu_de == 'Csv':
            self.frame_cot_eng = ttk.Frame(frame_chinh)
            self.label_cot_eng = ttk.Label(self.frame_cot_eng, text='Cột tiếng Anh:')
            self.label_cot_eng.pack(side='left')
            self.entry_cot_eng = ttk.Entry(self.frame_cot_eng, width=5, justify='center')
            self.entry_cot_eng.delete(0, 'end')
            self.entry_cot_eng.insert('end', self.du_lieu['cot_eng'])
            self.entry_cot_eng.pack(side='left')
            self.entry_cot_khoa_eng = ttk.Entry(self.frame_cot_eng, width=5, justify='center')
            self.entry_cot_khoa_eng.delete(0, 'end')
            self.entry_cot_khoa_eng.insert('end', self.du_lieu['cot_khoa_eng'])
            self.entry_cot_khoa_eng.pack(side='right')
            self.label_cot_khoa_eng = ttk.Label(self.frame_cot_eng, text='Cột khóa tiếng Anh:')
            self.label_cot_khoa_eng.pack(side='right')
            self.frame_cot_eng.pack(side='top', fill='x')
        #Label
        self.label_tep_vie = ttk.Label(frame_chinh, width=25, text='Tệp tiếng Việt')
        self.label_tep_vie.pack(side='top', fill='x')
        #Frame
        self.frame_tep_vie = ttk.Frame(frame_chinh)
        self.entry_tep_vie = ttk.Entry(self.frame_tep_vie, width=40)
        self.entry_tep_vie.pack(side='left')
        self.button_tep_vie = ttk.Button(self.frame_tep_vie, text='Duyệt...', command=self.Duyet_Tep_Dich)
        self.button_tep_vie.pack(side='left')
        self.frame_tep_vie.pack(side='top', fill='x')
        #Cột Csv
        if self.tieu_de == 'Csv':
            self.frame_cot_vie = ttk.Frame(frame_chinh)
            self.label_cot_vie = ttk.Label(self.frame_cot_vie, text='Cột tiếng Việt:')
            self.label_cot_vie.pack(side='left')
            self.entry_cot_vie = ttk.Entry(self.frame_cot_vie, width=5, justify='center')
            self.entry_cot_vie.delete(0, 'end')
            self.entry_cot_vie.insert('end', self.du_lieu['cot_vie'])
            self.entry_cot_vie.pack(side='left')
            self.entry_cot_khoa_vie = ttk.Entry(self.frame_cot_vie, width=5, justify='center')
            self.entry_cot_khoa_vie.delete(0, 'end')
            self.entry_cot_khoa_vie.insert('end', self.du_lieu['cot_khoa_vie'])
            self.entry_cot_khoa_vie.pack(side='right')
            self.label_cot_khoa_vie = ttk.Label(self.frame_cot_vie, text='Cột khóa tiếng Việt:')
            self.label_cot_khoa_vie.pack(side='right')
            self.frame_cot_vie.pack(side='top', fill='x')
        return frame_chinh
        
    def buttonbox(self):
        '''Nút bấm hộp thoại'''
        self.frame_box = ttk.Frame(self)
        self.button_nhap = ttk.Button(self.frame_box, text='Nhập', command=self.Button_Nhap)
        self.button_nhap.pack(side='left')
        self.button_huy = ttk.Button(self.frame_box, text='Hủy', command=self.destroy)
        self.button_huy.pack(side='left')
        self.frame_box.pack()
        self.bind('<Escape>', lambda event: self.destroy())
        self.bind('<Return>', lambda event: self.Button_Nhap())
        
    def Duyet_Tep_Nguon(self):
        '''Lấy đường dẫn tệp nguồn'''
        ten_tep = self.tk_goc.Hop_Thoai_Mo_Tep(self.tieu_de)
        if len(ten_tep) > 0:
            self.entry_tep_eng.delete(0, 'end')
            self.entry_tep_eng.insert('end', ten_tep)
        
    def Duyet_Tep_Dich(self):
        '''Lấy đường dẫn tệp đích'''
        ten_tep = self.tk_goc.Hop_Thoai_Mo_Tep(self.tieu_de)
        if len(ten_tep) > 0:
            self.entry_tep_vie.delete(0, 'end')
            self.entry_tep_vie.insert('end', ten_tep)
            
    def Button_Nhap(self):
        '''Trả lại kết quả'''
        self.du_lieu['tep_eng'] = self.entry_tep_eng.get()
        self.du_lieu['tep_vie'] = self.entry_tep_vie.get()
        try:
            self.du_lieu['cot_eng'] = int(eval(str(self.entry_cot_eng.get())))
        except:
            pass
        try:
            self.du_lieu['cot_vie'] = int(eval(str(self.entry_cot_vie.get())))
        except:
            pass
        try:
            self.du_lieu['cot_khoa_eng'] = int(eval(str(self.entry_cot_khoa_eng.get())))
        except:
            pass
        try:
            self.du_lieu['cot_khoa_vie'] = int(eval(str(self.entry_cot_khoa_vie.get())))
        except:
            pass
        self.destroy()