# Hợp đồng hai vòng độc lập

Chạy hai lần cùng một danh mục kiểm chỉ tốn gấp đôi thời gian mà không thêm thông tin. Giá trị nằm ở chỗ hai vòng **độc lập** và **soi từ hai góc khác nhau**.

## Khóa bản thảo

Trước vòng một, ghi hash của bản thảo và của mọi artifact đi kèm: bảng kết quả, artifact phân tích, source ledger. Cả hai vòng chạy trên đúng bộ hash đó.

Bản thảo đổi giữa chừng thì hủy vòng đang chạy và bắt đầu lại; không ghép phát hiện từ hai phiên bản khác nhau.

## Độc lập nghĩa là gì

- Vòng hai không đọc báo cáo vòng một, không đọc bản tóm tắt của nó, và không được nghe gợi ý kiểu "chú ý phần phương pháp".
- Không sửa bản thảo giữa hai vòng. Nếu đã sửa thì đó là chu kỳ mới: khóa hash mới, chạy lại cả hai vòng.
- Không dùng số lượng phát hiện của vòng một làm chỉ tiêu cho vòng hai.

Khi host cho phép chạy hai tiến trình tách biệt, chạy tách. Khi không, vòng hai vẫn phải bắt đầu từ bản thảo gốc và không tham chiếu kết quả trước đó.

## Hai góc soi

Hai vòng dùng hai trục khác nhau để không lặp lại nhau.

**Vòng 1 — tính vững của bằng chứng.** Câu hỏi nghiên cứu và thiết kế có khớp nhau không; dân số và tiêu chuẩn chọn có định nghĩa được không; kết cục chính có tiền định không; phân tích có đúng với kế hoạch không; số liệu trong bài có nhất quán giữa tóm tắt, bảng, hình và bàn luận; kết luận có nằm trong phạm vi thiết kế cho phép không; hạn chế có nêu đúng cái đáng lo nhất không.

**Vòng 2 — người đọc phản biện.** Đọc như một người phản biện hoài nghi nhưng thiện chí: chỗ nào sẽ bị hỏi lại; giải thích nào có cách lý giải khác chưa được loại trừ; yếu tố nhiễu nào chưa xử lý; kết quả âm tính có bị chôn không; phần bàn luận có né kết quả bất lợi không; bài có thiếu thông tin khiến người khác không lặp lại được không.

Mỗi phát hiện ở cả hai vòng đều phải có vị trí cụ thể trong bản thảo. Nhận xét chung chung kiểu "phần bàn luận còn yếu" không được tính là phát hiện.

## Mức độ

Mỗi phát hiện mang một mức:

- **Chặn** — làm sai lệch kết luận, hoặc khiến kết quả không diễn giải được.
- **Nặng** — làm giảm đáng kể độ tin cậy, nhiều khả năng bị phản biện yêu cầu sửa.
- **Nhẹ** — cải thiện chất lượng trình bày.

Không quy mức theo độ khó sửa. Một lỗi chặn khó sửa vẫn là lỗi chặn.

## Điều không được làm

Không bịa ra nhận xét để cho đủ số lượng. Vòng nào không tìm thấy gì ở mức chặn thì nói thẳng là không tìm thấy.

Không suy đoán danh tính hay yêu cầu của hội đồng, tạp chí cụ thể. Nếu bản thảo nhắm một tạp chí có yêu cầu riêng, lấy yêu cầu đó từ nguồn thật qua `kiem-chuan-bao-cao`, không đoán.

Không đánh giá thay cho tác giả về việc bản thảo có nên nộp hay không.
