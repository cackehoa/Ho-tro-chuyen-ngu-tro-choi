'''ProjectZomboidTrans.py
Việt hóa kiểu dữ liệu đặt biệt phần radio trò chơi Project Zomboid
'''

from .EngToVieThreadTrans import EngToVieThreadTrans

class ProjectZomboidTrans:
    def __init__(self, parent):
        self.controller = parent

    #Dịch trả về dữ liệu kiểu PZ
    def trans_data(self, data, tryTrans = 0, escChar = []):
        resultData = []
        db = self.controller.get_database()
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
                trans = EngToVieThreadTrans(db, eng, tryTrans, escChar)
                trans.start()
                resultData.append((eng, trans, [id_]))
        return resultData