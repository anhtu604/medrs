---
name: dao-duc-va-quan-tri-du-lieu
description: Use when a medical protocol needs ethics, consent, registration, privacy, data-governance, or approval-status planning. Dùng khi lập hồ sơ đạo đức và quản trị dữ liệu; không dùng để bịa số chấp thuận hoặc thay tư vấn pháp lý.
metadata:
  version: 2.0.0-alpha.1
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript]
---

# Đạo đức và quản trị dữ liệu

Lập artifact theo hồ sơ nguồn đã xác minh, không tuyên bố nghiên cứu đã được chấp thuận nếu tác giả chưa cung cấp bằng chứng.

## Đầu vào

Yêu cầu Passport, thẩm quyền áp dụng, giai đoạn nghiên cứu, loại dữ liệu, nơi lưu/chuyển dữ liệu, căn cứ xử lý, trạng thái đồng thuận, đăng ký và phê duyệt.

## Quy trình

1. Chọn `references/vietnam-profile.md` và/hoặc `references/international-profile.md` theo nơi thực hiện, tài trợ và đích nộp.
2. Đối chiếu `references/source-register.yaml`. Nếu nguồn `STALE` hoặc `UNVERIFIED`, dừng áp quy tắc hiện hành, gắn `OFFICIAL_RULE_REQUIRED`, rồi yêu cầu nguồn chính thức mới.
3. Dùng `references/data-governance.md` để lập luồng dữ liệu và quyền truy cập.
4. Trả artifact có: jurisdiction, study stage, data class, destination, authorization basis, consent/waiver state, registration state và unresolved approvals.

## Ranh giới

- Không tự điền số quyết định, tên hội đồng, ngày phê duyệt, miễn đồng thuận hoặc đăng ký thử nghiệm.
- Không gọi một kế hoạch là “tuân thủ” chỉ vì đã điền checklist.
- Quy trình nội bộ của cơ sở phải do tác giả cung cấp hoặc lấy từ nguồn chính thức hiện hành.
- Đây là hỗ trợ soạn hồ sơ, không phải ý kiến pháp lý hay quyết định của hội đồng đạo đức.

## Đầu ra

Tách rõ `CONFIRMED`, `DRAFT_INFERRED`, `UNRESOLVED`; liệt kê nguồn theo phiên bản và các điểm cần hội đồng/tác giả quyết định.
