'''ExportCsvDialog.py
Hộp thoại xuất CSV
'''
from tkinter import ttk, IntVar, filedialog
from tkinter.simpledialog import Dialog

class ExportCsvDialog(Dialog):
    def __init__(self, parent):
        #Cấu hình kiểu tệp cần mở
        self.typeFile = (('CSV', '*.csv'), ('Tất cả', '*.*'))
        self.tryTrans = IntVar()
        self.dataConfig = {
            'delimiter' : ',',
            'colEng' : 1,
            'colVie' : 2,
            'sourceFile' : '',
            'destinationFile': '',
            'tryTrans' : self.get_try_trans()
            }
        super().__init__(parent, 'Xuất tệp CSV')

    #Hiển thị phần thân hộp thoại
    def body(self, mainFrame):
        ttk.Label(mainFrame, width=25, text='Tệp nguồn (tiếng Anh):').pack(side='top', fill='x')
        #Lấy tiệp nguồn tiếng Anh
        exportFileFrame = ttk.Frame(mainFrame)
        self.sourceFileEntry = ttk.Entry(exportFileFrame, textvariable='', width=40)
        self.sourceFileEntry.pack(side='left')
        ttk.Button(exportFileFrame, text='Duyệt...', command=self.button_source_file).pack(side='left')
        exportFileFrame.pack(side='top', fill='x')
        #Lấy cột tiếng Anh
        colEngFarme = ttk.Frame(mainFrame)
        ttk.Label(colEngFarme, text='Cột tiếng Anh:').pack(side='left')
        self.colEngEntry = ttk.Entry(colEngFarme, width=5, justify='center')
        self.colEngEntry.pack(side='left')
        self.colEngEntry.insert('end', self.dataConfig['colEng'])
        colEngFarme.pack(side='top', fill='x')
        #Lấy dấu phân cách
        delimiterEngFrame = ttk.Frame(mainFrame)
        ttk.Label(delimiterEngFrame, text='Dấu phân cách:').pack(side='left')
        self.delimiterEntry = ttk.Entry(delimiterEngFrame, width=5, justify='center')
        self.delimiterEntry.insert('end', self.dataConfig['delimiter'])
        self.delimiterEntry.pack(side='left')
        delimiterEngFrame.pack(side='top', fill='x')
        #Lấy tệp đích xuất tiếng Việt
        ttk.Label(mainFrame, width=25, text='Tệp đích (tiếng Việt):').pack(side='top', fill='x')
        destinationVieFrame = ttk.Frame(mainFrame)
        self.destinationFileEntry = ttk.Entry(destinationVieFrame, textvariable='', width=40)
        self.destinationFileEntry.pack(side='left')
        ttk.Button(destinationVieFrame, text='Duyệt...', command=self.button_destination_file).pack(side='left')
        destinationVieFrame.pack(side='top', fill='x')
        #Lấy cột xuất tiếng Việt
        colVieFrame = ttk.Frame(mainFrame)
        ttk.Label(colVieFrame, text='Cột tiếng Việt:').pack(side='left')
        self.colVieEntry = ttk.Entry(colVieFrame, width=5, justify='center')
        self.colVieEntry.insert('end', self.dataConfig['colVie'])
        self.colVieEntry.pack(side='left')
        colVieFrame.pack(side='top', fill='x')
        ttk.Checkbutton(mainFrame, text='Cố dịch (Dịch một phần nếu có thể)', variable=self.tryTrans, onvalue=1, offvalue=0).pack(side='top', fill='x')

    #Đặt kiểu tệp cần lấy
    def get_type_file(self):
        return self.typeFile
        
    #Lấy tiệp nguồn (tệp tiếng Anh)
    def get_source_file(self):
        sourceFile = self.sourceFileEntry.get()
        return sourceFile.strip()

    #Xuất ra tệp đích (tệp tiếng Việt)
    def get_destination_file(self):
        destinationFile = self.destinationFileEntry.get()
        return destinationFile.strip()

    #Chỉ định cột lấy tiếng Anh
    def get_col_eng(self):
        colEng = int(self.colEngEntry.get())
        return colEng

    #Chỉ định cột xuất tiếng Việt
    def get_col_vie(self):
        colVie = int(self.colVieEntry.get())
        return colVie

    #Xác định dấu phân cách các cột trong tệp loại CSV
    def get_delimiter(self):
        delimiter = self.delimiterEntry.get()
        return delimiter

    #Trả về tình trạng cố dịch hay không?
    def get_try_trans(self):
        value = int(self.tryTrans.get())
        return value

    #Hiển thị phần nút bấm hộp thoại
    def buttonbox(self):
        boxFrame = ttk.Frame(self)
        ttk.Button(boxFrame, text='Xuất', command=self.button_export).pack(side='left', padx = 5)
        ttk.Button(boxFrame, text='Hủy', command=self.destroy).pack(side='left', padx = 5)
        boxFrame.pack()
        self.bind('<Escape>', lambda event: self.destroy())
        self.bind('<Return>', lambda event: self.button_export())
        
    #Hộp thoại mở tệp
    def button_source_file(self):
        sourceFile = filedialog.askopenfilename(title='Mở tệp CSV nguồn', filetypes=self.get_type_file())
        if len(sourceFile) > 0:
            self.sourceFileEntry.delete(0, 'end')
            self.sourceFileEntry.insert('end', sourceFile)

    #Hộp thoại lưu tệp
    def button_destination_file(self):
        destinationFile = filedialog.asksaveasfilename(title='Lưu tệp CSV đích', filetypes=self.get_type_file())
        if len(destinationFile) > 0:
            self.destinationFileEntry.delete(0, 'end')
            self.destinationFileEntry.insert('end', destinationFile)

    #Xác nhận xuất
    def button_export(self):
        self.dataConfig['delimiter'] = self.get_delimiter()
        self.dataConfig['colEng'] = self.get_col_eng()
        self.dataConfig['colVie'] = self.get_col_vie()
        self.dataConfig['sourceFile'] = self.get_source_file()
        self.dataConfig['destinationFile'] = self.get_destination_file()
        self.dataConfig['tryTrans'] = self.get_try_trans()
        self.destroy()