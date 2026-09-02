# Data-governance artifact

Ghi một hàng cho mỗi luồng dữ liệu:

| Trường | Giá trị bắt buộc |
|---|---|
| Data class | identifiable / coded / anonymized / aggregate / biological material |
| Source and destination | hệ thống/cơ sở cụ thể hoặc `UNRESOLVED` |
| Purpose | mục đích đã xác nhận |
| Authorization basis | consent / waiver / legal or institutional basis / `UNRESOLVED` |
| Access | vai trò được phép, nguyên tắc tối thiểu cần thiết |
| Safeguards | mã hóa, tách khóa, nhật ký truy cập, sao lưu |
| Retention and disposal | thời hạn, căn cứ, cách hủy hoặc `OFFICIAL_RULE_REQUIRED` |
| Transfer | nơi nhận, quốc gia, thỏa thuận và phê duyệt cần có |

Không gọi dữ liệu là “ẩn danh” nếu còn khóa hoặc có thể liên kết lại. Không tự chọn thời hạn lưu, căn cứ pháp lý hay quyền truy cập khi nguồn chính thức/cơ sở chưa xác nhận.
