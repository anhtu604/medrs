# Hợp đồng phán định tuân thủ

Đơn vị phán định là một mục của chuẩn, định danh đúng như `expected_ids` trong manifest. Không gộp mục, không tách mục, không đổi tên.

## Bốn phán định

| Phán định | Điều kiện | Bắt buộc kèm |
|---|---|---|
| `ĐÃ_BÁO_CÁO` | Nội dung mục có mặt và định vị được trong bản thảo | Vị trí chính xác: mục, trang, bảng hoặc hình |
| `BÁO_CÁO_MỘT_PHẦN` | Có đề cập nhưng thiếu thành phần mà mục yêu cầu | Vị trí, và thành phần nào còn thiếu |
| `CHƯA_BÁO_CÁO` | Không tìm thấy nội dung mục | Nơi đã tìm |
| `KHÔNG_ÁP_DỤNG` | Thiết kế không phát sinh nội dung này | Lý do theo thiết kế, không phải theo tiện lợi |

Không có vị trí cụ thể thì không phải `ĐÃ_BÁO_CÁO`. Cảm giác rằng nội dung "có ở đâu đó" không thay được một locator.

`KHÔNG_ÁP_DỤNG` là phán định hẹp. Nghiên cứu không có làm mù thì mục làm mù không áp dụng; nhưng nghiên cứu quên báo cáo cỡ mẫu thì đó là `CHƯA_BÁO_CÁO`, không phải không áp dụng.

## Thứ tự làm việc

1. Nạp manifest tương ứng và đọc `expected_ids`. Số mục xử lý phải bằng đúng số định danh trong danh sách đó.
2. Với mỗi mục, dùng `operational_prompt` làm tiêu chí và tìm trong bản thảo.
3. Ghi phán định kèm locator.
4. Đối chiếu lại: mọi định danh trong `expected_ids` đều phải có đúng một phán định. Thiếu một mục là lỗi chặn, không phải bỏ qua được.

## Xếp mức ưu tiên

Các mục chưa đạt được xếp theo hậu quả với người đọc, không theo thứ tự xuất hiện:

- **Chặn** — thiếu nội dung khiến không thể diễn giải hay tái lập kết quả: thiết kế, dân số, định nghĩa kết cục chính, cỡ mẫu, phương pháp thống kê, số đối tượng ở từng giai đoạn.
- **Nặng** — thiếu nội dung làm suy yếu đáng kể độ tin cậy: xử lý dữ liệu khuyết, phân tích phụ, xung đột lợi ích, nguồn tài trợ, đăng ký nghiên cứu.
- **Nhẹ** — thiếu nội dung chủ yếu ảnh hưởng tính đầy đủ hình thức.

Không quy đổi các mức này thành một điểm phần trăm tuân thủ. Một bản thảo đạt 90% mục nhưng thiếu định nghĩa kết cục chính thì không phải là bản thảo tốt.

## Giới hạn

Chuẩn báo cáo đo tính đầy đủ của báo cáo, không đo chất lượng thiết kế hay nguy cơ sai lệch. Một nghiên cứu yếu vẫn có thể đạt đủ mục nếu nó báo cáo trung thực cái yếu của mình. Nêu rõ điều này trong kết quả và chuyển đánh giá nguy cơ sai lệch cho `danh-gia-chat-luong-bang-chung`.

Không tự sửa bản thảo ở bước này. Đề xuất bổ sung được chuyển cho skill viết tương ứng.
