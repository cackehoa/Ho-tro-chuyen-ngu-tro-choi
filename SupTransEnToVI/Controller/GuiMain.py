'''GuiMain.py
Tạo gui tkinter tùy chỉnh
'''
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from ..View import *
from ..Model.Db import *
 
class GuiMain(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Khởi tạo giao diện chính
        self.title("Hỗ trợ chuyển ngữ")
        self.geometry('450x570')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #Khởi tạo view
        self.status = StringVar()
        self.status.set("Khởi tạo thành công")
        ttk.Label(self, textvariable = self.status, relief='sunken', anchor='w').pack(side='bottom', fill = 'x')
        self.config(menu=MenuBar(self))
        self.search = SearchFrame(self)
        self.treev = TreeViewFrame(self)
        self.manual = ManualDataFrame(self)

    def set_database(self, fileDatabase):
        self.dbSqlite = SqliteDb(fileDatabase)
        data = self.dbSqlite.get_allkeys('', 1)
        self.treev.set_treev(data)
    
    def get_database(self):
        return self.dbSqlite

    def get_treeview(self):
        return self.treev

    def get_manual_data(self):
        return self.manual

    def set_status(self, status):
        #Làm phẵng status
        sentence = ' '.join(status.split())
        self.status.set(sentence[:80])

    #Lọc khoảng trắng thừa
    def filter_whitespace(self, sentence):
        strStrip = sentence.strip()
        sentences = strStrip.split('\n')
        filterWhitespace = []
        for sent in sentences:
            filterWhitespace.append(' '.join(sent.split()))
        result = '\n'.join(filterWhitespace)
        return result

    '''
    Dùng để đóng chương trình một cách an toàn
    Làm những gì cần thực hiện trước khi đóng chương trình
    '''
    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Lưu dữ liệu đã thay đổi không?"):
            self.dbSqlite.save_database()
        self.destroy()