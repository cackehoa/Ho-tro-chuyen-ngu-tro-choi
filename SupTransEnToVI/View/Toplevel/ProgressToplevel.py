'''
ProgressToplevel.py
Hộp thoại thanh tiến trình
'''
from datetime import datetime
from tkinter import  ttk, Toplevel, StringVar

class ProgressToplevel(Toplevel):
    def __init__(self, parent, trans, destination, sourceFile):
        super().__init__(parent)
        self.controller = parent
        self.trans = trans #TypeTrans
        self.destination = destination #TypeFile
        self.txtStatus = StringVar()
        #self.txtTime = StringVar()
        #self.txtTime.set('00:00:00')
        self.time_start = datetime.now()
        if sourceFile == '':
            self.destination = None
            self.title('Cập nhật dữ liệu')
            ttk.Label(self, width = 25, text = 'Tệp nguồn: Cơ sở dữ liệu').pack(side = 'top', fill = 'x')
            ttk.Label(self, width = 25, text = 'Tệp đích: Cơ sở dữ liệu').pack(side = 'top', fill = 'x')
        else:
            self.title('Đang dịch')
            ttk.Label(self, width = 25, text = f'Tệp nguồn: {sourceFile}').pack(side = 'top', fill = 'x')
            ttk.Label(self, width = 25, text = f'Tệp đích: {self.destination.get_file_name()}').pack(side = 'top', fill = 'x')
        #ttk.Label(self, width = 25, textvariable = self.txtTime).pack(side = 'top', fill = 'x')
        ttk.Label(self, width = 25, text = 'Cửa sổ sẽ tự đóng khi xong').pack(side = 'top', fill = 'x')
        ttk.Label(self, width = 25, textvariable = self.txtStatus).pack(side = 'top', fill = 'x')
        self.progressBar = ttk.Progressbar(self, orient = 'horizontal', mode = 'determinate', length=500)
        self.progressBar['maximum'] = self.trans.get_count_data()
        self.progressBar.pack(side = 'top', fill = 'x')
        self.after(1000, self.play_progress)
        self.grab_set()
        self.wait_window()

    def play_progress(self):
        if self.progressBar['value'] < self.progressBar['maximum']:
            self.progressBar['value'] = self.trans.get_count_trans()
            self.txtStatus.set(f"({datetime.now() - self.time_start})\t{self.progressBar['value']} / {self.progressBar['maximum']}")
            #self.txtTime.set(datetime.now() - self.time_start)
            self.after(1000, self.play_progress)
            return
        ttk.Label(self, width = 25, text = 'Đang gộp dữ liệu...').pack(side = 'top', fill = 'x')
        result = self.trans.join_data()
        mesage = 'Lưu thành công: Cơ sở dữ liệu'
        if self.destination is not None:
            ttk.Label(self, width = 25, text = f'Đang lưu xuống tệp: {self.destination.get_file_name()}').pack(side = 'top', fill = 'x')
            self.destination.write_data(result)
            mesage = f'Lưu thành công: {self.destination.get_file_name()}'
        self.controller.set_status(mesage)
        ttk.Label(self, width = 25, text = mesage).pack(side = 'top', fill = 'x')
        self.controller.start_dynamic()
        #ttk.Button(self, text = 'Đóng', command = self.destroy).pack(side='top', padx = 5)
        self.destroy()