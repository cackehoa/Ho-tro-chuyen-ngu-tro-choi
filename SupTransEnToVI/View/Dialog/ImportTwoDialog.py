'''ImportTwoDialog.py
Hộp thoại nhập CSV
'''
from tkinter import ttk, IntVar, filedialog
from tkinter.simpledialog import Dialog

class ImportTwoDialog(Dialog):
    def __init__(self, parent, title, typeFile = (('CSV', '*.csv'), ('Tất cả', '*.*'))):
        #Cấu hình kiểu tệp cần mở
        self.typeFile = typeFile
        self.mTitle = title
        self.override = IntVar()
        self.dataConfig = {
            'engFile' : '',
            'vieFile': '',
            'override' : self.get_override()
            }
        super().__init__(parent, f'Nhập từ tệp {self.mTitle}')

    #Hiển thị phần thân hộp thoại
    def body(self, mainFrame):
        #Lấy tệp tiếng Anh
        ttk.Label(mainFrame, width=25, text='Tệp tiếng Anh:').pack(side='top', fill='x')
        engFileFrame = ttk.Frame(mainFrame)
        self.engFileEntry = ttk.Entry(engFileFrame, width=40)
        self.engFileEntry.pack(side='left')
        ttk.Button(engFileFrame, text='Duyệt...', command=self.button_eng_file).pack(side='left')
        engFileFrame.pack(side='top', fill='x')
        #Lấy tệp tiếng Việt
        ttk.Label(mainFrame, width=25, text='Tệp tiếng Việt:').pack(side='top', fill='x')
        vieFileFrame = ttk.Frame(mainFrame)
        self.vieFileEntry = ttk.Entry(vieFileFrame, width=40)
        self.vieFileEntry.pack(side='left')
        ttk.Button(vieFileFrame, text='Duyệt...', command=self.button_vie_file).pack(side='left')
        vieFileFrame.pack(side='top', fill='x')
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

    #Lấy tình trạng ghi đè hay không?
    def get_override(self):
        override = int(self.override.get())
        return override

    #Hộp thoại mở tệp tiếng Anh
    def button_eng_file(self):
        engFile = filedialog.askopenfilename(title=f'Mở tệp {self.mTitle} tiếng Anh', filetypes=self.get_type_file())
        if len(engFile) > 0:
            self.engFileEntry.delete(0, 'end')
            self.engFileEntry.insert('end', engFile)

    #Hộp thoại mở tệp tiếng Việt
    def button_vie_file(self):
        vieFile = filedialog.askopenfilename(title=f'Mở tệp {self.mTitle} tiếng Việt', filetypes=self.get_type_file())
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

    #Xác nhận nhập
    def button_import(self):
        self.dataConfig['engFile'] = self.get_eng_file()
        self.dataConfig['vieFile'] = self.get_vie_file()
        self.dataConfig['override'] = self.get_override()
        self.destroy()