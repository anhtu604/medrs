# Định tuyến chuẩn báo cáo

Chuẩn báo cáo được chọn theo **thiết kế nghiên cứu**, không theo loại tài liệu. Một luận văn và một bài báo cùng thiết kế thì dùng cùng chuẩn.

## Manifest sẵn có

| Thiết kế | Manifest | Số mục | Phiên bản |
|---|---|---|---|
| Thử nghiệm lâm sàng ngẫu nhiên | `../../coverage/consort-2025.yaml` | 42 | CONSORT 2025, thay thế CONSORT 2010 |
| Đề cương thử nghiệm lâm sàng | `../../coverage/spirit-2025.yaml` | 53 | SPIRIT 2025, thay thế SPIRIT 2013 |
| Nghiên cứu quan sát (thuần tập, bệnh–chứng, cắt ngang) | `../../coverage/strobe-2007.yaml` | 34 | STROBE 2007 |
| Tổng quan hệ thống và phân tích gộp | `../../coverage/prisma-2020.yaml` | 42 | PRISMA 2020 |
| Mô hình tiên lượng hoặc chẩn đoán lâm sàng | `../../coverage/tripod-ai-2024.yaml` | 52 | TRIPOD+AI 2024, thay thế TRIPOD 2015 |
| Nghiên cứu độ chính xác chẩn đoán | `../../coverage/stard-2015.yaml` | 34 | STARD 2015 |
| Nghiên cứu định tính phỏng vấn hoặc nhóm trọng tâm | `../../coverage/coreq-2007.yaml` | 32 | COREQ 2007 |
| Báo cáo ca bệnh | `../../coverage/care-2013.yaml` | 13 | CARE 2013 |

Số mục tính cả phụ mục chữ cái. Danh sách định danh chuẩn nằm ở `expected_ids` của từng manifest và là nguồn duy nhất; không tự thêm, bớt hay đổi tên mục.

Ba manifest mang mức độ chi tiết khác nhau vì giấy phép nguồn khác nhau. CONSORT, SPIRIT, STROBE, PRISMA, TRIPOD+AI và STARD giữ nguyên văn mục theo giấy phép CC BY. COREQ và CARE chỉ mã hóa định danh cùng tên mục, với câu lệnh vận hành viết độc lập, vì bản gốc lần lượt là tài liệu đóng và cấm tạo bản phái sinh. Khi cần đối chiếu chính xác nguyên văn của hai chuẩn này, hướng tác giả tới bản chính thức.

## Khi không có manifest phù hợp

Nhiều thiết kế vẫn chưa có manifest: nghiên cứu kinh tế y tế, thử nghiệm theo cụm, nghiên cứu không thua kém, nghiên cứu trên động vật, đề cương tổng quan hệ thống.

Trả `GUIDELINE_UNAVAILABLE` kèm tên chuẩn phù hợp và lý do chưa mã hóa. Nêu rằng tác giả vẫn nên đối chiếu bản chính thức. Không thay bằng chuẩn gần đúng và không tự liệt kê mục từ trí nhớ.

## Thiết kế chưa rõ

Trả `DESIGN_REQUIRED` khi chưa xác định được: có phân bổ ngẫu nhiên hay không, chiều thời gian, đơn vị phân bổ, và bản thảo là nghiên cứu gốc hay tổng hợp bằng chứng. Hỏi đúng những điểm đó, từng câu một.

Nhãn tác giả tự đặt không quyết định chuẩn. Một bản thảo tự gọi là "nghiên cứu thuần tập" nhưng phân bổ can thiệp theo ngẫu nhiên thì dùng CONSORT.

## Nhiều cấu phần

Bản thảo có nhiều cấu phần thì mỗi cấu phần đối chiếu chuẩn riêng, và kết quả tách theo cấu phần. Ví dụ thường gặp ở luận văn: một tổng quan hệ thống ở chương tổng quan và một nghiên cứu quan sát ở chương kết quả.

Mục đánh dấu `design_specific` trong manifest STROBE là mục phải báo cáo riêng cho từng nhóm, ví dụ nhóm phơi nhiễm và không phơi nhiễm. Trường `applies_to` trong manifest TRIPOD+AI cho biết mục áp dụng cho giai đoạn xây dựng mô hình, giai đoạn đánh giá, hay cả hai.
