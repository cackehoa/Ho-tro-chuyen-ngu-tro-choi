'''MenuBar.py
Đùng để quản lý thanh menu tùy chỉnh
'''
from tkinter import Menu
from .Dialog import *
from ..Model.File import *
from ..Model.TransEngToVie import TransEngToVie
from tkinter import messagebox

class MenuBar(Menu):
    def __init__(self, parent):
        super().__init__(parent,  tearoff=False)
        self.controller = parent
        #Menu hành động
        actionMenu = Menu(self, tearoff=0)
        actionMenu.add_command(label="Trang trước", command = lambda:self.controller.treev.show_treev('<'))
        actionMenu.add_command(label="Trang sau", command = lambda:self.controller.treev.show_treev('>'))
        actionMenu.add_separator()
        actionMenu.add_command(label="Lưu dữ liệu", command = self.save_data)
        actionMenu.add_separator()
        actionMenu.add_command(label="Thoát", command= lambda:self.controller.on_closing())
        self.add_cascade(label="Hành động", menu=actionMenu)
        #Menu nhập tay
        manualMenu = Menu(self, tearoff=0)
        manualMenu.add_command(label="Tạo mới", command = lambda:self.controller.manual.button_new())
        manualMenu.add_command(label="Cập nhật", command = lambda:self.controller.manual.button_update())
        manualMenu.add_command(label="Làm mới", command = lambda:self.controller.manual.button_refresh())
        manualMenu.add_command(label="Xóa", command = lambda:self.controller.manual.button_delete())
        self.add_cascade(label="Nhập tay", menu=manualMenu)
        #Menu xuất
        exportMenu = Menu(self, tearoff=0)
        exportMenu.add_command(label="CSV", command = self.export_csv)
        #exportMenu.add_command(label="INI", command = self.export_ini)
        #exportMenu.add_command(label="JSON", command = self.export_json)
        exportMenu.add_command(label="LUA", command = self.export_lua)
        #exportMenu.add_command(label="XUnity", command = self.export_xunity)
        self.add_cascade(label="Xuất", menu=exportMenu)
        #Menu nhập
        importMenu = Menu(self, tearoff=0)
        #importMenu.add_command(label="CSV", command = self.import_csv)
        #importMenu.add_command(label="INI", command = self.import_ini)
        #importMenu.add_command(label="JSON", command = self.import_json)
        #importMenu.add_command(label="LUA", command = self.import_lua)
        #importMenu.add_command(label="XUnity", command = self.import_xunity)
        self.add_cascade(label="Nhập", menu=importMenu)
        coverMenu = Menu(self, tearoff=0)
        coverMenu.add_command(label="XML thành PZ", command = self.cover_xml)
        self.add_cascade(label="Dành riêng", menu=coverMenu)

    def save_data(self):
        db = self.controller.get_database()
        db.save_database()
        self.controller.set_status("Lưu dữ liệu thành công")

    #Xuất tệp loại CSV
    def export_csv(self):
        self.controller.set_status('Xuất CSV...')
        exportCsv = ExportCsvDialog(self.controller)
        sourceFile = exportCsv.dataConfig['sourceFile']
        sourceCSV = CsvFile(sourceFile)
        sourceCSV.set_delimiter(exportCsv.dataConfig['delimiter'])
        if not sourceCSV.isFile():
            self.controller.set_status('Tệp tin không tồn tại')
            return
        data  = sourceCSV.read_all()
        #Dịch
        trans = TransEngToVie(self.controller)
        colVie = exportCsv.dataConfig['colVie']
        colEng = exportCsv.dataConfig['colEng']
        result = []
        if colVie < 0 or colEng < 0:
            colVie = -1
            result = data
        else:
            result = trans.trans_csv(data[1:], colEng, colVie, exportCsv.dataConfig['tryTrans'])
            result.insert(0, (data[0], None))
        destinationFile = exportCsv.dataConfig['destinationFile']
        if len(destinationFile) > 0:
            destinationCSV = CsvFile(destinationFile)
            destinationCSV.set_delimiter(exportCsv.dataConfig['delimiter'])
            destinationCSV.write_data(result, colVie)
            mesage = f'Lưu thành công: {destinationFile}'
        else:
            sourceCSV.write_data(result, colVie)
            mesage = f'Lưu đè thành công: {sourceFile}'
        self.controller.set_status(mesage)
        messagebox.showinfo("Xuất CSV", mesage)

    def export_ini(self):
        typeFile = ('INI', '*.ini'), ('Tất cả', '*.*')
        exportIni = ExportTwoDialog(self.controller, 'INI', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(exportIni.dataConfig)

    def export_json(self):
        self.controller.set_status('Xuất JSON...')
        typeFile = ('JSON', '*.json'), ('Tất cả', '*.*')
        exportJson = ExportTwoDialog(self.controller, 'JSON', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(exportJson.dataConfig)

    def export_lua(self):
        self.controller.set_status('Xuất LUA...')
        typeFile = ('LUA', '*.lua'), ('Tất cả', '*.*')
        exportLua = ExportTwoDialog(self.controller, 'LUA', typeFile)
        sourceFile = exportLua.dataConfig['sourceFile']
        sourceLua = LuaFile(sourceFile)
        if not sourceLua.isFile():
            self.controller.set_status('Tệp tin không tồn tại')
            return
        data = sourceLua.read_all()
        #Dịch
        trans = TransEngToVie(self.controller)
        result = trans.trans_lua(data, exportLua.dataConfig['tryTrans'])
        destinationFile = exportLua.dataConfig['destinationFile']
        if len(destinationFile) > 0:
            destinationLua = LuaFile(destinationFile)
            destinationLua.write_data(result)
            mesage = f'Lưu thành công: {destinationFile}'
        else:
            sourceLua.write_data(result)
            mesage = f'Lưu đè thành công: {sourceFile}'
        self.controller.set_status(mesage)
        messagebox.showinfo("Xuất lua", mesage)

    def export_xunity(self):
        typeFile = ('TXT', '*.txt'), ('Tất cả', '*.*')
        exportXUnity = ExportTwoDialog(self.controller, 'XUnity', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(exportXUnity.dataConfig)

    def import_csv(self):
        importCsv = ImportCsvDialog(self.controller)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(importCsv.dataConfig)

    def import_ini(self):
        typeFile = ('INI', '*.ini'), ('Tất cả', '*.*')
        importIni = ImportTwoDialog(self.controller, 'INI', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(importIni.dataConfig)

    def import_json(self):
        typeFile = ('JSON', '*.json'), ('Tất cả', '*.*')
        importJson = ImportTwoDialog(self.controller, 'JSON', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(importJson.dataConfig)

    def import_lua(self):
        typeFile = ('LUA', '*.lua'), ('Tất cả', '*.*')
        importLua = ImportTwoDialog(self.controller, 'LUA', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(importLua.dataConfig)

    def import_xunity(self):
        importXunity = ImportOneDialog(self.controller, 'XUnity')
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(importXunity.dataConfig)

    def cover_xml(self):
        self.controller.set_status('Chuyển đổi XML thành LUA...')
        typeFile = ('XML', '*.xml'), ('Tất cả', '*.*')
        covertLua = ExportTwoDialog(self.controller, 'XML', typeFile)
        sourceFile = covertLua.dataConfig['sourceFile']
        sourceXML = XmlFile(sourceFile)
        if not sourceXML.isFile():
            self.controller.set_status('Tệp tin không tồn tại')
            return
        data = sourceXML.read_all()
        trans = TransEngToVie(self.controller)
        result = trans.trans_xml_cover_PZ(data, covertLua.dataConfig['tryTrans'])
        destinationFile = covertLua.dataConfig['destinationFile']
        if len(destinationFile) > 0:
            destinationLua = LuaFile(destinationFile)
            destinationLua.writeDataPZ(result)
            mesage = f'Lưu thành công: {destinationFile}'
        else:
            sourceLua.writeDataPZ(result)
            mesage = f'Lưu đè thành công: {sourceFile}'
        self.controller.set_status(mesage)
        messagebox.showinfo("Chuyển đổi XML sang LUA", mesage)
        