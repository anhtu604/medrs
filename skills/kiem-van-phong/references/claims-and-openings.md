# Câu mở đoạn có luận điểm và diễn giải p, KTC

Dùng khi viết hoặc kiểm Kết quả, Bàn luận, Tóm tắt. Mẫu quét tự động: [../scripts/prose_patterns.py](../scripts/prose_patterns.py) (`--locale vi|en <file>`); kết quả là gợi ý sửa, không phải lỗi chặn.

## Câu mở đoạn

Người đọc nhìn bảng là biết bảng trình bày gì. Điều họ cần là phát hiện nào đáng chú ý và nó có nghĩa gì.

- **Kết quả**: mở đoạn bằng phát hiện chính, dẫn bảng hoặc hình trong ngoặc.
  - Thay "Bảng 3.4 trình bày mối liên quan giữa BMI mẹ và đái tháo đường thai kỳ" bằng "Thai phụ có BMI cao hơn có tỷ lệ đái tháo đường thai kỳ cao hơn (Bảng 3.4)".
  - EN: instead of "Table 4 shows the association between…", write "Women with higher BMI more often developed gestational diabetes (Table 4)".
- **Bàn luận**: mở đoạn bằng cách giải thích hoặc ý nghĩa của phát hiện, sau đó mới đưa bằng chứng, so sánh nghiên cứu và lý giải.
  - Thay "Nhiều nghiên cứu đã báo cáo tỷ lệ khác nhau…" bằng "Khác biệt về tiêu chuẩn chẩn đoán có thể giải thích một phần sự chênh lệch tỷ lệ giữa các nghiên cứu".
  - Không mở bằng chuỗi "tác giả A thấy…, tác giả B báo cáo…" mà đến cuối đoạn vẫn chưa thấy quan điểm của nghiên cứu này.
- Câu có luận điểm **không** có nghĩa là viết mạnh hơn dữ liệu. Liên quan vẫn là liên quan; không nâng thành "gây ra", "dẫn đến". Mức chắc chắn theo thiết kế và trần suy luận.
- Không bắt buộc ở Phương pháp, và không phải đoạn Kết quả nào cũng cần; một đoạn chỉ liệt kê đặc điểm mẫu có thể mở bằng mô tả.

## p và khoảng tin cậy

- p được tính **giả định không có khác biệt thật**. Nó cho biết dữ liệu lệch khỏi giả định đó bao nhiêu (khả năng thu được kết quả ít nhất cực đoan như đã quan sát), không phải xác suất kết quả "do ngẫu nhiên" và không phải xác suất can thiệp có hiệu quả.
- Không viết: "chỉ có 2% khả năng kết quả do ngẫu nhiên", "98% khả năng can thiệp hiệu quả", "95% xác suất giá trị thật nằm trong khoảng".
- KTC 95% là vùng giá trị còn tương thích với dữ liệu hiện có. Khoảng hẹp là ước lượng chính xác hơn; khoảng rộng là bất định lớn hơn.
- KTC của RR hoặc OR chứa 1 (của hiệu số trung bình chứa 0): dữ liệu còn tương thích với không khác biệt. Không có nghĩa là đã chứng minh không có tác động.
- Luôn nêu độ lớn tác động và KTC cùng với p; ý nghĩa thống kê không thay cho độ lớn và độ chính xác của ước lượng.
