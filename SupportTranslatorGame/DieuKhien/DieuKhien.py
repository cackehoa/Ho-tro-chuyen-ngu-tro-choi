#DieuKhien.py
#Controller: Điều khiển những tác của hiển thị với mô hình

class DieuKhien:
    def __init__(self, mo_hinh, hien_thi):
        '''Hàm khởi tạo với đối tượng mô hình và hiển thị'''
        self.mo_hinh_tep = mo_hinh.tep_tin
        self.mo_hinh_csdl = mo_hinh.csdl
        self.hien_thi = hien_thi
        self.tu_khoa = ''
    
    def Loc_Khoang_Trang(self, chuoi):
        '''Bỏ khoảng trắng thừa và ký tự đặt biệt đầu và cuối chuỗi
        Giữ lại ký tự xuống dòng '\n'
        '''
        cat_dau_duoi = chuoi.strip()
        doan_vans = cat_dau_duoi.split('\n')
        doan_van_bo_khoan_trang = []
        for doan in doan_vans:
            doan_van_bo_khoan_trang.append(' '.join(doan.split()))
        ket_qua = '\n'.join(doan_van_bo_khoan_trang)
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
        '''Lấy trang cần hiển thị
        Đầu vào nut_bam:
            'None' : Không thay đổi hoặc nhập trang bằng tay
            'trang_truoc' : khi ấn nút bấm bên trái <
            'trang_sau' : khi ấn nút bấm bên phải > '''
        trang = self.hien_thi.Lay_Trang_Hien_Tai()
        if nut_bam == 'trang_truoc':
            trang -=1
        elif nut_bam == 'trang_sau':
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
        sap_xep = 'eng'
        thu_tu = 'ASC'
        du_lieu = self.mo_hinh_csdl.Danh_Sach_Loc(bat_dau, so_dong, sap_xep, thu_tu, self.tu_khoa)
        self.hien_thi.Nhap_Danh_Sach_Moi(du_lieu)
        
    def Tao_Moi_Cau_Goc(self):
        '''Tạo mới câu gốc được nhập vào csdl'''
        txt_eng = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Eng())
        if len(txt_eng) < 2:
            self.hien_thi.text_eng.focus()
            return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Anh không có nội dung')
        if self.mo_hinh_csdl.Lay_Eng(txt_eng) is None:
            txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
            if len(txt_vie) == 0:
                self.hien_thi.text_vie.focus()
                return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Việt không có nội dung')
            id = self.mo_hinh_csdl.Nhap_Cau_Goc(txt_eng, txt_vie)
            #Cập nhật id mới
            self.hien_thi.Cap_Nhat_Txt_ID(id)
            self.Lay_Trang_Danh_Sach()
            return self.hien_thi.Nhap_Trang_Thai(f'Lưu câu mới với id={id}')
        return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Anh đã tồn tại')
            
    def Cap_Nhat_Cau_Goc(self):
        '''Cập nhật câu đang được chọn vào csdl'''
        id = self.hien_thi.Lay_Txt_Id()
        if id ==0:
            return self.hien_thi.Nhap_Trang_Thai('Chưa chọn câu nào')
        du_lieu = self.mo_hinh_csdl.Lay_Id(id)
        if du_lieu is not None:
            txt_eng = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Eng())
            if txt_eng == du_lieu[1]:
                txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
                self.mo_hinh_csdl.Cap_Nhat_Vie(id, txt_vie)
            else:
                if len(txt_eng) < 2:
                    self.hien_thi.text_eng.focus()
                    return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Anh không có nội dung')
                if self.mo_hinh_csdl.Lay_Eng(txt_eng) is None:
                    txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
                    self.mo_hinh_csdl.Cap_Nhat_Cau_Goc(id, txt_eng, txt_vie)
                else:
                    return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Anh đã tồn tại')
            self.Lay_Trang_Danh_Sach()
            return self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} được cập nhật')
        return self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} không tồn tại')
        
    def Xoa_Cau_Goc(self):
        '''Xóa câu đang được chọn khỏi csdl'''
        id = self.hien_thi.Lay_Txt_Id()
        self.mo_hinh_csdl.Xoa_Cau_Goc(id)
        self.Lay_Trang_Danh_Sach()
        self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} được xóa')
     
    def Luu_Du_Lieu_Vao_Csdl(self, du_lieu, ghi_de = 0):
        '''Nhập danh sách dữ liệu vào csdl
        Đầu vào:
            du_lieu: list [(eng, vie)]
            ghi_de: 0/1 #1 cho phép ghi đè nghĩa tiếng Việt của câu tiếng Anh đã có trong csdl
        '''
        nhap_moi = 0 #Số lượng câu nhập vào cơ sở dữ liệu
        nhap_de = 0 #Số lượng câu nhập đè
        bo_qua = 0 #Số lượng câu bỏ qua
        if ghi_de == 1:
            for cau_goc in du_lieu:
                eng = self.Loc_Khoang_Trang(cau_goc[0])
                #Câu tiếng Anh phải có hơn 2 ký tự
                if len(eng) > 1:
                    vie = self.Loc_Khoang_Trang(cau_goc[1])
                    #Câu tiếng Việt ít nhất phải có ít nhất 1 ký tự và khác câu tiếng Anh
                    if len(vie) == 0 or eng == vie:
                        bo_qua +=1
                        continue #for du_lieu
                    cau_eng = self.mo_hinh_csdl.Lay_Eng(eng)
                    #Nếu câu tiếng anh KHÔNG tồn tại thì nhập câu mới
                    if cau_eng is None:
                        #Nhập câu mới
                        self.mo_hinh_csdl.Nhap_Cau_Goc(eng, vie)
                        nhap_moi +=1
                        continue #for du_lieu
                    else:
                        #Cập nhật câu tiếng Việt có id
                        self.mo_hinh_csdl.Cap_Nhat_Vie(cau_eng[0], vie)
                        nhap_de +=1
                        continue #for du_lieu
                bo_qua +=1
        else: # Không ghi đè
            for cau_goc in du_lieu:
                eng = self.Loc_Khoang_Trang(cau_goc[0])
                #Câu tiếng Anh phải có hơn 2 ký tự
                if len(eng) > 1:
                    vie = self.Loc_Khoang_Trang(cau_goc[1])
                    #Câu tiếng Việt ít nhất phải có ít nhất 1 ký tự và khác câu tiếng Anh
                    if len(vie) == 0 or eng == vie:
                        bo_qua +=1
                        continue #for du_lieu
                    #Nếu câu tiếng anh KHÔNG tồn tại thì nhập câu mới
                    if self.mo_hinh_csdl.Lay_Eng(eng) is None:
                        #Nhập câu mới
                        self.mo_hinh_csdl.Nhap_Cau_Goc(eng, vie)
                        nhap_moi +=1
                        continue #for du_lieu
                bo_qua +=1
        if nhap_moi != 0 or nhap_de != 0:
            self.Lay_Trang_Danh_Sach()
        self.hien_thi.Nhap_Trang_Thai(f'Nhập mới: {nhap_moi} câu, ghi đè: {nhap_de} câu, bỏ qua: {bo_qua} câu')
        
    def Nhap_Tep_XUnity(self):
        '''Nhập dữ liệu từ tệp XUnity vào csdl'''
        #Nhập dữ liệu
        ten_tep = self.hien_thi.Hop_Thoai_Mo_Tep()
        if self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(ten_tep):
            #Dọc dữ liệu từ tập tin
            du_lieu = self.mo_hinh_tep.Doc_XUnity(ten_tep)
            self.Luu_Du_Lieu_Vao_Csdl(du_lieu)
        else:
            self.hien_thi.Nhap_Trang_Thai('Không có tệp XUnity để xử lý')
    
    def Xuat_Tep_XUnity(self):
        '''Dịch những câu có trong tệp nguồn XUnity rồi xuất ra tệp đích'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('XUnity')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_nguon']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp nguồn để xử lý')
        if len(hop_thoai['tep_dich']) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp đích để xuất ra')
        du_lieu = self.mo_hinh_tep.Doc_XUnity(hop_thoai['tep_nguon'])
        ket_qua = []
        khong_chuyen_ngu = []
        for dong in du_lieu:
            cau_eng = self.Loc_Khoang_Trang(dong[0])
            if len(cau_eng) < 2:
                ket_qua.append((dong[0], cau_eng))
                continue #Bỏ qua câu ngắn hơn 2
            cau_vie = self.Loc_Khoang_Trang(dong[1])
            vie = self.mo_hinh_csdl.Chuyen_Ngu(cau_eng, hop_thoai['co_dich'])
            #Nếu không dịch được thì trả lại kết quả cũ hoặc chính câu tiếng Anh
            if vie == cau_eng:
                if len(cau_vie) == 0:
                    ket_qua.append((dong[0], vie))
                else:
                    ket_qua.append((dong[0], cau_vie))
                if dong[0] not in khong_chuyen_ngu:
                    khong_chuyen_ngu.append(dong[0])
            else:
                if len(vie) == 0:
                    ket_qua.append((dong[0], cau_vie))
                    if dong[0] not in khong_chuyen_ngu:
                        khong_chuyen_ngu.append(dong[0])
                else:
                    ket_qua.append((dong[0], vie))
        self.mo_hinh_tep.Ghi_XUnity(hop_thoai['tep_dich'], ket_qua)
        self.mo_hinh_tep.Ghi_Khong_Chuyen_Ngu(khong_chuyen_ngu)
        self.hien_thi.Nhap_Trang_Thai('Xuất dữ liệu kiểu XUnity ra tệp thành công')
        
    def Nhap_Tep_Json(self):
        '''Nhập dữ liệu từ tệp Json vào csdl'''
        hop_thoai = self.hien_thi.Hop_Thoai_Nhap('Json')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_eng']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp Json tiếng Anh để xử lý')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_vie']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp Json tiếng Việt để xử lý')
        def Duyet_Nhap_Lieu_Json(du_lieu_eng, du_lieu_vie):
            '''Duyệt trích xuất dữ liệu tiếng Anh và tiếng Việt tương ứng
            Đầu vào:
                du_lieu_eng: dict #Json
                du_lieu_vie: dict #Json
            Đầu ra:
                ket_qua: list[(eng, vie)]
            '''
            ket_qua = []
            for khoa_chung in du_lieu_eng:
                if khoa_chung in du_lieu_vie.keys():
                    #Đệ quy với kiểu dữ liệu dict (Json)
                    keu_du_lieu_eng = type(du_lieu_eng[khoa_chung])
                    keu_du_lieu_vie = type(du_lieu_vie[khoa_chung])
                    if keu_du_lieu_eng is dict and keu_du_lieu_vie is dict:
                        ket_qua.extend(Duyet_Nhap_Lieu_Json(du_lieu_eng[khoa_chung], du_lieu_vie[khoa_chung]))
                    #Xử lý kiểu dữ liệu list với tuple như nhau
                    elif keu_du_lieu_eng is list or keu_du_lieu_eng is tuple:
                        if keu_du_lieu_vie is list or keu_du_lieu_vie is tuple:
                            nho_nhat = min(len(du_lieu_eng[khoa_chung]), len(du_lieu_vie[khoa_chung]))
                            for dong in range(nho_nhat):
                                #Nhập vào cơ sở dữ liệu
                                ket_qua.append((du_lieu_eng[khoa_chung][dong], du_lieu_vie[khoa_chung][dong]))
                    else:
                        #Nhập vào cơ sở dữ liệu
                        ket_qua.append((du_lieu_eng[khoa_chung], du_lieu_vie[khoa_chung]))
            return ket_qua
        du_lieu = Duyet_Nhap_Lieu_Json(self.mo_hinh_tep.Doc_Json(hop_thoai['tep_eng']), self.mo_hinh_tep.Doc_Json(hop_thoai['tep_vie']))
        self.Luu_Du_Lieu_Vao_Csdl(du_lieu, hop_thoai['ghi_de'])
    
    def Xuat_Tep_Json(self):
        '''Dịch những câu có trong tệp nguồn Json rồi xuất ra tệp đích'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('Json')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_nguon']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp Json nguồn để xử lý')
        if len(hop_thoai['tep_dich']) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp Json đích để xuất ra')
        du_lieu = self.mo_hinh_tep.Doc_Json(hop_thoai['tep_nguon'])
        khong_chuyen_ngu = []
        def Duyet_Chuyen_Ngu_Json(du_lieu, co_dich, khong_chuyen_ngu):
            for khoa_chung in du_lieu:
                keu_du_lieu = type(du_lieu[khoa_chung])
                if keu_du_lieu is dict:
                    #Đệ quy
                    du_lieu[khoa_chung] = Duyet_Chuyen_Ngu_Json(du_lieu[khoa_chung], co_dich, khong_chuyen_ngu)
                elif keu_du_lieu is list or keu_du_lieu is tuple:
                    for dong  in range(du_lieu[khoa_chung]):
                        cau_eng = self.Loc_Khoang_Trang(du_lieu[khoa_chung][dong])
                        if len(cau_eng) > 1:
                            vie = self.mo_hinh_csdl.Chuyen_Ngu(cau_eng, co_dich)
                            if cau_eng == vie and du_lieu[khoa_chung][dong] not in khong_chuyen_ngu:
                                    khong_chuyen_ngu.append(du_lieu[khoa_chung][dong])
                            du_lieu[khoa_chung][dong] = vie
                        else:
                            du_lieu[khoa_chung][dong] = cau_eng
                else:
                    cau_eng = self.Loc_Khoang_Trang(du_lieu[khoa_chung])
                    if len(cau_eng) > 1:
                        vie = self.mo_hinh_csdl.Chuyen_Ngu(cau_eng, co_dich)
                        if cau_eng == vie and du_lieu[khoa_chung] not in khong_chuyen_ngu:
                                khong_chuyen_ngu.append(du_lieu[khoa_chung])
                        du_lieu[khoa_chung] = vie
                    else:
                        du_lieu[khoa_chung] = cau_eng
            return du_lieu
        self.mo_hinh_tep.Ghi_Json(hop_thoai['tep_dich'], Duyet_Chuyen_Ngu_Json(du_lieu, hop_thoai['co_dich'], khong_chuyen_ngu))
        self.mo_hinh_tep.Ghi_Khong_Chuyen_Ngu(khong_chuyen_ngu)
        self.hien_thi.Nhap_Trang_Thai('Xuất dữ liệu kiểu Json ra tệp thành công')
        
    def Nhap_Tep_Csv(self):
        '''Nhập dữ liệu từ tệp Csv vào csdl'''
        hop_thoai = self.hien_thi.Hop_Thoai_Nhap('Csv')
        if self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_eng']):
            #Nếu tệp tiếng Việt không tồn tại
            du_lieu = []
            if hop_thoai['tep_vie'] == '' or hop_thoai['tep_vie'] == hop_thoai['tep_eng'] or not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_vie']):
                if hop_thoai['cot_eng'] != hop_thoai['cot_vie']:
                    du_lieu = self.mo_hinh_tep.Doc_Cot_Csv(hop_thoai)
            else: #Tệp tiếng Việt tồn tại
                du_lieu = self.mo_hinh_tep.Doc_Cot_2_Csv(hop_thoai)
            self.Luu_Du_Lieu_Vao_Csdl(du_lieu, hop_thoai['ghi_de'])
        else:
            self.hien_thi.Nhap_Trang_Thai('Không có tệp Csv để xử lý')
    
    def Xuat_Tep_Csv(self):
        '''Dịch những câu có trong tệp nguồn Csv rồi xuất ra tệp đích'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('Csv')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_nguon']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp Csv nguồn để xử lý')
        if len(hop_thoai['tep_dich']) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp Csv đích để xuất ra')
        du_lieu_csv = self.mo_hinh_tep.Doc_Csv(hop_thoai['tep_nguon'], hop_thoai['dau_phan_cach'])
        so_cot_tieu_de = len(du_lieu_csv['tieu_de'])
        if hop_thoai['cot_eng'] >= so_cot_tieu_de:
            return self.hien_thi.Nhap_Trang_Thai('Cột tiếng Anh không tồn tại')
        #Thêm mã 'vi' vào cuối tiêu đề
        if hop_thoai['cot_vie'] >= so_cot_tieu_de:
            du_lieu_csv['tieu_de'].append('vi')
        kq_du_lieu = []
        khong_chuyen_ngu = []
        for dong in du_lieu_csv['du_lieu']:
            so_dong = len(dong)
            #Cột tiếng Anh không tồn tại
            #Gặp một số tệp Csv không tiêu chuẩn
            if hop_thoai['cot_eng'] >= so_dong:
                kq_du_lieu.append(dong)
                continue
            cau_eng = self.Loc_Khoang_Trang(dong[hop_thoai['cot_eng']])
            #Câu tiếng Anh quá ngắn < 2
            if len(cau_eng) < 2:
                if hop_thoai['cot_vie'] < so_dong:
                    dong[hop_thoai['cot_vie']] = cau_eng
                else:
                    dong.append(cau_eng)
                kq_du_lieu.append(dong)
                continue
            vie = self.mo_hinh_csdl.Chuyen_Ngu(cau_eng, hop_thoai['co_dich'])
            if cau_eng == vie:
                if hop_thoai['cot_vie'] < so_dong and len(dong[hop_thoai['cot_vie']]) != 0:
                    vie = dong[hop_thoai['cot_vie']]
                if dong[hop_thoai['cot_eng']] not in khong_chuyen_ngu:
                    khong_chuyen_ngu.append(dong[hop_thoai['cot_eng']])
            #Nếu cột Việt không tồn tại thì thêm vào cuối
            if hop_thoai['cot_vie'] < so_dong:
                dong[hop_thoai['cot_vie']] = vie
            else:
                dong.append(vie)
            kq_du_lieu.append(dong)
        du_lieu_csv['du_lieu'] = kq_du_lieu
        self.mo_hinh_tep.Ghi_Csv(hop_thoai['tep_dich'], du_lieu_csv, hop_thoai['dau_phan_cach'])
        self.mo_hinh_tep.Ghi_Khong_Chuyen_Ngu(khong_chuyen_ngu)
        self.hien_thi.Nhap_Trang_Thai('Xuất dữ liệu kiểu Csv ra tệp thành công')
        
    def Nen_Tep_Tin(self):
        '''Hàm chuyên nén tệp thành gzip'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('Gzip')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_nguon']):
            return self.hien_thi.Nhap_Trang_Thai('Tệp nguồn không tồn tại')
        if len(hop_thoai['tep_dich']) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp đích')
        self.mo_hinh_tep.Nen_Tep_Gzip(hop_thoai['tep_nguon'],hop_thoai['tep_dich'])
        self.hien_thi.Nhap_Trang_Thai('Nén dữ liệu thành công')
        