'''EngToVieTrans.py
Chuyên sử dụng để chuyển ngữ
Đầu vào:
    db: database
    tryTrans: cố dịch
    escChar : danh sách cặp ký tự cần bỏ qua
'''
import re

class EngToVieTrans():
    '''Bộ đệm động listCahceTrans với hy vọng giảm tần xuất truy xuất csdl và tính toán dịch
    Định dạng dict{eng : dict{escChar :(vie, trans, update)}}
        eng: string câu tiếng Anh
        trans: boolean - Xác định khóa đã dịch hay chưa
            True - Nguyên bản
            False - Đã dịch
        vie: string câu dịch
        escChar: string danh sách cặp ký tự cần bỏ qua
        update: boolean xác định có cần cập nhật lại csdl hay không
            True - Nguyên bản
            False - Đã chỉnh sửa hoặc câu mới
    '''
    listCahceTrans = {}
    #Định nghĩa từ khóa có thể cắt nhỏ câu hy vọng dịch từng phần
    keywords = [
        ('but maybe', 'nhưng có lẽ'), ('But maybe', 'Nhưng có lẽ'), ('But Maybe', 'Nhưng có lẽ'), ('BUT MAYBE', 'NHƯNG CÓ LẼ'),
        ('but even if', 'nhưng ngay cả khi'), ('But even if', 'Nhưng ngay cả khi'), ('But Even If', 'Nhưng ngay cả khi'), ('BUT EVEN IF', 'NHƯNG NGAY CẢ KHI'),
        ('but', 'nhưng'), ('But', 'Nhưng'), ('BUT', 'NHƯNG'),
        ('maybe', 'có lẽ là'), ('Maybe', 'Có lẽ là'), ('MAYBE', 'CÓ LẼ LÀ'),
        ('because of', 'vì'), ('Because of', 'Vì'), ('Because Of', 'Vì'),('BECAUSE OF', 'VÌ'),
        ('because', 'bởi vì'), ('Because', 'Bởi vì'), ('BECAUSE', 'BỞI VÌ'),
        ('such as', 'chẳng hạn như'), ('Such as', 'Chẳng hạn như'), ('Such As', 'Chẳng hạn như'), ('SUCH AS', 'CHẲNG HẠN NHƯ'),
        ('as if ', 'như thể'), ('As if', 'Như thể'), ('As If', 'Như thể'), ('AS IF', 'NHƯ THỂ'),
        ('of course', 'tất nhiên'), ('Of course', 'Tất nhiên'), ('Of Course', 'Tất nhiên'), ('OF COURSE', 'TẤT NHIÊN'),
        ('so that', 'vậy nên'), ('So that', 'Vậy nên'), ('So That', 'Vậy nên'), ('SO THAT', 'VẬY NÊN'),
        ('for that', 'vì điều đó'), ('For that', 'Vì điều đó'), ('For That', 'Vì điều đó'), ('FOR THAT', 'VÌ ĐIỀU ĐÓ'),
        ('as if', 'như thể'), ('As if', 'Như thể'), ('As If', 'Như thể'), ('AS IF', 'NHƯ THỂ'),
        ('if', 'nếu'), ('If', 'Nếu'), ('IF', 'NẾU'),
        ('and', 'và'), ('And', 'Và'), ('AND', 'VÀ'),
        ('or', 'hoặc'), ('Or', 'Hoặc'), ('OR', 'HOẶC'),
        ('as long as', 'miễn là'), ('As long as', 'Miễn là'), ('AS LONG AS', 'MIỄN LÀ'),
        ('until now', 'cho đến bây giờ'), ('Until now', 'Cho đến bây giờ'), ('Until Now', 'Cho đến bây giờ'), ('UNTIL NOW', 'CHO ĐẾN BÂY GIỜ'),
        ('until', 'cho đến khi'), ('Until', 'Cho đến khi'), ('UNTIL', 'CHO ĐẾN KHI'),
        ('so', 'vậy'), ('So', 'Vậy'), ('SO', 'VẬY'),
        ('ever since', 'kể từ đó'), ('Ever since', 'Kể từ đó'), ('Ever Since', 'Kể từ đó'), ('EVER SINCE', 'KỂ TỪ ĐÓ'),
        ('since', 'kể từ khi'), ('Since', 'Kể từ khi'), ('SINCE', 'KỂ TỪ KHI'),
        ('perhaps', 'có lẽ'), ('Perhaps', 'Có lẽ'), ('PERHAPS', 'CÓ LẼ'),
        ('otherwise', 'nếu không thì'), ('Otherwise', 'Nếu không thì'), ('OTHERWISE', 'NẾU KHÔNG THÌ'),
        ('before', 'trước khi'), ('Before', 'Trước khi'), ('BEFORE', 'TRƯỚC KHI'),
        ('then', 'sau đó,'), ('Then', 'Sau đó,'), ('THEN', 'SAU ĐÓ,')]
    #Định nghĩa dấu xuống dòng
    newline = ['\n', '\\n']
    #Định nghĩa dấu phân cách
    delimiterSplit = ['.', '?', '!', '…', ':', ';', ',']
    #Định nghĩa ký tự rác trong câu
    patternTrash = re.escape('\\`~!@#$^&*()_—+={[}]\|:;"<,>.?/“”…¢₳฿₵₢₯€₠ƒ₣₴₭₤₥₱₰£﷼৳૱௹〒₮₩¥')
    #Định nghĩa ký tự dấu trong câu
    patternSign = re.escape('-\'%‘’')
    #Định nghĩa đại từ nhân xưng tiếng Anh
    pronounEN = [('I', 'Tôi'),
        ('you', 'bạn'), ('You', 'Bạn'), ('YOU', 'BẠN'),
        ('he', 'anh ấy'), ('He', 'Anh ấy'), ('HE', 'ANH ẤY'),
        ('she', 'cô ấy'), ('She', 'Cô ấy'), ('SHE', 'CÔ ẤY'),
        ('we', 'chúng ta'), ('We', 'Chúng ta'), ('WE', 'CHÚNG TA'),
        ('they', 'họ'), ('They', 'Họ'), ('THEY', 'HỌ')]
    #Định nghĩa đại từ nhân xưng tiếng Việt
    pronounVN = [('tôi', 'I'), ('Tôi', 'I'), ('TÔI', 'I'),
        ('các bạn', 'you'), ('Các bạn', 'You'), ('Các Bạn', 'You'), ('CÁC BẠN', 'YOU'), ('bạn', 'you'), ('Bạn', 'You'), ('BẠN', 'YOU'),
        ('anh ta', 'he'), ('Anh ta', 'He'), ('Anh Ta', 'He'), ('ANH TA', 'HE'), ('anh ấy', 'he'), ('Anh ấy', 'He'), ('Anh Ấy', 'He'), ('ANH ẤY', 'HE'), ('anh', 'he'), ('Anh', 'He'), ('ANH', 'HE'),
        ('ông ta', 'he'), ('Ông ta', 'He'), ('Ông Ta', 'He'), ('ÔNG TA', 'HE'), ('ông ấy', 'he'), ('Ông ấy', 'He'), ('Ông Ấy', 'He'), ('ÔNG ẤY', 'HE'), ('ông', 'he'), ('Ông', 'He'), ('ÔNG', 'HE'),
        ('chị ta', 'she'), ('Chị ta', 'She'), ('Chị Ta', 'She'), ('CHỊ TA', 'SHE'), ('chị ấy', 'she'), ('Chị ấy', 'She'), ('Chị Ấy', 'She'), ('CHỊ ẤY', 'SHE'), ('chị', 'she'), ('Chị', 'She'), ('CHỊ', 'SHE'),
        ('cô ấy', 'she'), ('Cô ấy', 'She'), ('Cô Ấy', 'She'), ('CÔ ẤY', 'SHE'), ('cô ta', 'she'), ('Cô ta', 'She'), ('Cô Ta', 'She'), ('CÔ TA', 'SHE'), ('cô', 'she'), ('Cô', 'She'), ('CÔ', 'SHE'),
        ('bà ấy', 'she'), ('Bà ấy', 'She'), ('Bà Ấy', 'She'), ('BÀ ẤY', 'SHE'), ('bà ta', 'she'), ('Bà ta', 'She'), ('Bà Ta', 'She'), ('BÀ TA', 'SHE'), ('bà', 'she'), ('Bà', 'She'), ('BÀ', 'SHE'),
        ('chúng ta', 'we'), ('Chúng ta', 'We'), ('Chúng Ta', 'We'), ('CHÚNG TA', 'WE'), ('chúng tôi', 'we'), ('Chúng tôi', 'We'), ('Chúng Tôi', 'We'), ('CHÚNG TÔI', 'WE'),
        ('bọn họ', 'they'), ('Bọn họ', 'They'), ('Bọn Họ', 'They'), ('BỌN HỌ', 'THEY'), ('họ', 'they'), ('Họ', 'They'), ('HỌ', 'THEY'),
        ('bọn chúng', 'they'), ('Bọn chúng', 'They'), ('Bọn Chúng', 'They'), ('BỌN CHÚNG', 'THEY'), ('chúng', 'they'), ('Chúng', 'They'), ('CHÚNG', 'THEY')]

    def __init__(cls, parent, cursor, escChar):
        db = parent.get_database()
        cls.dbRoot = db.get_db_root()
        cls.dbCache = db.get_db_cache()
        cls.cursor = cursor
        cls.escChar = []
        cls.strEscChar = ''
        cls.set_escChar(escChar)

    #Nhập vie
    def set_vie(cls, vie):
        cls.vie = vie

    #Lấy vie
    def get_vie(cls):
        return cls.vie

    #Trả về list
    def get_escchar(cls):
        return cls.escChar

    #Trả về string
    def get_key_escchar(cls):
        return cls.strEscChar

    def set_escChar(cls, escChar):
        if escChar != cls.strEscChar:
            cls.escChar = cls.cover_escchar_to_list(escChar)
            cls.strEscChar = cls.cover_escchar_to_string(cls.escChar)

    '''Chuyển đổi escChar chuỗi sang list[]
    @đầu vào:
        escChar: string
    @trả về: list
    '''
    @staticmethod
    def cover_escchar_to_list(escChar):
        result = []
        listChar = escChar.split(',')
        for row in listChar:
            char2 = row.strip()
            if len(char2) == 2:
                result.append((char2[0], char2[1]))
        return result

    '''Chuyển đổi escChar list sang chuỗi
    @đầu vào:
        escChar: list
    @trả về: string
    '''
    @staticmethod
    def cover_escchar_to_string(escChar):
        result = []
        for row in escChar:
            result.append(f'{row[0]}{row[1]}')
        result.sort()
        return ','.join(result)

    #Lọc rác đầu chuỗi
    @staticmethod
    def filter_trash_first(key):
        vieBeginExcess = re.findall(f"^([{EngToVieTrans.patternTrash}{EngToVieTrans.patternSign}\s0-9]*)([\S\s]+)$", key)
        trash = vieBeginExcess[0][0]
        text = vieBeginExcess[0][1]
        result = (trash, text)
        return result

    #Lọc rác cuối chuỗi
    @staticmethod
    def filter_trash_last(key):
        vieEndExcess = re.findall(f"^([{EngToVieTrans.patternTrash}{EngToVieTrans.patternSign}\s0-9]*)([\S\s]+)$", key[::-1])
        trash = vieEndExcess[0][0]
        text = vieEndExcess[0][1]
        result = (text[::-1], trash[::-1])
        return result

    #Lọc rác đầu cuối
    @staticmethod
    def filter_trash(key):
        temp1 = EngToVieTrans.filter_trash_first(key)
        temp2 = EngToVieTrans.filter_trash_last(temp1[1])
        result = (temp1[0], temp2[0], temp2[1])
        return result

    def save_to_db(cls, eng, vie):
        if cls.get_key_escchar() == '':
            cls.dbCache.save_cache_thread(eng, vie, '', cls.cursor)
            return
        '''Kiểm tra chuỗi có strEscChar tương ứng không
        (Có khi chuỗi ít strEscChar hơn strEscChar nhập vào, thậm chí không có)
        '''
        listEscCharChild = []
        for row in cls.get_escchar():
            strResult = re.findall(f"[\s]*{re.escape(row[0])}[^{re.escape(row[1])}]+{re.escape(row[1])}[\s]*", eng)
            if strResult:
                listEscCharChild.append(f'{row[0]}{row[1]}')
        listEscCharChild.sort()
        strEscCharChild = ','.join(listEscCharChild)
        cls.dbCache.save_cache_thread(eng, vie, strEscCharChild, cls.cursor)

    #Tạo bộ đệm động (đã qua xử lý)
    def set_cache(cls, eng, vie, trans = False, update = False):
        #Lưu dữ liệu xuống csdl (Cập nhật kết quả đã xử lý)
        if trans == False and update == False:
            cls.save_to_db(eng, vie)
        rowkey = cls.listCahceTrans.get(eng)
        if rowkey is None:
            rowkey = {cls.strEscChar : (vie, trans, update)}
            cls.listCahceTrans[eng] = rowkey
            return vie
        rowstrEscChar = rowkey.get(cls.strEscChar)
        if rowstrEscChar is None:
            rowkey[cls.strEscChar] = (vie, trans, update)
            cls.listCahceTrans[eng] = rowkey
            return vie
        '''Cập nhật lại dữ liệu nếu dữ liệu đã có chưa được dịch (trans = False)
        - Trường hợp câu đó trước đó chưa được dịch (trans = True)
        - Hoặc lỗi gì đó liên quan đến truy xuất cache
        '''
        if rowstrEscChar[1] and trans == False:
            rowkey[cls.strEscChar] = (vie, trans, update)
            cls.listCahceTrans[eng] = rowkey
        return rowstrEscChar[0]

    #Tải bộ đệm động
    def get_cache(cls, eng):
        #Lấy cache lưu trong bộ nhớ
        rowkey = cls.listCahceTrans.get(eng)
        if rowkey is None:
            #Tải cache từ cơ sở dữ liệu cache
            cache_sent = cls.dbCache.get_cache_thread(eng, cls.cursor)
            if len(cache_sent) == 0:
                return ''
            #Chuyển đổi cho đúng định dạng {escChar: list(vie, trans, update)}
            rowkey = {}
            for row in cache_sent:
                rowkey[row[1]] = (row[0], False, True)
            #Cập nhật bộ đệm động
            cls.listCahceTrans[eng] = rowkey
        rowstrEscChar = rowkey.get(cls.strEscChar)
        if rowstrEscChar is None:
            '''Xử lý tìm giá trị có thể thích hợp
            Lọc escChar có trong chuỗi và tìm kết quả lần nữa nếu có
            (Có khi chuỗi ít escChar hơn escChar nhập vào, thậm chí không có)
            '''
            listEscChar = []
            for row in cls.escChar:
                strResult = re.findall(f"[\s]*{re.escape(row[0])}[^{re.escape(row[1])}]+{re.escape(row[1])}[\s]*", eng)
                if strResult:
                    listEscChar.append(f'{row[0]}{row[1]}')
            listEscChar.sort()
            strEscChar = ','.join(listEscChar)
            rowstrEscChar = rowkey.get(strEscChar)
            if rowstrEscChar is None:
                return ''
            #Thêm dữ liệu phụ để truy xuất nhanh hơn
            cls.set_cache(eng, rowstrEscChar[0], False, True)
        return rowstrEscChar[0]

    #Lưu xuống csdl
    @staticmethod
    def save_cache_to_database(dbCache):
        #Tạm thời xóa chức năng này
        pass

    #Xóa bộ đệm cũ lập bộ đệm mới
    @staticmethod
    def reset_list_cahce_trans():
        EngToVieTrans.listCahceTrans = {}

    #Dịch bình thường (có sẵn trong csdl và bộ đệm)
    def trans_normal(cls, key):
        if len(key) < 2:
            return key
        transCache = cls.get_cache(key)
        if transCache != '':
            return transCache
        #Lấy câu chính xác
        sqlResult = cls.dbRoot.get_eng_thread(key, cls.cursor)
        if sqlResult is not None:
            return cls.set_cache(key, sqlResult[2])
        return key #Tránh trường lợp trans_try sử dụng

    #Cố dịch (đệ quy)
    def trans_try(cls, key):
        if len(key) < 2:
            return key
        transCache = cls.get_cache(key)
        if transCache != '':
            return transCache
        #Chia nhỏ theo ký tự sang dòng mới '\n'
        for newline in cls.newline:
            strSplit = key.split(newline)
            if len(strSplit) > 1:
                for i in range(len(strSplit)):
                    strSplit[i] = cls.trans_try(strSplit[i])
                return cls.set_cache(key, newline.join(strSplit))
        #Lấy câu gần đúng ngắn nhất về lọc phần thừa xem có khả năng cho kết quả không
        sqlResult = cls.dbRoot.get_like_eng_thread(key, cls.cursor)
        if sqlResult is not None:
            #Kết quả chính xác
            if key == sqlResult[1]:
                return cls.set_cache(key, sqlResult[2])
            #Lọc phần thừa đầu - cuối chuỗi eng
            engBeginExcess = re.findall(f'^([\S\s]*){re.escape(key)}([\S\s]*)$', sqlResult[1])
            if engBeginExcess:
                engBeginTrash = engBeginExcess[0][0]
                #Lọc rác đầu chuỗi vie
                vieBeginExcess = cls.filter_trash_first(sqlResult[2])
                #vieBeginExcess = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]*)([\S\s]+)$", sqlResult[2])
                vieBeginTrash = vieBeginExcess[0]
                #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                if engBeginTrash.strip() == vieBeginTrash.strip():
                    vieRemaining = vieBeginExcess[1]
                    #Lọc rác cuối chuỗi vie
                    vieEndExcess = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]*)([\S\s]+)$", vieRemaining[::-1])
                    vieEndTrash = vieEndExcess[0][0]
                    engEndTrash = engBeginExcess[0][1]
                    if engEndTrash.strip() == vieEndTrash[::-1].strip():
                        vieEndRemaining = vieEndExcess[0][1]
                        return cls.set_cache(key, vieEndRemaining[::-1])
            else:
                #Tìm chính xác chữ hoa/thường
                sqlLowercase = cls.dbRoot.get_glob_eng_thread(key, cls.cursor)
                if sqlLowercase is not None:
                    #Lọc phần thừa đầu - cuối chuỗi eng
                    engBeginExcess = re.findall(f'^([\S\s]*){re.escape(key)}([\S\s]*)$', sqlLowercase[1])
                    if engBeginExcess:
                        engBeginTrash = engBeginExcess[0][0]
                        #Lọc rác đầu chuỗi vie
                        vieBeginExcess = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]*)([\S\s]+)$", sqlLowercase[2])
                        vieBeginTrash = vieBeginExcess[0][0]
                        #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                        if engBeginTrash.strip() == vieBeginTrash.strip():
                            vieRemaining = vieBeginExcess[0][1]
                            #Lọc rác cuối chuỗi vie
                            vieEndExcess = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]*)([\S\s]+)$", vieRemaining[::-1])
                            vieEndTrash = vieEndExcess[0][0]
                            engEndTrash = engBeginExcess[0][1]
                            if engEndTrash.strip() == vieEndTrash[::-1].strip():
                                vieEndRemaining = vieEndExcess[0][1]
                                return cls.set_cache(key, vieEndRemaining[::-1])
                #Không tìm thấy chính xác hoặc ở trên không xử lý được
                engBeginExcess = re.findall(f'^([\S\s]*){re.escape(key)}([\S\s]*)$', sqlResult[1].lower())
                if engBeginExcess:
                    engBeginTrash = engBeginExcess[0][0]
                    #Lọc rác đầu chuỗi vie
                    vieBeginExcess = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]*)([\S\s]+)$", sqlResult[2])
                    vieBeginTrash = vieBeginExcess[0][0]
                    #Nếu phần thừa đầu chuỗi eng là rác đầu chuỗi vie
                    if engBeginTrash.strip() == vieBeginTrash.strip():
                        vieRemaining = vieBeginExcess[0][1]
                        #Lọc rác cuối chuỗi vie
                        vieEndExcess = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]*)([\S\s]+)$", vieRemaining[::-1])
                        vieEndTrash = vieEndExcess[0][0]
                        engEndTrash = engBeginExcess[0][1]
                        if engEndTrash.strip() == vieEndTrash[::-1].strip():
                            vieEndRemaining = vieEndExcess[0][1]
                            return cls.set_cache(key, vieEndRemaining[::-1])
        #Tìm đại từ nhân xưng có trong câu gần đúng và thay thế đại từ nhân xưng thích hợp
        for proEN in cls.pronounEN:
            #Tìm đầu câu với khoản trắng
            pronounResult = re.findall(f'^{re.escape(proEN[0])} ([\S\s]+)$', key)
            if pronounResult:
                #Tìm trong csdl xem có kết quả tương ứng không? Ví dụ: I cry
                sqlResult = cls.dbRoot.get_like_front_eng_thread(f' {pronounResult[0]}', cls.cursor)
                if sqlResult is not None:
                    #Kiểm tra xem câu thuộc dạng: đại từ nhân xưng + pronounResult[0]
                    checkPronoun = re.findall(f'^([\S\s]+) {re.escape(pronounResult[0])}$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0].strip()
                        for pro in cls.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng phía trước câu sql trả về
                            for proVN in cls.pronounVN:
                                proResult = re.findall(f'^{re.escape(proVN[0])} ([\S\s]+)$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return cls.set_cache(key, f'{proEN[1]} {proResult[0]}')
            #Tìm đầu câu với ký tự ' (ký tự ’ khá hiếm nên tạm thời bỏ qua, tốt nhất khi thêm dữ liệu lọc bỏ nó)
            pronounResult = re.findall(f'^{re.escape(proEN[0])}\'([\S\s]+)$', key)
            if pronounResult:
                #Tìm trong csdl xem có kết quả tương ứng không? Ví dụ: I'll cry
                sqlResult = cls.dbRoot.get_like_front_eng_thread(f'\'{pronounResult[0]}', cls.cursor)
                if sqlResult is not None:
                    #Kiểm tra xem câu thuộc dạng: đại từ nhân xưng + pronounResult[0]
                    checkPronoun = re.findall(f'^([\S\s]+)\'{re.escape(pronounResult[0])}$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0].strip()
                        for pro in cls.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng phía trước câu sql trả về
                            for proVN in cls.pronounVN:
                                proResult = re.findall(f'^{re.escape(proVN[0])} ([\S\s]+)$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return cls.set_cache(key, f'{proEN[1]} {proResult[0]}')
            #Tìm giữa câu với khoản trắng
            pronounResult = re.findall(f'^([\S\s]+) {re.escape(proEN[0])} ([\S\s]+)$', key)
            if pronounResult:
                sqlResult = cls.dbRoot.get_like_middle_eng_thread(f'{pronounResult[0][0]} ', f' {pronounResult[0][1]}', cls.cursor)
                if sqlResult is not None:
                    #Kiểm tra câu trả về thuộc dạng pronounResult[0][0] + đại từ nhân xưng + pronounResult[0][1] + ký tự đặt biệt
                    checkPronoun = re.findall(f'^{re.escape(pronounResult[0][0])} ([\S\s]+) {re.escape(pronounResult[0][1])}([\S\s]*)$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0][0].strip()
                        for pro in cls.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng ở giữa câu trả về
                            for proVN in cls.pronounVN:
                                proResult = re.findall(f'^([\S\s]*) {re.escape(proVN[0])} ([\S\s]*){re.escape(checkPronoun[0][1])}$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return cls.set_cache(key, f'{proResult[0][0]} {proEN[1]} {proResult[0][1]}')
            #Tìm giữa câu với ký tự '
            pronounResult = re.findall(f'^([\S\s]+) {re.escape(proEN[0])}\'([\S\s]+)$', key)
            if pronounResult:
                sqlResult = cls.dbRoot.get_like_middle_eng_thread(f'{pronounResult[0][0]} ', f'\'{pronounResult[0][1]}', cls.cursor)
                if sqlResult is not None:
                    #Kiểm tra câu trả về thuộc dạng pronounResult[0] + đại từ nhân xưng + pronounResult[1] + ký tự đặt biệt
                    checkPronoun = re.findall(f'^{re.escape(pronounResult[0][0])} ([\S\s]+)\'{re.escape(pronounResult[0][1])}([\S\s]*)$', sqlResult[1])
                    if checkPronoun:
                        isPronoun = False
                        checkText = checkPronoun[0][0].strip()
                        for pro in cls.pronounEN:
                            if pro[0] == checkText:
                                isPronoun = True
                                break
                        if isPronoun:
                            #Lọc đại từ nhân xưng ở giữa câu trả về
                            for proVN in cls.pronounVN:
                                proResult = re.findall(f'^([\S\s]*) {re.escape(proVN[0])} ([\S\s]*){re.escape(checkPronoun[0][1])}$', sqlResult[2])
                                if proResult:
                                    #Thay thế đại từ nhân xưng tương ứng
                                    if checkText == proVN[1]:
                                        return cls.set_cache(key, f'{proResult[0][0]} {proEN[1]} {proResult[0][1]}')
            #Tìm cuối câu với rác ở cuối (Rất khó tìm được vì có thể ra kết quả ngắn nhất Ví dụ: It's H)
            pronounResult = re.findall(f'^([\S\s]+) {re.escape(proEN[0])}([{cls.patternTrash}{cls.patternSign}\s0-9]*)$', key)
            if pronounResult:
                #Tìm trong csdl xem có kết quả tương ứng không? Ví dụ: It's you
                sqlResult = cls.dbRoot.get_like_rear_eng_thread(f'{pronounResult[0][0]} ', cls.cursor)
                if sqlResult is not None:
                    #Lọc đại từ nhân xưng phía sau câu sql trả về
                    for proVN in cls.pronounVN:
                        proResult = re.findall(f'^([\S\s]+) {re.escape(proVN[0])}[{cls.patternTrash}{cls.patternSign}\s0-9]*$', sqlResult[2])
                        if proResult:
                            #Thay thế đại từ nhân xưng tương ứng
                            if proEN[0] != proVN[1]:
                                return cls.set_cache(key, f'{proResult[0]} {proEN[1]}{pronounResult[0][1]}')
        #Chia nhỏ câu theo cặp ký tự thoát
        for row in cls.escChar:
            strResult = re.findall(f"[\s]*{re.escape(row[0])}[^{re.escape(row[1])}]+{re.escape(row[1])}[\s]*", key)
            if strResult:
                strSplit = key.split(strResult[0])
                for i in range(len(strSplit)):
                    strSplit[i] = cls.trans_try(strSplit[i])
                return cls.set_cache(key, strResult[0].join(strSplit))
        #Chia nhỏ câu với hy vọng dịch từng đoạn có thể dịch
        for delimiter in cls.delimiterSplit:
            strSplit = key.split(delimiter)
            if len(strSplit) > 1:
                for i in range(len(strSplit)):
                    strSplit[i] = cls.trans_try(strSplit[i])
                return cls.set_cache(key, delimiter.join(strSplit))
        #Lọc rác đầu chuỗi + khoản trắng + số
        strResult = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]+)([\S\s]*)$", key)
        if len(strResult) > 0:
            return cls.set_cache(key, strResult[0][0] + cls.trans_try(strResult[0][1]))
        #Lọc rác cuối chuỗi + khoản trắng + số
        strResult = re.findall(f"^([{cls.patternTrash}{cls.patternSign}\s0-9]+)([\S\s]*)$", key[::-1])
        if len(strResult) > 0:
            strTrash = strResult[0][0]
            strEnd = strResult[0][1]
            return cls.set_cache(key, cls.trans_try(strEnd[::-1]) + strTrash[::-1])
        #Chi nhỏ câu theo rác để lại ký tự patternTrash
        trashResult = re.findall(f"[\s]*[{cls.patternTrash}]+[\s]*", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = cls.trans_try(strSplit[i])
            return cls.set_cache(key, trashResult[0].join(strSplit))
        #Chia nhỏ câu theo từ khóa câu
        for keyword in cls.keywords:
            #Từ khóa ở giữa chia câu thành 2 phần
            keywordResult = re.findall(f'^([\S\s]*) {re.escape(keyword[0])} ([\S\s]*)$', key)
            if keywordResult:
                return cls.set_cache(key, f'{cls.trans_try(keywordResult[0][0])} {keyword[1]} {cls.trans_try(keywordResult[0][1])}')
            #Từ khóa ở đầu câu
            keywordResult = re.findall(f'^{re.escape(keyword[0])} ([\S\s]+)$', key)
            if keywordResult:
                return cls.set_cache(key, f'{keyword[1]} {cls.trans_try(keywordResult[0])}')
            #Từ khóa ở cuối câu
            keywordResult = re.findall(f'^([\S\s]+) {re.escape(keyword[0])}$', key)
            if keywordResult:
                return cls.set_cache(key, f'{cls.trans_try(keywordResult[0])} {keyword[1]}')
        #Chi nhỏ câu theo ' - '
        trashResult = re.findall(f"[\s]+\-[\s]+", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = cls.trans_try(strSplit[i])
            return cls.set_cache(key, trashResult[0].join(strSplit))
        trashResult = re.findall(f"[\s]*\-[\-]+[\s]*", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = cls.trans_try(strSplit[i])
            return cls.set_cache(key, trashResult[0].join(strSplit))
        #Chi nhỏ câu theo ký patternSign
        trashResult = re.findall(f"[\s]*[{cls.patternSign}]+[\s]*", key)
        if trashResult:
            strSplit = key.split(trashResult[0])
            for i in range(len(strSplit)):
                strSplit[i] = cls.trans_try(strSplit[i])
            return cls.set_cache(key, trashResult[0].join(strSplit))
        return cls.set_cache(key, key, True)
