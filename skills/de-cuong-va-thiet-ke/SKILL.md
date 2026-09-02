---
name: de-cuong-va-thiet-ke
description: Thiết kế câu hỏi, mục tiêu, quần thể, biến và chiến lược chọn mẫu cho nghiên cứu y học. Designs medical research protocols. Không tính cỡ mẫu, chọn mô hình theo kết quả quan sát hay viết Results.
metadata:
  version: 2.0.0-alpha.1
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation]
---

# Đề cương và thiết kế

Develop a defensible design artifact from a confirmed Research Passport. Read [references/contract.yaml](references/contract.yaml) before accepting work and [references/design-contract.md](references/design-contract.md) when design details are needed.

## Owns

Research question, objectives, hypotheses, design family, target population, eligibility, sampling frame and strategy, variable operationalization, timing, and bias controls.

## Boundary

Do not calculate numeric sample size, select a fitted model, interpret results, or change objectives after observing significance. Hand sample-size and estimand work to `co-mau-va-ke-hoach-phan-tich` with the design artifact.

## Workflow

1. Confirm project stage and distinguish planned from completed work.
2. Align question, objective, outcome timing, design, and feasible population.
3. Identify threats to selection, information, confounding, temporal ordering, and loss to follow-up without claiming a formal risk-of-bias appraisal.
4. Return assumptions and unresolved choices for author approval.

## Output

Return a machine-readable design artifact, protocol outline, decision log, handoff fields for sample-size planning, and unresolved markers. Do not name a reporting checklist as completed unless its sourced coverage profile exists.

