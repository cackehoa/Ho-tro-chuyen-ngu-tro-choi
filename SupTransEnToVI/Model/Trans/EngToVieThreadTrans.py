'''EngToVieThreadTrans.py
Mỗi luồng dịch một câu
Đầu vào:
    db: database
    eng: câu tiếng Anh
    tryTrans: cố dịch
Đầu ra:
    get_vie(): câu tiếng Việt
'''
import re
import threading
from .EngToVieTrans import EngToVieTrans

class EngToVieThreadTrans(threading.Thread):
    def __init__(self, parent, eng, tryTrans = 0, escChar = []):
        self.controller = parent
        self.tryTrans = tryTrans
        self.escChar = escChar
        self.set_eng(eng)
        super().__init__()

    #Nhập eng
    def set_eng(self, eng):
        self.eng = eng

    #Lấy eng
    def get_eng(self):
        return self.eng

    #Nhập vie
    def set_vie(self, vie):
        self.vie = vie

    #Lấy vie
    def get_vie(self):
        return self.vie

    #Hàm chạy mặt định của luồng
    def run(self):
        #Cấp phát con trỏ dành riêng cho luồng
        db = self.controller.get_database()
        cursor = db.create_new_cursor()
        trans = EngToVieTrans(self.controller, cursor, self.escChar)
        if self.tryTrans:
            self.set_vie(trans.trans_try(self.get_eng()))
        else:
            self.set_vie(trans.trans_normal(self.get_eng()))
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None