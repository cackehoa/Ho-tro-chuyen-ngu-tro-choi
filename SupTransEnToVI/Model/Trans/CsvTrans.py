'''CsvTrans.py
Việt hóa kiểu dữ liệu đặt biệt chuẩn CSV
'''
import os
import threading
from .TypeTrans import TypeTrans
from .EngToVieTrans import EngToVieTrans

'''Lớp xử lý luồng dịch'''
class CsvThread(threading.Thread):
    #Hàm khởi tạo
    def __init__(self, parent, data, colEng, colVie, tryTrans, escChar):
        self.controller = parent
        self.sourceData = data
        self.colEng = colEng
        self.colVie = colVie
        self.tryTrans = tryTrans
        self.escChar = escChar
        self.resultData = []
        self.countData = 0
        super().__init__()

    #Hàm chạy mặt định của luồng
    def run(self):
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        maxRow = max (self.colEng, self.colVie)
        trans = EngToVieTrans(self.controller, cursor, self.escChar)
        if self.tryTrans:
            for row in self.sourceData:
                self.countData += 1
                count = len(row)
                #Bỏ qua dòng trống
                if count == 0:
                    continue
                #Vị trí tồn tại mới dịch (tăng tốc)
                if count > maxRow:
                    txtEng = self.controller.filter_whitespace(row[self.colEng])
                    row[self.colVie] = trans.trans_try(txtEng)
                self.resultData.append(row)
        else:
            for row in self.sourceData:
                self.countData += 1
                count = len(row)
                #Bỏ qua dòng trống
                if count == 0:
                    continue
                #Vị trí tồn tại mới dịch (tăng tốc)
                if count > maxRow:
                    txtEng = self.controller.filter_whitespace(row[self.colEng])
                    row[self.colVie] = trans.trans_normal(txtEng)
                self.resultData.append(row)
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None

'''Lớp tạo đa luồng dịch CSV'''
class CsvTrans(TypeTrans):
    #Ghép list lại rồi trả về
    def join_data(self):
        result = []
        #Thêm header
        result.append(self.data0)
        for csvThread in self.listThread:
            csvThread.join()
            result.extend(csvThread.resultData)
        return result
        
    #Phân luồng dữ liệu CSV cần dịch
    def trans_data(self, data, colEng = 1, colVie = 2, tryTrans = 0, escChar = []):
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        self.countData = len(data) - 1
        #Lưu header
        self.data0 = data[0]
        # Chỉ chạy 1 Thread
        if self.countData < countCpu*100 or countCpu == 1:
            csvThread = CsvThread(self.controller, data[1:], colEng, colVie, tryTrans, escChar)
            csvThread.start()
            self.listThread.append(csvThread)
            return
        # Chạy countCpu Thread
        countChild = self.countData//countCpu
        for cpu in range(countCpu - 1):
            csvThread = CsvThread(self.controller, data[cpu*countChild + 1:(cpu+1)*countChild + 1], colEng, colVie, tryTrans, escChar)
            csvThread.start()
            self.listThread.append(csvThread)
        csvThread = CsvThread(self.controller, data[(countCpu-1)*countChild + 1:], colEng, colVie, tryTrans, escChar)
        csvThread.start()
        self.listThread.append(csvThread)
        