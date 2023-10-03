'''ExportTwoDialog.py
Hộp thoại xuất CSV
'''
from tkinter import ttk, IntVar, filedialog
from tkinter.simpledialog import Dialog

class ExportTwoDialog(Dialog):
    def __init__(self, parent, title, typeFile = (('TXT', '*.txt'), ('Tất cả', '*.*')), escChar = '<>'):
        #Cấu hình kiểu tệp cần mở
        self.typeFile = typeFile
        self.mTitle = title
        self.tryTrans = IntVar()
        self.escChar = escChar #string
        self.dataConfig = {
            'sourceFile' : '',
            'destinationFile': '',
            'tryTrans' : self.get_try_trans(),
            'escChar' : [] #list
            }
        super().__init__(parent, f'Xuất tệp {self.mTitle}')

    #Hiển thị phần thân hộp thoại
    def body(self, mainFrame):
        #Lấy tiệp nguồn tiếng Anh
        ttk.Label(mainFrame, width=25, text='Tệp nguồn (tiếng Anh):').pack(side='top', fill='x')
        exportFileFrame = ttk.Frame(mainFrame)
        self.sourceFileEntry = ttk.Entry(exportFileFrame, textvariable='', width=40)
        self.sourceFileEntry.pack(side='left')
        ttk.Button(exportFileFrame, text='Duyệt...', command=self.button_source_file).pack(side='left')
        exportFileFrame.pack(side='top', fill='x')
        #Lấy tệp đích xuất tiếng Việt
        ttk.Label(mainFrame, width=25, text='Tệp đích (tiếng Việt):').pack(side='top', fill='x')
        destinationVieFrame = ttk.Frame(mainFrame)
        self.destinationFileEntry = ttk.Entry(destinationVieFrame, textvariable='', width=40)
        self.destinationFileEntry.pack(side='left')
        ttk.Button(destinationVieFrame, text='Duyệt...', command=self.button_destination_file).pack(side='left')
        destinationVieFrame.pack(side='top', fill='x')
        #Kiểm tra cố dịch (mặc định là không)
        ttk.Checkbutton(mainFrame, text='Cố dịch (Dịch một phần nếu có thể)', variable=self.tryTrans, onvalue=1, offvalue=0).pack(side='top', fill='x')
        #Danh sách cặp ký tự bỏ qua không dịch bên trong
        ttk.Label(mainFrame, width=25, text='Danh sách cặp ký tự bỏ qua không dịch bên trong:\nPhân tách với nhau bằng dấu phẩy \',\'').pack(side='top', fill='x')
        self.escCharEntry = ttk.Entry(mainFrame, textvariable='', width=40)
        self.escCharEntry.pack(side='top', fill='x')
        self.escCharEntry.delete(0, 'end')
        #self.escCharEntry.insert('end', '<>')
        #self.dataConfig
        self.escCharEntry.insert('end', self.escChar)

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

    #Trả về tình trạng cố dịch hay không?
    def get_try_trans(self):
        value = int(self.tryTrans.get())
        return value

    #Trả về danh sách cặp ký tự bỏ qua không dịch bên trong
    def get_esc_char_list(self):
        value = self.escCharEntry.get()
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
        sourceFile = filedialog.askopenfilename(title=f'Mở tệp {self.mTitle} nguồn', filetypes=self.get_type_file())
        if len(sourceFile) > 0:
            self.sourceFileEntry.delete(0, 'end')
            self.sourceFileEntry.insert('end', sourceFile)

    #Hộp thoại lưu tệp
    def button_destination_file(self):
        destinationFile = filedialog.asksaveasfilename(title=f'Lưu tệp {self.mTitle} đích', filetypes=self.get_type_file())
        if len(destinationFile) > 0:
            self.destinationFileEntry.delete(0, 'end')
            self.destinationFileEntry.insert('end', destinationFile)

    #Xác nhận xuất
    def button_export(self):
        self.dataConfig['sourceFile'] = self.get_source_file()
        self.dataConfig['destinationFile'] = self.get_destination_file()
        self.dataConfig['tryTrans'] = self.get_try_trans()
        self.dataConfig['escChar'] = self.get_esc_char_list()
        self.destroy()