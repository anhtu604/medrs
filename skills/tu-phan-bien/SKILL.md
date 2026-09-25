---
name: tu-phan-bien
description: Tự phản biện bản thảo qua hai vòng độc lập rồi mới đối chiếu và sửa, dùng khi chưa có nhận xét từ người phản biện thật. Runs two independent self-review rounds before revision. Không để vòng sau đọc kết quả vòng trước, không sửa giữa hai vòng, không thay phản biện thật.
metadata:
  version: 2.0.0-alpha.8
  role: gate
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review, evidence-synthesis]
---

# Tự phản biện

Follow the shared [working principles](../medrs/references/working-principles.md).

Read [references/two-round-contract.md](references/two-round-contract.md) before starting. Round 1 applies [references/validation-contract.md](references/validation-contract.md) and the reporting-guideline check of `kiem-chuan-bao-cao`; round 2 adds the argument pass of `kiem-van-phong`. Read [references/reconciliation.md](references/reconciliation.md) before comparing the rounds.

Dùng khi tác giả muốn biết bản thảo yếu ở đâu trước khi gửi đi. Khi đã có nhận xét từ người phản biện thật, đó là việc của `phan-bien-va-chinh-sua`; skill này không thay thế phản biện thật và không dự đoán hội đồng sẽ nói gì.

## Hai vòng độc lập

Chạy hai vòng rà soát trên cùng một bản thảo đã khóa hash. Vòng hai không được đọc kết quả vòng một; mọi thứ khiến vòng sau bị neo theo vòng trước đều phá giá trị của việc chạy hai lần.

Không sửa bản thảo giữa hai vòng. Sửa xong mới chạy lại là chu kỳ mới, không phải vòng hai.

Hai vòng dùng hai góc soi khác nhau, không lặp cùng một danh mục.

## Đối chiếu

Chỉ sau khi cả hai vòng xong mới gộp kết quả. Phát hiện được cả hai vòng nêu là ưu tiên cao nhất. Phát hiện chỉ một vòng nêu vẫn giữ nguyên giá trị, đánh dấu là chưa đồng thuận. Hai vòng mâu thuẫn nhau thì đưa cả hai cho tác giả, không tự chọn bên.

## Sửa

Sửa chỉ bắt đầu sau khi tác giả duyệt danh mục đã đối chiếu. Mỗi mục sửa đi qua skill phụ trách miền tương ứng, không sửa trực tiếp ở đây. Sau khi sửa, bản thảo mang hash mới và mọi phát hiện gắn với hash cũ phải được kiểm lại.

Trả về hai báo cáo vòng riêng biệt, bảng đối chiếu, mức ưu tiên, mục mâu thuẫn, danh mục sửa đã duyệt và trạng thái kiểm lại.
