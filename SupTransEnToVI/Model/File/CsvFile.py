'''CsvFile.py
Xử lý tệp loại CSV
'''
import csv
from .TypeFile import TypeFile

class CsvFile(TypeFile):
    def __init__(self, fileName, delimiter = ','):
        super().__init__(fileName)
        self.set_delimiter(delimiter)

    #Nhập dấu phân cách
    def set_delimiter(self, delimiter):
        self.delimiter = delimiter

    #Lấy dấu phân cách
    def get_delimiter(self):
        return self.delimiter

    '''Đọc tất cả dữ liệu kiểu CSV
    Trả về: list
    '''
    def read_all(self):
        result = []
        with open(self.get_file_name(), "r", encoding = 'utf-8') as readFile:
            readCSV = csv.reader(readFile, delimiter = self.get_delimiter())
            for row in readCSV:
                result.append(row)
        return result

    '''Chỉ đọc dữ liệu từ 2 cột cùng tập tin CSV
    Trả về: list [(col1, col2)]
    '''
    def read_2col(self, col1 = 0, col2 = 1):
        result = []
        with open(self.get_file_name(), "r", encoding = 'utf-8') as readFile:
            readCSV = csv.reader(readFile, delimiter = self.get_delimiter())
            #Bỏ qua dòng tiêu đề đầu tiên
            header = next(readCSV)
            countCol = len(header)
            maxCol = max(col1, col2)
            if maxCol < countCol:
                for row in readCSV:
                    #Bỏ qua dòng thiếu cột cần lấy
                    if len(row) > maxCol:
                        result.append((row[col1], row[col2]))
        return result

    '''Đọc dữ liệu từ 2 tiệp tin CSV
    Lấy col1 trong tập tin self.fileName
    Lấy col2 trong tập tin fileName2
    Điều kiện key1 = key2
    Với key1 trong self.fileName và key2 trong fileName2
    Trả về: list[(col1, col2)]
    '''
    def read_2col_2file(self, fileName2, col1 = 1, col2 = 2, key1 = 0, key2 = 0):
        result = []
        return result

    def write_data(self, data, colVie = -1):
        with open(self.get_file_name(), 'w', encoding = 'utf-8', newline = '') as writeFile:
            writeCSV = csv.writer(writeFile, delimiter = self.get_delimiter())
            #Ghi nhiều hàng dữ liệu
            if colVie == -1:
                writeCSV.writerows(data)
            #Ghi từng hàng dữ liệu
            else:
                for row in data:
                    if row[1] == None:
                        writeCSV.writerow(row[0])
                    else:
                        row[1].join()
                        row[0][colVie] = row[1].get_vie()
                        writeCSV.writerow(row[0])
