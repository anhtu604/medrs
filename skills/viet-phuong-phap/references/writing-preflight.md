# Shared writing preflight

Every section writer reads this reference by relative path before returning a draft. The rules live here only.

## Inputs

- Research Passport and active locale-profile version
- section draft and section hash
- claim/evidence table
- unresolved markers

## Checks

1. `FABRICATION`: every fact, citation, number, approval, policy, and completed procedure is traceable to a confirmed Passport value or source. Otherwise emit the applicable unresolved marker.
2. `UNRESOLVED`: unresolved scientific or administrative decisions remain visible and are not converted into fluent prose that appears final.
3. `CAUSALITY`: causal verbs do not exceed the design and estimand. Observational association is not rewritten as intervention effect.
4. `LOCALE`: language, terminology, attribution, tense, forms of address, and section conventions match the active locale profile rather than literal translation.

## Output

Return `status` as `PASS` or `REVISE`, one record per check, markers, locale-profile identifier, Passport hash, and section hash. In a multi-section draft, the complete `kiem-van-phong` gate remains `PENDING`; this preflight is not a substitute for the assembled-document audit.

## Độ sâu và độ dài

Lấy phạm vi, độ sâu phân tích và ngân sách từ profile loại tài liệu (`profiles/document-type/<loại>.yaml` trong thư mục hỗ trợ của MedRS), chọn theo `document_type` trong Research Passport. Giá trị cũ như `thesis` hay `journal-article` được ánh xạ tự động; nói lựa chọn trong một dòng. Chỉ hỏi khi tác giả muốn khác mặc định.

## Giọng tác giả

Nếu cạnh Research Passport có `author-style-profile.json`, soạn ngay theo giọng đó: độ dài câu và đoạn, từ nối, ngôi xưng, quy ước số và cách đặt trích dẫn trong `measured`, và các khuôn diễn đạt trong `patterns`. Hồ sơ quyết định lựa từ và nhịp câu; số liệu, trích dẫn và mức độ mệnh đề không đổi vì giọng văn.

Chỉ dùng `patterns` sau khi xác minh với văn bản gốc bằng `scripts/style_profile.py --check-profile author-style-profile.json <các văn bản gốc>`. Nếu không có văn bản gốc hoặc kiểm tra không đạt, bỏ qua `patterns` chưa xác minh và chỉ dùng `measured`.
