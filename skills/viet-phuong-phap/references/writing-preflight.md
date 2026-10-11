# Shared writing preflight

Every section writer reads this reference by relative path before returning a draft. The rules live here only.

Select audit scope through [the shared gate lifecycle](../../kiem-van-phong/references/gate-lifecycle.md). Import its `required_gate_scope` helper when automating; selecting scope never marks the audit PASS. Carry statistical qualifications and unresolved data status into every dependent claim.

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
5. `PROJECT_DECISIONS`: use the effective terminology/codebook, scoped author decisions and protected arguments; scan all changed manuscript surfaces for workflow codes.
6. `RESULT_IDENTITY`: every numerical sentence matches indicator, denominator, group, time/pair, test and adjustment as well as value; do not borrow an equal p from another comparison.
7. `PLAIN_PROSE`: each sentence adds a concrete point. Remove generic contribution filler and repeated caveats while preserving necessary qualification and source support.

## Output

Return `status` as `PASS` or `REVISE`, one record per check, markers, locale-profile identifier, Passport hash, and section hash. In a multi-section draft, the complete `kiem-van-phong` gate remains `PENDING`; this preflight is not a substitute for the assembled-document audit.

## Độ sâu và độ dài

Lấy phạm vi, độ sâu phân tích và ngân sách từ profile loại tài liệu (`profiles/document-type/<loại>.yaml` trong thư mục hỗ trợ của MedRS), chọn theo `document_type` trong Research Passport. Khi lập ngân sách viết, ánh xạ các giá trị cũ như `thesis` hay `journal-article` sang profile tương ứng và nói lựa chọn trong một dòng. Chỉ hỏi khi tác giả muốn khác mặc định.

## Giọng tác giả

Nếu cạnh Research Passport có `author-style-profile.json`, soạn ngay theo giọng đó: độ dài câu và đoạn, từ nối, ngôi xưng, quy ước số và cách đặt trích dẫn trong `measured`, và các khuôn diễn đạt trong `patterns`. Hồ sơ quyết định lựa từ và nhịp câu; số liệu, trích dẫn và mức độ mệnh đề không đổi vì giọng văn.

Chỉ dùng `patterns` sau khi xác minh với văn bản gốc bằng `scripts/style_profile.py --check-profile author-style-profile.json <các văn bản gốc>`. Nếu không có văn bản gốc hoặc kiểm tra không đạt, bỏ qua `patterns` chưa xác minh và chỉ dùng `measured`.
