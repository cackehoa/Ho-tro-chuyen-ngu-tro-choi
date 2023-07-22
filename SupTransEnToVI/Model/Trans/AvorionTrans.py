'''AvorionTrans.py
Việt hóa tệp ngôn ngữ trong trò chơi Avorion
'''
import os
import threading
from .EngToVieTrans import EngToVieTrans

# Luồng dịch danh sách Avorion
class AvorionThread(threading.Thread):

    def __init__(self, parent, data, tryTrans, escChar):
        self.controller = parent
        self.sourceData = data
        self.tryTrans = tryTrans
        self.escChar = escChar
        self.resultData = []
        super().__init__()

    #Hàm chạy mặt định của luồng
    def run(self):
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        trans = EngToVieTrans(db, cursor, self.escChar)
        if self.tryTrans:
            for line in self.sourceData:
                if line[0] == 'msgid':
                    eng = self.controller.filter_whitespace(line[1])
                    vie = trans.trans_try(eng)
                    self.resultData.append(('msgid', line[1], vie))
                else:
                    self.resultData.append(line)
        else:
            for line in self.sourceData:
                if line[0] == 'msgid':
                    eng = self.controller.filter_whitespace(line[1])
                    vie = trans.trans_normal(eng)
                    self.resultData.append(('msgid', line[1], vie))
                else:
                    self.resultData.append(line)
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None

# Tạo đa luồng nhằm tăng tốc
class AvorionTrans:

    def __init__(self, parent):
        self.controller = parent

    # Dùng để chạy đa luồng
    def trans_data_thread(self, data, tryTrans, escChar):
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        trans = EngToVieTrans(db, cursor, escChar)
        result = []
        if tryTrans:
            for line in data:
                if line[0] == 'msgid':
                    eng = self.controller.filter_whitespace(line[1])
                    vie = trans.trans_try(eng)
                    result.append(('msgid', line[1], vie))
                else:
                    result.append(line)
        else:
            for line in data:
                if line[0] == 'msgid':
                    eng = self.controller.filter_whitespace(line[1])
                    vie = trans.trans_normal(eng)
                    result.append(('msgid', line[1], vie))
                else:
                    result.append(line)
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None
        return result

    def trans_data_test(self, data, tryTrans = 0, escChar = []):
        countData = len(data)
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        # Chỉ chạy 1 Thread
        if countData < countCpu*100 or countCpu == 1:
            avorionThread = threading.Thread(target=self.trans_data_thread, args=(data, tryTrans, escChar))
        result = []
        return result

    def trans_data(self, data, tryTrans = 0, escChar = []):
        countData = len(data)
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        # Chỉ chạy 1 Thread
        if countData < countCpu*100 or countCpu == 1:
            avorionThread = AvorionThread(self.controller, data, tryTrans, escChar)
            avorionThread.start()
            avorionThread.join()
            return avorionThread.resultData
        # Chạy countCpu Thread
        countChild = countData//countCpu
        listThread = []
        for cpu in range(countCpu - 1):
            avorionThread = AvorionThread(self.controller, data[cpu*countChild:(cpu+1)*countChild], tryTrans, escChar)
            avorionThread.start()
            listThread.append(avorionThread)
        avorionThread = AvorionThread(self.controller, data[(countCpu-1)*countChild:], tryTrans, escChar)
        avorionThread.start()
        listThread.append(avorionThread)
        # Ghép list lại rồi trả về
        result = []
        for avorionThread in listThread:
            avorionThread.join()
            result.extend(avorionThread.resultData)
        return result