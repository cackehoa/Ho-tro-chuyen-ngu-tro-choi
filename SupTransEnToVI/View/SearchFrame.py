'''SearchFrame.py
Hiển thị bộ tìm kiếm
'''
from tkinter import ttk

class SearchFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = parent
        self.pack(side = 'top')
        ttk.Label(self, text='Từ khóa:').pack(side='left')
        self.searchEntry = ttk.Entry(self, width=40)
        self.searchEntry.pack(side='left')
        self.searchEntry.bind('<Return>', lambda event: self.show_list())
        ttk.Button(self, text='Lọc', command = lambda: self.show_list()).pack(side='left')
    
    def show_list(self):
        txt = self.get_key()
        treev = self.controller.get_treeview()
        treev.set_key(txt)
        treev.set_page(1)
        treev.show_treev()
        
    def  set_key(self, value):
         self.searchEntry.delete(0, 'end')
         self.searchEntry.insert('end', value)
         
    def  get_key(self):
         return self.searchEntry.get()