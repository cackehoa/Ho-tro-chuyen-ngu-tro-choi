'''TypeFile.py
Định dạng chung cho các loại tệp
'''
import os

class TypeFile:
    def __init__(self, fileName):
        self.set_file_name(fileName)
        self.str_normalize = [
            ("\\\"", "\""),
            ("\\'", "'"),
            ("\\n", "\n"),
            ("\\r", "\r"),
            ("\\t", "\t"),
            ("\\\\", "\\")]
        self.str_re_normalize = [
            ("\\", "\\\\"),
            ("\t", "\\t"),
            ("\r", "\\r"),
            ("\n", "\\n"),
            ("\'", "\\\'"),
            ("\"", "\\\"")]

    def set_file_name(self, fileName):
        self.fileName = fileName.strip()

    def get_file_name(self):
        return self.fileName

    def isFile(self):
        return len(self.get_file_name()) > 0 and os.path.exists(self.get_file_name()) and os.path.isfile(self.get_file_name())

    #Chuẩn hóa dữ liệu theo database
    def cover_normalize(self, data):
        value = data
        for row in self.str_normalize:
            value = value.replace(row[0], row[1])
        return value

    #Chuẩn hóa dữ liệu theo dữ liệu tương ứng
    def cover_re_normalize(self, data):
        value = data
        for row in self.str_re_normalize:
            value = value.replace(row[0], row[1])
        return value

    #Đọc nội dung tệp theo từng dòng
    def read_all(self):
        result = []
        with open(self.get_file_name(), 'r', encoding = 'utf-8') as readFile:
            for row in readFile:
                if len(row) > 1:
                    result.append(row)
        return result

    #Ghi nội dung xuống tệp theo dòng
    def write_data(self, data):
        with open(self.get_file_name(), 'w', encoding = 'utf-8') as writeFile:
            for row in data:
                writeFile.write(f"{row}\n")