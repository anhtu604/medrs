# Hợp đồng phân tích thời gian đến biến cố và mô hình tiên lượng

Áp dụng khi kết cục là thời gian đến biến cố, hoặc khi nghiên cứu xây dựng/đánh giá một mô hình tiên lượng. Chốt các mục dưới đây trong kế hoạch phân tích trước khi chạy; thay đổi sau khi thấy kết quả là `DEVIATION` và phải ghi lý do cùng thời điểm.

## Định nghĩa bắt buộc

| Mục | Phải xác định | Hỏng nếu bỏ qua |
|---|---|---|
| Mốc thời gian gốc | Thời điểm nào là ngày 0 cho mỗi đối tượng | Thời gian sống không so sánh được giữa các nhóm |
| Biến cố | Biến cố nào được tính, xác định bằng nguồn nào | Trộn biến cố khác nhau vào cùng một đường cong |
| Kiểm duyệt | Điều kiện kiểm duyệt và thời điểm kết thúc theo dõi | Nhầm mất theo dõi với sống sót |
| Biến cố cạnh tranh | Có biến cố ngăn biến cố quan tâm xảy ra không | Kaplan–Meier ước lượng quá cao nguy cơ tích lũy |
| Thang thời gian | Thời gian từ khi vào nghiên cứu, hay tuổi | Hiệu chỉnh sai theo tuổi |

Kiểm duyệt phải không phụ thuộc tiên lượng. Nếu bệnh nhân nặng hơn bỏ theo dõi nhiều hơn, giả định này vi phạm; nêu rõ và phân tích độ nhạy thay vì bỏ qua.

## Sai lệch thường gặp trong nghiên cứu lâm sàng

- **Thời gian bất tử**: khoảng thời gian mà theo thiết kế đối tượng bắt buộc còn sống để được xếp vào một nhóm. Phân nhóm theo việc có nhận điều trị hay không, khi điều trị xảy ra sau mốc gốc, tạo ra sai lệch này. Xử lý bằng biến phụ thuộc thời gian hoặc phân tích mốc, không bằng phân nhóm tại mốc gốc.
- **Phân nhóm theo đáp ứng điều trị**: đáp ứng chỉ quan sát được ở người sống đủ lâu, nên so sánh người đáp ứng với người không đáp ứng luôn thiên vị.
- **Chọn điểm cắt biến liên tục theo giá trị p nhỏ nhất**: bị từ chối. Điểm cắt phải tiền định hoặc giữ biến ở dạng liên tục.

## Đường cong và bảng số còn theo dõi

Mọi đường cong sống còn phải kèm bảng số đối tượng còn trong nguy cơ tại các mốc thời gian. Đuôi đường cong nơi còn rất ít đối tượng không được diễn giải như một ước lượng ổn định.

Khi có biến cố cạnh tranh, báo cáo hàm nguy cơ tích lũy theo phương pháp phù hợp thay vì phần bù của Kaplan–Meier.

## Mô hình Cox

Kiểm tra giả định nguy cơ tỷ lệ và báo cáo cách kiểm tra, không chỉ khẳng định đã thỏa. Giả định không thỏa thì nêu và xử lý bằng phân tầng, hệ số phụ thuộc thời gian, hoặc mô hình khác; không im lặng giữ nguyên.

Số biến đưa vào bị giới hạn bởi số biến cố, không bởi cỡ mẫu. Báo cáo số biến cố cùng số biến. Chọn biến bằng thủ tục từng bước dựa trên p-value bị từ chối theo hợp đồng của `phan-tich-so-lieu`.

Báo cáo tỷ số nguy cơ kèm khoảng tin cậy và nêu rõ nó là trung bình theo thời gian khi giả định tỷ lệ chỉ thỏa xấp xỉ.

## Mô hình tiên lượng

Phân biệt rõ giai đoạn xây dựng và giai đoạn đánh giá; nêu đây là đánh giá nội bộ hay ngoại bộ.

- **Khả năng phân biệt** và **mức hiệu chuẩn** phải báo cáo cùng nhau. Chỉ báo cáo diện tích dưới đường cong là không đủ: một mô hình phân biệt tốt vẫn có thể cho xác suất sai lệch hệ thống.
- Hiệu chuẩn báo cáo bằng đồ thị hiệu chuẩn kèm độ dốc và hệ số chặn, không bằng một kiểm định đạt/không đạt.
- Đánh giá nội bộ dùng lấy mẫu lặp hoặc kiểm chứng chéo trên toàn bộ quy trình xây dựng mô hình, bao gồm cả bước chọn biến. Chọn biến trước rồi mới kiểm chứng chéo sẽ cho ước lượng lạc quan.
- Báo cáo mức co hồi hoặc hiệu chỉnh quá khớp đã áp dụng.
- Số biến cố trên mỗi biến ứng viên phải nêu rõ; mô hình xây trên quá ít biến cố được đánh dấu là thăm dò.

Bản thảo mô tả mô hình tiên lượng phải đối chiếu chuẩn báo cáo tương ứng qua `kiem-chuan-bao-cao`.

## Bàn giao

Mã chạy thật thuộc `phan-tich-r` hoặc `phan-tich-stata` theo backend đã chốt, giữ nguyên hợp đồng tái lập của các skill đó. Đường cong sống còn, đồ thị hiệu chuẩn và đường cong ROC chuyển cho `bieu-do-cong-bo`, kèm cơ sở thanh sai số và số còn theo dõi.
