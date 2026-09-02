---
name: phan-tich-stata
description: Sinh, kiểm tra và điều phối chạy Stata do-file tái lập cho nghiên cứu y học; reads real logs and outputs. Không tạo log giả, chọn lệnh theo ý nghĩa thống kê hoặc nhận đã chạy khi thiếu runtime.
metadata:
  version: 2.0.0-alpha.1
  role: leaf
  locale: [vi, en]
  document_types: [analysis, thesis, dissertation, journal-article]
---

# Phân tích bằng Stata

Generate an auditable Stata do-file from a confirmed analysis plan. Read [references/reproducibility-contract.md](references/reproducibility-contract.md) before creating or interpreting execution artifacts, and honor [../phan-tich-so-lieu/references/analysis-deviation-contract.md](../phan-tich-so-lieu/references/analysis-deviation-contract.md).

Require an input schema, value labels and reference groups, analysis-set filters, missing-data rules, model specification, planned tables/figures, and de-identified data or traceable real output.

When Stata is unavailable, return a `.do` file marked `NOT_RUN`, required version/packages, expected artifacts, and run instructions. Do not fabricate numeric output or logs. A verified run records `about`, command, exit status, full raw log, warnings, seed where relevant, and hashes of do-file, data, log, tables, figures, and diagnostics.

Keep raw logs unchanged and link presentation outputs back to them. Report denominators, missingness, estimates, confidence intervals, exact p-values where relevant, exclusions and assumption checks. Preserve planned versus achieved sample sizes and all attempted exploratory specifications.

