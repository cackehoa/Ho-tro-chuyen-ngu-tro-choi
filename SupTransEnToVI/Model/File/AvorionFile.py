'''AvorionFile.py
Đọc nội dung tập tin Po
Dành riêng cho trò chơi Avorion'''

import re
from .TypeFile import TypeFile

class AvorionFile(TypeFile):

    def __init__(self, fileName, controller):
        super().__init__(fileName)
        self.controller = controller

    '''Đọc nội dung tệp theo từng dòng
    Đầu ra:
        com : chuỗi chú thích
        msgid : chuỗi msgid
        other : chuỗi chưa xác định
    '''
    def read_all(self):
        result = []
        with open(self.get_file_name(), 'r', encoding = 'utf-8') as readFile:
            listMsgid = []
            beginMsgid = False
            for line in readFile:
                text = self.controller.filter_whitespace(line)
                # Xác định kiểu dữ liệu ban đầu
                checkCom = re.findall('^#', text)
                if checkCom:
                    result.append(('com', text))
                    continue
                checkMsgid = re.findall('^msgid\s+\"([\s\S]*)\"\s*$', text)
                if checkMsgid:
                    beginMsgid = True
                    listMsgid.append(('msgid', checkMsgid[0]))
                    continue
                checkMsgid_plural = re.findall('^msgid_plural\s+\"([\s\S]*)\"\s*$', text)
                if checkMsgid_plural:
                    beginMsgid = True
                    listMsgid.append(('msgid_plural', checkMsgid_plural[0]))
                    continue
                # Bỏ qua biến msgstr (biến này sẽ được dịch và in ra sau)
                checkMsgstr = re.findall('^msgstr\s+"[\s\S]*\"\s*$', text)
                if checkMsgstr:
                    continue
                checkMsgstr = re.findall('^msgstr\[\d+\]\s+"[\s\S]*"\s*$', text)
                if checkMsgstr:
                    continue
                if beginMsgid:
                    result.append(('msgstr', listMsgid))
                    listMsgid = []
                    beginMsgid = False
                result.append(('other', text))
        return result

    def write_data(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8') as fileWrite:
            for line in data:
                if line[0] == 'msgstr':
                    dem = len(line[1])
                    if dem == 1:
                        fileWrite.write(f'{line[1][0][0]} "{line[1][0][1]}"\n')
                        fileWrite.write(f'msgstr "{line[1][0][2]}"\n')
                    else:
                        for n in range(dem):
                            fileWrite.write(f'{line[1][n][0]} "{line[1][n][1]}"\n')
                        for n in range(dem):
                            fileWrite.write(f'msgstr[{n}] "{line[1][n][2]}"\n')
                else:
                    fileWrite.write(f'{line[1]}\n')