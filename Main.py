#Main.py
#Mình sẽ cố viết ứng dụng theo dạng MVC để sau này dễ quản lý
#Tệp tin này với mục đích nhằm khởi chạy cả ứng dụng

import os

from SupportTranslatorGame import UngDung

if __name__ == "__main__":
    '''Chạy ứng dụng'''
    #tên tệp mặc định
    tep_csdl = os.path.join(os.getcwd(), 'database.db')
    ud = UngDung(tep_csdl)
    ud.mainloop()