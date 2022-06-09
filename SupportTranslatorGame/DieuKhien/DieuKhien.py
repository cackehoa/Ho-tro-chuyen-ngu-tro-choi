#DieuKhien.py
#Controller: Điều khiển những tác của hiển thị với mô hình
import re

class DieuKhien:
    def __init__(self, mo_hinh, hien_thi):
        '''Hàm khởi tạo với đối tượng mô hình và hiển thị'''
        #self.mo_hinh = mo_hinh
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
        Kiem_tra_eng = self.mo_hinh_csdl.Lay_Eng(txt_eng)
        if len(Kiem_tra_eng) == 0:
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
        if len(du_lieu) == 0:
            return self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} không tồn tại')
        for cau_goc in du_lieu:
            txt_eng = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Eng())
            if txt_eng == cau_goc[1]:
                txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
                self.mo_hinh_csdl.Cap_Nhat_Vie(id, txt_vie)
            else:
                if len(txt_eng) < 2:
                    self.hien_thi.text_eng.focus()
                    return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Anh không có nội dung')
                Kiem_tra_eng = self.mo_hinh_csdl.Lay_Eng(txt_eng)
                if len(Kiem_tra_eng) == 0:
                    txt_vie = self.Loc_Khoang_Trang(self.hien_thi.Lay_Txt_Vie())
                    self.mo_hinh_csdl.Cap_Nhat_Cau_Goc(id, txt_eng, txt_vie)
                else:
                    return self.hien_thi.Nhap_Trang_Thai('Câu tiếng Anh đã tồn tại')
            self.Lay_Trang_Danh_Sach()
            return self.hien_thi.Nhap_Trang_Thai(f'Câu có id={id} được cập nhật')
        
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
                    if len(cau_eng) == 0:
                        #Nhập câu mới
                        self.mo_hinh_csdl.Nhap_Cau_Goc(eng, vie)
                        nhap_moi +=1
                        continue #for du_lieu
                    else: #Ghi đè
                        #Câu tiếng Việt ít nhất phải có ít nhất 1 ký tự và khác câu tiếng Anh
                        for dong in cau_eng:
                            #Cập nhật câu tiếng Việt có id
                            self.mo_hinh_csdl.Cap_Nhat_Vie(dong[0], vie)
                            nhap_de +=1
                            break
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
                    cau_eng = self.mo_hinh_csdl.Lay_Eng(eng)
                    #Nếu câu tiếng anh KHÔNG tồn tại thì nhập câu mới
                    if len(cau_eng) == 0:
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
        if ten_tep !='' and self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(ten_tep):
            #Dọc dữ liệu từ tập tin
            du_lieu = self.mo_hinh_tep.Doc_XUnity(ten_tep)
            self.Luu_Du_Lieu_Vao_Csdl(du_lieu)
        else:
            self.hien_thi.Nhap_Trang_Thai('Không có tệp XUnity để xử lý')
        
    def Nhap_Tep_Json(self):
        '''Nhập dữ liệu từ tệp Json vào csdl'''
        hop_thoai = self.hien_thi.Hop_Thoai_Nhap('Json')
        print(hop_thoai)
        
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
    
    def Chuyen_Ngu(self, eng, co_dich = 0):
        '''Cố chuyển câu tiếng Anh sang tiếng Việt nhiều nhất có thể
        Đầu vào:
            eng: string #Câu tiếng Anh
            co_dich: int #Cố dịch = 1
        Đầu ra:
            vie: string #Câu tiếng Việt hoặc eng
        '''
        if len(eng) > 1:
            cau_eng = self.mo_hinh_csdl.Lay_Eng(eng)
            for cau in cau_eng:
                return cau[2]
            #Tách nhỏ câu ra để dịch
            if co_dich == 1:
                def Tach_Dich(eng, dau_cau):
                    '''Tách nhỏ câu theo dấu câu dau_cau rồi dịch'''
                    cau_dich = []
                    tach_cau = eng.split(dau_cau)
                    for cau in tach_cau:
                        cau_dich.append(self.Chuyen_Ngu(cau.strip(), 1))
                    return dau_cau.join(cau_dich)
                #Bọc câu bằng dấu bọc dau_boc để hy vọng tìm được giá trị tương ứng trong csdl
                dau_bocs = ['"', '\'']
                for dau_boc in dau_bocs:
                    eng_them_dau = dau_boc + eng + dau_boc
                    cau_eng = self.mo_hinh_csdl.Lay_Eng(eng_them_dau)
                    for cau in cau_eng:
                        vie = cau[2]
                        #Xóa dấu câu tránh gấp đôi
                        if vie[-1:] == dau_boc: #Cuối
                            if vie[:1] == dau_boc: #Đầu
                                return vie[1:-1] #Trừ đầu - cuối
                            return vie[:-1] #Trừ cuối
                        else: 
                            if vie[:1] == dau_boc:
                                return vie[1:] #Trừ đầu
                        return vie
                #Chia nhỏ câu theo dấu câu
                dau_caus = ['\n', '\\n', '.', '!', '?', ';', '…', ':'] #Điểm tách là dấu câu
                for dau_cau in dau_caus:
                    #Tách tại điểm tách và 1 ký tự rỗng theo sau
                    dau_cau_rong = dau_cau + ' '
                    if eng.find(dau_cau_rong) != -1:
                        return Tach_Dich(eng, dau_cau_rong)
                    #Tách tại điểm tách
                    if eng.find(dau_cau) != -1:
                        return Tach_Dich(eng, dau_cau)
                    #Thêm dấu câu dau_cau cuối câu để hy vọng tìm giá trị tương ứng có csdl
                    eng_them_dau = eng + dau_cau
                    cau_eng = self.mo_hinh_csdl.Lay_Eng(eng_them_dau)
                    for cau in cau_eng:
                        vie = cau[2]
                        #Xóa dấu câu tránh gấp đôi
                        do_dai = len(dau_cau)
                        if vie[-do_dai:] == dau_cau:
                            return vie[:-do_dai]
                        return vie
                #Tách câu theo dấu câu để cố dịch thử
                dau_bocs.append('-')
                for dau_boc in dau_bocs:
                    dau_cau_rong = ' ' + dau_cau + ' '
                    if eng.find(dau_cau_rong) != -1:
                        return Tach_Dich(eng, dau_cau_rong)
                    dau_cau_rong = dau_cau + ' '
                    if eng.find(dau_cau_rong) != -1:
                        return Tach_Dich(eng, dau_cau_rong)
                    dau_cau_rong = ' ' + dau_cau
                    if eng.find(dau_cau_rong) != -1:
                        return Tach_Dich(eng, dau_cau_rong)
                    if eng.find(dau_boc) != -1:
                        return Tach_Dich(eng, dau_boc)
                #Chia nhỏ theo thẻ html
                mau_html = '(<[\S\s]+>)'
                chuoi_tach = re.findall(mau_html, eng)
                for chuoi in chuoi_tach:
                    return Tach_Dich(eng, chuoi)
        return eng #Trả lại câu tiếng Anh
        
    def Xuat_Tep_XUnity(self):
        '''Dịch những câu có trong tệp nguồn XUnity rồi xuất ra tệp đích'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('XUnity')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_nguon']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp nguồn để xử lý')
        if len(hop_thoai['tep_dich']) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp đích để xuất ra')
        du_lieu = self.mo_hinh_tep.Doc_XUnity(hop_thoai['tep_nguon'])
        ket_qua = []
        for dong in du_lieu:
            cau_eng = self.Loc_Khoang_Trang(dong[0])
            if len(cau_eng) == 0:
                continue #Bỏ qua câu rỗng
            cau_vie = self.Loc_Khoang_Trang(dong[1])
            vie = self.Chuyen_Ngu(cau_eng, hop_thoai['co_dich'])
            #Nếu không dịch được thì trả lại kết quả cũ hoặc chính câu tiếng Anh
            if vie == cau_eng and len(cau_vie) != 0:
                ket_qua.append((dong[0], cau_vie))
            else:
                ket_qua.append((dong[0], vie)) #Dịch
        self.mo_hinh_tep.Ghi_XUnity(hop_thoai['tep_dich'], ket_qua)
        self.hien_thi.Nhap_Trang_Thai('Xuất dữ liệu kiểu XUnity ra tệp thành công')
        
    def Xuat_Tep_Json(self):
        '''Dịch những câu có trong tệp nguồn Json rồi xuất ra tệp đích'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('Json')
        print(hop_thoai)
        
    def Xuat_Tep_Csv(self):
        '''Dịch những câu có trong tệp nguồn Csv rồi xuất ra tệp đích'''
        hop_thoai = self.hien_thi.Hop_Thoai_Xuat('Csv')
        if not self.mo_hinh_tep.Kiem_Tra_Tep_Ton_Tai(hop_thoai['tep_nguon']):
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp nguồn để xử lý')
        if len(hop_thoai['tep_dich']) == 0:
            return self.hien_thi.Nhap_Trang_Thai('Không có tệp đích để xuất ra')
        du_lieu_csv = self.mo_hinh_tep.Doc_Csv(hop_thoai['tep_nguon'], hop_thoai['dau_phan_cach'])
        so_cot_tieu_de = len(du_lieu_csv['tieu_de'])
        if hop_thoai['cot_eng'] >= so_cot_tieu_de:
            return self.hien_thi.Nhap_Trang_Thai('Cột tiếng Anh không tồn tại')
        #Thêm mã 'vi' vào cuối tiêu đề
        if hop_thoai['cot_vie'] >= so_cot_tieu_de:
            du_lieu_csv['tieu_de'].append('vi')
        kq_du_lieu = []
        for dong in du_lieu_csv['du_lieu']:
            so_dong = len(dong)
            #Cột tiếng Anh không tồn tại
            if hop_thoai['cot_eng'] >= so_dong:
                continue
            cau_eng = self.Loc_Khoang_Trang(dong[hop_thoai['cot_eng']])
            vie = self.Chuyen_Ngu(cau_eng, hop_thoai['co_dich'])
            #Nếu cột Việt không tồn tại thì thêm vào cuối
            if hop_thoai['cot_vie'] < so_dong:
                dong[hop_thoai['cot_vie']] = vie
            else:
                dong.append(vie)
            kq_du_lieu.append(dong)
        du_lieu_csv['du_lieu'] = kq_du_lieu
        self.mo_hinh_tep.Ghi_Csv(hop_thoai['tep_dich'], du_lieu_csv, hop_thoai['dau_phan_cach'])
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
        