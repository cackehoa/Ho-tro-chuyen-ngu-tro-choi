'''AvorionFile.py
Đọc nội dung tập tin Po
Dành riêng cho trò chơi Avorion'''

import re
from .TypeFile import TypeFile

class AvorionFile(TypeFile):

    def __init__(self, fileName):
        super().__init__(fileName)

    '''Đọc nội dung tệp theo từng dòng
    Đầu ra:
        com : chuỗi chú thích
        msgid : chuỗi msgid
        other : chuỗi chưa xác định
    '''
    def read_all(self):
        result = []
        with open(self.get_file_name(), 'r', encoding = 'utf-8') as readFile:
            for line in readFile:
                text = line.strip()
                # Xác định kiểu dữ liệu ban đầu
                checkCom = re.findall('^#', text)
                if checkCom:
                    result.append(('com', text))
                    continue
                checkMsgid = re.findall('^msgid[\s]+\"([\s\S]*)\"[\s]*$', text)
                if checkMsgid:
                    result.append(('msgid', checkMsgid[0]))
                    continue
                # Bỏ qua biến msgstr (biến này sẽ được dịch)
                checkMsgstr = re.findall('^msgstr[\s]+\"([\s\S]*)\"[\s]*$', text)
                if checkMsgstr:
                    #result.append(('msgstr', checkMsgstr[0]))
                    continue
                result.append(('other', text))
        return result

    def write_data(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8') as fileWrite:
            for line in data:
                if line[0] == 'msgid':
                    fileWrite.write(f'msgid "{line[1]}"\n')
                    fileWrite.write(f'msgstr "{line[2]}"\n')
                else:
                    fileWrite.write(f'{line[1]}\n')