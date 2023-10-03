'''
IniFile.py
Xử lý tệp loại ini
'''
import re
from .TypeFile import TypeFile

class IniFile(TypeFile):
    #Khởi tạo
    def __init__(self, fileName):
        super().__init__(fileName)

    '''
    Đọc theo từng dòng
    '''
    def read_all(self):
        with open(self.get_file_name(), "r", encoding='utf-8') as fileRead:
            lines = fileRead.readlines()
        result = []
        for line in lines:
            text = line.strip()
            #Lọc chú thích
            checkCom = re.findall('^\[[\s\S]*\]$', text)
            if checkCom:
                result.append(('com', text))
                continue
            #Lọc biến
            checkVar = re.findall('^([^=]+)=([\s\S]+)$', text)
            if checkVar:
                key = checkVar[0][0].strip()
                value = checkVar[0][1].strip()
                result.append(('var', key, value))
                continue
            result.append(('other', text))
        return result

    '''
    Ghi dữ liệu xuống tệp tin
    '''
    def write_data(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8') as fileWrite:
            for line in data:
                if line[0] == 'var':
                    fileWrite.write(f'{line[1]}={line[2]}\n')
                    continue
                fileWrite.write(f'{line[1]}\n')