---
name: bo-cuc-tai-lieu
description: "Sắp xếp bố cục chương mục của luận văn, luận án hoặc bài báo theo profile nguồn chính thức, tạo bản mới không ghi đè. Restructures document sections. Định dạng Word thuộc skill định dạng tài liệu."
metadata:
  version: 3.0.0-rc.1
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article]
---

# Bố cục tài liệu

Follow the shared [working principles](../medrs/references/working-principles.md).
When editing or writing into a Word file, follow the [Zotero field contract](../quan-ly-trich-dan/references/zotero-field-contract.md).

Read [references/structure-contract.md](references/structure-contract.md). For HMU theses, also read [references/hmu-profile-use.md](references/hmu-profile-use.md) and `../../profiles/institution/hmu/thesis-master-2020-current-2026.yaml`.

First verify the target institution/journal, document type, submission stage, source version, checksum and freshness. If an official profile is absent, stale or mismatched, return `OFFICIAL_RULE_REQUIRED`; do not turn remembered conventions into requirements. Compare the actual draft's semantic sections with the target order and preserve unknown blocks for author review.

Produce a proposed mapping and move/rename/split/merge plan before changing the document. A move requires explicit author approval. Missing required content becomes `AUTHOR_INPUT_REQUIRED`; never manufacture text to make the outline pass. Optional sections remain optional unless the source states a condition that makes them mandatory.

After approval, write a new artifact, never overwrite the source. Inspect that generated artifact and report its actual recognized order, missing/unknown sections, heading-depth findings, change log and validation status. Hand Word styles, margins, TOC fields, section breaks, pagination, rendering and visual inspection to `dinh-dang-tai-lieu`.
