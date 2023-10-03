'''
IniTrans.py
Việt hóa tệp ngôn ngữ dạng ini
'''
import os
import threading
from .TypeTrans import TypeTrans
from .EngToVieTrans import EngToVieTrans

'''Lớp xử lý luồng dịch'''
class IniThread(threading.Thread):
    #Hàm khởi tạo
    def __init__(self, parent, data, tryTrans, escChar):
        self.controller = parent
        self.sourceData = data
        self.tryTrans = tryTrans
        self.escChar = escChar
        self.resultData = []
        self.countData = 0
        super().__init__()

    #Hàm chạy mặt định của luồng
    def run(self):
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        trans = EngToVieTrans(self.controller, cursor, self.escChar)
        if self.tryTrans:
            for line in self.sourceData:
                self.countData += 1
                if line[0] == 'var':
                    vie = trans.trans_try(line[2])
                    self.resultData.append(('var', line[1], vie))
                    continue
                self.resultData.append(line)
        else:
            for line in self.sourceData:
                self.countData += 1
                if line[0] == 'var':
                    line[2] = trans.trans_normal(line[2])
                self.resultData.append(line)

'''Lớp tạo đa luồng dịch'''
class IniTrans(TypeTrans):
    #Phân luồng dữ liệu ini cần dịch
    def trans_data(self, data, tryTrans = 0, escChar = []):
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        self.countData = len(data)
        # Chỉ chạy 1 Thread
        if self.countData < countCpu*100 or countCpu == 1:
            varThread = IniThread(self.controller, data, tryTrans, escChar)
            varThread.start()
            self.listThread.append(varThread)
            return
        # Chạy countCpu Thread
        countChild = self.countData//countCpu
        for cpu in range(countCpu - 1):
            varThread = IniThread(self.controller, data[cpu*countChild:(cpu+1)*countChild], tryTrans, escChar)
            varThread.start()
            self.listThread.append(varThread)
        varThread = IniThread(self.controller, data[(countCpu-1)*countChild:], tryTrans, escChar)
        varThread.start()
        self.listThread.append(varThread)
        