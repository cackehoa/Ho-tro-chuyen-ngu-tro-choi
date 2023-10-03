'''MenuBar.py
Đùng để quản lý thanh menu tùy chỉnh
'''
from tkinter import Menu
from .Dialog import *
from .Toplevel import *
from ..Model.File import *
from ..Model.Trans import *
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
        exportMenu.add_command(label="INI", command = self.export_ini)
        #exportMenu.add_command(label="JSON", command = self.export_json)
        exportMenu.add_command(label="LUA", command = self.export_lua)
        #exportMenu.add_command(label="XUnity", command = self.export_xunity)
        self.add_cascade(label="Xuất", menu=exportMenu)
        '''#Menu nhập
        importMenu = Menu(self, tearoff=0)
        #importMenu.add_command(label="CSV", command = self.import_csv)
        #importMenu.add_command(label="INI", command = self.import_ini)
        #importMenu.add_command(label="JSON", command = self.import_json)
        #importMenu.add_command(label="LUA", command = self.import_lua)
        #importMenu.add_command(label="XUnity", command = self.import_xunity)
        self.add_cascade(label="Nhập", menu=importMenu)'''
        coverMenu = Menu(self, tearoff=0)
        coverMenu.add_command(label="Dịch XML thành ProjectZomboid", command = self.cover_pz)
        coverMenu.add_command(label="Avorion", command = self.export_avorion)
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
        #Xác định đối tượng lưu
        destinationCSV = sourceCSV
        destinationFile = exportCsv.dataConfig['destinationFile']
        if len(destinationFile) > 0:
            destinationCSV = CsvFile(destinationFile)
            destinationCSV.set_delimiter(exportCsv.dataConfig['delimiter'])
        #Không xử lý gì khi dữ liệu đầu vào sai
        colVie = exportCsv.dataConfig['colVie']
        colEng = exportCsv.dataConfig['colEng']
        if colVie < 0 or colEng < 0:
            destinationCSV.write_data(data)
            self.controller.set_status(f'Lưu thành công: {destinationFile}')
        else:
            #Tắt bộ động
            self.controller.stop_dynamic()
            #Dịch
            trans = CsvTrans(self.controller)
            trans.trans_data(data, colEng, colVie, exportCsv.dataConfig['tryTrans'], exportCsv.dataConfig['escChar'])
            self.controller.set_status(f'Chờ dịch: {sourceFile}')
            progressCsv = ProgressToplevel(self.controller, trans, destinationCSV, sourceFile)

    def export_ini(self):
        typeFile = ('INI', '*.ini'), ('Tất cả', '*.*')
        exportIni = ExportTwoDialog(self.controller, 'INI', typeFile)
        sourceFile = exportIni.dataConfig['sourceFile']
        sourceIni = IniFile(sourceFile)
        if not sourceIni.isFile():
            self.controller.set_status('Tệp tin không tồn tại')
            return
        data  = sourceIni.read_all()
        #Xác định đối tượng lưu
        destinationIni = sourceIni
        destinationFile = exportIni.dataConfig['destinationFile']
        if len(destinationFile) > 0:
            destinationIni = IniFile(destinationFile)
        #Tắt bộ động
        self.controller.stop_dynamic()
        #Dịch
        trans = IniTrans(self.controller)
        trans.trans_data(data, exportIni.dataConfig['tryTrans'], exportIni.dataConfig['escChar'])
        progressIni = ProgressToplevel(self.controller, trans, destinationIni, sourceFile)
        self.controller.set_status(f'Chờ dịch: {sourceFile}')

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
        #Tắt bộ động
        self.controller.stop_dynamic()
        data = sourceLua.read_all()
        #Dịch
        trans = LuaTrans(self.controller)
        result = trans.trans_data(data, exportLua.dataConfig['tryTrans'], exportLua.dataConfig['escChar'])
        destinationFile = exportLua.dataConfig['destinationFile']
        destinationLua = sourceLua
        if len(destinationFile) > 0:
            destinationLua = LuaFile(destinationFile)
        destinationLua.write_data(result)
        mesage = f'Lưu thành công: {destinationFile}'
        self.controller.set_status(mesage)
        messagebox.showinfo("Xuất lua", mesage)

    def export_xunity(self):
        typeFile = ('TXT', '*.txt'), ('Tất cả', '*.*')
        exportXUnity = ExportTwoDialog(self.controller, 'XUnity', typeFile)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        print(exportXUnity.dataConfig)

    def import_csv(self):
        #importCsv = ImportCsvDialog(self.controller)
        #importCsv = ProgressDialog(self.controller)
        self.controller.set_status('Chức năng này chưa được hoàng thành')
        messagebox.showinfo('Cảnh báo', 'Chức năng này chưa được hoàng thành')
        #print(importCsv.dataConfig)

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

    '''Chuyển đổi và dịch dữ liệu xml sang dữ liệu đặt trưng của trò chơi Project Zomboid
    Tệp nguồn XML: \media\radio\RadioData.xml
    Chuyển đổi và dịch thành: \media\radio\*.txt
    '''
    def cover_pz(self):
        self.controller.set_status('Dịch XML thành dữ liệu kiểu Project Zomboid...')
        typeFile = ('XML', '*.xml'), ('Tất cả', '*.*')
        covertLua = ExportTwoDialog(self.controller, 'XML', typeFile, '[]')
        sourceFile = covertLua.dataConfig['sourceFile']
        sourceXML = XmlFile(sourceFile)
        if not sourceXML.isFile():
            self.controller.set_status('Tệp tin không tồn tại')
            return
        #Tắt bộ động
        self.controller.stop_dynamic()
        #Dịch
        data = sourceXML.read_all()
        trans = ProjectZomboidTrans(self.controller)
        result = trans.trans_data(data, covertLua.dataConfig['tryTrans'], covertLua.dataConfig['escChar'])
        destinationFile = covertLua.dataConfig['destinationFile']
        if len(destinationFile) < 1:
            destinationFile = sourceFile + '.temp'
        destinationLua = LuaFile(destinationFile)
        destinationLua.writeDataPZ(result)
        mesage = f'Lưu thành công: {destinationFile}'
        self.controller.set_status(mesage)
        messagebox.showinfo("Chuyển đổi XML sang LUA", mesage)
        
    '''Việt hóa dữ liệu đặt biệt trong trò chơi Avorion
    Tệp nguồn: data\localization\template.pot
    Tệp đích: data\localization\*.po
    '''
    def export_avorion(self):
        self.controller.set_status('Dịch tệp của trò chơi Avorion...')
        typeFile = ('PO trong Avorion', '*.po'), ('Tất cả', '*.*')
        coverAvorion = ExportTwoDialog(self.controller, 'PO', typeFile, '{}')
        sourceFile = coverAvorion.dataConfig['sourceFile']
        sourceAvorion = AvorionFile(sourceFile, self.controller)
        if not sourceAvorion.isFile():
            self.controller.set_status('Tệp tin không tồn tại')
            return
        #Tắt bộ động
        self.controller.stop_dynamic()
        #Dịch
        data = sourceAvorion.read_all()
        trans = AvorionTrans(self.controller)
        trans.trans_data(data, coverAvorion.dataConfig['tryTrans'], coverAvorion.dataConfig['escChar'])
        destinationFile = coverAvorion.dataConfig['destinationFile']
        destinationAvorion = sourceAvorion
        if len(destinationFile) > 0:
            destinationAvorion = AvorionFile(destinationFile, self.controller)
        progressAvorion = ProgressToplevel(self.controller, trans, destinationAvorion, sourceFile)
        self.controller.set_status(f'Chờ dịch: {sourceFile}')