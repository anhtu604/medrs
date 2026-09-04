---
name: phan-tich-r
description: Sinh, kiểm tra và điều phối chạy script R tái lập cho nghiên cứu y học; reads real outputs and builds tables. Không bịa kết quả hoặc nhận đã chạy khi thiếu R runtime, dữ liệu và provenance.
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [analysis, thesis, dissertation, journal-article]
---

# Phân tích bằng R

Generate an auditable R script from a confirmed analysis plan. Read [references/reproducibility-contract.md](references/reproducibility-contract.md) before creating or interpreting execution artifacts, and honor the parent deviation rules in [../phan-tich-so-lieu/references/analysis-deviation-contract.md](../phan-tich-so-lieu/references/analysis-deviation-contract.md).

Require an input schema, coding and reference levels, analysis sets, missing-data rules, model specification, planned tables/figures, and de-identified data or traceable real output.

When R is unavailable, return a `.R` file marked `NOT_RUN`, required package list, expected artifacts, and run instructions. Do not emit numeric results. When execution is available, preserve `sessionInfo()`, command, exit status, console log, warnings, seed where relevant, and hashes of code, data, and outputs.

Produce code, provenance sidecar, diagnostics, missingness/denominator report, tidy estimates with confidence intervals, and publication-table inputs. Tables must trace to a real model object; simulated examples remain visibly excluded from research results.

