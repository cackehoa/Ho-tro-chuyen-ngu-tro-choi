'''GuiMain.py
Tạo gui tkinter tùy chỉnh
'''
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from ..View import *
from ..Model.Db import *
from ..Dynamic import *
from ..Model.Trans.EngToVieTrans import EngToVieTrans
 
class GuiMain(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Khởi tạo giao diện chính
        self.title("Hỗ trợ chuyển ngữ")
        self.geometry('450x600')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #Khởi tạo view
        self.val_dynamic = "Luồng không chạy"
        self.status = StringVar()
        self.set_status("Khởi tạo thành công")
        ttk.Label(self, textvariable = self.status, relief='sunken', anchor='w').pack(side='bottom', fill = 'x')
        self.config(menu=MenuBar(self))
        self.search = SearchFrame(self)
        self.treev = TreeViewFrame(self)
        self.manual = ManualDataFrame(self)
        self.objEvent = None
        self.objDynamic = Dynamic(self)

    def set_database(self, fileDatabase):
        self.dbSqlite = SqliteDb(fileDatabase)
        data = self.dbSqlite.dbRoot.get_allkeys('', 1)
        self.treev.set_treev(data)
        #Đánh dấu lại tất cả chưa được dịch
        #self.dbSqlite.dbCache.set_retrains('')
        self.start_dynamic()
    
    '''Trả về đối tượng database
    (thống nhất cho các loại đối tượng csdl được truyền vào)'''
    def get_database(self):
        return self.dbSqlite

    #Trả về đối tượng treeview
    def get_treeview(self):
        return self.treev

    def get_manual_data(self):
        return self.manual

    #Cập nhật trạng thái
    def set_status(self, status):
        #Làm phẵng status
        sentence = ' '.join(status.split())
        self.val_status = sentence[:80]
        self.status.set(f'{self.val_dynamic}\n{self.val_status}')

    def set_status_dynamic(self, status):
        self.val_dynamic = status
        self.status.set(f'{self.val_dynamic}\n{self.val_status}')

    #Lọc khoảng trắng thừa
    def filter_whitespace(self, sentence):
        strStrip = sentence.strip()
        sentences = strStrip.split('\n')
        filterWhitespace = []
        for sent in sentences:
            filterWhitespace.append(' '.join(sent.split()))
        result = '\n'.join(filterWhitespace)
        return result

    #Lấy đối tượng Dynamic
    def get_dynamic(self):
        return self.objDynamic

    #Bật Dynamic
    def start_dynamic(self, reset = False):
        #return None
        self.objDynamic.start(reset)
        return self.objDynamic

    #Tắt Dynamic
    def stop_dynamic(self):
        #return None
        self.objDynamic.stop()
        return self.objDynamic

    '''-----------------------
    Hàm được viết liên quan đến việc quản lý các event đa nhiệm
    -----------------------'''
    #Xác định đối tượng xử lý event
    def set_obj_event(self, obj):
        self.objEvent = obj

    #Hàm kiểm tra đa nhiệm đã làm việc đến đâu
    def update_event(self):
        #Không có đối tượng cần xử lý
        if self.objEvent == None:
            return
        #Lấy tiến độ
        progress = self.objEvent.get_progress()
        #Lấy tổng tiến độ
        totalProgress = self.objEvent.get_total_progress()
        #Tiến độ các luồng chạy xong
        if progress == totalProgress:
            self.objEvent.end_progress()
            #Đóng thành tiến độ
            return
        #Điều chỉnh thanh tiến độ
        self.after(1000, self.update_event)

    #Gọi hàm lưu lại những thay đổi
    def save_cache_to_database(self):
        self.set_status('Đang lưu dữ liệu bộ đệm xuống csdl...')

    '''Dùng để đóng chương trình một cách an toàn
    Làm những gì cần thực hiện trước khi đóng chương trình
    '''
    def on_closing(self):
        self.objDynamic.stop()
        if messagebox.askokcancel("Thoát", "Lưu dữ liệu đã thay đổi không?"):
            db = self.get_database()
            db.save_database()
            print('Cập nhật csdl thành công')
        print('Chương trình đã kết thúc.')
        self.destroy()