'''TreeViewFrame.py
Hiển thị kết quả tìm kiếm
'''
from tkinter import ttk

class TreeViewFrame(ttk.Treeview):
    def __init__(self, parent):
        col = ('id', 'eng', 'vie')
        super().__init__(parent, columns=col, show='headings')
        self.controller = parent
        self.key = ''
        self.column('id', width=50, anchor='c') #Đặt cột id rộng 50
        self.heading('id', text='ID')
        self.heading('eng', text='Tiếng Anh')
        self.heading('vie', text='Tiếng Việt')
        self.bind('<Double-1>', lambda event:self.db_click_treev())
        self.pack(side = 'top', fill = 'x', padx = 4, pady=4)
        bottomFrame = ttk.Frame(self.controller)
        ttk.Button(bottomFrame, text='<', command = lambda: self.show_treev('<')).pack(side='left')
        self.pageEntry = ttk.Entry(bottomFrame, width=10, justify='center')
        self.pageEntry.pack(side='left')
        self.pageEntry.bind('<Return>', lambda event:self.show_treev())
        self.set_page(1)
        ttk.Button(bottomFrame, text='>', command=lambda: self.show_treev('>')).pack(side='left')
        bottomFrame.pack()

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def show_treev(self, action = 'auto'):
        page = self.get_page()
        if action == '>':
            page = page + 1
        elif action == '<':
            page = page - 1
        self.set_page(page)
        db = self.controller.get_database()
        data = db.get_allkeys(self.get_key(), page)
        self.set_treev(data)
        self.controller.set_status(f"Trang {page} với từ khóa: {self.get_key()}")

    def set_treev(self, data):
        self.delete(*self.get_children())
        for col in data:
            self.insert('', 'end', values=col)

    def db_click_treev(self):
        item = self.focus()
        data = self.item(item, 'values')
        if data:
            id_ = data[0]
            db = self.controller.get_database()
            data = db.get_id(id_)
            if data is None:
                self.controller.set_status("Không có dữ liệu trong database.")
            else:
                manual = self.controller.get_manual_data()
                manual.set_id(id_)
                manual.set_eng(data[1])
                manual.set_vie(data[2])
                self.controller.set_status(f"Câu {id_}: {data[1]}")
                manual.show_button()
        else:
            self.controller.set_status("Không có dữ liệu trên treeview.")

    def set_page(self, page):
        page = int(page)
        if page < 1:
            page = 1
        self.pageEntry.delete(0, 'end')
        self.pageEntry.insert('end', page)

    def get_page(self):
        page = int(self.pageEntry.get())
        return page