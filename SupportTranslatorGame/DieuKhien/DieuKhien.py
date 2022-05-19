#DieuKhien.py
#Controller: Điều khiển những tác của hiển thị với mô hình

class DieuKhien:
    def __init__(self, mo_hinh, hien_thi):
        '''Hàm khởi tạo với đối tượng mô hình và hiển thị'''
        self.mo_hinh = mo_hinh
        self.hien_thi = hien_thi
        self.tu_khoa = ''
    
    def Loc_Khoang_Trang(self, chuoi):
        '''Bỏ khoảng trắng thừa và ký tự đặt biệt đầu và cuối chuỗi'''
        #Xóa khoảng trắng đôi
        ket_qua = chuoi.strip()
        ket_qua = ' '.join(ket_qua.split())
        return ket_qua
        
    def Tao_Loc_Moi(self, event=None):
        '''Hàm giúp tạo bộ lọc mới'''
        self.hien_thi.Dat_Trang_Hien_Tai(1)
        self.tu_khoa = self.Loc_Khoang_Trang(self.hien_thi.Lay_Tu_Khoa())
        self.Lay_Danh_Sach()
        if self.tu_khoa == '':
            self.hien_thi.Nhap_Trang_Thai('Hiển thị danh sách tất cả các câu')
        else:
            self.hien_thi.Nhap_Trang_Thai(f'Lọc với từ khóa: {self.tu_khoa}')
    
    def Lay_Trang_Danh_Sach(self, nut_bam = 'None'):
        '''Hàm giúp lấy trang cần hiển thị
        Đầu vào nut_bam:
            None : Không thay đổi hoặc nhập trang bằng tay
            trai : khi ấn nút bấm bên trái <
            phai : khi ấn nút bấm bên phải > '''
        trang = self.hien_thi.Lay_Trang_Hien_Tai()
        if nut_bam == 'trai':
            trang -=1
        elif nut_bam == 'phai':
            trang +=1
        if trang < 1:
            trang = 1 #Đảm bảo trang nhỏ nhất là 1
        self.hien_thi.Dat_Trang_Hien_Tai(trang)
        self.Lay_Danh_Sach(trang)
        self.hien_thi.Nhap_Trang_Thai(f'Đang hiển thị trang {trang}')
        
    def Lay_Danh_Sach(self, trang=1):
        '''Lấy thông dữ liệu trang tương ứng từ cơ sở dũ liệu và hiển thị'''
        #Số dòng mặc định lấy ra là 10
        so_dong = 10
        bat_dau = (trang-1)*so_dong
        du_lieu = self.mo_hinh.csdl.Danh_Sach_Loc(bat_dau, so_dong, self.tu_khoa)
        self.hien_thi.Nhap_Danh_Sach_Moi(du_lieu)
        
    def Tao_Moi_Cau_Goc(self):
        '''Tạo mới câu gốc'''
        txt_eng = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Eng())
        if len(txt_eng) < 2:
            self.hien_thi.text_eng.focus()
            return self.hien_thi.Nhap_Trang_Thai('Câu (eng) không có nội dung')
        Kiem_tra_eng = self.mo_hinh.csdl.Lay_Eng(txt_eng)
        if len(Kiem_tra_eng) == 0:
            txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
            if len(txt_vie) == 0:
                self.hien_thi.text_vie.focus()
                return self.hien_thi.Nhap_Trang_Thai('Câu (vie) không có nội dung')
            id = self.mo_hinh.csdl.Nhap_Cau_Goc(txt_eng, txt_vie)
            #Cập nhật id mới
            self.hien_thi.Cap_Nhat_Txt_ID(id)
            self.Lay_Trang_Danh_Sach()
            return self.hien_thi.Nhap_Trang_Thai(f'Lưu câu mới với id={id}')
        return self.hien_thi.Nhap_Trang_Thai('Câu đã tồn tại')
            
    def Cap_Nhat_Cau_Goc(self):
        '''Cập nhật câu đang được chọn'''
        id = self.hien_thi.Lay_Txt_Id()
        if id ==0:
            return self.hien_thi.Nhap_Trang_Thai('Chưa chọn câu nào')
        du_lieu = self.mo_hinh.csdl.Lay_Id(id)
        if len(du_lieu) == 0:
            return self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} không tồn tại')
        for cau_goc in du_lieu:
            txt_eng = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Eng())
            if txt_eng == cau_goc[1]:
                txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
                self.mo_hinh.csdl.Cap_Nhat_Vie(id, txt_vie)
            else:
                if len(txt_eng) < 2:
                    self.hien_thi.text_eng.focus()
                    return self.hien_thi.Nhap_Trang_Thai('Câu (eng) không có nội dung')
                Kiem_tra_eng = self.mo_hinh.csdl.Lay_Eng(txt_eng)
                if len(Kiem_tra_eng) == 0:
                    txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
                    self.mo_hinh.csdl.Cap_Nhat_Cau_Goc(id, txt_eng, txt_vie)
                else:
                    return self.hien_thi.Nhap_Trang_Thai('Câu đã tồn tại')
            self.Lay_Trang_Danh_Sach()
            return self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} được cập nhật')
        
    def Xoa_Cau_Goc(self):
        id = self.hien_thi.Lay_Txt_Id()
        self.mo_hinh.csdl.Xoa_Cau_Goc(id)
        self.Lay_Trang_Danh_Sach()
        self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} được xóa')
        
    def Nhap_Tep_XUnity(self):
        '''Xử lý tiệp loại XUnity'''
        #Nhập dữ liệu
        ten_tep = self.hien_thi.Hop_Thoai_Mo_Tep()
        self.hien_thi.Nhap_Trang_Thai(f'Đang xử lý tệp: {ten_tep}')
        if ten_tep !='' and self.mo_hinh.tep_tin.Kiem_Tra_Tep_Ton_Tai(ten_tep):
            #Dọc dữ liệu từ tập tin
            du_lieu = self.mo_hinh.tep_tin.Doc_XUnity(ten_tep)
            nhap_csdl = 0 #Số lượng câu nhập vào cơ sở dữ liệu
            bo_qua = 0 #Số lượng câu bỏ qua
            for cau_goc in du_lieu:
                eng = self.Loc_Khoang_Trang(cau_goc[0])
                #Câu tiếng Anh phải có hơn 2 ký tự
                if len(eng) > 1:
                    cau_eng = self.mo_hinh.csdl.Lay_Eng(eng)
                    #Nếu câu tiếng anh không tồn tại thì nhập câu mới (tồn tại tạm thời không làm gì hết)
                    if len(cau_eng) == 0:
                        vie = self.Loc_Khoang_Trang(cau_goc[1])
                        #Câu tiếng Việt ít nhất phải có 1 ký tự hoặc khác tiếng Anh
                        if len(vie) == 0 or eng == vie:
                            bo_qua +=1
                        else:
                            #Lưu vào csdl
                            self.mo_hinh.csdl.Nhap_Cau_Goc(eng, vie)
                            nhap_csdl +=1
                    else:
                        bo_qua +=1
            self.Lay_Trang_Danh_Sach()
            self.hien_thi.Nhap_Trang_Thai(f'Nhập XUnity: {nhap_csdl} câu, bỏ qua: {bo_qua} câu')
        else:
            self.hien_thi.Nhap_Trang_Thai('Không có tệp để xử lý')
        
    def Nhap_Tep_Json(self):
        ten_tep = self.hien_thi.Hop_Thoai_Mo_Tep('Json')
        
    def Chuyen_Ngu(self, eng):
        '''Cố chuyển câu tiếng Anh sang tiếng Việt nhiều nhất có thể
        Đầu vào:
            eng: string
        Đầu ra:
            vie: string
        '''
        if len(eng) > 1:
            cau_eng = self.mo_hinh.csdl.Lay_Eng(eng)
            if len(cau_eng) > 0:
                for cau in cau_eng:
                    return cau[2]
            #Cố gắn tách nhỏ câu ra để dịch
            return '' #Nếu không dịch được trả lại chuỗi rỗng
        return eng
        
    def Xuat_Tep_XUnity(self):
        ten_tep = self.hien_thi.Hop_Thoai_Xuat('XUnity')
        tep_nguon = ten_tep[0]
        tep_dich = ten_tep[1]
        if len(tep_nguon) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp nguồn để xử lý')
        if len(tep_dich) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp đích để xuất ra')
        if not self.mo_hinh.tep_tin.Kiem_Tra_Tep_Ton_Tai(tep_nguon):
            return self.hien_thi.Nhap_Trang_Thai('Tệp nguồn không tồn tại')
        self.hien_thi.Nhap_Trang_Thai(f'Đang đọc dữ tệp: {tep_nguon}')
        du_lieu = self.mo_hinh.tep_tin.Doc_XUnity(tep_nguon)
        self.hien_thi.Nhap_Trang_Thai('Đang xử lý dữ liệu')
        ket_qua = []
        for dong in du_lieu:
            cau_eng = self.Loc_Khoang_Trang(dong[0])
            if len(cau_eng) == 0:
                break
            cau_vie = self.Loc_Khoang_Trang(dong[1])
            vie = self.Chuyen_Ngu(cau_eng)
            #Nếu không dịch được thì trả lại kết quả cũ hoặc chính câu tiếng Anh
            if len(vie) == 0:
                if len(cau_vie) == 0:
                    ket_qua.append((dong[0], cau_eng))
                else:
                    ket_qua.append((dong[0], cau_vie))
            else:
                ket_qua.append((dong[0], vie))
        self.hien_thi.Nhap_Trang_Thai(f'Đang xuất dữ liệu ra tệp: {tep_dich}')
        self.mo_hinh.tep_tin.Ghi_XUnity(tep_dich, ket_qua)
        self.hien_thi.Nhap_Trang_Thai('Xuất dữ liệu kiểu XUnity ra tệp thành công')
        
    def Xuat_Tep_Json(self):
        ten_tep = self.hien_thi.Hop_Thoai_Xuat('Json')
        print(ten_tep)