# Hợp đồng truy cập thư viện trích dẫn

## Chọn backend

Khai báo đúng một backend trước khi truy vấn, và nêu lại backend đó trong kết quả.

| Backend | Điều kiện dùng | Giới hạn |
|---|---|---|
| Zotero cục bộ | Host chạy trên máy tác giả và đọc được tệp `zotero.sqlite` | Không dùng được trên sandbox web hoặc Cowork từ xa |
| Tệp xuất BibTeX/RIS/CSL-JSON | Tác giả cung cấp tệp xuất | Ảnh chụp tại một thời điểm; không phản ánh thay đổi sau đó |
| Không có thư viện | Tác giả chỉ đưa danh mục trong bản thảo | Không kiểm chứng được toàn văn; mọi phán định dừng ở mức siêu dữ liệu |

Nếu backend cần thiết không khả dụng, trả `CAPABILITY_UNAVAILABLE` kèm tên backend, lý do, và đường đi thay thế. Không suy đoán nội dung thư viện, không dựng bản ghi giả để minh họa.

## Bất biến chỉ-đọc

Thư viện là tài sản của tác giả và là bản ghi công việc của họ.

- Không ghi, sửa, xóa, gắn thẻ, gộp trùng, hay dọn thùng rác trong mọi trường hợp.
- Không sao chép toàn bộ cơ sở dữ liệu sang nơi khác; đọc tại chỗ.
- Mở kết nối ở chế độ chỉ-đọc bất biến để không tranh chấp khóa ghi khi ứng dụng Zotero đang mở.
- Nêu rõ giới hạn: chế độ bất biến bỏ qua nhật ký ghi trước, nên thay đổi vừa thực hiện trong ứng dụng có thể chưa hiện ra. Khi tác giả nói vừa thêm tài liệu mà không thấy, yêu cầu họ đóng hoặc để Zotero nghỉ rồi đọc lại; không kết luận tài liệu không tồn tại.

## Quy tắc truy vấn

- Phân giải định danh trường theo tên tại thời điểm chạy từ bảng `fields`; số định danh thay đổi giữa các phiên bản Zotero lớn, nên mọi số cố định đều sai sớm hay muộn.
- Loại trừ mục nằm trong `deletedItems` khỏi mọi truy vấn, trừ khi tác giả yêu cầu rõ ràng tính cả thùng rác. Tài liệu đã bị tác giả loại vẫn nằm trong bảng `items` cho tới khi thùng rác được dọn.
- Truy vấn trên toàn bộ thư viện, kể cả thư viện nhóm trong bảng `groups`, trừ khi tác giả giới hạn phạm vi. Liệt kê các thư viện sẵn có ở đầu phiên để tác giả gọi theo tên.
- Không tin số đếm ghi sẵn ở bất kỳ tài liệu nào, kể cả tài liệu này; đếm bằng truy vấn trực tiếp.

## Ghi vết

Mỗi lần đọc thư viện ghi lại: backend, phạm vi thư viện và bộ sưu tập, thời điểm đọc, số bản ghi khớp, và tiêu chí lọc. Không có ghi vết thì kết quả không tái lập được và phải báo là chưa kiểm chứng.

## Trạng thái bản ghi

- `RESOLVED` — có định danh bền vững (DOI, PMID, PMCID) đã đối chiếu với bản ghi nguồn.
- `UNRESOLVED` — thiếu định danh bền vững, hoặc chỉ khớp theo nhan đề. Giữ nguyên trạng thái này cho tới khi tác giả xác nhận; không tự nâng cấp.
- `RETRACTED` — nằm trong danh sách thu hồi. Báo trước mọi phán định khác.

Không tự tạo mục tham khảo mới, không tự điền trường còn trống, và không đoán năm hay tạp chí từ nhan đề.
