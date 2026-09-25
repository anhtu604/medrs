# Hợp đồng trường trích dẫn Zotero

Mọi skill viết hoặc sửa bản thảo Word đi qua hợp đồng này. Mục tiêu: không bao giờ biến một trích dẫn Zotero sống thành chữ chết.

## Sửa đoạn có sẵn

1. Xuất đoạn văn thành văn bản có token: `python scripts/zotero_roundtrip.py export ban-thao.docx --out doan-van.json`. Mỗi trường Zotero hiện thành `⟦Z:n⟧`, mỗi trường khác như tham chiếu chéo hiện thành `⟦F:n⟧`.
2. Chỉ sửa chữ. Giữ mọi token, mỗi token đúng một lần, có thể dời vị trí trong câu.
3. Áp lại: `python scripts/zotero_roundtrip.py apply ban-thao.docx doan-van.json --out ban-moi.docx`. Công cụ đặt lại nguyên văn từng trường và kiểm tra.
4. Kiểm tra mất hoặc thay đổi XML của bất kỳ trường nào (kể cả tham chiếu chéo), hoặc mất hay đổi giá trị `ZOTERO_PREF_*`, là lỗi chặn: tệp không được giao.

Đoạn báo `editable: false` — nằm trong danh mục tài liệu tham khảo, chứa hình, chú thích chân trang, hoặc trường trải nhiều đoạn — không sửa qua đường này. Đoạn có `mixed_formatting: true` sẽ mất định dạng nhấn mạnh trong câu sau khi viết lại; báo tác giả để định dạng lại.

## Viết mới

Khi soạn, ghi trích dẫn bằng mã mục Zotero: `⟦cite:ABCD2345⟧`, nhiều mục thì `⟦cite:ABCD2345;EFGH6789⟧`. Tìm mã mục bằng truy vấn thư viện theo `library-access-contract.md`. Khi áp, thêm `--zotero-db <đường dẫn zotero.sqlite>`; công cụ sinh trường `ADDIN ZOTERO_ITEM CSL_CITATION` sống. Tác giả mở Word, bấm **Zotero → Refresh** để Zotero dựng chữ trích dẫn theo style và dựng lại danh mục.

Mã không tìm thấy, hoặc không đọc được thư viện, thì thành ô `[CẦN TRÍCH DẪN: …]` và vào danh sách `Việc cần bổ sung`. Không bao giờ sinh trường cho mục không phân giải được.

## Theo môi trường

| Môi trường | Giữ trường khi sửa | Sinh trường mới |
|---|---|---|
| Claude Code hoặc Codex trên máy tác giả | Có | Có, đọc `zotero.sqlite` |
| Cowork trên web | Có | Không đọc được thư viện: ô trống cộng mục trong danh sách cuối |

Công cụ cần `python-docx`. Thư viện Zotero chỉ được mở ở chế độ chỉ-đọc bất biến và không bao giờ bị ghi.
