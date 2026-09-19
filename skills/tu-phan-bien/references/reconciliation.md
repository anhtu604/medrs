# Đối chiếu hai vòng và chuyển sang sửa

Chỉ mở bước này khi cả hai vòng đã xong và đã ghi lại riêng biệt. Hai báo cáo vòng được giữ nguyên trong kết quả cuối; đối chiếu là lớp thêm vào, không thay thế chúng.

## Ghép phát hiện

Hai phát hiện được coi là cùng một vấn đề khi chúng trỏ tới cùng vị trí **và** cùng nguyên nhân. Cùng vị trí nhưng khác nguyên nhân là hai phát hiện riêng.

| Trạng thái | Nghĩa | Xử lý |
|---|---|---|
| `ĐỒNG_THUẬN` | Cả hai vòng nêu cùng vấn đề | Ưu tiên cao nhất trong danh mục sửa |
| `MỘT_VÒNG` | Chỉ một vòng nêu | Giữ nguyên giá trị; ghi rõ vòng nào nêu |
| `MÂU_THUẪN` | Hai vòng kết luận ngược nhau về cùng một chỗ | Trình bày cả hai lập luận cho tác giả quyết |

`MỘT_VÒNG` không phải là phát hiện yếu hơn. Hai góc soi khác nhau nên phần lớn phát hiện thật sẽ chỉ xuất hiện ở một vòng; coi nhẹ chúng là đánh mất chính lý do chạy hai góc.

Số lượng phát hiện đồng thuận không phải là thước đo chất lượng bản thảo. Không quy đổi kết quả đối chiếu thành một điểm số.

## Mâu thuẫn

Khi hai vòng nói ngược nhau, không tự chọn bên và không lấy trung bình. Trình bày: vị trí, lập luận của từng vòng, và thông tin nào sẽ giải quyết được bất đồng. Thường thì mâu thuẫn chỉ ra một chỗ bản thảo viết chưa rõ, chứ không phải một trong hai vòng sai.

## Danh mục sửa

Sắp theo mức độ, trong cùng mức thì `ĐỒNG_THUẬN` lên trước. Mỗi mục ghi: vị trí, mô tả vấn đề, mức, trạng thái đối chiếu, skill sẽ xử lý, và việc sửa có cần dữ liệu hay phân tích mới không.

Mục cần chạy lại phân tích hoặc cần dữ liệu chưa có không được chuyển thành sửa câu chữ. Đánh dấu `CẦN_DỮ_LIỆU` và để tác giả quyết.

## Cổng duyệt

Không sửa gì trước khi tác giả duyệt danh mục. Tác giả có quyền bác bỏ bất kỳ phát hiện nào; ghi lại việc bác bỏ kèm lý do thay vì lặng lẽ bỏ qua hoặc tự ý làm.

## Chuyển sang sửa

Mỗi mục đã duyệt đi qua skill phụ trách miền của nó: phần viết cho skill viết tương ứng, thống kê cho `phan-tich-so-lieu`, bằng chứng cho `tong-hop-bang-chung` hoặc `danh-gia-chat-luong-bang-chung`, trích dẫn cho `quan-ly-trich-dan`, văn phong cho `kiem-van-phong`, chuẩn báo cáo cho `kiem-chuan-bao-cao`, bố cục và định dạng cho `bo-cuc-tai-lieu` và `dinh-dang-tai-lieu`.

Không sửa trực tiếp trong skill này. Việc sửa nằm ở nơi có hợp đồng của miền đó.

## Sau khi sửa

Bản thảo sau sửa mang hash mới, nên mọi phát hiện gắn hash cũ mất hiệu lực. Kiểm lại từng mục đã sửa trên artifact mới và ghi trạng thái: đã xử lý, xử lý một phần, hoặc tác giả từ chối.

Một chu kỳ hai vòng mới chỉ cần thiết khi sửa đã chạm thiết kế, phân tích hay kết luận. Sửa câu chữ không kích hoạt chu kỳ mới.
