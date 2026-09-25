---
name: tong-hop-bang-chung
description: "Tổng hợp bằng chứng cho tổng quan tường thuật, hệ thống, phạm vi hoặc phân tích gộp, kèm bản đồ bằng chứng. Synthesises evidence across study types."
metadata:
  version: 3.0.0-rc.1
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article, review]
---

# Tổng hợp bằng chứng

Follow the shared [working principles](../medrs/references/working-principles.md).

Read [references/synthesis-modes.md](references/synthesis-modes.md). Before any quantitative pooling, also read [references/meta-analysis-readiness.md](references/meta-analysis-readiness.md). Consume the confirmed question/protocol, record and access ledgers from `tim-y-van`, eligibility decisions, study characteristics, extraction provenance, target synthesis mode, and quality-appraisal state.

Select only the mode actually supported. Narrative synthesis and evidence mapping do not become systematic reviews through prose. Keep included, excluded and unresolved records with reasons. Treat abstract-only evidence as limited; do not infer full Methods, detailed risk of bias or unreported effect data. Preserve supportive, neutral and contradictory evidence in a contradiction matrix.

Meta-analysis requires compatible estimands/outcomes/time points, effect and uncertainty or valid conversion data, denominators, independent study units, resolved multiple reports, verified extraction, prespecified model and sensitivity plan. Otherwise return `META_ANALYSIS_NOT_READY` and a structured gap register, never simulated pooled results.

Return mode decision, protocol gaps, search/screening ledger links, citation verification, study table, evidence map, contradiction matrix, extraction table, appraisal links, meta-analysis readiness, claim ceiling, unresolved markers and handoff to `viet-tong-quan` or `viet-ban-luan`.

