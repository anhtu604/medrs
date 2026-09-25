---
name: phan-tich-stata
description: "Viết và chạy do-file Stata tái lập cho phân tích y học, kèm nhật ký, phiên bản và băm kết quả. Writes and runs reproducible Stata analyses."
metadata:
  version: 2.0.0-alpha.8
  role: leaf
  locale: [vi, en]
  document_types: [analysis, thesis, dissertation, journal-article]
---

# Phân tích bằng Stata

Follow the shared [working principles](../medrs/references/working-principles.md).

Generate an auditable Stata do-file from a confirmed analysis plan. Read [references/reproducibility-contract.md](references/reproducibility-contract.md) before creating or interpreting execution artifacts, and honor [../phan-tich-so-lieu/references/analysis-deviation-contract.md](../phan-tich-so-lieu/references/analysis-deviation-contract.md).

Require an input schema, value labels and reference groups, analysis-set filters, missing-data rules, model specification, planned tables/figures, and de-identified data or traceable real output.

When Stata is unavailable, return a `.do` file marked `NOT_RUN`, required version/packages, expected artifacts, and run instructions. Do not fabricate numeric output or logs. A verified run records `about`, command, exit status, full raw log, warnings, seed where relevant, and hashes of do-file, data, log, tables, figures, and diagnostics.

Keep raw logs unchanged and link presentation outputs back to them. Report denominators, missingness, estimates, confidence intervals, exact p-values where relevant, exclusions and assumption checks. Preserve planned versus achieved sample sizes and all attempted exploratory specifications.

