#HopThoaiNhap.py
#Quản lý nhập tiệp tiếng Anh và tiếng Việt

from tkinter import ttk, IntVar
from tkinter.simpledialog import Dialog as Hop_thoai

class HopThoaiNhap(Hop_thoai):
    def __init__(self, tk_goc, tieu_de):
        self.tk_goc = tk_goc
        self.tieu_de = tieu_de
        self.ghi_de = IntVar()
        self.du_lieu = {'tep_eng' : '',
            'tep_vie' : '',
            'ghi_de' : 0,
            'cot_eng' : 1,
            'cot_khoa_eng' : 0,
            'cot_vie' : 2,
            'cot_khoa_vie' : 0
            }
        super().__init__(tk_goc, 'Nhập ' + tieu_de)
        
    def body(self, frame_chinh):
        '''Thân hộp thoại'''
        #Nhập tệp tiếng Anh
        ttk.Label(frame_chinh, width=25, text='Tệp tiếng Anh:').pack(side='top', fill='x')
        frame_tep_eng = ttk.Frame(frame_chinh)
        self.entry_tep_eng = ttk.Entry(frame_tep_eng, width=40)
        self.entry_tep_eng.pack(side='left')
        ttk.Button(frame_tep_eng, text='Duyệt...', command=self.Duyet_Tep_Eng).pack(side='left')
        frame_tep_eng.pack(side='top', fill='x')
        #Cột tiếng Anh Csv
        if self.tieu_de == 'Csv':
            frame_cot_eng = ttk.Frame(frame_chinh)
            ttk.Label(frame_cot_eng, text='Cột tiếng Anh:').pack(side='left')
            self.entry_cot_eng = ttk.Entry(frame_cot_eng, width=5, justify='center')
            self.entry_cot_eng.delete(0, 'end')
            self.entry_cot_eng.insert('end', self.du_lieu['cot_eng'])
            self.entry_cot_eng.pack(side='left')
            self.entry_cot_khoa_eng = ttk.Entry(frame_cot_eng, width=5, justify='center')
            self.entry_cot_khoa_eng.delete(0, 'end')
            self.entry_cot_khoa_eng.insert('end', self.du_lieu['cot_khoa_eng'])
            self.entry_cot_khoa_eng.pack(side='right')
            ttk.Label(frame_cot_eng, text='Cột khóa tiếng Anh:').pack(side='right')
            frame_cot_eng.pack(side='top', fill='x')
        #Nhập tệp tiếng Việt
        ttk.Label(frame_chinh, width=25, text='Tệp tiếng Việt').pack(side='top', fill='x')
        frame_tep_vie = ttk.Frame(frame_chinh)
        self.entry_tep_vie = ttk.Entry(frame_tep_vie, width=40)
        self.entry_tep_vie.pack(side='left')
        ttk.Button(frame_tep_vie, text='Duyệt...', command=self.Duyet_Tep_Vie).pack(side='left')
        #self.button_tep_vie.pack(side='left')
        frame_tep_vie.pack(side='top', fill='x')
        #Cột tiếng Việt Csv
        if self.tieu_de == 'Csv':
            frame_cot_vie = ttk.Frame(frame_chinh)
            ttk.Label(frame_cot_vie, text='Cột tiếng Việt:').pack(side='left')
            self.entry_cot_vie = ttk.Entry(frame_cot_vie, width=5, justify='center')
            self.entry_cot_vie.delete(0, 'end')
            self.entry_cot_vie.insert('end', self.du_lieu['cot_vie'])
            self.entry_cot_vie.pack(side='left')
            self.entry_cot_khoa_vie = ttk.Entry(frame_cot_vie, width=5, justify='center')
            self.entry_cot_khoa_vie.delete(0, 'end')
            self.entry_cot_khoa_vie.insert('end', self.du_lieu['cot_khoa_vie'])
            self.entry_cot_khoa_vie.pack(side='right')
            ttk.Label(frame_cot_vie, text='Cột khóa tiếng Việt:').pack(side='right')
            frame_cot_vie.pack(side='top', fill='x')
        #Kiểm tra ghi đè
        ttk.Checkbutton(frame_chinh, text='Ghi đè', variable=self.ghi_de, onvalue=1, offvalue=0).pack(side='top', fill='x')
        return frame_chinh
        
    def buttonbox(self):
        '''Nút bấm hộp thoại'''
        frame_box = ttk.Frame(self)
        ttk.Button(frame_box, text='Nhập', command=self.Button_Nhap).pack(side='left')
        ttk.Button(frame_box, text='Hủy', command=self.destroy).pack(side='left')
        frame_box.pack()
        self.bind('<Escape>', lambda event: self.destroy())
        self.bind('<Return>', lambda event: self.Button_Nhap())
        
    def Duyet_Tep_Eng(self):
        '''Lấy đường dẫn tệp tiếng Anh'''
        ten_tep = self.tk_goc.Hop_Thoai_Mo_Tep(self.tieu_de)
        if len(ten_tep) > 0:
            self.entry_tep_eng.delete(0, 'end')
            self.entry_tep_eng.insert('end', ten_tep)
        
    def Duyet_Tep_Vie(self):
        '''Lấy đường dẫn tệp tiếng Việt'''
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
        self.du_lieu['ghi_de'] = self.ghi_de.get()
        self.destroy()