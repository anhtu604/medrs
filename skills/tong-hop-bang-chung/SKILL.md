---
name: tong-hop-bang-chung
description: Tổng hợp bằng chứng y học từ record ledger đã xác minh theo narrative, systematic, scoping, evidence-map hoặc meta-analysis readiness. Không đổi nhãn review, bịa citation, bỏ nghiên cứu trái chiều hay gộp khi thiếu số liệu.
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review]
---

# Tổng hợp bằng chứng

Read [references/synthesis-modes.md](references/synthesis-modes.md). Before any quantitative pooling, also read [references/meta-analysis-readiness.md](references/meta-analysis-readiness.md). Consume the confirmed question/protocol, record and access ledgers from `tim-y-van`, eligibility decisions, study characteristics, extraction provenance, target synthesis mode, and quality-appraisal state.

Select only the mode actually supported. Narrative synthesis and evidence mapping do not become systematic reviews through prose. Keep included, excluded and unresolved records with reasons. Treat abstract-only evidence as limited; do not infer full Methods, detailed risk of bias or unreported effect data. Preserve supportive, neutral and contradictory evidence in a contradiction matrix.

Meta-analysis requires compatible estimands/outcomes/time points, effect and uncertainty or valid conversion data, denominators, independent study units, resolved multiple reports, verified extraction, prespecified model and sensitivity plan. Otherwise return `META_ANALYSIS_NOT_READY` and a structured gap register, never simulated pooled results.

Return mode decision, protocol gaps, search/screening ledger links, citation verification, study table, evidence map, contradiction matrix, extraction table, appraisal links, meta-analysis readiness, claim ceiling, unresolved markers and handoff to `viet-tong-quan` or `viet-ban-luan`.

