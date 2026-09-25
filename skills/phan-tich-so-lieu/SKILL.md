---
name: phan-tich-so-lieu
description: "Điều phối phân tích số liệu y học theo kế hoạch và diễn giải kết quả theo ý nghĩa lâm sàng và cỡ hiệu ứng, chạy qua R hoặc Stata. Coordinates analysis and interprets results clinically."
metadata:
  version: 3.0.0-rc.1
  role: leaf
  locale: [vi, en]
  document_types: [analysis, thesis, dissertation, journal-article]
---

# Phân tích số liệu

Follow the shared [working principles](../medrs/references/working-principles.md).

Coordinate execution through `phan-tich-r` or `phan-tich-stata`; do not impersonate either runtime. Before accepting any change to the confirmed analysis plan, read [references/analysis-deviation-contract.md](references/analysis-deviation-contract.md). For time-to-event outcomes or a clinical prediction model, read [references/time-to-event-contract.md](references/time-to-event-contract.md) first.

## Required inputs

Require a confirmed Research Passport and analysis plan, analysis-set definition, variable dictionary, de-identified verified data or author-supplied real output, and the intended backend. Preserve planned and achieved sample sizes as separate fields.

## Execution boundary

Probe the requested backend. If it is unavailable, produce code and an execution checklist with status `NOT_RUN`. If the author supplies output, hash it and use `USER_SUPPLIED_OUTPUT_UNVERIFIED`; interpret conditionally until its data/script linkage is confirmed. Use `RUN_VERIFIED` only with executable, version, command, exit status, code/input/output hashes, log, and warnings.

Refuse significance-driven model selection, outcome switching, unexplained exclusions, or rewriting target sample size after recruitment. Label justified departures `DEVIATION`, record rationale and timing, and retain prespecified, sensitivity, and exploratory analyses separately.

## Interpretation

Interpret each estimate by its clinical meaning first: the size and direction of the effect, its confidence interval, and whether it crosses a minimal clinically important difference when the author supplies one. P-values support that reading; they do not lead it. State what each estimate shows at the strength the design supports.

## Output

Return an `AnalysisRun`, assumption checks, missingness and denominator accounting, effect estimates with confidence intervals, exact p-values where relevant, sensitivity results, deviations, limitations, and routes to the backend artifacts. Never fabricate coefficients, tables, figures, logs, or interpretations.
