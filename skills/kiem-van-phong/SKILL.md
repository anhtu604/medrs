---
name: kiem-van-phong
description: Use when auditing or revising Vietnamese or English medical academic prose before standalone delivery, document assembly, submission, or defense. Dùng để kiểm lập luận, bằng chứng, giọng tác giả và văn phong; không dùng để dự đoán văn bản có phải do AI viết.
metadata:
  version: 2.0.0-alpha.2
  role: gate
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript, review]
---

# Kiểm văn phong

Gate này đánh giá chất lượng và tính liêm chính của văn bản y học. Nó không chấm “độ giống người”, không dự đoán tác giả và không tối ưu để né bộ phát hiện AI.

## Đầu vào

- bản thảo hoặc section artifact;
- Research Passport, claim–evidence table và source ledger;
- thiết kế nghiên cứu, kết quả đã xác nhận và target profile;
- locale profile Việt hoặc Anh;
- audit state trước đó, nếu có.

## Bốn pass

1. Nạp `references/scientific-integrity.md` để kiểm sự kiện, nguồn, kết quả, phê duyệt và trần suy luận.
2. Nạp `references/argument-quality.md` để nối từng luận điểm với kết quả, nguồn, lý giải hoặc marker.
3. Chỉ nạp `references/composition-vi.md` hoặc `references/composition-en.md` theo locale đang hoạt động.
4. Nạp `references/formulaic-writing-audit.md` để tìm triệu chứng sáo rỗng và sửa vấn đề sâu hơn, không gán nhãn tác giả.

## Vòng đời

- Section độc lập: chạy một full gate trước khi giao.
- Tài liệu nhiều phần: writer chỉ chạy shared preflight; full gate chạy sau lần ráp đầu tiên.
- Sau sửa nội dung: tái kiểm phần có hash/dependency đổi và kiểm nhất quán toàn văn. Không đổi thì tái sử dụng kết quả cũ.
- Trước nộp: full gate cuối chỉ cần khi sửa đổi đã làm mất hiệu lực audit lắp ráp.

## Đầu ra

Trả về artifact theo `schemas/style-audit.schema.json`, danh sách vấn đề gắn vị trí, sửa đổi đề xuất, marker chưa giải quyết và điểm cần tác giả duyệt. Không tự xác nhận nguồn, số liệu hoặc dụng ý của tác giả.
