---
name: tim-hieu-de-tai
description: "Trò chuyện cùng tác giả để hiểu thật kỹ đề tài trước khi viết: kiến thức nền có nguồn, câu hỏi và mục tiêu, phương pháp, kết quả mong đợi; hỏi ngược để kiểm tra và ghi vào README dự án. Guides the author to understand the study before writing."
metadata:
  version: 3.2.0
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, journal-article, project-ck2, project-institutional]
---

# Tìm hiểu đề tài

Follow the shared [working principles](../medrs/references/working-principles.md).

Read [references/conversation-contract.md](references/conversation-contract.md) before the first turn. Nhận việc qua `medrs` khi dự án chưa có gì rõ ràng hoặc khi tác giả muốn trao đổi về đề tài.

Workspace và README theo [project workspace](../leader-nghien-cuu/references/project-workspace.md): `initialize_project` tạo các mục ngữ cảnh; không ghi đè chữ tác giả. Trạng thái cuộc trò chuyện đọc và ghi bằng [scripts/topic_understanding.py](scripts/topic_understanding.py):

```
python topic_understanding.py status <thư mục dự án>
python topic_understanding.py part <thư mục> <YYYY-MM-DD> <background|question|methods|expected> <EXPLAINED|CHECKED_BACK|DONE>
python topic_understanding.py open-items <thư mục> <YYYY-MM-DD> <số điểm còn mở>
python topic_understanding.py defer <thư mục> <YYYY-MM-DD>
python topic_understanding.py confirm <thư mục> <YYYY-MM-DD> "<lời xác nhận của tác giả>"
```

Ngày là ngày thực hiện. Không có Python: theo cùng các trạng thái, ghi trực tiếp vào mục "Hiểu đề tài" của README.

Y văn tìm qua [tim-y-van](../tim-y-van/SKILL.md); bản nháp, đề cương và Research Passport qua [ho-so-nghien-cuu](../ho-so-nghien-cuu/SKILL.md). Xác nhận xong thì chuyển cho `leader-nghien-cuu`.

Mỗi lượt trả về: một câu hỏi hoặc phần giải thích, phần đang làm, các mục README vừa cập nhật, và điểm còn mở.
