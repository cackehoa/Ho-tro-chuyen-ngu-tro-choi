'''LuaTrans.py
Đầu vào chuẩn danh sách biến dữ liệu kiểu Lua
Độ sâu cấp: 1
'''

from .EngToVieThreadTrans import EngToVieThreadTrans

'''Tạo đa luồng nhằm tăng tốc'''
class LuaTrans:
    def __init__(self, parent):
        self.controller = parent

    #Dịch và trả về dữ liệu kiểu lua
    def trans_data(self, data, tryTrans = 0, escChar = []):
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
