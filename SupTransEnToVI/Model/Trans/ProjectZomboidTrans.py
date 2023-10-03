'''ProjectZomboidTrans.py
Việt hóa kiểu dữ liệu đặt biệt phần radio trò chơi Project Zomboid
'''
import threading

from .EngToVieTrans import EngToVieTrans
from .EngToVieThreadTrans import EngToVieThreadTrans

'''Lớp tạo luồng dịch'''
class ProjectZomboidThread(threading.Thread):
    #Hàm khởi tạo
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
        trans = EngToVieTrans(self.controller, cursor, self.escChar)
        if self.tryTrans:
            pass
        else:
            pass
        #Giải phóng con trỏ hy vọng không bị kẹt
        cursor.close()
        cursor = None

'''Tạo đa luồng nhằm tăng tốc'''
class ProjectZomboidTrans:
    #Hàm khởi tạo
    def __init__(self, parent):
        self.controller = parent

    #Dịch trả về dữ liệu kiểu PZ
    def trans_data(self, data, tryTrans = 0, escChar = []):
        resultData = []
        for LineEntry in data.iter('LineEntry'):
            id_ = LineEntry.attrib['ID']
            eng = self.controller.filter_whitespace(LineEntry.text)
            isEng = True
            for i in range(len(resultData)):
                if eng == resultData[i][0]:
                    isEng = False
                    resultData[i][2].append(id_)
                    break
            if isEng:
                trans = EngToVieThreadTrans(self.controller, eng, tryTrans, escChar)
                trans.start()
                resultData.append((eng, trans, [id_]))
        return resultData