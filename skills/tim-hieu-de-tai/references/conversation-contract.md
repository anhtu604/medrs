# Hợp đồng cuộc trò chuyện tìm hiểu đề tài

Mục đích: giúp **tác giả** hiểu thật kỹ đề tài của mình trước khi viết, và để MedRS có cùng hiểu biết đó dưới dạng ghi lại được. MedRS là người hướng dẫn, không phải người chấm điểm. Câu hỏi ngược là để cùng hiểu, không để thi.

## Khi nào bắt đầu

- Thư mục dự án chưa có workspace, hoặc mục "Hiểu đề tài" chưa `CONFIRMED`: chạy `scripts/topic_understanding.py status <thư mục>` (host chỉ có chat: đọc mục "Hiểu đề tài" trong README).
- Dự án đã có từ 3.1 (README có nội dung, chưa có mục "Hiểu đề tài") hoặc đang giữa một vòng sửa: chỉ đề nghị một dòng; không tự mở cuộc trò chuyện. Tác giả đồng ý thì đi đường "có bản nháp" bên dưới.
- `DEFERRED_BY_AUTHOR`: nhắc một dòng ở lần gọi sau, rồi làm việc tác giả yêu cầu.
- Gọi lại khi đang dở: tiếp tục ở `next_part`, không bắt đầu lại, không hỏi lại điều đã ghi.
- Tác giả gửi đề cương, bản thảo hoặc luận văn dở: đọc trước qua `ho-so-nghien-cuu` (chế độ adopt), điền sẵn những gì đã rõ, chỉ trao đổi chỗ còn mờ hoặc mâu thuẫn.

## Nhịp mỗi phần

Một câu hỏi mỗi lượt, lời đơn giản, theo ngôn ngữ tác giả. Với mỗi phần:

1. Giải thích hoặc tóm tắt điều đã biết → `part … EXPLAINED`.
2. Hỏi tác giả những gì còn thiếu.
3. **Hỏi ngược** bằng một câu tình huống cụ thể gắn với chính đề tài, hoặc nhờ tác giả nói lại bằng lời của mình. Trả lời đúng ý → `CHECKED_BACK`. Trả lời lệch hoặc mơ hồ → giải thích lại, hoặc ghi vào "Điểm cần làm rõ" và cập nhật `open-items`; phần đó chưa xong.
4. Ghi nội dung đã thống nhất vào mục README tương ứng → `DONE`. Script từ chối `DONE` khi chưa qua hỏi ngược.

Ví dụ câu hỏi ngược: "Một trẻ sinh ở tuần 33, cân nặng 1.600 g thì có được đưa vào nghiên cứu không?", "Nếu kết quả không có ý nghĩa thống kê, bạn sẽ kết luận gì?", "Kết cục chính đo lúc nào, bằng công cụ gì?".

## Bốn phần

1. **Kiến thức nền** (trọng tâm chính): bệnh hoặc vấn đề, định nghĩa và phân loại, dịch tễ và gánh nặng ở thế giới và Việt Nam, cơ chế ở mức cần thiết, chẩn đoán, điều trị hoặc quản lý hiện hành, thuật ngữ chuẩn tiếng Việt và tiếng Anh. Sau đó là toàn cảnh nghiên cứu: trong nước và quốc tế đã biết gì, còn khoảng trống nào.
2. **Câu hỏi nghiên cứu và mục tiêu**: chuyển từ chủ đề sang câu hỏi cụ thể. Ví dụ: không dừng ở "nghiên cứu về đái tháo đường thai kỳ" mà hỏi "tỷ lệ kiểm soát đường huyết đạt mục tiêu ở thai phụ đái tháo đường thai kỳ tại bệnh viện X là bao nhiêu?". Dùng PICO/PECO khi hợp. Mục tiêu cụ thể, đo được; nêu kết cục chính.
3. **Phương pháp dự kiến và lý do**: thiết kế (tiến cứu hay hồi cứu theo lời tác giả, không suy ra từ nguồn dữ liệu), đối tượng, tiêu chuẩn chọn và loại, địa điểm, thời gian, cỡ mẫu, biến số và định nghĩa (theo codebook khi có), quy trình lâm sàng, phân tích thống kê. Hỏi vì sao chọn cách này, giới hạn suy luận của thiết kế, và dữ liệu có thật sự trả lời được câu hỏi không.
4. **Kết quả mong đợi**: sau nghiên cứu sẽ có gì, đóng góp gì, sản phẩm (luận văn, bài báo trong nước hay quốc tế, thực hành), mốc thời gian.

## Y văn

- Tìm y văn thật qua `tim-y-van`; với bước này dùng chế độ khảo sát nhanh (quick-seed) và ghi vết truy vấn như mọi lần tìm.
- Mục đích là minh họa kiến thức nền và cho tác giả thấy toàn cảnh, không phải sàng lọc hệ thống.
- Mỗi ý quan trọng ở phần kiến thức nền mang một nhãn: **có nguồn** (kèm PMID hoặc DOI đã kiểm), **giả thuyết** (suy luận, chưa có nguồn), hoặc **cần tìm hiểu thêm**. Không có nguồn thật thì không gán nguồn.
- Không truy cập được cơ sở dữ liệu: nói rõ, giảng bằng kiến thức chung với nhãn chưa có nguồn, ghi việc tìm y văn vào "Việc tiếp theo". Không biến "không tìm được" thành "không có y văn".
- Bảng y văn nền trong README: tài liệu (tác giả, năm, PMID/DOI), câu hỏi nghiên cứu, thiết kế, quần thể, kết quả chính, hạn chế, dùng cho ý nào. `viet-tong-quan` và `viet-ban-luan` dùng lại bảng này.
- Có Zotero thì có thể đề xuất đưa nguồn vào thư viện qua `quan-ly-trich-dan`; không tự ghi vào thư viện.

## README

Các mục ngữ cảnh do `project_workspace.py` tạo. Ghi theo mục, không ghi đè chữ tác giả đã viết; mâu thuẫn thì giữ cả hai và ghi vào "Điểm cần làm rõ". Không ghi định danh người bệnh hay dữ liệu thô. Quyết định tác giả chốt trong lúc trò chuyện ghi vào "Quyết định của tác giả" kèm ngày; thuật ngữ chốt vào "Thuật ngữ và định nghĩa đã chốt".

"Việc tiếp theo" chia thành việc nhỏ 20–30 phút, mỗi việc có một sản phẩm cụ thể (ví dụ: tìm 5 bài phù hợp; lập bảng tổng hợp 5 bài; viết một đoạn về khoảng trống nghiên cứu).

Host chỉ có chat: đưa README dạng file tải về và nói rõ chưa tạo thư mục nào.

## Kết thúc

- Chỉ khi cả bốn phần `DONE`. Đưa bản tóm tắt khoảng một trang để tác giả đọc.
- Tác giả xác nhận bằng lời của mình (ví dụ "tôi đã hiểu rõ") → `confirm <thư mục> <ngày> "<lời tác giả>"`. Không tự xác nhận thay tác giả.
- Đồng bộ câu hỏi, mục tiêu, thiết kế, loại tài liệu vào Research Passport qua `ho-so-nghien-cuu` chế độ `confirm`. Passport đã có giá trị khác: dùng cách phơi bày mâu thuẫn sẵn có của `ho-so-nghien-cuu`, hỏi tác giả một lần, ghi quyết định, không ghi đè.
- Chuyển cho `leader-nghien-cuu` lập kế hoạch các phần viết.
- Tác giả muốn tạm dừng để làm việc khác: `defer`, làm theo yêu cầu, giữ nguyên tiến độ.
