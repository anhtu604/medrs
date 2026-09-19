---
name: bieu-do-cong-bo
description: Chọn, dựng và kiểm định biểu đồ cùng bảng đạt chuẩn công bố cho nghiên cứu y học bằng R hoặc Stata. Designs publication-grade medical figures and tables. Không vẽ khi chưa chốt đơn vị phân tích và cơ sở thanh sai số, không cắt trục để phóng đại hiệu quả, không khẳng định đã dựng hình khi thiếu runtime.
metadata:
  version: 2.0.0-alpha.5
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review, evidence-synthesis]
---

# Biểu đồ công bố

Read [references/evidence-contract.md](references/evidence-contract.md) before choosing a chart. For form selection read [references/figure-families.md](references/figure-families.md); before delivery read [references/publication-qa.md](references/publication-qa.md).

## Hợp đồng bằng chứng

Chốt hợp đồng bằng chứng trước khi chọn dạng hình: mệnh đề khoa học cần đỡ, đơn vị phân tích, chỉ số chính và chiều tốt/xấu, cơ sở thanh sai số, ô khuyết, và liệu thiết kế có cho phép tuyên bố hơn kém hay không. Còn mục nào chưa rõ thì trả bản kiểm kê thiếu sót, không trả hình đã hoàn thiện.

## Chọn dạng trình bày

Chọn theo mệnh đề cần đỡ, không theo độ bắt mắt. Khi người đọc cần con số chính xác, bảng mạnh hơn hình; nói rõ điều đó thay vì ép mọi kết quả thành hình. Hình và bảng đi cùng nhau phải mang hai vai trò khác nhau, không lặp lại cùng một nội dung.

## Dựng hình

R với ggplot2 là đường mặc định; Stata dùng khi dự án đã chạy trên Stata. Chuyển yêu cầu chạy thật cho `phan-tich-r` hoặc `phan-tich-stata` và tuân theo hợp đồng tái lập của các skill đó.

Khi không có runtime, trả mã nguồn chạy được kèm trạng thái `UNPERFORMED`; không mô tả hình như đã dựng, không đoán giá trị trục hay hình dạng phân bố.

Mọi hình dựng từ kết quả phân tích phải truy được về cùng artifact mà `phan-tich-so-lieu` đã ghi nhận. Hình không khớp số liệu trong bản thảo là lỗi chặn.

## Bàn giao

Nội dung sơ đồ dòng chảy theo chuẩn báo cáo lấy từ skill giữ nguồn tương ứng, không dựng lại từ trí nhớ. Chuyển chú thích hình cho `viet-ket-qua`, nhúng và đánh số hình trong Word cho `dinh-dang-tai-lieu`.

Trả về hợp đồng bằng chứng đã chốt, dạng hình đã chọn kèm lý do, mã dựng hình, tên tệp và định dạng xuất, kết quả kiểm định chất lượng, và các điểm cần tác giả quyết định.
