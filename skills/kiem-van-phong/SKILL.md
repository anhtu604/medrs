---
name: kiem-van-phong
description: "Kiểm và nâng chất văn phong học thuật y học tiếng Việt hoặc tiếng Anh: lập luận, bằng chứng, nhịp câu, và viết lại theo hồ sơ văn phong riêng của tác giả. Audits and rewrites prose in the author's voice."
metadata:
  version: 3.0.0-rc.1
  role: gate
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript, review]
---

# Kiểm văn phong

Follow the shared [working principles](../medrs/references/working-principles.md).
When editing or writing into a Word file, follow the [Zotero field contract](../quan-ly-trich-dan/references/zotero-field-contract.md).

Gate này đánh giá và nâng chất lượng, tính liêm chính của văn bản y học, gồm cả việc viết lại cho câu văn tự nhiên hơn. Nó không chấm “độ giống người”, không dự đoán tác giả và không tối ưu để né bộ phát hiện AI; mục tiêu là văn tốt hơn, không phải qua được công cụ kiểm tra.

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
5. Khi tác giả yêu cầu viết lại chứ không chỉ chẩn đoán, nạp `references/prose-rewriting.md`; nếu có `author-style-profile.json`, viết theo hồ sơ đó. Dựng hồ sơ bằng `scripts/style_profile.py`.

## Vòng đời

- Section độc lập: chạy một full gate trước khi giao.
- Tài liệu nhiều phần: writer chỉ chạy shared preflight; full gate chạy sau lần ráp đầu tiên.
- Sau sửa nội dung: tái kiểm phần có hash/dependency đổi và kiểm nhất quán toàn văn. Không đổi thì tái sử dụng kết quả cũ.
- Trước nộp: full gate cuối chỉ cần khi sửa đổi đã làm mất hiệu lực audit lắp ráp.

## Đầu ra

Trả về artifact theo `schemas/style-audit.schema.json`, danh sách vấn đề gắn vị trí, sửa đổi đề xuất, marker chưa giải quyết và điểm cần tác giả duyệt. Không tự xác nhận nguồn, số liệu hoặc dụng ý của tác giả.
