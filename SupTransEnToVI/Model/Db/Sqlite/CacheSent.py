'''CacheSent.py
Đây là phần code cho bộ đệm csdl (CACHE_SENT)
Các câu dịch bởi chương trình sẽ được lưu ở đây nhằm lấy ra sau này cho nhanh giảm chi phí truy vấn
(Dự kiến: Cho phép tải các câu trong bản dịch có sẵn để truy vấn khi cần)
Hy vọng sẽ tăng tốc dịch:
    - Khuyết điểm: Dữ liệu phát sinh ra nhiều hơn, tăng dung lượng tệp database
    - Ưu điểm: Các câu được dịch qua sẽ không phải tốn nhiều chi phí nhằm dịch lại (tăng tốc khi tạo bản dịch mới sau khi chỉnh sửa)
'''
from datetime import datetime

class CacheSent:
	#Khởi tạo
    def __init__(cls, parent):
        cls.parent = parent
        cls.cursor = parent.get_cursor()

    #Tải danh sách escChar
    def get_list_escchar(cls):
        sql_select = '''SELECT escChar
            FROM CACHE_SENT
            GROUP BY escChar
            ORDER BY length(escChar), escChar
            '''
        cls.cursor.execute(sql_select)
        result = cls.cursor.fetchall()
        return result
        
    '''Ghép 2 danh sách dữ liệu và lọc dữ liệu trùng lặp trong kết quả mới
    Yêu cầu dữ liệu đầu vào data1 và data2:
        - Định dạng đầu vào và đầu ra list[list[id, eng]]
        - Sắp xếp tăng dần theo id_ (ORDER BY id ASC)
        - Không trùng id_ (khi truy vấn chắc chắc không trùng)
    '''
    def filter_duplicate_data(cls, data1, data2):
        result = []
        #Biến nhớ vị trị data2
        count = 0
        #Độ dài data2
        len_data2 = len(data2)
        for row in data1:
            #Cuối chuỗi 2
            if count == len_data2:
                result.append(row)
                continue
            #Giá trị trùng
            if row[0] == data2[count][0]:
                result.append(row)
                count += 1
                continue
            if row[0] < data2[count][0]:
                result.append(row)
                continue
            result.append(data2[count])
            count += 1
            while count != len_data2 and row[0] > data2[count][0]:
                result.append(data2[count])
                count += 1
            result.append(row)
        while count != len_data2:
                result.append(data2[count])
                count += 1
        return result

    #Tìm danh sách câu eng gần đúng
    def get_list_cache_sent(cls, eng, escChar):
        sql_select = '''SELECT id, eng
            FROM CACHE_SENT
            WHERE eng LIKE ? and escChar = ? ESCAPE '\\'
            ORDER BY id
            '''
        cls.cursor.execute(sql_select, (f'%{cls.parent.escape_string_like(eng)}%', cls.parent.escape_string_like(escChar)))
        result = cls.cursor.fetchall()
        return result

    '''Tải danh sách bộ đệm cần cập nhật
    Định dạng kết quả trả về
        list[tuple(escChar, list[(id, eng)])]
    '''
    def get_list_cache_update_thread(cls, cursor):
        sql_select = '''SELECT id, eng, escChar
            FROM CACHE_SENT
            WHERE retrains = 1
            ORDER BY length(eng), escChar
            '''
        cursor.execute(sql_select)
        result = cursor.fetchall()
        return result

    #Kiểm tra ảnh hưởng đến bộ đệm (chức năng viết thêm để kiểm tra)
    def get_count_data_sent(cls, eng):
        sql_select = '''SELECT *
            FROM CACHE_SENT
            WHERE eng LIKE ? ESCAPE '\\'
        '''
        #ESCAPE '\\'
        cls.cursor.execute(sql_select, (f'%{cls.parent.escape_string_like(eng)}%',))
        #cls.cursor.execute(sql_select, (f'%{eng}%',))
        result = cls.cursor.fetchall()
        return result
        
    #Đánh dấu bộ đệm phải dịch lại
    def set_retrains(cls, eng):
        sql_update = '''UPDATE CACHE_SENT
            SET retrains = 1
            WHERE eng LIKE ? AND retrains = 0
        '''
        #Tránh trường hợp dịch lại hàng loạt câu có 1 ký tự bất kỳ
        if len(eng) > 1:
            cls.cursor.execute(sql_update, (f'%{eng}%',))

    #Tìm chính xác tất cả câu eng trong bộ đệm
    def get_cache_thread(cls, eng, cursor):
        sql_select = '''SELECT vie, escChar
            FROM CACHE_SENT
            WHERE eng = ? and retrains = 0
            '''
        cursor.execute(sql_select, (eng,))
        result = cursor.fetchall()
        return result

    #Tạo mới (thread)
    def new_cache_thread(cls, eng, vie, escChar, cursor):
        sql_insert = '''INSERT INTO CACHE_SENT(eng, vie, escChar)
            VALUES(?,?,?)
            '''
        cursor.execute(sql_insert, (eng, vie, escChar))
        return cursor.lastrowid
    
    #Tạo mới
    def new_cache(cls, eng, vie, escChar):
        return cls.new_cache_thread(eng, vie, escChar, cls.cursor)

    #Cập nhật vie bởi id (thread)
    def update_cache_thread(cls, id_, vie, cursor):
        sql_update = '''UPDATE CACHE_SENT
            SET vie = ?,
                retrains = 0,
                day_update = ?
            WHERE  id = ?
            '''
        cursor.execute(sql_update, (vie, datetime.now(), id_))

    #Cập nhật vie bởi id
    def update_cache(cls, id_, vie):
        cls.update_cache_thread(id_, vie, cls.cursor)

    #Lưu bộ đệm xuống csdl (thread)
    def save_cache_thread(cls, eng, vie, escChar, cursor):
        sql_select = '''SELECT id
            FROM CACHE_SENT
            WHERE eng = ? and escChar = ?
            '''
        cursor.execute(sql_select, (eng, escChar))
        sent = cursor.fetchone()
        if sent is None:
            cls.new_cache_thread(eng, vie, escChar, cursor)
        else:
            cls.update_cache_thread(sent[0], vie, cursor)

    #Lưu bộ đệm xuống csdl
    def save_cache(cls, eng, vie, escChar):
        cls.save_cache_thread(eng, vie, escChar, cls.cursor)

    #Xóa dữ liệu (có lẽ không cần nhưng cứ viết sẵn)
    def delete_cache(cls, id_):
        sql_delete = '''DELETE FROM CACHE_SENT
        WHERE  id = ?
        '''
        cls.cursor.execute(sql_delete, (id_,))