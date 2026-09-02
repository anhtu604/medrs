# Protocol versus completed-study mode

| Câu hỏi | Protocol | Completed study |
|---|---|---|
| Thủ thuật | `PLANNED`; mô tả như kế hoạch | Chỉ `CONFIRMED_EXECUTED` |
| Thời gian/địa điểm | dự kiến nếu chưa xác nhận | giá trị thực có provenance |
| Cỡ mẫu | mục tiêu và giả định đã duyệt | số đã tuyển chỉ từ dữ liệu xác nhận |
| Phân tích | kế hoạch định trước | phân tích đã thực hiện và sai lệch đã xác nhận |
| Đạo đức | trạng thái nộp/đang chờ | số/ngày chấp thuận chỉ từ chứng từ |
| Sai lệch | nêu quy tắc xử lý dự kiến | liệt kê sai lệch thực và lý do |

Một câu về quy trình đã hoàn tất cần provenance đến bản ghi, log, báo cáo hoặc xác nhận tác giả. Nếu không có, bỏ câu khỏi bản hoàn tất và gắn `DATA_REQUIRED`; không suy ra từ thì quá khứ trong bản thảo cũ.
