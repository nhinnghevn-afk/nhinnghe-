# Nhìn Nghề — nội dung bản xem trước

Trang chủ và phần dùng chung được triển khai theo bản hợp nhất ngày 16/11/2026.

## Nguồn quản lý

- `site.json`: nhận diện, năm mục menu, liên hệ và trạng thái bản xem trước.
- `home.html`: sáu khối nội dung Trang chủ đã biên tập.
- `privacy.html`: nội dung giải thích chức năng lưu trên thiết bị và liên hệ.
- `activities.json`: bản ghi từng sự kiện và quy tắc biên tập theo trạng thái.
- `activities-copy.json`: nội dung trang Hoạt động và trang chuỗi.
- `dist/career-articles.json`: tiêu đề và lời dẫn ba bài viết.
- `dist/student-programs.json`: nhãn trạng thái chương trình.
- `dist/school-public-data.json`: dữ liệu công khai chọn lọc; không thay bằng gói nội bộ.

Tạo lại Trang chủ, các trang hoạt động và thành phần chung theo thứ tự:

```sh
python scripts/build-home-common.py
python scripts/build-activities.py
```

## Kiểm tra ngày 16/11/2026

- 18 đích nội dung: một tiêu đề chính, một vùng nội dung chính, menu/chân trang thống nhất.
- Liên kết nội bộ, mốc nội dung và tệp được tham chiếu đều có đích.
- Kiểm tra bố cục trình duyệt ở chiều rộng máy tính 1348px và khung điện thoại 390px: không tràn ngang trên 18 trang; khung 900px của Trang chủ cũng đạt.
- Menu mở/đóng, Enter/Escape, liên kết bỏ qua điều hướng và trạng thái trang đang xem hoạt động.
- Các lối vào đối tượng dẫn đúng nội dung; phần hướng dẫn phụ huynh tự mở khi đi đến mốc liên kết.
- Tìm ngành xóa phần chi tiết cũ khi không còn khớp; lọc vùng trường hoạt động.
- Lưu nghề, ghi chú, tải lại để khôi phục, hủy xóa và xác nhận xóa đã kiểm tra qua giao diện.
- Kiểm tra bố cục in bằng cách áp dụng các quy tắc CSS dành cho in: hiển thị ghi chú, ẩn menu/chân trang/nút vận hành. Không kiểm tra máy in vật lý.
- Nội dung chính của 16 trang hoàn thiện trước đó không đổi; cùng bộ tên 25 nghề trên trang sách và phát triển năng lực; dữ liệu công khai có 57 ngành và ba nguồn trường chọn lọc.
- Việc tạo lại các trang cho kết quả ổn định. Tệp kiểm tra tạm không nằm trong bản phát hành.

## Phạm vi còn giữ nguyên

Chỉ cập nhật địa chỉ xem trước, giữ quyền xem hiện tại. Chưa kết nối nhinnghe.vn; chưa mở đăng ký, tài khoản, tải tệp hoặc thanh toán. Hai sự kiện vẫn dự kiến và chưa xác nhận tổ chức. Nguồn DUE vẫn chờ xác minh trong hồ sơ biên tập, không thêm vào dữ liệu công khai. Không đưa sách đầy đủ, dữ liệu tư vấn nội bộ hoặc bản lưu trước sửa vào `dist/`.


## Cụm chương trình đầu tiên — 16/11/2026

- `dist/school-programs.json` quản lý đúng 10 lựa chọn công khai đã chốt trong bảng đối chiếu v2: NEU 7, UEF 2, RMIT 1. Không chứa bảng đối chiếu đầy đủ hoặc dữ liệu tư vấn nội bộ.
- `school-public.js` nối ngành đang xem → danh sách chương trình → hồ sơ phương thức xét tuyển. Chọn chương trình đưa tiêu điểm đến hồ sơ tương ứng; đổi ngành hoặc bộ lọc sẽ xóa hồ sơ không còn nằm trong kết quả.
- Cụm Quản trị kinh doanh có cả lựa chọn cùng tên và chương trình kinh doanh mở rộng, ghi nhãn riêng. BP343 là mã chương trình RMIT, không gán thành mã ngành Việt Nam.
- NEU và UEF dùng thông tin tuyển sinh 2026 để tham khảo. RMIT ghi lịch kỳ nhập học 2027 trên trang chương trình và yêu cầu kiểm tra lại điều kiện hiện hành trước khi nộp.
- Ba cổng trường NEU, UEH, UEL trước đây vẫn có trong phần tra cứu thêm, tách khỏi danh sách chương trình theo ngành.
- Danh sách lưu trên thiết bị tiếp tục lưu nghề/ngành/trường độc lập, chưa lưu cấu trúc chương trình/năm. Hướng dẫn người đọc ghi thêm mã và năm nguồn.
- Đã kiểm giao diện máy tính 1363px và khung điện thoại 390px: không tràn ngang; mở hồ sơ NEU, UEF Tài năng và RMIT đúng nội dung; tìm UEF trả hai lựa chọn; vùng Trung có thông báo rỗng và nút đặt lại; đổi sang Kế toán báo chưa có chương trình đã kiểm và xóa hồ sơ xét tuyển trước đó.
- Đã kiểm cú pháp JS, số lượng/ID/URL của 10 mục, liên kết/tệp/mốc nội bộ trên 18 trang. Giữ nguyên phạm vi bản xem trước, không kết nối tên miền chính thức và không mở đăng ký.


## Nguyên tắc công khai và đồng hành — 16/11/2026

Đã chốt: mở rộng danh mục cơ bản theo phần đã xác minh; giá trị dịch vụ là giúp gia đình so sánh, cân nhắc lựa chọn và xây bước chuẩn bị. Không làm mờ danh mục chưa xác minh như nội dung phải trả phí.

Phần Học ở đâu có hai khối: thông tin cơ bản miễn phí và phạm vi đồng hành. Liên kết Tìm hiểu hình thức đồng hành dẫn đến phần giải thích ngay trên trang; hình thức/chi phí/khả năng tiếp nhận vẫn chờ công bố, chưa mở đăng ký. Danh mục hiện tại giữ 10 lựa chọn đã chốt, không bổ sung tự động từ dữ liệu nội bộ.


## Một hồ sơ mẫu và 24 hồ sơ khám phá — 17/11/2026

- Hồ sơ mẫu công khai: `/hoc-sinh/ho-so-mau/quan-ly-du-an-van-hanh/`, nhóm 14. Biên tập chọn lọc từ Career Playbook nhóm 14 (A1–A2, C3, D1) và bản đồ nghề–ngành nội bộ mới; không xuất toàn bộ sách, bộ rubric, tài liệu thực hành hoặc bảng phân tích.
- Mẫu có hai nhánh nghề, năm ví dụ ngành theo ba mức nền tảng, câu hỏi đọc chương trình, bài thử giả định theo hai nhánh và bước tìm hiểu tiếp. Năm ngành được chọn: Quản lý dự án, Quản trị kinh doanh, Hệ thống thông tin quản lý, Quản trị nhân lực, Bất động sản. Mức minh họa ở cấp ngành, chưa kết luận cho từng chương trình/trường.
- Dữ liệu công khai đánh dấu đúng một `profileKind: sample` và 24 `basic`. Cả 25 mục vẫn có công việc, kết quả, nền tảng, ít nhất hai ngành gợi mở và bài thử có đầu ra; không có hồ sơ chỉ gồm tên hoặc nút khóa trả phí. Chỉ bổ sung liên kết mẫu và lời mời đồng hành cho phần đối chiếu cá nhân.
- Liên kết mẫu có ở đầu phần Nghề và trong từng hồ sơ. Tham số `nghe=14` cho phép mở trực tiếp phần tóm tắt mẫu. Trường và xét tuyển tiếp tục dùng đúng mười lựa chọn trước đó; không phân loại nghề–chương trình tự động từ mức cấp ngành.
- Đã đơn giản hóa lời giới thiệu danh mục trường và bỏ đoạn giải thích chuẩn bị dịch vụ từng gây khó hiểu. Giữ trạng thái chưa mở đăng ký ở thanh bản xem trước và không tạo nút đăng ký.
- Kiểm tra: dữ liệu 1+24, JavaScript, liên kết/tệp/mốc trên 19 trang; giao diện máy tính và khung điện thoại 390px, bảng chỉ cuộn trong vùng riêng; mở nhóm 14 và nhóm 06 cho thấy đúng loại hồ sơ, ngành và lời mời đồng hành. Không đưa dữ liệu phân tích đầy đủ hoặc dữ liệu cá nhân vào bản phát hành.
