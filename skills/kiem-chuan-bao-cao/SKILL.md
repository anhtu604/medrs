---
name: kiem-chuan-bao-cao
description: Đối chiếu bản thảo với chuẩn báo cáo hợp thiết kế, bao phủ từng mục của bản chính thức. Checks manuscripts against reporting guidelines item by item. Không chọn chuẩn khi thiết kế chưa rõ, không dựng lại mục từ trí nhớ, không kết luận tuân thủ khi chưa định vị chỗ báo cáo.
metadata:
  version: 2.0.0-alpha.6
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review, evidence-synthesis]
---

# Kiểm chuẩn báo cáo

Read [references/guideline-routing.md](references/guideline-routing.md) to choose the instrument, then [references/compliance-contract.md](references/compliance-contract.md) before judging any item.

Chuẩn báo cáo trả lời câu hỏi bản thảo có **báo cáo đủ** hay không. Nó không đánh giá nguy cơ sai lệch và không thay thế `danh-gia-chat-luong-bang-chung`.

## Chọn chuẩn

Chọn theo thiết kế nghiên cứu, không theo loại tài liệu. Thiết kế chưa xác định thì trả `DESIGN_REQUIRED` và hỏi; không đoán. Bản thảo có nhiều cấu phần thì mỗi cấu phần nhận một chuẩn riêng.

## Bao phủ từng mục

Mọi mục lấy từ manifest bao phủ trong `../../coverage/`, không dựng lại từ trí nhớ. Manifest thiếu hoặc không đọc được là lỗi chặn, không phải lý do để tự liệt kê mục.

Mỗi mục nhận một phán định kèm vị trí báo cáo trong bản thảo: đã báo cáo, báo cáo một phần, chưa báo cáo, hoặc không áp dụng cho thiết kế này. `Không áp dụng` phải nêu lý do theo thiết kế. Không gộp mục chưa đạt thành một nhãn tổng thể trấn an.

Không có vị trí cụ thể thì mục đó chưa được coi là đã báo cáo, kể cả khi nội dung có vẻ xuất hiện đâu đó.

## Bàn giao

Nhận thiết kế và artifact từ `ho-so-nghien-cuu`; trả danh mục thiếu sót cho `kiem-chung-ban-thao` và `phan-bien-va-chinh-sua`. Sơ đồ dòng chảy đối tượng do `bieu-do-cong-bo` dựng, nhưng nhãn và mục lấy từ manifest ở đây.

Trả về chuẩn đã chọn kèm phiên bản và nguồn, bảng phán định từng mục có vị trí báo cáo, danh sách chưa đạt theo mức ưu tiên, và các mục cần tác giả xác nhận.
