'''CsvTrans.py
Việt hóa kiểu dữ liệu đặt biệt chuẩn CSV
'''

from .EngToVieThreadTrans import EngToVieThreadTrans

class CsvTrans:
    def __init__(self, parent):
        self.controller = parent

    #Dịch và trả về dữ liệu kiểu CSV
    def trans_data(self, data, colEng, colVie, tryTrans = 0, escChar = []):
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