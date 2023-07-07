'''EngToVieTrans.py
Dịch tiếng Anh sang tiếng Việt
'''
#import re
from .EngToVieThreadTrans import EngToVieThreadTrans

class EngToVieTrans:
    def __init__(self, parent):
        self.controller = parent

    #Dịch và trả về dữ liệu kiểu CSV
    def trans_csv(self, data, colEng, colVie, tryTrans = 0, escChar = []):
        result = []
        maxRow = max (colEng, colVie)
        db = self.controller.get_database()
        trans = None
        for row in data:
            count = len(row)
            #Bỏ qua dòng trống
            if count == 0:
                continue
            elif count > maxRow:
                txtEng = self.controller.filter_whitespace(row[colEng])
                trans = EngToVieThreadTrans(db, txtEng, tryTrans, escChar)
                trans.start()
            else:
                trans = None
            result.append((row, trans))
        return result

    #Dịch và trả về dữ liệu kiểu lua
    def trans_lua(self, data, tryTrans = 0, escChar = []):
        db = self.controller.get_database()
        result = []
        for line in data:
            #Tìm phần cần dịch
            if line[0] == 'var':
                listVar = []
                for value in line[2]:
                    eng = self.controller.filter_whitespace(value)
                    trans = EngToVieThreadTrans(db, eng, tryTrans, escChar)
                    trans.start()
                    listVar.append(trans)
                result.append(('var', line[1], listVar))
                continue
            if line[0] == 'list':
                listData = []
                for row in line[2]:
                    #Tìm phần cần dịch
                    if row[0] == 'var':
                        listVar = []
                        for value in row[2]:
                            eng = self.controller.filter_whitespace(value)
                            trans = EngToVieThreadTrans(db, eng, tryTrans, escChar)
                            trans.start()
                            listVar.append(trans)
                        listData.append(('var', row[1], listVar))
                        continue
                    listData.append(row)
                result.append(('list', line[1], listData))
                continue
            result.append(line)
        return result

    #Dịch trả về dữ liệu kiểu PZ
    def trans_xml_cover_PZ(self, data, tryTrans = 0, escChar = []):
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