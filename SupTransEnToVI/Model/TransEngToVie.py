'''TransEngToVie.py
Dịch tiếng Anh sang tiếng Việt
'''
import re

class TransEngToVie:
    def __init__(self, parent):
        self.controller = parent

    #Chuẩn hóa dữ liệu theo database
    def normalize_data(self, data, str_normalize = []):
        if str_normalize:
            normalize = str_normalize
        else:
            normalize = [
                ("\\\"", "\""),
                ("\\'", "'"),
                ("\\n", "\n"),
                ("\\r", "\r"),
                ("\\t", "\t"),
                ("\\\\", "\\")]
        value = data
        for row in normalize:
            value = value.replace(row[0], row[1])
        return value

    #Chuẩn hóa dữ liệu theo dữ liệu tương ứng
    def re_normalize_data(self, data, str_re_normalize = []):
        if str_re_normalize:
            normalize = str_re_normalize
        else:
            normalize = [
                ("\\", "\\\\"),
                ("\t", "\\t"),
                ("\r", "\\r"),
                ("\n", "\\n"),
                ("\'", "\\\'"),
                ("\"", "\\\"")]
        value = data
        for row in normalize:
            value = value.replace(row[0], row[1])
        return value

    #Dịch bình thường
    def trans_normal(self, key):
        if len(key) < 2:
            return key
        db = self.controller.get_database()
        sqlResult = db.get_eng(key)
        if sqlResult is not None:
            return sqlResult[2]
        return key

    def trans_try(self, key):
        if len(key) < 2:
            return key
        #Như phần trans_normal
        db = self.controller.get_database()
        sqlResult = db.get_eng(key)
        if sqlResult is not None:
            return sqlResult[2]
        #Chi nhỏ câu theo thẻ html
        patternHtml = r'<[^>]+>'
        strResult = re.findall(f"[\s]*{patternHtml}[\s]*", key)
        if len(strResult) > 0:
            strSplit = key.split(strResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = self.trans_try(strSplit[i])
            return strResult[0].join(strSplit)
        #Định nghĩa ký tự rác
        patternTrash = '\\\*\+\-\.\,\(\)\[\]\{\}\?\^\$\"\'\|/><&#!…%@=:;_~`“”‘’'
        #Lọc rác đầu chuỗi
        strResult = re.findall(f"^([{patternTrash}\s0-9]+)([\S\s]*)$", key)
        if len(strResult) > 0:
            return strResult[0][0] + self.trans_try(strResult[0][1])
        #Lọc rác cuối chuỗi
        strResult = re.findall(f"^([{patternTrash}\s0-9]+)([\S\s]*)$", key[::-1])
        if len(strResult) > 0:
            strTrash = strResult[0][0]
            strEnd = strResult[0][1]
            return self.trans_try(strEnd[::-1]) + strTrash[::-1]
        #Lấy câu gần đúng ngắn nhất về lọc phần thừa xem có khả năng cho kết quả không
        sqlResult = db.get_like_eng(key)
        if sqlResult is not None:
            #Lọc phần thừa đầu chuỗi eng
            engBeginExcess = re.findall(f'^([\s\S]*){re.escape(key)}([\s\S]*)$', sqlResult[1])
            if engBeginExcess:
                engBeginTrash = engBeginExcess[0][0]
                #Lọc rác đầu chuỗi vie
                vieBeginExcess = re.findall(f"^([{patternTrash}\s0-9]*)([\S\s]*)$", sqlResult[2])
                vieBeginTrash = vieBeginExcess[0][0]
                #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                if engBeginTrash.strip() == vieBeginTrash.strip():
                    vieRemaining = vieBeginExcess[0][1]
                    #Lọc rác cuối chuỗi vie
                    vieEndExcess = re.findall(f"^([{patternTrash}\s0-9]*)([\S\s]*)$", vieRemaining[::-1])
                    vieEndTrash = vieEndExcess[0][0]
                    engEndTrash = engBeginExcess[0][1]
                    if engEndTrash.strip() == vieEndTrash[::-1].strip():
                        vieEndRemaining = vieEndExcess[0][1]
                        return vieEndRemaining[::-1]
        #Chia nhỏ câu với hy vọng dịch từng đoạn có thể dịch
        delimiterSplit = ['\n', '\\n', '.', '?', '!', '…', ';', ':', ',', '"', '*', '(', ')']
        for delimiter in delimiterSplit:
            strSplit = key.split(delimiter)
            if len(strSplit) > 1:
                for i in range(len(strSplit)):
                    strSplit[i] = self.trans_try(strSplit[i])
                return delimiter.join(strSplit)
        #Chi nhỏ câu theo rác
        trashResult = re.findall(f"([\s]*[{patternTrash}]+[\s]*)", key)
        if len(trashResult) > 0:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = self.trans_try(strSplit[i])
            return trashResult[0].join(strSplit)
        return key

    #Dịch và trả về dữ liệu kiểu CSV
    def trans_csv(self, data, colEng, colVie, tryTrans = 0):
        result = []
        maxRow = max (colEng, colVie)
        if tryTrans == 0:
            for row in data:
                if len(row) > maxRow:
                    txtEng = self.controller.filter_whitespace(row[colEng])
                    txtVie = self.trans_normal(txtEng)
                    row[colVie] = txtVie
                result.append(row)
            return result
        for row in data:
            if len(row) > maxRow:
                txtEng = self.controller.filter_whitespace(row[colEng])
                txtVie = self.trans_try(txtEng)
                row[colVie] = txtVie
            result.append(row)
        return result

    #Dịch và trả về dữ liệu kiểu lua
    def trans_lua(self, data, tryTrans):
        str_re_normalize = [("\n", "\\n")]
        result = []
        if tryTrans == 0:
            for line in data:
                #Tìm phần cần dịch
                if line[0] == 'var':
                    listVar = []
                    for value in line[2]:
                        eng = self.normalize_data(value)
                        eng = self.controller.filter_whitespace(eng)
                        vie = self.trans_normal(eng)
                        vie = self.re_normalize_data(vie, str_re_normalize)
                        listVar.append(vie)
                    result.append(('var', line[1], listVar))
                    continue
                if line[0] == 'list':
                    listData = []
                    for row in line[2]:
                        if row[0] == 'var':
                            listVar = []
                            for value in row[2]:
                                eng = self.normalize_data(value)
                                eng = self.controller.filter_whitespace(eng)
                                vie = self.trans_normal(eng)
                                vie = self.re_normalize_data(vie, str_re_normalize)
                                listVar.append(vie)
                            listData.append(('var', row[1], listVar))
                            continue
                        listData.append(row)
                    result.append(('list', line[1], listData))
                    continue
                result.append(line)
            return result
        for line in data:
            #Tìm phần cần dịch
            if line[0] == 'var':
                listVar = []
                for value in line[2]:
                    eng = self.normalize_data(value)
                    eng = self.controller.filter_whitespace(eng)
                    vie = self.trans_try(eng)
                    vie = self.re_normalize_data(vie, str_re_normalize)
                    listVar.append(vie)
                result.append(('var', line[1], listVar))
                continue
            if line[0] == 'list':
                listData = []
                for row in line[2]:
                    if row[0] == 'var':
                        listVar = []
                        for value in row[2]:
                            eng = self.normalize_data(value)
                            eng = self.controller.filter_whitespace(eng)
                            vie = self.trans_try(eng)
                            vie = self.re_normalize_data(vie, str_re_normalize)
                            listVar.append(vie)
                        listData.append(('var', row[1], listVar))
                        continue
                    listData.append(row)
                result.append(('list', line[1], listData))
                continue
            result.append(line)
        return result