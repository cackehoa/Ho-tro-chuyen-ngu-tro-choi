'''TransEngToVieThread.py
Mỗi luồng dịch một câu
Đầu vào:
    db: database
    eng: câu tiếng Anh
Đầu ra:
    get_vie(): câu tiếng Việt
'''
import re
import threading

class TransEngToVieThread(threading.Thread):
    def __init__(self, db, eng, tryTrans = 0):
        super().__init__()
        self.db = db
        self.tryTrans = tryTrans
        self.set_eng(eng)

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

    #Dịch bình thường
    def trans_normal(self, key):
        if len(key) < 2:
            return key
        sqlResult = self.db.get_eng_thread(key, self.cursor)
        if sqlResult is not None:
            return sqlResult[2]
        return key

    #Cố dịch
    def trans_try(self, key):
        if len(key) < 2:
            return key
        #Như phần trans_normal
        sqlResult = self.db.get_eng_thread(key, self.cursor)
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
        patternTrash = '\\\*\+\-\.\,\(\)\[\]\{\}\?\^\$\"\'\|/><&#!…%@=:;_–~`“”‘’'
        #Lọc rác đầu chuỗi + khoản trắng + số
        strResult = re.findall(f"^([{patternTrash}\s0-9]+)([\S\s]*)$", key)
        if len(strResult) > 0:
            return strResult[0][0] + self.trans_try(strResult[0][1])
        #Lọc rác cuối chuỗi + khoản trắng + số
        strResult = re.findall(f"^([{patternTrash}\s0-9]+)([\S\s]*)$", key[::-1])
        if len(strResult) > 0:
            strTrash = strResult[0][0]
            strEnd = strResult[0][1]
            return self.trans_try(strEnd[::-1]) + strTrash[::-1]
        #Lấy câu gần đúng ngắn nhất về lọc phần thừa xem có khả năng cho kết quả không
        sqlResult = self.db.get_like_eng_thread(key, self.cursor)
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
        #Chi nhỏ câu theo rác
        trashResult = re.findall(f"[\s]*[{patternTrash}]+[\s]*", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = self.trans_try(strSplit[i])
            return trashResult[0].join(strSplit)
        #Chia nhỏ câu theo từ khóa câu
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
            #Từ khóa ở cuối câu
            keywordResult = re.findall(f'^([\s\S]+) {re.escape(keyword[0])}$', key)
            if keywordResult:
                return f'{self.trans_try(keywordResult[0])} {keyword[1]}'
        return key

    #Hàm chạy mặt định của luồng
    def run(self):
        #Lấy con trỏ dành riêng cho luồng
        self.cursor = self.db.create_new_cursor()
        if self.tryTrans:
            self.set_vie(self.trans_try(self.get_eng()))
        else:
            self.set_vie(self.trans_normal(self.get_eng()))
        #Giải phóng con trỏ hy vọng không bị kẹt
        self.cursor.close()
        self.cursor = None