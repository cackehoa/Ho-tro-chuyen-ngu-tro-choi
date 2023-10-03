'''WaitToplevel.py
Hộp thoại chờ có đưa ra thông báo cần chờ.
'''
from tkinter import  ttk, Toplevel, IntVar

class WaitToplevel(Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.controller = parent
        self.data = data
        self.count = len(data)
        self.title('Đợi...')
        #ttk.Label(self, width = 25, text = 'Đang xử lý xin chờ...').pack(side = 'top', fill = 'x')
        self.after(1000, self.play_progress)
        self.grab_set()
        self.wait_window()
        
        def check_action(self):
            pass

        def play_progress(self):
            ttk.Label(self, width = 25, text = 'Đang cập nhật bộ đệm...').pack(side = 'top', fill = 'x')
            db = self.controller.get_database()
            EngToVieTrans.save_cache_to_database(db.dbCache)