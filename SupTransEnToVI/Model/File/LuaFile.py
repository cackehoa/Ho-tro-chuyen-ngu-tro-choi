'''LuaFile.py
Xử lý tệp loại lua
'''
import re
from .TypeFile import TypeFile

class LuaFile(TypeFile):
    def __init__(self, fileName):
        super().__init__(fileName)
        #self.str_normalize = [("\\\"","\""), ("\\n", "\n")]
        self.str_re_normalize = [("\n", "\\n")]

    '''Đọc theo từng dòng trong tệp tin
    Đầu ra:
        list : danh sách dữ liệu trong cặp '{' và '}'
        com : danh sách kiểu chú thích liền kề
        var : danh sách các biến và giá trị có dạng '^([^=]*)=([\s\S]*)$'
        other : dạng chuỗi chưa xác định
    '''
    def read_all(self):
        with open(self.get_file_name(), "r", encoding='utf-8') as fileRead:
            lines = fileRead.readlines()
        isCom = False
        valCom = []
        isStr = False
        isList = False
        dataList = []
        keyList = ''
        key = ''
        result = []
        for line in lines:
            text = line.strip()
            #Kiểm tra dấu đóng list
            checkList = re.findall('\}$', text)
            if checkList:
                if isList:
                    isList = False
                    result.append(('list', keyList, dataList))
                    continue
                else:
                    raise ValueError('Dấu đóng \'}\' thừa')
            #Kiểm tra xem có phải chú thích đơn dòng dạng: -- Chú thích
            checkCom = re.findall('^--', text)
            if checkCom:
                if isList:
                    dataList.append(('com', [text]))
                    continue
                result.append(('com', [text]))
                continue
            #Kiểm tra xem có phải chú thích đơn dòng dạng: /* Chú thích */
            checkCom = re.findall('^/\*[\s\S]*\*/$', text)
            if checkCom:
                if isList:
                    dataList.append(('com', [text]))
                    continue
                result.append(('com', [text]))
                continue
            #Kiểm tra xem có phải chú thích đơn dòng dạng: /// Chú thích ///
            checkCom = re.findall('^///[\s\S]*///$', text)
            if checkCom:
                if isList:
                    dataList.append(('com', [text]))
                    continue
                result.append(('com', [text]))
                continue
            #Kiểm tra xem có phải bắt đầu chú thích nhiều dòng dạng: /* Chú thích
            checkCom = re.findall('^/\*', text)
            if checkCom:
                isCom = True
                valCom = [text]
                continue
            #Kiểm tra xem có phải kết thúc chú thích nhiều dòng dạng: Chú thích */
            checkCom = re.findall('\*/$', text)
            if checkCom:
                isCom = False
                valCom.append(text)
                if isList:
                    dataList.append(('com', valCom))
                    continue
                result.append(('com', valCom))
                continue
            #Đang đọc chú thích nhiều dòng
            if isCom:
                valCom.append(text)
                continue
            #Kiểm tra có phải biến tiêu chuẩn không
            checkVar = re.findall('^([^=]*)=([\s\S]*)$', text)
            if checkVar:
                #Xử lý chuỗi nhiều dòng phía trước nhưng không có kết
                if isStr:
                    isStr = False
                    if isList:
                        dataList.append(('var', key, valStr))
                    else:
                        result.append(('var', key, valStr))
                key = checkVar[0][0].strip()
                value = checkVar[0][1].strip()
                #Kiểm tra giá trị chuỗi đơn dòng dạng: "Chuỗi đơn dòng",
                checkStr = re.findall('^"([\s\S]*)(?:"[\s]*,|")$', value)
                if checkStr:
                    if isList:
                        eng = self.cover_normalize(checkStr[0])
                        dataList.append(('var', key, [eng]))
                        continue
                    eng = self.cover_normalize(checkStr[0])
                    result.append(('var', key, [eng]))
                    continue
                #Kiểm tra giá trị chuỗi đa dòng dạng: "Chuỗi đa dòng"..
                checkStr = re.findall('^"([\s\S]*)"[\s]*\.\.$', value)
                if checkStr:
                    isStr = True
                    eng = self.cover_normalize(checkStr[0])
                    valStr = [eng]
                    continue
                #Bắt đầu list
                if value == '{':
                    if isList:
                        raise ValueError('Không truy hỗ trợ độ sâu cấp 2')
                    isList = True
                    dataList = []
                    keyList = key
                    continue
                if isList:
                    dataList.append(('other', text))
                    continue
                result.append(('other', text))
                continue
            if isStr:
                #Kiểm tra giá trị chuỗi đa dòng dạng: "Chuỗi đa dòng"..
                checkStr = re.findall('^"([\s\S]*)"[\s]*\.\.$', text)
                if checkStr:
                    eng = self.cover_normalize(checkStr[0])
                    valStr.append(eng)
                    continue
                #Kiểm tra giá trị chuỗi kết thúc đa dòng dạng: "Chuỗi kết thúc đa dòng",
                checkStr = re.findall('^"([\s\S]*)(?:"[\s]*,|"[\s]*\.\.,|")$', text)
                if checkStr:
                    isStr = False
                    eng = self.cover_normalize(checkStr[0])
                    valStr.append(eng)
                    if isList:
                        dataList.append(('var', key, valStr))
                        continue
                    result.append(('var', key, valStr))
                    continue
            #Chuỗi không xác định
            if isList:
                dataList.append(('other', text))
                continue
            result.append(('other', text))
        return result

    '''Ghi từng dòng ra tệp tin
    Đầu vào:
        list : danh sách dữ liệu trong cặp '{' và '}'
        com : danh sách kiểu chú thích liền kề
        var : biến có dạng trả về là danh sách thread trans
        other : dạng chuỗi chưa xác định
    '''
    def write_data(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8') as fileWrite:
            for line in data:
                if line[0] == 'com':
                    for com in line[1]:
                        fileWrite.write(f'{com}\n')
                    continue
                if line[0] == 'other':
                    fileWrite.write(f'{line[1]}\n')
                    continue
                if line[0] == 'var':
                    fileWrite.write(f'{line[1]} = ')
                    col = len(line[2])
                    for i in range(col - 1):
                        line[2][i].join()
                        fileWrite.write(f'"{self.cover_re_normalize(line[2][i].get_vie())}"..\n    ')
                    line[2][col-1].join()
                    fileWrite.write(f'"{self.cover_re_normalize(line[2][col-1].get_vie())}"\n')
                    continue
                if line[0] == 'list':
                    fileWrite.write(f'{line[1]} = ' + '{\n')
                    for row in line[2]:
                        if row[0] == 'com':
                            for com in row[1]:
                                fileWrite.write(f'    {com}\n')
                            continue
                        if row[0] == 'other':
                            fileWrite.write(f'{row[1]}\n')
                            continue
                        if row[0] == 'var':
                            fileWrite.write(f'    {row[1]} = ')
                            col = len(row[2])
                            for i in range(col - 1):
                                row[2][i].join()
                                fileWrite.write(f'"{self.cover_re_normalize(row[2][i].get_vie())}"..\n        ')
                            row[2][col-1].join()
                            fileWrite.write(f'"{self.cover_re_normalize(row[2][col-1].get_vie())}",\n')
                            continue
                        fileWrite.write(f'    {row[1]}\n')
                    fileWrite.write('}\n')
                    continue
                fileWrite.write(f'{line[1]}\n')

    '''Viết riêng cho xử lý dữ liệu Project Zombie
    Xuất ra tệp ngôn ngữ định dạng PZ
    '''
    def writeDataPZ(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8') as fileWrite:
            fileWrite.write('''// Localization Master Table
// version: 1
// guid: b73aa63e-6286-4c32-9e48-3b0024c22b51
// Language: Vietnamese (VN)
[Info]
	guid = b73aa63e-6286-4c32-9e48-3b0024c22b51
	language = VN
	version = 1
	translator = cackehoa
	translator = LeTa
	translator = thuytruc1502
[/Info]''')
            fileWrite.write('\n\n[Translations]\n\n')
            for collection in data:
                collection[1].join()
                fileWrite.write('[Collection]\n')
                fileWrite.write(f'    text = {self.cover_re_normalize(collection[1].get_vie())}\n')
                fileWrite.write(f'    // {collection[0]}\n')
                for member in collection[2]:
                    fileWrite.write(f'    member = {member}\n')
                fileWrite.write('[/Collection]\n')
            fileWrite.write('[/Translations]\n')