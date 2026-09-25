---
name: dinh-dang-tai-lieu
description: "Định dạng Word chuẩn cho luận văn, luận án và bản thảo: style, lề, đề mục đánh số tự động, mục lục, chú thích bảng hình và tham chiếu chéo. Formats Word documents."
metadata:
  version: 3.0.0-rc.1
  role: leaf
  locale: [vi, en]
  document_types: [thesis, dissertation, journal-article]
---

# Định dạng tài liệu

Follow the shared [working principles](../medrs/references/working-principles.md).

Read [references/backend-and-validation-contract.md](references/backend-and-validation-contract.md) and [references/word-style-and-refresh-contract.md](references/word-style-and-refresh-contract.md). For heading numbering, caption sequences and cross-references, read [references/heading-numbering-and-cross-references.md](references/heading-numbering-and-cross-references.md). For HMU, also read [references/hmu-word-mechanics.md](references/hmu-word-mechanics.md) and `../../profiles/institution/hmu/word-format-master-2020-current-2026.yaml`.

For a new HMU document, use [assets/hmu-word-styles.docx](assets/hmu-word-styles.docx) as the style carrier when the host can preserve DOCX styles. For an existing document, merge or recreate those definitions; never replace the user's content with the carrier file.

Verify the target profile's official source, version, freshness and checksum. Inspect the actual input DOCX. If the source is missing or stale, return `OFFICIAL_RULE_REQUIRED`; if a required mapping is ambiguous, return `AUTHOR_INPUT_REQUIRED`. Receive semantic order from `bo-cuc-tai-lieu`; do not move, split, merge or write sections here.

Select a backend only after a capability probe. Word COM is valid only on local Windows with its bridge; LibreOffice UNO requires both UNO and its executable; otherwise use OOXML-only. Never claim fields updated, pagination correct, or visual layout passed from OOXML inspection alone.

Show the formatting plan and obtain author approval. Write a new DOCX, preserve unrecognized package parts and tracked changes, and never overwrite the source. Treat named styles as authoritative: repair and assign body, heading, TOC, table-of-figures, caption, bibliography, table-text and list styles; clear conflicting direct formatting without erasing semantic emphasis. Set fields to update, normalize automatic bullets through deterministic numbering, and allocate table columns from content demand with bounded widths.

Reopen the output after field refresh and validate the actual style definitions and assignments, direct-formatting drift, section properties, fields, captions, adaptive table grids and numbering indents. A rendering backend must produce a PDF and page images before visual checks can pass. Return output/change-log/validation hashes, backend evidence, performed checks, unperformed checks and `AUTHOR_APPROVAL_REQUIRED` where human inspection remains.
