---
name: viet-phuong-phap
description: "Viết phần Đối tượng và phương pháp cho đề cương hoặc nghiên cứu đã hoàn thành, đúng thì của từng loại tài liệu. Writes the Methods section."
metadata:
  version: 3.1.0
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript]
---

# Viết Phương pháp

Follow the shared [working principles](../medrs/references/working-principles.md).
Select standalone/assembled/revision scope using [the shared gate lifecycle](../kiem-van-phong/references/gate-lifecycle.md).
When editing or writing into a Word file, follow the [Zotero field contract](../quan-ly-trich-dan/references/zotero-field-contract.md).

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
5. Chạy `kiem-van-phong` khi skill và ngữ cảnh có sẵn; nếu chưa chạy ghi `UNPERFORMED` với lý do thực tế. Không dùng nhãn Slice cũ để bỏ kiểm. Với bản nhiều phần, gate toàn văn chạy khi ráp tài liệu.

Khi sửa Methods đọc [references/clinical-methods-checks.md](references/clinical-methods-checks.md): giữ đủ quy trình lâm sàng, tên riêng tác giả xác nhận và thiết kế thống nhất.

## Đầu ra

Bản nháp Methods, claim/evidence table, marker chưa giải quyết, dependency, preflight result và yêu cầu tác giả duyệt. Không tự tạo số chấp thuận, số liệu, phần mềm đã chạy hay trích dẫn.
