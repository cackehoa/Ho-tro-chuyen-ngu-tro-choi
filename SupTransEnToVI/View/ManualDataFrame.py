'''ManualDataFrame.py
Bộ nhập liệu thủ công
'''
from tkinter import ttk, Text

class ManualDataFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = parent
        self.pack(side = 'top', fill = 'x')
        #inputFrame = ttk.Frame(self).pack(side = 'top')
        ttk.Label(self, text = 'ID:').pack(side = 'top', fill = 'x', padx = 4)
        self.idText = Text(self, height = 1, width = 40, bg='light green')
        self.idText.insert('end', '0')
        self.idText.configure(state='disabled')
        self.idText.pack(side = 'top', fill = 'x', padx = 4, pady=4)
        ttk.Label(self, text = 'Tiếng Anh:').pack(side = 'top', fill = 'x', padx = 4)
        self.engText = Text(self, height = 4, width = 40)
        self.engText.pack(side = 'top', fill = 'x', padx = 4, pady=4)
        ttk.Label(self, text = 'Tiếng Việt:').pack(side = 'top', fill = 'x', padx = 4)
        self.vieText = Text(self, height = 4, width = 40)
        self.vieText.pack(side = 'top', fill = 'x', padx = 4, pady=4)
        buttonFrame = ttk.Frame(self).pack(side = 'top')
        ttk.Button(buttonFrame, text='Tạo mới', command=self.button_new).pack(side = 'left', padx = 4)
        self.updateButton = ttk.Button(buttonFrame, text='Cập nhật', command=self.button_update)
        self.updateButton.pack(side = 'left', padx = 4)
        self.refreshButton = ttk.Button(buttonFrame, text='Làm mới', command=self.button_refresh)
        self.refreshButton.pack(side = 'left', padx = 4)
        self.deleteButton = ttk.Button(buttonFrame, text='Xóa', command=self.button_delete)
        self.deleteButton.pack(side = 'left', padx = 4)
        self.hide_button()

    #Lấy id
    def get_id(self):
        id_ = int(self.idText.get('1.0', 'end'))
        return id_
    
    #Cập nhật id
    def set_id(self, id_):
        self.idText.configure(state='normal')
        self.idText.delete('1.0', 'end')
        self.idText.insert('end', id_)
        self.idText.configure(state='disabled')

    #Lấy nhật tiếng Anh
    def get_eng(self):
        eng = self.engText.get('1.0', 'end')
        eng = self.controller.filter_whitespace(eng)
        return eng

    #Cập nhật tiếng Anh
    def set_eng(self, eng):
        self.engText.delete('1.0', 'end')
        self.engText.insert('end' , eng)

    #Lấy tiếng Việt
    def get_vie(self):
        vie = self.vieText.get('1.0', 'end')
        vie = self.controller.filter_whitespace(vie)
        return vie

    #Cập nhật tiếng Việt
    def set_vie(self, vie):
        self.vieText.delete('1.0', 'end')
        self.vieText.insert('end' , vie)

    #Hiển thị nút bấm
    def show_button(self):
        self.updateButton.configure(state='normal')
        self.refreshButton.configure(state='normal')
        self.deleteButton.configure(state='normal')

    #Hiển thị nút bấm
    def hide_button(self):
        self.updateButton.configure(state='disabled')
        self.refreshButton.configure(state='disabled')
        self.deleteButton.configure(state='disabled')

    #Nhập mới dữ liệu
    def button_new(self):
        eng = self.get_eng()
        if len(eng) < 2:
            self.controller.set_status(f"Câu quá ngắn: {eng}")
            return
        vie = self.get_vie()
        if eng == vie or len(vie) < 1:
            self.controller.set_status(f"Hình như chưa dịch: {eng}")
            return
        db = self.controller.get_database()
        row = db.get_eng(eng)
        #Tạo mới
        if row is None:
            id_ = db.new_row(eng, vie)
            #Cập nhật lại thay đổi
            self.set_id(id_)
            treev = self.controller.get_treeview()
            treev.set_key(eng)
            treev.set_page(1)
            treev.show_treev()
            self.set_eng(eng)
            self.set_vie(vie)
            self.controller.set_status(f"Câu {id_} mới: {eng}")
            self.show_button()
            return
        #Hiển thị dữ liệu đã có
        self.set_id(row[0])
        self.set_eng(row[1])
        self.set_vie(row[2])
        self.controller.set_status(f"Câu đã tồn tại: {eng}")
        self.show_button()

    #Cập nhật mới dữ liệu
    def button_update(self):
        id_ = self.get_id()
        #Tạo mới
        if id_ == 0:
            self.button_new()
            return
        eng = self.get_eng()
        if len(eng) < 2:
            self.controller.set_status(f"Câu quá ngắn: {eng}")
            return
        vie = self.get_vie()
        if eng == vie or len(vie) < 1:
            self.controller.set_status(f"Hình như chưa dịch: {eng}")
            return
        db = self.controller.get_database()
        row = db.get_eng(eng)
        if row is not None:
            if id_ != int(row[0]):
                self.controller.set_status(f"Câu đã tồn tại: {eng}")
                return
        db.update_row(id_, eng, vie)
        treev = self.controller.get_treeview()
        treev.set_key(eng)
        treev.set_page(1)
        treev.show_treev()
        self.set_eng(eng)
        self.set_vie(vie)
        self.controller.set_status(f"Cập nhật {id_}: {eng}")

    #Xóa dữ liệu
    def button_delete(self):
        id_ = self.get_id()
        eng = self.get_eng()
        db = self.controller.get_database()
        db.delete_row(id_)
        self.set_id(0)
        treev = self.controller.get_treeview()
        treev.show_treev()
        self.controller.set_status(f"Xóa {id_}: {eng}")
        self.hide_button()

    #Trả về giá trị trước đó
    def button_refresh(self):
        id_ = self.get_id()
        db = self.controller.get_database()
        row = db.get_id(id_)
        if row is None:
            self.set_id(0)
            self.controller.set_status(f"Có lỗi không xác định với: {id_}")
            self.hide_button()
            return
        self.set_eng(row[1])
        self.set_vie(row[2])
        self.controller.set_status(f"Làm mới giá trị: {id_}")
        