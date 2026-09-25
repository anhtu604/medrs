---
name: quan-ly-trich-dan
description: "Quản lý trích dẫn Zotero trong Word: giữ nguyên trường trích dẫn khi sửa, gắn trích dẫn sống từ thư viện của tác giả và kiểm độ trung thực. Manages live Zotero citations."
metadata:
  version: 2.0.0-alpha.8
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review, evidence-synthesis]
---

# Quản lý trích dẫn

Follow the shared [working principles](../medrs/references/working-principles.md).

Read [references/library-access-contract.md](references/library-access-contract.md) before touching any library. For verification work, also read [references/citation-faithfulness.md](references/citation-faithfulness.md).

Xác định backend trước: thư viện Zotero cục bộ, tệp xuất BibTeX/RIS/CSL-JSON, hay không có thư viện nào. Khai báo backend đã dùng trong mọi kết quả trả về.

## Truy cập thư viện

Thư viện là tài sản của tác giả. Mọi truy cập là chỉ-đọc: không thêm, sửa, gắn thẻ, gộp trùng hay dọn thùng rác. Nếu host không đọc được thư viện cục bộ, trả trạng thái `UNAVAILABLE` kèm đường đi thay thế bằng tệp xuất; không mô phỏng nội dung thư viện.

Phân giải định danh trường tại thời điểm chạy thay vì dùng số cố định, loại trừ mục đã xóa, và ghi lại thời điểm đọc. Bản ghi thiếu DOI/PMID giữ trạng thái `UNRESOLVED` cho tới khi tác giả xác nhận.

## Kiểm chứng trung thực

Kiểm tra thu hồi và đính chính trước tiên; một bài đã thu hồi được báo ngay trước mọi phán định khác. Sau đó đối chiếu từng mệnh đề với nguồn được trích và phán định theo bốn mức trong hợp đồng: trung thực, nói quá, quy sai nguồn, hoặc không có trong nguồn.

Mọi con số cụ thể phải xuất hiện trong chính bài được trích. Số liệu chỉ được thuật lại từ một bài khác là quy sai nguồn, kể cả khi con số đúng.

## Bàn giao

Nhận truy xuất mới từ `tim-y-van`; trả kết quả phán định cho `tu-phan-bien`; chuyển yêu cầu kiểu trích dẫn và danh mục tham khảo trong Word cho `dinh-dang-tai-lieu`.

Trả về backend đã dùng, phạm vi thư viện, bảng phán định theo từng cặp trích dẫn × mệnh đề, danh sách thu hồi, mục chưa phân giải và giới hạn năng lực.
