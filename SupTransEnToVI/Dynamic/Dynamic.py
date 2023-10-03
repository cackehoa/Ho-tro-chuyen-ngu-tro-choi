'''Dynamic.py
Code để chương trình dịch lại bộ đệm khi rãnh
- Tự động chạy khi chương trình rãnh
- Chạy trên một luồng khác
'''
import threading
from ..Model.Trans.EngToVieTrans import EngToVieTrans

#Luồng dịch nội dung bị ảnh hưởng đổi động
class DynamicThread(threading.Thread):
    def __init__(cls, parent):
        cls.controller = parent
        cls.permit = True
        cls.length_data = 0
        cls.count_data = 0
        cls.reset_cache = False
        super().__init__()

    '''Đặt quyền
        permit: boolean
    '''
    def set_permit(cls, permit):
        cls.permit = permit

    def get_permit(cls):
        return cls.permit

    def get_length_data(cls):
        return cls.length_data
        
    def get_count_data(cls):
        return cls.count_data

    def set_reset_cache(cls, reset):
        cls.reset_cache = reset

    #Hàm chạy mặt định của luồng
    def run(cls):
        #Kiểm tra quyền
        if cls.permit:
            db = cls.controller.get_database()
            cursor = db.create_new_cursor()
            dbCache = db.get_db_cache()
            #Lấy dữ liệu cần dịch
            data = dbCache.get_list_cache_update_thread(cursor)
            cls.length_data = len(data)
            trans = EngToVieTrans(cls.controller, cursor, '')
            if cls.reset_cache:
                trans.reset_list_cahce_trans()
            for sent in data:
                if cls.permit == False:
                    break
                cls.count_data += 1
                trans.set_escChar(sent[2])
                vie = trans.trans_try(sent[1])
            #Chạy hết đánh dấu dừng
            cls.set_permit(False)

#Đối tượng giúp kiểm soát luồng động đang chạy
class Dynamic:
	#Khởi tạo
    def __init__(cls, parent):
        cls.controller = parent
        cls.dynamicThread = None

    #Bắt đầu luồng
    def start(cls, reset):
        if cls.dynamicThread is not None:
            cls.stop()
        cls.controller.set_status_dynamic('Khởi tạo luồng mới...')
        cls.dynamicThread = DynamicThread(cls.controller)
        cls.dynamicThread.set_reset_cache(reset)
        cls.dynamicThread.start()
        #Gọi hàm hiển thị sau 1s
        cls.show_status()
        cls.controller.after(2500, cls.show_status)

    #Kết thúc luồng
    def stop(cls):
        if cls.dynamicThread is not None:
            cls.controller.set_status_dynamic('Bắt đầu đóng luồng...')
            cls.dynamicThread.set_permit(False)
            cls.dynamicThread.join()
            cls.dynamicThread = None
            cls.controller.set_status_dynamic('Đã đóng luồng.')

    #Hiển thị trạng thái luồng để theo tiện theo dõi
    def show_status(cls):
        if cls.dynamicThread is None:
            cls.controller.set_status_dynamic('Luồng đã kết thúc')
            return
        #Luồng đang chạy
        if cls.dynamicThread.get_permit():
            cls.controller.set_status_dynamic(f'Cập nhật {cls.dynamicThread.count_data}/{cls.dynamicThread.length_data} bộ đệm thay đổi')
            cls.controller.after(2500, cls.show_status)
            return
        #Luồng tạm dừng
        cls.controller.set_status_dynamic(f'{cls.dynamicThread.count_data}/{cls.dynamicThread.length_data} - Luồng tạm dừng...')
        