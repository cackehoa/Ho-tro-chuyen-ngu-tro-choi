#main.py
#Tiệp tin chính khởi chạy ứng dụng
import os
from SupTransEnToVI.Controller import GuiMain

if __name__ == "__main__":
    '''Chạy ứng dụng'''
    #Tệp csdl mặc định
    fileDatabase = os.path.join(os.getcwd(), 'database.db')
    gui = GuiMain()
    gui.set_database(fileDatabase)
    gui.mainloop()