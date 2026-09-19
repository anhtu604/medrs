# Chọn dạng hình theo mệnh đề

Chọn dạng hình từ mệnh đề cần đỡ, không từ dạng hình quen tay.

## Bản đồ mệnh đề sang dạng hình

| Mệnh đề cần đỡ | Dạng thường đúng | Ghi chú |
|---|---|---|
| So sánh giá trị giữa vài nhóm | Cột có thanh sai số, hoặc chấm theo nhóm | Ít nhóm và cần số chính xác thì bảng mạnh hơn |
| Mô tả phân bố một biến liên tục | Hộp, violin, raincloud, histogram | Cỡ mẫu nhỏ thì vẽ luôn từng điểm |
| Quan hệ giữa hai biến liên tục | Chấm phân tán kèm đường khớp và dải tin cậy | Nêu rõ mô hình khớp; không kéo dài ngoài miền số liệu |
| Diễn tiến theo thời gian | Đường | Trục thời gian theo tỷ lệ thật, không theo thứ tự lần khám |
| Thời gian đến biến cố | Kaplan–Meier kèm bảng số còn lại theo dõi | Thiếu bảng số còn lại là hình chưa đủ |
| Khả năng phân biệt của mô hình chẩn đoán | ROC kèm giá trị AUC và khoảng tin cậy | Kèm điểm cắt chỉ khi điểm cắt đã tiền định |
| Mức độ hiệu chuẩn của mô hình tiên lượng | Đường hiệu chuẩn | Không thay bằng ROC; hai thứ trả lời hai câu hỏi khác nhau |
| Mức đồng thuận giữa hai phép đo | Bland–Altman | Không dùng hệ số tương quan để kết luận đồng thuận |
| Hiệu quả gộp qua nhiều nghiên cứu | Forest | Nội dung lấy từ `tong-hop-bang-chung`, không tự gộp |
| Bất đối xứng trong tổng hợp | Funnel | Chỉ vẽ khi số nghiên cứu đủ theo hợp đồng tổng hợp |
| Dòng chảy đối tượng qua nghiên cứu | Sơ đồ dòng chảy theo chuẩn báo cáo | Mục và nhãn lấy từ skill giữ nguồn chuẩn báo cáo |

Sơ đồ dòng chảy theo chuẩn báo cáo không được dựng lại từ trí nhớ. Lấy danh mục mục và nhãn từ skill đang giữ nguồn chuẩn đó; thiếu nguồn thì báo chặn.

## Dạng nên tránh

- Hình tròn và hình vành khuyên khi cần so sánh chính xác; mắt người so góc kém hơn so chiều dài.
- Biểu đồ radar trừ khi so sánh thật sự là một hồ sơ nhiều chiều với ít nhóm.
- Hiệu ứng ba chiều, đổ bóng, chuyển màu trang trí: làm sai lệch tương quan diện tích mà không thêm thông tin.
- Cột chỉ vẽ trung bình khi phân bố lệch hoặc cỡ mẫu nhỏ; vẽ luôn phân bố.
- Trục tung không bắt đầu từ mốc có nghĩa nhằm làm khác biệt trông lớn hơn. Khi phải cắt trục, đánh dấu chỗ cắt rõ ràng và nói lý do trong chú thích.
- Hai trục tung khác đơn vị trên cùng một hình: quan hệ nhìn thấy phụ thuộc vào cách chọn thang, không phải vào số liệu.
- Dùng màu làm kênh thông tin duy nhất; thêm hình dạng, kiểu nét hoặc nhãn trực tiếp.

## Hình và bảng

Hình cho hình thái và xu hướng; bảng cho giá trị chính xác. Khi người đọc cần đọc ra con số, nói thẳng rằng bảng phù hợp hơn thay vì ép thành hình.

Khi trả cả hình lẫn bảng, mỗi thứ mang một vai trò riêng: hình đỡ mệnh đề chính, bảng cung cấp giá trị đầy đủ kèm khoảng tin cậy. Không lặp cùng nội dung ở hai nơi.
