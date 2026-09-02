---
name: danh-gia-chat-luong-bang-chung
description: Đánh giá nguy cơ sai lệch và độ chắc chắn bằng chứng y học bằng RoB 2, GRADE hoặc CERQual theo từng kết quả/phát hiện. Appraises evidence quality. Không kiểm checklist báo cáo, đoán signalling answer hay dùng nhãn chung cho toàn nghiên cứu.
metadata:
  version: 2.0.0-alpha.1
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, journal-article, review]
---

# Đánh giá chất lượng bằng chứng

Read [references/appraisal-routing.md](references/appraisal-routing.md) first. For RoB 2, also read [references/rob2-use-contract.md](references/rob2-use-contract.md) and `../../coverage/rob2-parallel-2019.yaml`. For certainty of quantitative intervention effects, read [references/grade-certainty.md](references/grade-certainty.md) and `../../coverage/grade-interventions-6.5.1.yaml`. For qualitative review findings, read [references/cerqual-confidence.md](references/cerqual-confidence.md) and `../../coverage/cerqual-2018.yaml`.

Choose the framework from the study and inference target, not from the preferred output label. Define the result, outcome or review finding before judging it. Record the source used for every answer. Missing protocols, analysis plans, reports or result-specific evidence remain `UNRESOLVED`; they are never reconstructed from memory.

For RoB 2, complete every applicable signalling-question identifier, retain NI where justified, and use the official algorithm/version for domain and overall judgments. This plugin's summaries are navigation aids, not a replacement for the licensed official workbook. For GRADE and CERQual, explain each domain/component and the resulting direction of concern. Do not auto-rate an RCT high or treat study-level appraisal as outcome-level certainty.

Return framework/version, target of inference, evidence locators, item-level answers, domain judgments, official-tool provenance, unresolved items, overall judgment with rationale, sensitivity implications, and handoff to `tong-hop-bang-chung` or `kiem-chung-ban-thao`.
