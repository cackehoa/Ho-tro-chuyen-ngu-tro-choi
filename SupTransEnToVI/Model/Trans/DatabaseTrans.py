'''
DatabaseTrans.py
Dịch lại dữ liệu tạm cần thay đổi sau khi cập nhật
'''
import os
import threading
from .TypeTrans import TypeTrans
from .EngToVieTrans import EngToVieTrans

class DatabaseThread(threading.Thread):
    def __init__(self, parent, data, escChar):
        self.controller = parent
        self.sourceData = data
        self.tryTrans = 1
        self.escChar = escChar
        self.resultData = []
        self.countData = 0
        super().__init__()

    #Hàm chạy mặt định của luồng
    def run(self):
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        trans = EngToVieTrans(self.controller, cursor, self.escChar)
        #Chạy với điều kiện self.tryTrans luôn luôn đúng
        for row in self.sourceData:
            self.countData += 1
            #txtEng = self.controller.filter_whitespace(row[1])
            row[2] = trans.trans_try(row[1])
            self.resultData.append(row)
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None

class DatabaseTrans(TypeTrans):
    #Trả về tổng số dữ liệu đã xử lý
    def get_count_trans(self):
        total = 0
        for row in self.listThread:
            for col in row[1]:
                total += col.countData
        return total

    #Cập nhật lại dữ liệu xuống cơ sở dữ liệu
    def join_data(self):
        db = self.controller.get_database()
        for row in self.listThread:
            for col in row[1]:
                col.join()
                for data in col.resultData:
                    db.update_temp_sent(data[0], data[2])
        return None

    #Phân luồng dữ liệu tạm cần dịch lại
    def trans_data(self, key):
        #Tải danh sách escChar từ cơ sở dữ liệu
        db = self.controller.get_database()
        listEscChar = db.get_list_escchar()
        #Thêm phần tử mặc định
        if len(listEscChar) == 0:
            listEscChar.append('')
        #Tải dữ liệu từ cơ sở dữ liệu theo escChar
        data = []
        for escChar in listEscChar:
            dataEscChar = db.get_list_temp_sent(key, escChar)
            data.append((escChar, dataEscChar))
        # Mỗi luồng 1 countCpu
        countCpu = os.cpu_count()
        for row in data:
            #Đếm dataEscChar
            self.countData += len(row[1])
            # Chỉ chạy 1 Thread
            if self.countData < countCpu*100 or countCpu == 1:
                dataEscCharThread = DatabaseThread(self.controller, data, escChar)
                dataEscCharThread.start()
                listThread.append(dataEscCharThread)
                self.listThread.append((escChar, listThread))
                continue
            # Chạy countCpu Thread
            countChild = self.countData//countCpu
            for cpu in range(countCpu - 1):
                dataEscCharThread = DatabaseThread(self.controller, data[cpu*countChild:(cpu+1)*countChild], escChar)
                dataEscCharThread.start()
                listThread.append(dataEscCharThread)
            dataEscCharThread = DatabaseThread(self.controller, data[(countCpu-1)*countChild:], escChar)
            dataEscCharThread.start()
            listThread.append(dataEscCharThread)
            self.listThread.append((escChar, listThread))
        