'''AvorionTrans.py
Việt hóa tệp ngôn ngữ trong trò chơi Avorion
'''
import os
import threading
from .TypeTrans import TypeTrans
from .EngToVieTrans import EngToVieTrans

'''Lớp xử lý luồng dịch'''
class AvorionThread(threading.Thread):
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
                if line[0] == 'msgstr':
                    msgstr = []
                    for row in line[1]:
                        vie = trans.trans_try(row[1])
                        msgstr.append((row[0], row[1], vie))
                    self.resultData.append(('msgstr', msgstr))
                else:
                    self.resultData.append(line)
        else:
            for line in self.sourceData:
                self.countData += 1
                if line[0] == 'msgstr':
                    msgstr = []
                    for row in line[1]:
                        vie = trans.trans_normal(row[1])
                        msgstr.append((row[0], row[1], vie))
                    self.resultData.append(('msgstr', msgstr))
                else:
                    self.resultData.append(line)
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None

'''Lớp tạo đa luồng dịch Avorion'''
class AvorionTrans(TypeTrans):
    #Phân luồng dữ liệu Avorion cần dịch
    def trans_data(self, data, tryTrans = 0, escChar = []):
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        self.countData = len(data)
        # Chỉ chạy 1 Thread
        if self.countData < countCpu*100 or countCpu == 1:
            avorionThread = AvorionThread(self.controller, data, tryTrans, escChar)
            avorionThread.start()
            self.listThread.append(avorionThread)
            return
        # Chạy countCpu Thread
        countChild = self.countData//countCpu
        for cpu in range(countCpu - 1):
            avorionThread = AvorionThread(self.controller, data[cpu*countChild:(cpu+1)*countChild], tryTrans, escChar)
            avorionThread.start()
            self.listThread.append(avorionThread)
        avorionThread = AvorionThread(self.controller, data[(countCpu-1)*countChild:], tryTrans, escChar)
        avorionThread.start()
        self.listThread.append(avorionThread)
        