---
name: dinh-dang-tai-lieu
description: Use when a medical thesis, dissertation, or manuscript DOCX needs source-governed Word styles, margins, headings, TOC, captions, section breaks, page numbering, rendering, or pre-submission format validation. Không dùng để đổi nội dung hay bố cục ngữ nghĩa.
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article]
---

# Định dạng tài liệu

Read [references/backend-and-validation-contract.md](references/backend-and-validation-contract.md). For HMU, also read [references/hmu-word-mechanics.md](references/hmu-word-mechanics.md) and `../../profiles/institution/hmu/word-format-master-2020-current-2026.yaml`.

Verify the target profile's official source, version, freshness and checksum. Inspect the actual input DOCX. If the source is missing or stale, return `OFFICIAL_RULE_REQUIRED`; if a required mapping is ambiguous, return `AUTHOR_INPUT_REQUIRED`. Receive semantic order from `bo-cuc-tai-lieu`; do not move, split, merge or write sections here.

Select a backend only after a capability probe. Word COM is valid only on local Windows with its bridge; LibreOffice UNO requires both UNO and its executable; otherwise use OOXML-only. Never claim fields updated, pagination correct, or visual layout passed from OOXML inspection alone.

Show the formatting plan and obtain author approval. Write a new DOCX, preserve unrecognized package parts and tracked changes, and never overwrite the source. Reopen the output and validate actual styles, section properties, fields, captions and numbering. A rendering backend must produce a PDF and page images before visual checks can pass. Return output/change-log/validation hashes, backend evidence, performed checks, unperformed checks and `AUTHOR_APPROVAL_REQUIRED` where human inspection remains.
