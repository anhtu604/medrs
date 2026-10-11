# MedRS — sử dụng trong Claude Cowork

Một plugin, 28 skill liên kết nội bộ. Bắt đầu bằng /medrs và mô tả việc
cần làm, kèm thư mục dự án hoặc bản thảo mới nhất. Leader lập kế hoạch,
tái dùng quyết định đã xác nhận và kiểm nội dung cùng hình thức trước giao.
Các skill chuyên môn được gọi nội bộ, không cần nhớ 28 lệnh.

Ví dụ: /medrs tiếp nhận luận văn đang dở, đọc bản mới nhất, lập README và
hồ sơ nghiên cứu nháp; sửa phương pháp và bố cục theo nguồn tôi cung cấp.

Mỗi dự án phải có README mô tả mục tiêu, thiết kế, quyết định và tiến độ;
final/ chỉ giữ bộ đã nghiệm thu hiện hành; history/YYYY-MM-DD/ giữ trung
gian, toàn bộ log và ghi chú thay đổi. Không xóa lịch sử khi nâng cấp.
Tác giả quyết định trạng thái dữ liệu; chưa xác nhận dữ liệu thật đã thay
thì không tự xóa nhãn mô phỏng. Những phần chưa xác minh được viết có điều
kiện, không khẳng định chắc chắn.

## Word và dữ liệu

Tách bố cục nội dung khỏi định dạng Word. Style, mục lục, danh mục,
cột bảng và bullet được kiểm trên file sinh ra. Sau sửa phải lưu, refresh,
mở lại, render và soi đúng file cuối; sửa tiếp làm receipt cũ hết giá trị.
Thiếu Word/UNO/render: chỉ giao bản chưa nghiệm thu hình thức, không báo đạt.
Word COM chỉ có trên Windows cục bộ với Word và runtime phù hợp; máy chủ
Windows không chứng minh VM Cowork có COM. UNO cần LibreOffice, Python UNO
và kiểm thực tế ở bề mặt đang chạy. R/Stata chỉ thực thi khi có runtime.

Giữ trường Zotero, chú thích và chỉnh sửa của tác giả; không coi text trích
dẫn hiển thị là liên kết Zotero hợp lệ. CK2/đề tài cơ sở mặc định cơ bản,
bám câu hỏi nghiên cứu, không tự thêm phân tích nâng cao hoặc nội dung màu mè.

## Giới hạn phải nhìn thấy

Đọc [nguồn và nghiệm thu còn thiếu](docs/source-gaps.md) trước yêu cầu chứng nhận
chuẩn trường/tạp chí. Metadata CURRENT không thay thế file nguồn thực tế.
Checklist hạn chế bản quyền cần bản gốc hợp lệ tại thời điểm dùng; không
đánh giá toàn bộ công cụ từ bản đồ mục ngắn hoặc trí nhớ.

Cowork dùng tài nguyên trong skills/, profiles/, coverage/, schemas/.
Không cần thư mục src/ hoặc scripts/ của repo. Đây là gói đang kiểm thử
trên nhánh nâng cấp, chưa được chứng nhận hoàn thành toàn bộ phạm vi.
Không tự gửi file sang AI khác; cần đồng ý riêng về đích và dữ liệu.

/medrs là entrypoint trên host hỗ trợ plugin Claude, không phải lệnh chạy
được mặc định trên mọi chat. ChatGPT Chat/Work cần adapter hoặc đính kèm
thủ công; cài repo cục bộ không tự kết nối sandbox đám mây.

Giấy phép MedRS: CC BY-NC 4.0; kiểm điều kiện trước dùng thương mại.
