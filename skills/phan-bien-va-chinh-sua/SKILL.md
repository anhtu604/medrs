---
name: phan-bien-va-chinh-sua
description: Use when reviewing a medical manuscript or thesis, answering reviewers point by point, revising after peer review, examining a thesis, or verifying revision commitments. Không dùng cho kiểm tra trước nộp khi chưa có nhận xét phản biện.
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review]
---

# Phản biện và chỉnh sửa

Read [references/review-revision-contract.md](references/review-revision-contract.md). For point-by-point responses, also read [references/response-matrix.md](references/response-matrix.md). For thesis examination, read [references/thesis-examination.md](references/thesis-examination.md).

Preserve each reviewer/examiner comment verbatim with reviewer, round, page/line or source locator. Classify the request, assess whether it is scientifically valid, and choose `accept`, `partial`, `decline`, or `clarify` with evidence. Politeness never requires accepting an unsupported change. Never invent new analyses, ethics approvals, citations or results to satisfy a comment.

For accepted or partially accepted requests, make the change in a new artifact and link the response to its exact locator and artifact hash. A response that claims a change without a changed artifact is blocked. When any number changes, use the claim ledger to propagate it through abstract, text, tables, figures, supplement and response letter; unresolved mismatches remain `PROPAGATION_INCOMPLETE`.

Run the relevant section writer, statistical workflow, `kiem-van-phong`, `kiem-chung-ban-thao`, structure or formatting skill when the commitment touches that domain. Reopen and re-review the changed artifact. If its hash changes after review, invalidate the commitment and return `RE_REVIEW_REQUIRED`.

Return review findings or response matrix, evidence/rationale, commitments, changed-artifact links and hashes, propagation report, disclosure changes, unresolved items and re-review state.
