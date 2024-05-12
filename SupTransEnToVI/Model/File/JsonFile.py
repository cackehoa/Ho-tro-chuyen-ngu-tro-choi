'''JsonFile.py
Xử lý tệp loại Json
'''
import json
from .TypeFile import TypeFile

class JsonFile(TypeFile):
    def __init__(self, fileName):
        super().__init__(fileName)
    
    #Đọc tất cả dữ liệu rồi trả về kiểu Json
    def read_all(self):
        result = []
        with open(self.get_file_name(), "r", encoding = 'utf-8') as readFile:
            try:
                result = json.loads(readFile.read())
            except ValueError as ex:
                print(f'Gặp lỗi khi đọc tệp kiểu Json.\nTên tệp: {self.get_file_name()}.\nThông điệp báo lỗi: {ex}')
        return result
    
    #Ghi dữ liệu ra tệp tin dưới định dạng Json
    def write_data(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8', newline = '') as writeFile:
            json.dump(data, writeFile, ensure_ascii = False, indent = 4)