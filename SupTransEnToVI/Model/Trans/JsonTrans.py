'''
JsonTrans.py
Việt hóa tệp ngôn ngữ dạng ini
'''
import os
import threading
from .TypeTrans import TypeTrans
from .EngToVieTrans import EngToVieTrans

'''Lớp xử lý luồng dịch'''
class JsonThread(threading.Thread):
    #Hàm khởi tạo
    def __init__(self, parent, data, tryTrans, escChar):
        self.controller = parent
        self.sourceData = data
        self.tryTrans = tryTrans
        self.escChar = escChar
        self.resultData = {}
        self.countData = 0
        super().__init__()
    
    #Hàm chạy mặt định của luồng
    def run(self):
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        trans = EngToVieTrans(self.controller, cursor, self.escChar)
        if self.tryTrans:
            for key in self.sourceData:
                self.countData += 1
                #Chỉ dịch kiểu string
                if isinstance(self.sourceData[key], str):
                    txtEng = self.controller.filter_whitespace(self.sourceData[key])
                    self.resultData[key] = trans.trans_try(txtEng)
                    continue
                #Tạm thời không dịch sâu
                self.resultData[key] = self.sourceData[key]
        else:
            for key in self.sourceData:
                self.countData += 1
                #Chỉ dịch kiểu string
                if isinstance(self.sourceData[key], str):
                    txtEng = self.controller.filter_whitespace(self.sourceData[key])
                    self.resultData[key] = trans.trans_normal(txtEng)
                    continue
                #Tạm thời không dịch sâu
                self.resultData[key] = self.sourceData[key]

'''Lớp tạo đa luồng dịch'''
class JsonTrans(TypeTrans):
    #Ghép dict lại rồi trả về
    def join_data(self):
        result = {}
        for row in self.listThread:
            row.join()
            for key in row.resultData:
                result[key] = row.resultData[key]
        return result

    #Phân luồng dữ liệu ini cần dịch
    def trans_data(self, data, tryTrans = 0, escChar = []):
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        self.countData = len(data)
        # Chỉ chạy 1 Thread
        if self.countData < countCpu*100 or countCpu == 1:
            varThread = JsonThread(self.controller, data, tryTrans, escChar)
            varThread.start()
            self.listThread.append(varThread)
            return
        # Chạy countCpu Thread
        countChild = self.countData//countCpu
        for cpu in range(countCpu - 1):
            varThread = JsonThread(self.controller, dict(list(data.items())[cpu*countChild:(cpu+1)*countChild]), tryTrans, escChar)
            varThread.start()
            self.listThread.append(varThread)
        varThread = JsonThread(self.controller, dict(list(data.items())[(countCpu-1)*countChild:]), tryTrans, escChar)
        varThread.start()
        self.listThread.append(varThread)