---
name: co-mau-va-ke-hoach-phan-tich
description: Lập estimand, giả định, cỡ mẫu và kế hoạch phân tích định trước cho nghiên cứu y học. Plans estimands, power and analysis sets. Không dùng kết quả quan sát để chọn mô hình hay tối ưu ý nghĩa thống kê.
metadata:
  version: 2.0.0-alpha.1
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation]
---

# Cỡ mẫu và kế hoạch phân tích

Create a prospective, reproducible analysis-plan artifact. Read [references/contract.yaml](references/contract.yaml) for ownership and [references/estimand-and-power.md](references/estimand-and-power.md) for sourced planning requirements.

## Required inputs

Confirmed objective, design, primary outcome and scale, target population, comparison, effect or precision target with provenance, type-I error, power, allocation, clustering/repeated-measure assumptions, expected missingness or attrition, and planned analysis family.

Do not invent a plausible effect size. If an assumption lacks a source or author decision, emit `SOURCE_REQUIRED` or `AUTHOR_APPROVAL_REQUIRED` and provide a sensitivity grid rather than one definitive sample size.

## Boundary

Do not inspect observed outcomes to select a model, outcome definition, subgroup, or target sample. Do not interpret results. R or Stata code may be proposed for reproducibility, but execution is not claimed without a callable runtime and captured output.

## Output

Return estimand, assumptions table, formula or named method, calculation trace, target and adjusted sample sizes, analysis sets, planned model family, missing-data strategy, sensitivity analyses, planned tables/figures, R/Stata route, and decision log.

