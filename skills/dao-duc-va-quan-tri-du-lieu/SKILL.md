---
name: dao-duc-va-quan-tri-du-lieu
description: Use when a medical protocol needs ethics, consent, registration, privacy, data-governance, or approval-status planning. Dùng khi lập hồ sơ đạo đức và quản trị dữ liệu; không dùng để bịa số chấp thuận hoặc thay tư vấn pháp lý.
metadata:
  version: 2.0.0-alpha.8
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript]
---

# Đạo đức và quản trị dữ liệu

Follow the shared [working principles](../medrs/references/working-principles.md).

Soạn mục đạo đức và kế hoạch quản trị dữ liệu từ thông tin tác giả cung cấp. Viết theo giọng khẳng định: nghiên cứu đã tuân thủ những gì và bảo vệ người tham gia ra sao, thay vì liệt kê rủi ro.

## Đầu vào

Dùng Passport và những gì tác giả nêu: thẩm quyền, giai đoạn, loại dữ liệu, nơi lưu và chuyển, căn cứ xử lý, đồng thuận, đăng ký và phê duyệt. Thông tin tác giả nêu được ghi `CONFIRMED` và dùng ngay. Mục nào thiếu thì để ô như `[Số QĐ]` và đưa vào danh sách cuối.

## Quy trình

1. Chọn `references/vietnam-profile.md` và/hoặc `references/international-profile.md` theo nơi thực hiện, tài trợ và đích nộp.
2. Đối chiếu `references/source-register.yaml`. Nguồn quá hạn kiểm tra thì viết theo quy định gần nhất đã biết và thêm "kiểm lại quy định hiện hành" vào danh sách cuối; không dừng.
3. Dùng `references/data-governance.md` để lập luồng dữ liệu và quyền truy cập.
4. Viết mục đạo đức hoàn chỉnh: hội đồng và quyết định chấp thuận, đồng thuận hoặc miễn đồng thuận, bảo mật và ẩn danh, lưu trữ, đăng ký.

## Ranh giới

Số quyết định, tên hội đồng, ngày phê duyệt, miễn đồng thuận và mã đăng ký lấy đúng từ tác giả. Đây là hỗ trợ soạn hồ sơ, không phải ý kiến pháp lý.

## Đầu ra

Mục đạo đức hoàn chỉnh, bảng thông tin đã xác nhận, và danh sách `Việc cần bổ sung` cho các ô còn trống.
