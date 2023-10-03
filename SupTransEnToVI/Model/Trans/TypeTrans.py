'''
TypeTrans.py
Lớp việt hóa chung nhằm định nghĩa một vài thứ chung (Interface)
'''
class TypeTrans:
    #Khởi tạo
    def __init__(self, parent):
        self.controller = parent
        self.listThread = []
        self.countData = 0

    #Trả về tổng dữ liệu cần xử lý
    def get_count_data(self):
        return self.countData

    #Cập nhật tổng dữ liệu cần xử lý
    def set_count_data(self, count):
        self.countData = count

    #Trả về tổng số dữ liệu đã xử lý
    def get_count_trans(self):
        total = 0
        for row in self.listThread:
            total += row.countData
        return total

    #Ghép list lại rồi trả về
    def join_data(self):
        result = []
        for row in self.listThread:
            row.join()
            result.extend(row.resultData)
        return result

    #Phân luồng dữ liệu cần dịch
    def trans_data(self, data, tryTrans = 0, escChar = []):
        pass