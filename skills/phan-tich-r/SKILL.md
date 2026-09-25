---
name: phan-tich-r
description: "Viết và chạy mã R tái lập cho phân tích y học, kèm nhật ký, phiên bản gói và băm kết quả. Writes and runs reproducible R analyses."
metadata:
  version: 3.0.0-rc.1
  role: leaf
  locale: [vi, en]
  document_types: [analysis, thesis, dissertation, journal-article]
---

# Phân tích bằng R

Follow the shared [working principles](../medrs/references/working-principles.md).

Generate an auditable R script from a confirmed analysis plan. Read [references/reproducibility-contract.md](references/reproducibility-contract.md) before creating or interpreting execution artifacts, and honor the parent deviation rules in [../phan-tich-so-lieu/references/analysis-deviation-contract.md](../phan-tich-so-lieu/references/analysis-deviation-contract.md).

Require an input schema, coding and reference levels, analysis sets, missing-data rules, model specification, planned tables/figures, and de-identified data or traceable real output.

When R is unavailable, return a `.R` file marked `NOT_RUN`, required package list, expected artifacts, and run instructions. Do not emit numeric results. When execution is available, preserve `sessionInfo()`, command, exit status, console log, warnings, seed where relevant, and hashes of code, data, and outputs.

Produce code, provenance sidecar, diagnostics, missingness/denominator report, tidy estimates with confidence intervals, and publication-table inputs. Tables must trace to a real model object; simulated examples remain visibly excluded from research results.

