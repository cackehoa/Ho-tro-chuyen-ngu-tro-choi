'''PoFile.py
Đọc nội dung tập tin Po
Dành riêng cho trò chơi Avorion'''

from .TypeFile import TypeFile

class PoFile(TypeFile):

    def __init__(self, fileName):
        super().__init__(fileName)

    #Đọc nội dung tệp theo từng dòng
    def read_all(self):
        result = []
        with open(self.get_file_name(), 'r', encoding = 'utf-8') as readFile:
            for row in readFile:
                if len(row) > 1:
                    result.append(row)
        return result