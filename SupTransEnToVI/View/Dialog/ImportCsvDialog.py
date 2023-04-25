'''ImportCsvDialog.py
Hộp thoại nhập CSV
'''
from tkinter import ttk, IntVar, filedialog
from tkinter.simpledialog import Dialog

class ImportCsvDialog(Dialog):
    def __init__(self, parent):
        #Cấu hình kiểu tệp cần mở
        self.typeFile = (('CSV', '*.csv'), ('Tất cả', '*.*'))
        self.override = IntVar()
        self.dataConfig = {
            'delimiter' : ',',
            'colEng' : 1,
            'colVie' : 2,
            'keyEng' : 0,
            'keyVie' : 0,
            'engFile' : '',
            'vieFile': '',
            'override' : self.get_override()
            }
        super().__init__(parent, 'Nhập từ tệp CSV')

    #Hiển thị phần thân hộp thoại
    def body(self, mainFrame):
        #Lấy tệp tiếng Anh
        ttk.Label(mainFrame, width=25, text='Tệp tiếng Anh:').pack(side='top', fill='x')
        engFileFrame = ttk.Frame(mainFrame)
        self.engFileEntry = ttk.Entry(engFileFrame, width=40)
        self.engFileEntry.pack(side='left')
        ttk.Button(engFileFrame, text='Duyệt...', command=self.button_eng_file).pack(side='left')
        engFileFrame.pack(side='top', fill='x')
        #Lấy cột tiếng Anh
        colEngFrame = ttk.Frame(mainFrame)
        ttk.Label(colEngFrame, text='Cột tiếng Anh:').pack(side='left')
        self.colEngEntry = ttk.Entry(colEngFrame, width=5, justify='center')
        self.colEngEntry.insert('end', self.dataConfig['colEng'])
        self.colEngEntry.pack(side='left')
        #Lấy cột khóa tiếng Anh
        self.keyEngEntry = ttk.Entry(colEngFrame, width=5, justify='center')
        self.keyEngEntry.insert('end', self.dataConfig['keyEng'])
        self.keyEngEntry.pack(side='right')
        ttk.Label(colEngFrame, text='Cột khóa tiếng Anh:').pack(side='right')
        colEngFrame.pack(side='top', fill='x')
        #Lấy dấu phân cách
        delimiterFrame = ttk.Frame(mainFrame)
        ttk.Label(delimiterFrame, text='Dấu phân cách:').pack(side='left')
        self.delimiterEntry = ttk.Entry(delimiterFrame, width=5, justify='center')
        self.delimiterEntry.insert('end', self.dataConfig['delimiter'])
        self.delimiterEntry.pack(side='left')
        delimiterFrame.pack(side='top', fill='x')
        #Lấy tệp tiếng Việt
        ttk.Label(mainFrame, width=25, text='Tệp tiếng Việt: (Bỏ qua, nếu tiếng Anh và Việt cùng tệp)').pack(side='top', fill='x')
        vieFileFrame = ttk.Frame(mainFrame)
        self.vieFileEntry = ttk.Entry(vieFileFrame, width=40)
        self.vieFileEntry.pack(side='left')
        ttk.Button(vieFileFrame, text='Duyệt...', command=self.button_vie_file).pack(side='left')
        vieFileFrame.pack(side='top', fill='x')
        #Lấy cột tiếng Việt
        colVieFrame = ttk.Frame(mainFrame)
        ttk.Label(colVieFrame, text='Cột tiếng Việt:').pack(side='left')
        self.colVieEntry = ttk.Entry(colVieFrame, width=5, justify='center')
        self.colVieEntry.insert('end', self.dataConfig['colVie'])
        self.colVieEntry.pack(side='left')
        #Lấy cột khóa tiếng Việt
        self.keyVieEntry = ttk.Entry(colVieFrame, width=5, justify='center')
        self.keyVieEntry.insert('end', self.dataConfig['keyVie'])
        self.keyVieEntry.pack(side='right')
        ttk.Label(colVieFrame, text='Cột khóa tiếng Việt:').pack(side='right')
        colVieFrame.pack(side='top', fill='x')
        #Kiểm tra ghi đè
        ttk.Checkbutton(mainFrame, text='Ghi đè (Nếu cảm thấy nội dung dịch chính xác hơn)', variable=self.override, onvalue=1, offvalue=0).pack(side='top', fill='x')

    #Đặt kiểu tệp cần lấy
    def get_type_file(self):
        return self.typeFile

    #Lấy tệp tiếng Anh
    def get_eng_file(self):
        engFile = self.engFileEntry.get()
        return engFile

    #Lấy tệp tiếng Việt
    def get_vie_file(self):
        vieFile = self.vieFileEntry.get()
        return vieFile

    #Xác định dấu phân cách các cột trong tệp loại CSV
    def get_delimiter(self):
        delimiter = self.delimiterEntry.get()
        return delimiter

    #Chỉ định cột lấy tiếng Anh
    def get_col_eng(self):
        colEng = int(self.colEngEntry.get())
        return colEng

    #Chỉ định cột lấy tiếng Việt
    def get_col_vie(self):
        colVie = int(self.colVieEntry.get())
        return colVie

    #Chỉ định cột lấy khóa tiếng Anh
    def get_key_eng(self):
        keyEng = int(self.keyEngEntry.get())
        return keyEng

    #Chỉ định cột lấy khóa tiếng Việt
    def get_key_vie(self):
        keyVie = int(self.keyVieEntry.get())
        return keyVie

    #Lấy tình trạng ghi đè hay không?
    def get_override(self):
        override = int(self.override.get())
        return override

    #Hộp thoại mở tệp tiếng Anh
    def button_eng_file(self):
        engFile = filedialog.askopenfilename(title='Mở tệp CSV tiếng Anh', filetypes=self.get_type_file())
        if len(engFile) > 0:
            self.engFileEntry.delete(0, 'end')
            self.engFileEntry.insert('end', engFile)

    #Hộp thoại mở tệp tiếng Việt
    def button_vie_file(self):
        vieFile = filedialog.askopenfilename(title='Mở tệp CSV tiếng Việt', filetypes=self.get_type_file())
        if len(vieFile) > 0:
            self.vieFileEntry.delete(0, 'end')
            self.vieFileEntry.insert('end', vieFile)

    #Hiển thị phần nút bấm hộp thoại
    def buttonbox(self):
        boxFrame = ttk.Frame(self)
        ttk.Button(boxFrame, text='Nhập', command=self.button_import).pack(side='left', padx = 5)
        ttk.Button(boxFrame, text='Hủy', command=self.destroy).pack(side='left', padx = 5)
        boxFrame.pack()
        self.bind('<Escape>', lambda event: self.destroy())
        self.bind('<Return>', lambda event: self.button_import())

    def button_test(self):
        print('Test')

    #Xác nhận nhập
    def button_import(self):
        self.dataConfig['delimiter'] = self.get_delimiter()
        self.dataConfig['engFile'] = self.get_eng_file()
        self.dataConfig['vieFile'] = self.get_vie_file()
        self.dataConfig['colEng'] = self.get_col_eng()
        self.dataConfig['colVie'] = self.get_col_vie()
        self.dataConfig['keyEng'] = self.get_key_eng()
        self.dataConfig['keyVie'] = self.get_key_vie()
        self.dataConfig['override'] = self.get_override()
        self.destroy()