'''TransEngToVie.py
Dịch tiếng Anh sang tiếng Việt
'''
import re
from .TransEngToVieThread import TransEngToVieThread

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

    #Cố dịch
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
        patternTrash = '\\\*\+\-\.\,\(\)\[\]\{\}\?\^\$\"\'\|\s/><&#!…%@=:;_–~`“”‘’'
        #Lọc rác đầu chuỗi
        strResult = re.findall(f"^([{patternTrash}\s0-9]+)([\S\s]*)$", key)
        if strResult:
            return strResult[0][0] + self.trans_try(strResult[0][1])
        #Lọc rác cuối chuỗi
        strResult = re.findall(f"^([{patternTrash}\s0-9]+)([\S\s]*)$", key[::-1])
        if strResult:
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
        delimiterSplit = ['\n', '\\n', '.', '?', '!', '…', ';', ':', ',']
        for delimiter in delimiterSplit:
            strSplit = key.split(delimiter)
            if len(strSplit) > 1:
                for i in range(len(strSplit)):
                    strSplit[i] = self.trans_try(strSplit[i])
                return delimiter.join(strSplit)
        #Chia nhỏ câu theo từ khóa giữa câu
        keywords = [('but', 'nhưng'), ('But', 'Nhưng'), ('BUT', 'NHƯNG'),
            ('because', 'bởi vì'), ('Because', 'Bởi vì'), ('BECAUSE', 'BỞI VÌ'),
            ('if', 'nếu'), ('If', 'Nếu'), ('IF', 'NẾU'),
            ('and', 'và'), ('And', 'Và'), ('AND', 'VÀ'),
            ('or', 'hoặc'), ('Or', 'Hoặc'), ('OR', 'HOẶC')]
        for keyword in keywords:
            #Từ khóa ở giữa chia câu thành 2 phần
            keywordResult = re.findall(f'^([\s\S]*) {re.escape(keyword[0])} ([\s\S]*)$', key)
            if keywordResult:
                return f'{self.trans_try(keywordResult[0][0])} {keyword[1]} {self.trans_try(keywordResult[0][1])}'
            #Từ khóa ở đầu câu
            keywordResult = re.findall(f'^{re.escape(keyword[0])} ([\s\S]+)$', key)
            if keywordResult:
                return f'{keyword[1]} {self.trans_try(keywordResult[0])}'
            #Từ khóa ở cuối câu (tạm thời chưa viết nhằm giúp dịch nhanh hơn)
        #Chi nhỏ câu theo rác
        trashResult = re.findall(f"[\s]*[{patternTrash}]+[\s]*", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = self.trans_try(strSplit[i])
            return trashResult[0].join(strSplit)
        return key

    #Dịch và trả về dữ liệu kiểu CSV
    def trans_csv(self, data, colEng, colVie, tryTrans = 0):
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
                trans = TransEngToVieThread(db, txtEng, tryTrans)
                trans.start()
            else:
                trans = None
            result.append((row, trans))
        return result

    #Dịch và trả về dữ liệu kiểu lua
    def trans_lua(self, data, tryTrans):
        db = self.controller.get_database()
        result = []
        for line in data:
            #Tìm phần cần dịch
            if line[0] == 'var':
                listVar = []
                for value in line[2]:
                    eng = self.controller.filter_whitespace(value)
                    trans = TransEngToVieThread(db, eng, tryTrans)
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
                            trans = TransEngToVieThread(db, eng, tryTrans)
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
    def trans_xml_cover_PZ(self, data, tryTrans):
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
                trans = TransEngToVieThread(db, eng, tryTrans)
                trans.start()
                resultData.append((eng, trans, [id_]))
        return resultData