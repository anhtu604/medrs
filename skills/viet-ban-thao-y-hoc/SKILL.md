---
name: viet-ban-thao-y-hoc
description: "Điều phối viết toàn bộ bài báo, luận văn hoặc luận án theo profile loại tài liệu, gọi từng skill viết phần rồi ráp bản thảo; chuyển luận văn thành bài báo. Orchestrates full manuscripts."
metadata:
  version: 2.0.0-alpha.8
  role: orchestrator
  locale: [vi, en]
  document_types: [journal-article, thesis, dissertation]
---

# Viết bản thảo y học

Follow the shared [working principles](../medrs/references/working-principles.md).
When editing or writing into a Word file, follow the [Zotero field contract](../quan-ly-trich-dan/references/zotero-field-contract.md).

Read [references/assembly-workflow.md](references/assembly-workflow.md). Use the Research Passport, its document-type profile from `../../profiles/document-type/`, the locale profile, the source ledger and the verified analysis artifacts. Converting a thesis into an article means switching the document-type profile and reassembling from the same verified results. Route prose to the matching section writer; route semantic order to `bo-cuc-tai-lieu`, Word mechanics to `dinh-dang-tai-lieu`, and analysis to `phan-tich-so-lieu`.

Assemble only completed section artifacts. Run one full `kiem-van-phong` gate on the first complete assembly; after substantive revision, re-audit affected chunks and run one final document gate. Then call `tu-phan-bien`. Never resolve conflicting facts by preference, and never draft missing Results.

Return a manuscript manifest, section states and hashes, dependency graph, unresolved markers, target-profile compliance state, gate history, and submission blockers.
