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

class EngToVieThreadTrans(threading.Thread):
    def __init__(self, db, eng, tryTrans = 0, escChar = []):
        super().__init__()
        self.db = db
        self.tryTrans = tryTrans
        self.escChar = escChar
        self.set_eng(eng)
        #Định nghĩa từ khóa cần cắt nhỏ
        self.keywords = [
            ('but maybe', 'nhưng có lẽ'), ('But maybe', 'Nhưng có lẽ'), ('But Maybe', 'Nhưng có lẽ'), ('BUT MAYBE', 'NHƯNG CÓ LẼ'),
            ('but even if', 'nhưng ngay cả khi'), ('But even if', 'Nhưng ngay cả khi'), ('But Even If', 'Nhưng ngay cả khi'), ('BUT EVEN IF', 'NHƯNG NGAY CẢ KHI'),
            ('but', 'nhưng'), ('But', 'Nhưng'), ('BUT', 'NHƯNG'),
            ('because', 'bởi vì'), ('Because', 'Bởi vì'), ('BECAUSE', 'BỞI VÌ'),
            ('if', 'nếu'), ('If', 'Nếu'), ('IF', 'NẾU'),
            ('and', 'và'), ('And', 'Và'), ('AND', 'VÀ'),
            ('or', 'hoặc'), ('Or', 'Hoặc'), ('OR', 'HOẶC'),
            ('then', 'sau đó,'), ('Then', 'Sau đó,'), ('THEN', 'SAU ĐÓ,')]
        #Định nghĩa dấu phân cách
        self.delimiterSplit = ['\n', '\\n', '.', '?', '!', '…', ':', ';', ',']
        #Định nghĩa ký tự rác
        #self.patternTrash = '\\\*\+\-\.\,\(\)\[\]\{\}\?\^\$\"\'\|/><&#!…%@=:;_–~`“”‘’'
        self.patternTrash = re.escape('\\`~!@#$%^&*()_—-+={[}]\|:;\'"<,>.?/“”‘’…')
        #Định nghĩa đại từ nhân xưng tiếng Anh
        self.pronounEN = [('I', 'Tôi'),
            ('you', 'bạn'), ('You', 'Bạn'), ('YOU', 'BẠN'),
            ('he', 'anh ấy'), ('He', 'Anh ấy'), ('HE', 'ANH ẤY'),
            ('she', 'cô ấy'), ('She', 'Cô ấy'), ('SHE', 'CÔ ẤY'),
            ('we', 'chúng tôi'), ('We', 'Chúng tôi'), ('WE', 'CHÚNG TÔI'),
            ('they', 'họ'), ('They', 'Họ'), ('THEY', 'HỌ')]
        #Định nghĩa đại từ nhân xưng tiếng Việt
        self.pronounVN = [('tôi', 'I'), ('Tôi', 'I'), ('TÔI', 'I'),
            ('các bạn', 'you'), ('Các bạn', 'You'), ('Các Bạn', 'You'), ('CÁC BẠN', 'YOU'), ('bạn', 'you'), ('Bạn', 'You'), ('BẠN', 'YOU'),
            ('anh ta', 'he'), ('Anh ta', 'He'), ('Anh Ta', 'He'), ('ANH TA', 'HE'), ('anh ấy', 'he'), ('Anh ấy', 'He'), ('Anh Ấy', 'He'), ('ANH ẤY', 'HE'), ('anh', 'he'), ('Anh', 'He'), ('ANH', 'HE'),
            ('ông ta', 'he'), ('Ông ta', 'He'), ('Ông Ta', 'He'), ('ÔNG TA', 'HE'), ('ông ấy', 'he'), ('Ông ấy', 'He'), ('Ông Ấy', 'He'), ('ÔNG ẤY', 'HE'), ('ông', 'he'), ('Ông', 'He'), ('ÔNG', 'HE'),
            ('chị ta', 'she'), ('Chị ta', 'She'), ('Chị Ta', 'She'), ('CHỊ TA', 'SHE'), ('chị ấy', 'she'), ('Chị ấy', 'She'), ('Chị Ấy', 'She'), ('CHỊ ẤY', 'SHE'), ('chị', 'she'), ('Chị', 'She'), ('CHỊ', 'SHE'),
            ('cô ấy', 'she'), ('Cô ấy', 'She'), ('Cô Ấy', 'She'), ('CÔ ẤY', 'SHE'), ('cô ta', 'she'), ('Cô ta', 'She'), ('Cô Ta', 'She'), ('CÔ TA', 'SHE'), ('cô', 'she'), ('Cô', 'She'), ('CÔ', 'SHE'),
            ('bà ấy', 'she'), ('Bà ấy', 'She'), ('Bà Ấy', 'She'), ('BÀ ẤY', 'SHE'), ('bà ta', 'she'), ('Bà ta', 'She'), ('Bà Ta', 'She'), ('BÀ TA', 'SHE'), ('bà', 'she'), ('Bà', 'She'), ('BÀ', 'SHE'),
            ('chúng ta', 'we'), ('Chúng ta', 'We'), ('Chúng Ta', 'We'), ('CHÚNG TA', 'WE'), ('chúng tôi', 'we'), ('Chúng tôi', 'We'), ('Chúng Tôi', 'We'), ('CHÚNG TÔI', 'WE'),
            ('bọn họ', 'they'), ('Bọn họ', 'They'), ('Bọn Họ', 'They'), ('BỌN HỌ', 'THEY'), ('họ', 'they'), ('Họ', 'They'), ('HỌ', 'THEY'),
            ('bọn chúng', 'they'), ('Bọn chúng', 'They'), ('Bọn Chúng', 'They'), ('BỌN CHÚNG', 'THEY'), ('chúng', 'they'), ('Chúng', 'They'), ('CHÚNG', 'THEY')]

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
        #Lấy câu gần đúng ngắn nhất về lọc phần thừa xem có khả năng cho kết quả không
        sqlResult = self.db.get_like_eng_thread(key, self.cursor)
        if sqlResult is not None:
            #Lọc phần thừa đầu - cuối chuỗi eng
            if key == sqlResult[1]:
                return sqlResult[2]
            engBeginExcess = re.findall(f'^([\S\s]*){re.escape(key)}([\S\s]*)$', sqlResult[1])
            if engBeginExcess:
                engBeginTrash = engBeginExcess[0][0]
                #Lọc rác đầu chuỗi vie
                vieBeginExcess = re.findall(f"^([{self.patternTrash}\s0-9]*)([\S\s]+)$", sqlResult[2])
                vieBeginTrash = vieBeginExcess[0][0]
                #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                if engBeginTrash.strip() == vieBeginTrash.strip():
                    vieRemaining = vieBeginExcess[0][1]
                    #Lọc rác cuối chuỗi vie
                    vieEndExcess = re.findall(f"^([{self.patternTrash}\s0-9]*)([\S\s]+)$", vieRemaining[::-1])
                    vieEndTrash = vieEndExcess[0][0]
                    engEndTrash = engBeginExcess[0][1]
                    if engEndTrash.strip() == vieEndTrash[::-1].strip():
                        vieEndRemaining = vieEndExcess[0][1]
                        return vieEndRemaining[::-1]
            else:
                #Tìm chính xác chữ hoa/thường
                sqlLowercase = self.db.get_glob_eng_thread(key, self.cursor)
                if sqlLowercase is not None:
                    #Lọc phần thừa đầu - cuối chuỗi eng
                    engBeginExcess = re.findall(f'^([\S\s]*){re.escape(key)}([\S\s]*)$', sqlLowercase[1])
                    if engBeginExcess:
                        engBeginTrash = engBeginExcess[0][0]
                        #Lọc rác đầu chuỗi vie
                        vieBeginExcess = re.findall(f"^([{self.patternTrash}\s0-9]*)([\S\s]+)$", sqlLowercase[2])
                        vieBeginTrash = vieBeginExcess[0][0]
                        #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                        if engBeginTrash.strip() == vieBeginTrash.strip():
                            vieRemaining = vieBeginExcess[0][1]
                            #Lọc rác cuối chuỗi vie
                            vieEndExcess = re.findall(f"^([{self.patternTrash}\s0-9]*)([\S\s]+)$", vieRemaining[::-1])
                            vieEndTrash = vieEndExcess[0][0]
                            engEndTrash = engBeginExcess[0][1]
                            if engEndTrash.strip() == vieEndTrash[::-1].strip():
                                vieEndRemaining = vieEndExcess[0][1]
                                return vieEndRemaining[::-1]
                #Không tìm thấy chính xác hoặc ở trên không xử lý được
                engBeginExcess = re.findall(f'^([\S\s]*){re.escape(key)}([\S\s]*)$', sqlResult[1].lower())
                if engBeginExcess:
                    engBeginTrash = engBeginExcess[0][0]
                    #Lọc rác đầu chuỗi vie
                    vieBeginExcess = re.findall(f"^([{self.patternTrash}\s0-9]*)([\S\s]+)$", sqlResult[2])
                    vieBeginTrash = vieBeginExcess[0][0]
                    #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                    if engBeginTrash.strip() == vieBeginTrash.strip():
                        vieRemaining = vieBeginExcess[0][1]
                        #Lọc rác cuối chuỗi vie
                        vieEndExcess = re.findall(f"^([{self.patternTrash}\s0-9]*)([\S\s]+)$", vieRemaining[::-1])
                        vieEndTrash = vieEndExcess[0][0]
                        engEndTrash = engBeginExcess[0][1]
                        if engEndTrash.strip() == vieEndTrash[::-1].strip():
                            vieEndRemaining = vieEndExcess[0][1]
                            return vieEndRemaining[::-1]
        #Tìm đại từ nhân xưng có trong câu gần đúng và thay thế đại từ nhân xưng thích hợp
        for proEN in self.pronounEN:
            #Tìm đầu câu với khoản trắng
            pronounResult = re.findall(f'^{re.escape(proEN[0])} ([\S\s]+)$', key)
            if pronounResult:
                #Tìm trong csdl xem có kết quả tương ứng không? Ví dụ: I cry
                sqlResult = self.db.get_like_front_eng_thread(f' {pronounResult[0]}', self.cursor)
                if sqlResult is not None:
                    #Kiểm tra xem câu thuộc dạng: đại từ nhân xưng + pronounResult[0]
                    checkPronoun = re.findall(f'^([\S\s]+) {re.escape(pronounResult[0])}$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0].strip()
                        for pro in self.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng phía trước câu sql trả về
                            for proVN in self.pronounVN:
                                proResult = re.findall(f'^{re.escape(proVN[0])} ([\S\s]+)$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return f'{proEN[1]} {proResult[0]}'
            #Tìm đầu câu với ký tự ' (ký tự ’ khá hiếm nên tạm thời bỏ qua, tốt nhất khi thêm dữ liệu lọc bỏ nó)
            pronounResult = re.findall(f'^{re.escape(proEN[0])}\'([\S\s]+)$', key)
            if pronounResult:
                #Tìm trong csdl xem có kết quả tương ứng không? Ví dụ: I'll cry
                sqlResult = self.db.get_like_front_eng_thread(f'\'{pronounResult[0]}', self.cursor)
                if sqlResult is not None:
                    #Kiểm tra xem câu thuộc dạng: đại từ nhân xưng + pronounResult[0]
                    checkPronoun = re.findall(f'^([\S\s]+)\'{re.escape(pronounResult[0])}$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0].strip()
                        for pro in self.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng phía trước câu sql trả về
                            for proVN in self.pronounVN:
                                proResult = re.findall(f'^{re.escape(proVN[0])} ([\S\s]+)$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return f'{proEN[1]} {proResult[0]}'
            #Tìm giữa câu với khoản trắng
            pronounResult = re.findall(f'^([\S\s]+) {re.escape(proEN[0])} ([\S\s]+)$', key)
            if pronounResult:
                sqlResult = self.db.get_like_middle_eng_thread(f'{pronounResult[0][0]} ', f' {pronounResult[0][1]}', self.cursor)
                if sqlResult is not None:
                    #Kiểm tra câu trả về thuộc dạng pronounResult[0] + đại từ nhân xưng + pronounResult[1] + ký tự đặt biệt
                    checkPronoun = re.findall(f'^{re.escape(pronounResult[0][0])} ([\S\s]+) {re.escape(pronounResult[0][1])}([\S\s]*)$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0][0].strip()
                        for pro in self.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng ở giữa câu trả về
                            for proVN in self.pronounVN:
                                proResult = re.findall(f'^([\S\s]*) {re.escape(proVN[0])} ([\S\s]*){checkPronoun[0][1]}$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return f'{proResult[0][0]} {proEN[1]} {proResult[0][1]}'
            #Tìm giữa câu với ký tự '
            pronounResult = re.findall(f'^([\S\s]+) {re.escape(proEN[0])}\'([\S\s]+)$', key)
            if pronounResult:
                sqlResult = self.db.get_like_middle_eng_thread(f'{pronounResult[0][0]} ', f'\'{pronounResult[0][1]}', self.cursor)
                if sqlResult is not None:
                    #Kiểm tra câu trả về thuộc dạng pronounResult[0] + đại từ nhân xưng + pronounResult[1] + ký tự đặt biệt
                    checkPronoun = re.findall(f'^{re.escape(pronounResult[0][0])} ([\S\s]+)\'{re.escape(pronounResult[0][1])}([\S\s]*)$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0][0].strip()
                        for pro in self.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng ở giữa câu trả về
                            for proVN in self.pronounVN:
                                proResult = re.findall(f'^([\S\s]*) {re.escape(proVN[0])} ([\S\s]*){checkPronoun[0][1]}$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return f'{proResult[0][0]} {proEN[1]} {proResult[0][1]}'
            #Tìm cuối câu với rác ở cuối (Rất khó tìm được vì có thể ra kết quả ngắn nhất Ví dụ: It's H)
            pronounResult = re.findall(f'^([\S\s]+) {re.escape(proEN[0])}([{self.patternTrash}\s0-9]*)$', key)
            if pronounResult:
                #Tìm trong csdl xem có kết quả tương ứng không? Ví dụ: It's you
                sqlResult = self.db.get_like_rear_eng_thread(f'{pronounResult[0][0]} ', self.cursor)
                if sqlResult is not None:
                    #Lọc đại từ nhân xưng phía sau câu sql trả về
                    for proVN in self.pronounVN:
                        proResult = re.findall(f'^([\S\s]+) {re.escape(proVN[0])}[{self.patternTrash}\s0-9]*$', sqlResult[2])
                        if proResult:
                            #Thay thế đại từ nhân xưng tương ứng
                            if proEN[0] != proVN[1]:
                                return f'{proResult[0]} {proEN[1]}{pronounResult[0][1]}'
        #Chia nhỏ câu theo cặp ký tự thoát
        for row in self.escChar:
            strResult = re.findall(f"[\s]*{re.escape(row[0])}[^{re.escape(row[1])}]+{re.escape(row[1])}[\s]*", key)
            if strResult:
                strSplit = key.split(strResult[0])
                for i in range(len(strSplit)):
                    strSplit[i] = self.trans_try(strSplit[i])
                return strResult[0].join(strSplit)
        #Lọc rác đầu chuỗi + khoản trắng + số
        strResult = re.findall(f"^([{self.patternTrash}\s0-9]+)([\S\s]*)$", key)
        if len(strResult) > 0:
            return strResult[0][0] + self.trans_try(strResult[0][1])
        #Lọc rác cuối chuỗi + khoản trắng + số
        strResult = re.findall(f"^([{self.patternTrash}\s0-9]+)([\S\s]*)$", key[::-1])
        if len(strResult) > 0:
            strTrash = strResult[0][0]
            strEnd = strResult[0][1]
            return self.trans_try(strEnd[::-1]) + strTrash[::-1]
        #Chia nhỏ câu với hy vọng dịch từng đoạn có thể dịch
        for delimiter in self.delimiterSplit:
            strSplit = key.split(delimiter)
            if len(strSplit) > 1:
                for i in range(len(strSplit)):
                    strSplit[i] = self.trans_try(strSplit[i])
                return delimiter.join(strSplit)
        #Chi nhỏ câu theo rác
        trashResult = re.findall(f"[\s]*[{self.patternTrash}]+[\s]*", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = self.trans_try(strSplit[i])
            return trashResult[0].join(strSplit)
        #Chia nhỏ câu theo từ khóa câu
        for keyword in self.keywords:
            #Từ khóa ở giữa chia câu thành 2 phần
            keywordResult = re.findall(f'^([\S\s]*) {re.escape(keyword[0])} ([\S\s]*)$', key)
            if keywordResult:
                return f'{self.trans_try(keywordResult[0][0])} {keyword[1]} {self.trans_try(keywordResult[0][1])}'
            #Từ khóa ở đầu câu
            keywordResult = re.findall(f'^{re.escape(keyword[0])} ([\S\s]+)$', key)
            if keywordResult:
                return f'{keyword[1]} {self.trans_try(keywordResult[0])}'
            #Từ khóa ở cuối câu
            keywordResult = re.findall(f'^([\S\s]+) {re.escape(keyword[0])}$', key)
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