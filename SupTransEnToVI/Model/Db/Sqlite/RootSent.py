'''RootSent.py
Đây là phần lưu câu dịch chỉnh chu nhất làm tiền đề dịch cho tất cả
'''
from datetime import datetime

class RootSent:
	#Khởi tạo
    def __init__(cls, parent):
        cls.parent = parent
        cls.cursor = parent.get_cursor()

    #Lấy tất cả từ khóa theo từng trang
    def get_allkeys(cls, key, page):
        maxRow = 10
        startRow = (page-1)*maxRow
        if key == '':
            sql_select = '''SELECT id, eng, vie
                FROM ROOT_SENT
                ORDER BY eng
                LIMIT ?, ?
                '''
            cls.cursor.execute(sql_select, (startRow, maxRow))
        else:
            sql_select = '''SELECT id, eng, vie
                FROM ROOT_SENT
                WHERE eng LIKE ? ESCAPE '\\'
                ORDER BY length(eng), eng DESC
                LIMIT ?, ?
                '''
            cls.cursor.execute(sql_select, (f'%{cls.parent.escape_string_like(key)}%', startRow, maxRow))
        result = cls.cursor.fetchall()
        return result

    #Lấy theo id_
    def get_id(cls, id_):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE id = ?
            '''
        cls.cursor.execute(sql_select, (id_,))
        result = cls.cursor.fetchone()
        return result

    #Tìm chính xác theo câu eng
    def get_eng(cls, eng):
        return cls.get_eng_thread(eng, cls.cursor)

    #Tìm chính xác theo câu eng (Thread)
    def get_eng_thread(cls, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE eng = ?
            '''
        cursor.execute(sql_select, (eng,))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng ngắn nhất
    def get_like_eng(cls, eng):
        return cls.get_like_eng_thread(eng, cls.cursor)

    #Lấy câu gần đúng ngắn nhất (Thread)
    def get_like_eng_thread(cls, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'%{cls.parent.escape_string_like(eng)}%',))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng ngắn nhất (Thread)
    def get_glob_eng_thread(cls, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE eng GLOB ?
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'*{eng}*',))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng phía trước ngắn nhất (Thread)
    def get_like_front_eng_thread(cls, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'%{cls.parent.escape_string_like(eng)}',))
        result = cursor.fetchone()
        return result

    
    #Lấy câu gần đúng ở giữa ngắn nhất (Thread)
    def get_like_middle_eng_thread(cls, eng1, eng2, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'{cls.parent.escape_string_like(eng1)}%{cls.parent.escape_string_like(eng2)}%',))
        result = cursor.fetchone()
        return result

    #Lấy câu gần đúng phía sau ngắn nhất (Thread)
    def get_like_rear_eng_thread(cls, eng, cursor):
        sql_select = '''SELECT id, eng, vie
            FROM ROOT_SENT
            WHERE eng LIKE ? ESCAPE '\\'
            ORDER BY length(eng), eng DESC
            '''
        cursor.execute(sql_select, (f'{cls.parent.escape_string_like(eng)}%',))
        result = cursor.fetchone()
        return result

    #Thêm sent mới vào database
    def new_sent(cls, eng, vie):
        sql_insert = '''INSERT INTO ROOT_SENT(eng, vie)
            VALUES(?,?)
            '''
        cls.cursor.execute(sql_insert, (eng, vie))
        return cls.cursor.lastrowid

    #Cập nhật sent vào database
    def update_sent(cls, id_, eng, vie):
        sql_update = '''UPDATE ROOT_SENT
            SET eng= ?,
                vie = ?,
                day_update = ?
            WHERE  id = ?
            '''
        cls.cursor.execute(sql_update, (eng, vie, datetime.now(), id_))

    #Xóa sent khỏi database
    def delete_sent(cls, id_):
        sql_delete = '''DELETE FROM ROOT_SENT
        WHERE  id = ?
        '''
        cls.cursor.execute(sql_delete, (id_,))

    #Lấy danh sách câu mới cập nhật
    def get_list_root_update(cls):
        result = []
        sql_select = '''SELECT eng
            FROM ROOT_SENT
            WHERE day_update > ?
            '''
        cls.cursor.execute(sql_select, (cls.config['cache_update'],))
        result = cls.cursor.fetchall()
        return result