---
name: bo-cuc-tai-lieu
description: Lập và áp dụng bố cục ngữ nghĩa cho luận văn, luận án hoặc bài báo theo profile nguồn chính thức. Restructures approved sections in a new artifact. Không chỉnh font, lề, trường mục lục, phân trang hoặc tự viết phần còn thiếu.
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article]
---

# Bố cục tài liệu

Read [references/structure-contract.md](references/structure-contract.md). For HMU theses, also read [references/hmu-profile-use.md](references/hmu-profile-use.md) and `../../profiles/institution/hmu/thesis-master-2020-current-2026.yaml`.

First verify the target institution/journal, document type, submission stage, source version, checksum and freshness. If an official profile is absent, stale or mismatched, return `OFFICIAL_RULE_REQUIRED`; do not turn remembered conventions into requirements. Compare the actual draft's semantic sections with the target order and preserve unknown blocks for author review.

Produce a proposed mapping and move/rename/split/merge plan before changing the document. A move requires explicit author approval. Missing required content becomes `AUTHOR_INPUT_REQUIRED`; never manufacture text to make the outline pass. Optional sections remain optional unless the source states a condition that makes them mandatory.

After approval, write a new artifact, never overwrite the source. Inspect that generated artifact and report its actual recognized order, missing/unknown sections, heading-depth findings, change log and validation status. Hand Word styles, margins, TOC fields, section breaks, pagination, rendering and visual inspection to `dinh-dang-tai-lieu`.
