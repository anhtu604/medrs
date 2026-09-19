# Đánh số đề mục tự động và tham chiếu chéo

Hai cơ chế này quyết định việc chèn thêm một mục hay một bảng ở giữa tài liệu có làm hỏng toàn bộ phần sau hay không. Chúng phải do Word tính, không do tác giả gõ tay.

## Đánh số đề mục

Số đề mục phải gắn vào style, không gõ vào đầu dòng. Một đề mục mang số gõ tay sẽ sai ngay khi có mục mới chèn phía trên, và không vào được mục lục đúng thứ tự.

- Dùng **một** định nghĩa numbering đa cấp trừu tượng cho toàn bộ đề mục, liên kết từng cấp với `Heading 1` đến `Heading 4`. Không tạo mỗi chương một định nghĩa riêng.
- Định dạng số theo profile của cơ sở đào tạo: cấp 1 là số chương, các cấp sau nối tiếp theo chương, ví dụ dạng `1.2` và `1.2.3`. Lấy dạng chính xác từ profile, không tự chọn.
- Mỗi cấp khai báo rõ vị trí dừng tab, thụt lề trái và thụt lề treo, để dòng thứ hai của đề mục dài thẳng hàng với chữ chứ không thẳng hàng với số.
- Đề mục không đánh số, ví dụ lời cam đoan, mục lục, danh mục chữ viết tắt, tài liệu tham khảo và phụ lục, dùng style riêng hoặc cấp không có số. Không tắt số bằng cách định dạng trực tiếp.

Khi nhận tài liệu có sẵn, phát hiện số gõ tay ở đầu đề mục bằng mẫu ký tự, báo cho tác giả và chỉ bỏ sau khi được duyệt. Không tự xóa, vì có thể là số mà tác giả cố ý giữ.

Nhiều định nghĩa numbering xung đột là hậu quả thường gặp của việc sao chép giữa các tệp. Gộp về một định nghĩa duy nhất và kiểm lại toàn bộ đề mục sau khi gộp.

## Đánh số bảng, hình và phụ lục

Số bảng và hình do trường `SEQ` sinh, gắn theo chương, đặt trong đoạn mang style `Caption`.

- Chú thích bảng đặt phía trên bảng, chú thích hình đặt phía dưới hình, trừ khi profile quy định khác.
- Mỗi loại đối tượng có một chuỗi `SEQ` riêng; bảng, hình, biểu đồ và phụ lục không dùng chung chuỗi.
- Số gắn theo chương lấy số chương từ đề mục cấp 1, nên việc đổi thứ tự chương phải tự động đổi số bảng.

## Tham chiếu chéo

Mọi lần nhắc tới một bảng, hình, đề mục, phụ lục hay tài liệu tham khảo trong thân bài phải là trường tham chiếu, không phải chữ gõ tay.

- Chèn tham chiếu trỏ tới chú thích tương ứng, chỉ lấy phần nhãn và số chứ không lấy toàn bộ nội dung chú thích.
- Giữ liên kết để người đọc bản điện tử nhảy được tới đối tượng.
- Sau khi cập nhật trường, mọi tham chiếu phải hiển thị số; còn sót thông báo lỗi nguồn tham chiếu nghĩa là chú thích đích đã bị xóa hoặc thay, và đó là lỗi chặn.
- Chuỗi chữ dạng "Bảng 3.1" nằm trong thân bài mà không phải trường tham chiếu được báo cho tác giả kèm vị trí. Đây là nguyên nhân phổ biến nhất của việc luận văn dẫn sai số bảng sau khi chèn thêm bảng.

## Kiểm sau khi cập nhật trường

Thêm các mục sau vào báo cáo cơ học, mỗi mục có trạng thái riêng và không được gộp thành một dòng đạt chung:

- định nghĩa numbering đề mục tồn tại và chỉ có một;
- từng cấp numbering gắn đúng `Heading 1` đến `Heading 4`;
- không còn số gõ tay ở đầu đề mục;
- chuỗi `SEQ` tách riêng theo từng loại đối tượng;
- số bảng và hình gắn theo chương đúng profile;
- mọi tham chiếu chéo phân giải được, không còn trường lỗi;
- không còn chuỗi chữ dạng nhãn-và-số gõ tay trong thân bài.

Mục lục, danh mục bảng và danh mục hình chỉ được coi là đạt sau khi trường đã cập nhật và các mục trên đã kiểm. Đọc OOXML không chứng minh được số hiển thị đúng; khi thiếu backend kết xuất, giữ trạng thái `UNPERFORMED` và yêu cầu tác giả kiểm bằng mắt.
