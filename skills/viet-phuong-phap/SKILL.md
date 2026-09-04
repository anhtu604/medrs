---
name: viet-phuong-phap
description: Use when drafting or revising a medical Methods section from a Research Passport, protocol, or confirmed study record. Dùng cho phần Phương pháp; không dùng để mô tả thủ thuật chưa thực hiện như đã hoàn tất hoặc để viết Kết quả.
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript]
---

# Viết Phương pháp

Viết từ artifact đã xác nhận và phân biệt nghiêm ngặt giữa kế hoạch với việc đã thực hiện.

## Đầu vào bắt buộc

- Research Passport và locale profile đang hoạt động
- design contract, kế hoạch cỡ mẫu/phân tích, artifact đạo đức và quản trị dữ liệu
- mode `protocol` hoặc `completed-study`
- nguồn xác nhận cho mọi thủ thuật được mô tả là đã làm

## Chế độ

`protocol` dùng cấu trúc dự kiến/kế hoạch, không đổi sang quá khứ như thể nghiên cứu đã hoàn tất. `completed-study` chỉ mô tả thủ thuật có provenance xác nhận, đồng thời nêu sai lệch so với đề cương.

## Quy trình

1. Nạp locale profile và `references/protocol-vs-completed.md`.
2. Ráp các tiểu mục theo target profile; thiếu profile thì giữ cấu trúc nội dung, không tuyên bố đúng mẫu trường/tạp chí.
3. Lập claim/evidence table cho thiết kế, đối tượng, biến số, quy trình, phân tích và đạo đức.
4. Chạy `references/writing-preflight.md` đúng một lần trước khi trả bản nháp.
5. Ghi full `kiem-van-phong` gate là `PENDING`; skill này thuộc Slice 2 và không được giả lập trong Slice 1.

## Đầu ra

Bản nháp Methods, claim/evidence table, marker chưa giải quyết, dependency, preflight result và yêu cầu tác giả duyệt. Không tự tạo số chấp thuận, số liệu, phần mềm đã chạy hay trích dẫn.
