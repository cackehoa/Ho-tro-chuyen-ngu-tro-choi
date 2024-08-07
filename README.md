# Ứng dụng hỗ trợ chuyển ngữ trò chơi
Đây là ứng dụng hỗ trợ chuyển ngữ trò chơi viết bằng [Python](https://www.python.org/)
(Không phải ứng dụng chuyển ngữ, dịch thuật)

# Lời nói đầu:
- Bạn dịch game, website, app... nhưng chúng liên tục cập nhật bạn phải dịch lại và tìm kiếm khác biệt gây khó khăn mất thời gian cho bạn
- Bạn thường xuyên dịch nhưng không có tiền mua API dịch và không thích kết quả của công cụ dịch miễn phí lắm
- Bạn muốn dịch nhanh một phần cơ bản trong trò chơi như: cài đặt
- Bạn muốn lưu trữ những phần dịch trước đây của mình và tra cứu khi cần

Công cụ này của mình phát triển nhằm hỗ trợ những bạn dịch thuật nhưng không có nhiều tiền để trả cho các công cụ dịch online và muốn tự tạo từ điển cho mình từ những gì mình đã dịch để áp dụng sau này hoặc muốn share cho nhau.

# Ý tưởng cơ bản:
- Công cụ sẽ học từ các bản dịch trước đó của bạn sau đó ghi nhớ lại vào cơ sở dữ liệu và áp dụng cho các bản dịch sau. Tất nhiên cho phép bạn tự nhập và tự cập nhật và thay đổi bản dịch nếu cần.
- Có thể dùng googletrans để dịch những câu mới nhưng phiên bản miễn phí nên dịch hơi cùi (phần này mình hiện tại chỉ lên ý tưởng chưa phát triển)
- Đưa vào bản dịch càng hoàn chỉnh thì bản dịch ra càng tốt (dự định sử dụng AI nhưng chỉ trên dự định thôi)
- Mình dùng tkinter để tạo GUI hiển thị dữ liệu (hien_thi)

# Ưu điểm:
- Chương trình có thể học nhanh từ bản dịch có sẵn sau khi so sánh với bản gốc
- Dịch nhanh được các từ khóa cơ bản trong một diện hẹp nào đó. VD: trong game sẽ dịch nhanh
````Full screen````
thành
````Toàn màn hình````
- Dịch được các câu cơ bản chính xác theo ý bạn vì bạn đã lưu nó vào cơ sở dữ liệu
- Giúp dịch nhanh bản cập nhật mới nhất bằng cách học bản dịch trước đó và để lại các thay đổi chưa dịch
- Giúp bạn tạo ra bản dịch ít lỗi nhất
- Cùng một câu có thể cho phép bạn có nhiều bản dịch và chọn 1 phiên bản mà bạn cho là ok nhất (mặc định là bản dịch đầu tiên nhập vào, mới lên ý tưởng máy học AI chưa phát triển)
- Có thể share cơ sở dữ liệu lẫn nhau một cách đơn giản (chỉ copy tệp database.db cho nhau thôi)

# Khuyết điểm:
- Rất rõ ràng là không dịch được những gì chưa có trong cơ sở dữ liệu hoặc chưa được học (AI mới chỉ là ý tưởng ban đầu chưa áp dụng)
- Không hỗ trợ nhiều kiểu định dạng (hiện tại mình dự kiến hỗ trợ chuẩn **json** và một số chuẩn khác trong khi mình dịch game thấy được)
- Phải bỏ nhiều thời gian tự mình cập nhật dữ liệu để chương trình ngày càng hoàn thiện (mình dịch khá nhiều game và thấy phải dịch lặp đi lặp lại một số từ một số câu thông dụng rất mất công)
- Khi tự học không xác định được câu dịch đúng và sai. Mình sẽ để bản dịch có sẵn thành mặc định và bạn có thể tự chọn bản dịch bạn cho là hay nhất nếu muốn.
- Không hỗ trợ nhiều ngôn ngữ (Thay vì Anh-Việt bạn có thể sử dụng nó như Trung-Việt, Hàn-Việt,Việt-Pháp tùy bạn muốn nhưng mình đề nghị bạn không nên dùng đa ngôn ngữ kiểu Anh+Trung+Hàn - Việt vì nó không tối ưu và chạy rất chậm và làm cơ sở dữ liệu phồng to)
- Không hỗ trợ nhiều ngành (tốt nhất bạn nên tạo nó cho một ngành biệt lập nào đó thì bản dịch sẽ tốt nhất có thể theo ngành ấy)
- Chạy khá chậm do không viết chạy trên nhiều luồng (thread) đây cũng là hạn chế của [SQLite](https://www.sqlite.org/) và trình độ của mình

# Ngôn ngữ lập trình
Tại sao chọn [Python](https://www.python.org/): vì nó khá là đơn giản và tiện (được hỗ trợ rất nhiều và không quá phức tạp lại hỗ trợ unicode)

Bạn có thể chạy trên nhiều hệ điều hành khác nhau chứ không bị giới hạn ở 1 hệ điều hành nào đó do trình biên dịch

Phiên bản [Python](https://www.python.org/) mình đang làm việc: 3.9

Mình sẽ không hướng dẫn bạn cài [Python](https://www.python.org/) hoặc những vấn đề liên quan.

# Cơ sở dữ liệu:
Mình chọn [SQLite](https://www.sqlite.org/) vì nó đơn giản và tiện (đỡ mất công cài đặt, chạy máy ảo và dễ dàng share cho nhau)

Mình nghĩ sau này sẽ viết code để trộn 2 cơ sở dữ liệu lại với nhau thành một cơ sở dữ liệu mới tổng hợp những gì đã có sẵn (mới lên ý tưởng, giờ chưa đâu)

Tệp cơ sở dữ liệu mình share trên này đã nhập một số kết quả việt hóa một số game của mình.

# Mô hình MVC:
Mình dự tính sẽ phát triển ứng dụng nhiều hơn nếu cần nên mình sử dụng mô hình MVC và hướng đối tượng

Ai rành CNTT thì góp ý cho mình nhé, mình tự tìm hiểu và làm theo ý của bản thân thôi

# Thư viện cần cài đặt:
Hiện tại mới mới bắt đầu viết nên tạm thời sử dụng thư viện mặt định có sẵn của [Python](https://www.python.org/)

# Tên biến & chú thích:
Mình phát triển cho chính mình sử dụng nên tên biến, đối tượng, lớp, ngôn ngữ hiển thị - chú thích đều là tiếng Việt (chưa có ý định đa ngôn ngữ hóa và nói thật là mình rất ngu tiếng Anh nên không đặt tên biến là tiếng Anh vì có thể sau này mình không nhớ biến đó tiếng Anh là cái quái gì)

# Tập tin & định dạng hỗ trợ:
## 1. [Json](https://www.json.org/) (\*.json):
Ví dụ
````
{
	'English': 'Tiếng Anh',
	'Hello': 'Xin chào'
}
````

Tôi đã gặp khi việt hóa game: Subnautica, [Subnautica below zero](https://github.com/cackehoa/Subnautica-Below-Zero-viet-hoa), [Stonehearth](https://github.com/cackehoa/Mod-Stonehearth-viet-hoa)
## 2. CSV (\*.csv):
Ví dụ
````
id,eng,vie
language,English,Tiếng Việt
````


Biến thể thường hay thấy khi mình dịch game:
````
id*eng*vie
language*English*Tiếng Việt
````

Tôi đã gặp khi việt hóa game: [Surviving Mars](https://github.com/cackehoa/Mod-Surviving-Mars-Viet-Hoa), thường các game unity có tệp loại textaset
## 3. XUnity (\*.txt):
Ví dụ
````
English=Tiếng Anh
Hello=Xin chào
````

Tôi đã gặp khi việt hóa game: DoorKickers, [Car Mechanic Simulator](https://github.com/cackehoa/Car-Mechanic-Simulator-2018-Mercedes-Benz-viet-hoa)
## 4. INI (\*.ini):
Ví dụ
````
English=Tiếng Anh
Hello=Xin chào
````

## 5. Lua (\*.lua):
Ví dụ:
````
English = "Tiếng Anh",
Hello = "Xin chào",
Animal = {
	Dog = "Chó",
	Cat = "Mèo"
}
````

# Trò chơi chuyên biệt:
Đây là một số định dạng được viết chuyên cho một số trò chơi chuyên biệt mà mình gặp và chỉ đúng với trò chơi đó. Nếu bạn áp dụng vào định dạng khác có thể cho ra kết quả không mong muốn.

## 1. Dịch XML thành ProjectZombie
Dùng để dịch tiệp chuẩn xml trong ProjectZombie sang định chuẩn khác khi việt hóa

## 2. Avorion
Dành riêng khi dịch trò chơi Avorion

# Hướng dẫn sử dụng chi tiết:
Xem thêm tag Wiki nhé
# Liên lạc và ủng hộ
- Ủng hộ tại: [Playerduo](https://playerduo.net/cackehoa)
- Fanpage: [fackebook](https://www.facebook.com/cackehoa)
- Discord: [Discord](https://discord.gg/Z5C98FG)
- Youtube: [Cắc kè hoa](https://www.youtube.com/c/Cắckèhoa)
