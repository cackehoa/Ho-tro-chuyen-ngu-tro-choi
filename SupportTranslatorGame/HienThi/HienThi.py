#HienThi.py
#View: Quản lý hiển thị ra cho người sử dụng tương tác

from tkinter import ttk, Text, Menu#,Toplevel
from tkinter import filedialog as Hop_Thoai_Tep
from tkinter import messagebox as Hop_Thoai_Thong_Bao
from .HopThoaiXuat import HopThoaiXuat
from .HopThoaiNhap import HopThoaiNhap

class HienThi(ttk.Frame):
    def __init__(self, tk_goc):
        '''Khởi tạo các đối tượng cần hiển thị'''
        self.tk_goc = tk_goc
        super().__init__(self.tk_goc)
        self.Tao_Tieu_De_Danh_Sach()

    def Nhap_Dieu_Khien(self, dieu_khien):
        '''Nhập đối tượng điều khiển'''
        self.dieu_khien = dieu_khien
        #Khởi tạo dữ liệu danh sách ban đầu
        self.label_trang_thai = ttk.Label(self.tk_goc, text='Khởi tạo thành công', relief='sunken', anchor='w')
        self.Tao_Menu()
        self.Tao_Bo_Loc()
        self.dieu_khien.Tao_Loc_Moi()
        self.Tao_Bo_Nhap()
        #self.Tao_Thanh_Trang_Thai()
        self.label_trang_thai.grid(columnspan=2, ipadx=1, ipady=1, sticky='nsew')
        
    def Tao_Menu(self):
        '''Khởi tạo menu'''
        self.menubar = Menu(self.tk_goc)
        #Tạo menu hành động
        menu_hanh_dong = Menu(self.menubar, tearoff=0)
        menu_hanh_dong.add_command(label='Lọc', command=self.dieu_khien.Tao_Loc_Moi)
        menu_hanh_dong.add_command(label='Trang trước', command=lambda:self.dieu_khien.Lay_Trang_Danh_Sach('trang_truoc'))
        menu_hanh_dong.add_command(label='Trang sau', command=lambda:self.dieu_khien.Lay_Trang_Danh_Sach('trang_sau'))
        menu_hanh_dong.add_separator()
        menu_hanh_dong.add_command(label='Chọn', command=self.Double_Click_Danh_Sach)
        menu_hanh_dong.add_command(label='Tạo mới', command=self.dieu_khien.Tao_Moi_Cau_Goc)
        menu_hanh_dong.add_command(label='Cập nhật', command=self.dieu_khien.Cap_Nhat_Cau_Goc)
        menu_hanh_dong.add_command(label='Xóa', command=self.dieu_khien.Xoa_Cau_Goc)
        menu_hanh_dong.add_separator()
        menu_hanh_dong.add_command(label='Thoát', command=self.tk_goc.quit)
        self.menubar.add_cascade(label='Hành động', menu=menu_hanh_dong)
        #Tạo menu nhập
        menu_nhap = Menu(self.menubar, tearoff=0)
        menu_nhap.add_command(label='Csv', command=self.dieu_khien.Nhap_Tep_Csv)
        menu_nhap.add_command(label='Json', command=self.dieu_khien.Nhap_Tep_Json)
        menu_nhap.add_command(label='XUnity', command=self.dieu_khien.Nhap_Tep_XUnity)
        self.menubar.add_cascade(label='Nhập', menu=menu_nhap)
        #Tạo menu xuất
        menu_xuat = Menu(self.menubar, tearoff=0)
        menu_xuat.add_command(label='Csv', command=self.dieu_khien.Xuat_Tep_Csv)
        menu_xuat.add_command(label='Json', command=self.dieu_khien.Xuat_Tep_Json)
        menu_xuat.add_command(label='XUnity', command=self.dieu_khien.Xuat_Tep_XUnity)
        self.menubar.add_cascade(label='Xuất', menu=menu_xuat)
        #Tạo menu công cụ
        menu_cong_cu = Menu(self.menubar, tearoff=0)
        menu_cong_cu.add_command(label='Nén Gzip', command=self.dieu_khien.Nen_Tep_Tin)
        self.menubar.add_cascade(label='Công cụ', menu=menu_cong_cu)
        self.tk_goc.config(menu=self.menubar)
        
    def Tao_Bo_Loc(self):
        '''Khởi tạo bộ lọc'''
        #Tạo frame để chứa bộ lọc
        frame_loc = ttk.Frame(self.tk_goc)
        frame_loc.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        #Tạo nhãn lọc
        ttk.Label(frame_loc, text='Từ khóa:').pack(side='left', fill='x')
        #Tạo ô nhập từ khóa
        self.entry_loc = ttk.Entry(frame_loc, textvariable='', width=40)
        self.entry_loc.pack(side='left', fill='x')
        self.entry_loc.bind('<Return>', self.dieu_khien.Tao_Loc_Moi)
        self.entry_loc.focus()
        #Tạo nút lọc
        ttk.Button(frame_loc, text='Lọc', command=self.dieu_khien.Tao_Loc_Moi).pack(side='left', fill='x')
        
    def Lay_Tu_Khoa(self):
        '''Trả lại từ khóa được nhập'''
        tu_khoa = self.entry_loc.get()
        return tu_khoa
        
    def Tao_Tieu_De_Danh_Sach(self):
        '''Khởi tạo tiêu đề cây danh sách'''
        #Xuất kết quả tìm kiếm lên Treeview
        cot = ('id','eng','vie')
        self.treeview_danh_sach = ttk.Treeview(self.tk_goc, columns=cot, show='headings')
        self.treeview_danh_sach.column('id', width=50, anchor='c') #Đặt cột id rộng 50
        self.treeview_danh_sach.heading('id', text='ID')
        self.treeview_danh_sach.heading('eng', text='Câu gốc')
        self.treeview_danh_sach.heading('vie', text='Câu dịch')
        self.treeview_danh_sach.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        frame_danh_sach_button = ttk.Frame(self.tk_goc)
        frame_danh_sach_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        #Dùng thủ thuật để canh giữa
        frame_danh_sach_con = ttk.Frame(frame_danh_sach_button)
        frame_danh_sach_con.pack()
        #Nút bấm trước
        ttk.Button(frame_danh_sach_con, text='<', command=lambda:self.dieu_khien.Lay_Trang_Danh_Sach('trang_truoc')).pack(side='left')
        #Trang hiện tại
        self.entry_trang_hien_tai = ttk.Entry(frame_danh_sach_con, textvariable='', width=10, justify='center')
        self.entry_trang_hien_tai.pack(side='left')
        self.entry_trang_hien_tai.bind('<Return>',lambda event:self.dieu_khien.Lay_Trang_Danh_Sach())
        #Nút bấm sau
        ttk.Button(frame_danh_sach_con, text='>', command=lambda:self.dieu_khien.Lay_Trang_Danh_Sach('trang_sau')).pack(side='left')
        
    def Lay_Trang_Hien_Tai(self):
        '''Lấy trang hiện tại đang nhập'''
        try:
            trang = int(eval(str(self.entry_trang_hien_tai.get())))
        except:
            return 1
        return trang
        
    def Dat_Trang_Hien_Tai(self, trang):
        '''Đặt lại số trang đang hiển thị'''
        self.entry_trang_hien_tai.delete(0, 'end')
        self.entry_trang_hien_tai.insert('end', trang)
        
    def Nhap_Danh_Sach_Moi(self, du_lieu):
        '''Xóa danh danh đang hiển thị và nhập lại'''
        self.treeview_danh_sach.delete(*self.treeview_danh_sach.get_children())
        for gia_tri in du_lieu:
            self.treeview_danh_sach.insert('', 'end', values=gia_tri)
        self.treeview_danh_sach.bind('<Double-1>', self.Double_Click_Danh_Sach)
        
    def Tao_Bo_Nhap(self):
        '''Khởi tạo bộ hiển thị và nhập liệu'''
        #Tạo frame để chứa bộ nhập
        frame_nhap = ttk.Frame(self.tk_goc)
        frame_nhap.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        #Nhập id
        ttk.Label(frame_nhap, text='ID:').grid(row=0, column=0, sticky='e')
        self.text_id = Text(frame_nhap, height = 1, width = 40, bg='light green')
        self.text_id.insert('end', '0')
        self.text_id.configure(state='disabled') #self.text_id.configure(state='normal')
        self.text_id.grid(row=0, column=1, sticky='nsew')
        #Nhập tiếng Anh
        ttk.Label(frame_nhap, text='Tiếng Anh:').grid(row=1, column=0, sticky='e')
        self.text_eng = Text(frame_nhap, height = 4, width = 40)
        self.text_eng.grid(row=1, column=1, sticky='nsew')
        #Nhập tiếng Việt
        ttk.Label(frame_nhap, text='Tiếng Việt:').grid(row=2, column=0, sticky='e')
        self.text_vie = Text(frame_nhap, height = 4, width = 40)
        self.text_vie.grid(row=2, column=1, sticky='nsew')
        #Tạo frame để chứa nút bấm bộ nhập
        frame_nhap_button = ttk.Frame(self.tk_goc)
        frame_nhap_button.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')
        ttk.Button(frame_nhap_button, text='Chọn', command=self.Double_Click_Danh_Sach).pack()
        ttk.Button(frame_nhap_button, text='Tạo mới', command=self.dieu_khien.Tao_Moi_Cau_Goc).pack()
        ttk.Button(frame_nhap_button, text='Cập nhật', command=self.dieu_khien.Cap_Nhat_Cau_Goc).pack()
        ttk.Button(frame_nhap_button, text='Xóa', command=self.dieu_khien.Xoa_Cau_Goc).pack()
    
    def Cap_Nhat_Txt_ID(self, id):
        '''Mở và đóng không cho chỉnh sửa id bằng tay
        Đầu vào:
            id: int '''
        self.text_id.configure(state='normal')
        self.text_id.delete('1.0', 'end')
        self.text_id.insert('end' ,id)
        self.text_id.configure(state='disabled')
        
    def Lay_Txt_Id(self):
        '''Trả lại id từ textbox'''
        try:
            id = int(eval(str(self.text_id.get('1.0', 'end'))))
            return id
        except:
            return 0
        
    def Lay_Txt_Vie(self):
        '''Trả lại chuỗi tiếng Việt từ textbox'''
        return self.text_vie.get('1.0', 'end')
        
    def Lay_Txt_Eng(self):
        '''Trả lại chuỗi tiếng Anh từ textbox'''
        return self.text_eng.get('1.0', 'end')
        
    def Double_Click_Danh_Sach(self, event=None):
        '''Xử lý sự kiện nhấp đúp vào danh sách'''
        #item = self.treeview_danh_sach.selection()
        item = self.treeview_danh_sach.focus()
        gia_tri = self.treeview_danh_sach.item(item, 'values')
        if gia_tri:
            #Xóa hết dữ liệu trong Text area
            self.Cap_Nhat_Txt_ID(gia_tri[0])
            self.text_eng.delete('1.0', 'end')
            self.text_eng.insert('end' ,gia_tri[1])
            self.text_vie.delete('1.0', 'end')
            self.text_vie.insert('end' ,gia_tri[2])
            self.Nhap_Trang_Thai(f'Chọn câu có id={gia_tri[0]}')
    
    def Nhap_Trang_Thai(self, trang_thai):
        '''Cho phép hiển thị trạng thái hiện tại'''
        self.label_trang_thai.config(text = trang_thai)
        
    def Hop_Thoai_Mo_Tep(self, loai_tep = 'XUnity'):
        '''Mở ra hộp thoại cho phép nhập vào vị trí chính xác của tệp tin'''
        kieu_tep = (('XUnity', '*.txt'),
            ('Csv', '*.csv'),
            ('Json', '*.json'),
            ('Tất cả tệp', '*.*'))
        if loai_tep == 'Json':
                kieu_tep = (('Json', '*.json'),
                    ('Csv', '*.csv'),
                    ('XUnity', '*.txt'),
                    ('Tất cả tệp', '*.*'))
        if loai_tep == 'Csv':
                kieu_tep = (('Csv', '*.csv'),
                    ('Json', '*.json'),
                    ('XUnity', '*.txt'),
                    ('Tất cả tệp', '*.*'))
        ten_tep = Hop_Thoai_Tep.askopenfilename(title='Mở tệp', filetypes=kieu_tep) # initialdir='/' thư mục mặc định
        return ten_tep
        
    def Hop_Thoai_Luu_Tep(self, loai_tep = 'XUnity'):
        '''Hộp thoại lưu tệp'''
        kieu_tep = (('XUnity', '*.txt'),
            ('Csv', '*.csv'),
            ('Json', '*.json'),
            ('Tất cả tệp', '*.*'))
        if loai_tep == 'Json':
                kieu_tep = (('Json', '*.json'),
                    ('Csv', '*.csv'),
                    ('XUnity', '*.txt'),
                    ('Tất cả tệp', '*.*'))
        if loai_tep == 'Csv':
                kieu_tep = (('Csv', '*.csv'),
                    ('Json', '*.json'),
                    ('XUnity', '*.txt'),
                    ('Tất cả tệp', '*.*'))
        ten_tep = Hop_Thoai_Tep.asksaveasfilename(title='Lưu tệp', filetypes=kieu_tep)
        return ten_tep
        
    def Hop_Thoai_Xuat(self, loai_tep = 'XUnity'):
        '''Mở hộp thoại lấy tệp nguồn và đích
        Trả về:
            (tep_nguon, tep_dich)
        '''
        hop_thoai = HopThoaiXuat(self, loai_tep)
        return hop_thoai.du_lieu
        
    def Hop_Thoai_Nhap(self, loai_tep = 'XUnity'):
        '''Mở hộp thoại lấy tệp nguồn và đích
        Trả về:
            (tep_nguon, tep_dich)
        '''
        hop_thoai = HopThoaiNhap(self, loai_tep)
        return hop_thoai.du_lieu
        
    def Hop_Thoai_Thong_Bao(self, noi_dung):
        '''Bật lên thông báo có nội dung là noi_dung'''
        Hop_Thoai_Thong_Bao.showinfo('Thông báo', noi_dung)
        
    