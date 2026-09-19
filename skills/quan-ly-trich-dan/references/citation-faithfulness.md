# Hợp đồng kiểm chứng trung thực trích dẫn

Đơn vị phán định là một cặp **trích dẫn × mệnh đề**, không phải một trích dẫn. Cùng một bài được trích cho ba mệnh đề thì có ba phán định riêng.

## Thứ tự bắt buộc

1. Đối chiếu danh sách thu hồi và đính chính cho mọi tài liệu được trích. Bài đã thu hồi được báo ngay, trước mọi phán định khác, kèm trạng thái và ngày thu hồi lấy từ nguồn.
2. Định vị từng tài liệu trong thư viện theo tác giả và năm. Không tìm thấy thì phán định là `KHÔNG_KIỂM_CHỨNG_ĐƯỢC`, không phải `KHÔNG_CÓ_TRONG_NGUỒN`.
3. Đọc tóm tắt trước; mâu thuẫn lộ rõ ở tóm tắt thì ghi nhận ngay.
4. Mở toàn văn khi mệnh đề nói về phương pháp, số liệu, hoặc giới hạn. Không mở được toàn văn thì phán định dừng ở mức siêu dữ liệu và phải ghi rõ điều đó.
5. Trích đoạn nguyên văn ngắn làm bằng chứng cho mỗi phán định, kèm vị trí trong tài liệu.

## Bốn mức phán định

| Mức | Định nghĩa | Việc cần làm |
|---|---|---|
| Trung thực | Nguồn nói đúng điều được quy cho nó, trong cùng phạm vi và cùng mức chắc chắn | Giữ nguyên |
| Nói quá | Nguồn có nói, nhưng bản thảo mở rộng phạm vi, dân số, chiều nhân quả, hoặc mức chắc chắn | Thu hẹp câu văn về đúng phạm vi nguồn |
| Quy sai nguồn | Phát hiện có thật nhưng thuộc về một tài liệu khác mà nguồn được trích chỉ thuật lại | Trích tài liệu gốc, hoặc trích cả hai với vai trò rõ ràng |
| Không có trong nguồn | Không tìm thấy cơ sở cho mệnh đề trong nguồn | Bỏ trích dẫn hoặc thay bằng nguồn thật |

Mức thứ năm, `KHÔNG_KIỂM_CHỨNG_ĐƯỢC`, dùng khi không truy cập được nguồn. Đây là trạng thái năng lực, không phải kết luận về bản thảo, và không bao giờ được trình bày như đã kiểm chứng đạt.

## Kiểm tra số liệu

Mọi con số cụ thể trong bản thảo — tỷ lệ, tần suất, cỡ mẫu, tỷ số, khoảng tin cậy — phải xuất hiện trong chính tài liệu được trích.

Lỗi thường gặp nhất là trích một bài tổng quan cho con số mà bài tổng quan chỉ thuật lại từ nghiên cứu gốc. Văn bản nguồn khi đó có dạng "theo nghiên cứu của ... , tỷ lệ là ...", tức là thuật lại chứ không phải phát hiện của chính nó. Trường hợp này luôn là quy sai nguồn, kể cả khi con số hoàn toàn đúng.

Con số khớp nhưng khác đơn vị, khác mẫu số, khác thời điểm đo, hoặc khác dân số cũng là nói quá chứ không phải trung thực.

## Kết quả trả về

Bảng một dòng cho mỗi cặp trích dẫn × mệnh đề, gồm: định danh trích dẫn, mệnh đề được quy, mức phán định, trích đoạn làm bằng chứng, vị trí trong nguồn, và hành động đề xuất.

Kèm theo: danh sách bài đã thu hồi, danh sách không kiểm chứng được kèm lý do, và ghi chú rằng phán định chỉ bao phủ các mệnh đề đã liệt kê chứ không chứng nhận toàn bộ bản thảo.

Không tự sửa câu văn của tác giả trong bước này. Đề xuất sửa được chuyển cho `kiem-chung-ban-thao` và `phan-bien-va-chinh-sua`.
