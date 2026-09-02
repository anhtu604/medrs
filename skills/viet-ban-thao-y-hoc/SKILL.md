---
name: viet-ban-thao-y-hoc
description: Điều phối viết và ráp bài báo, luận văn hoặc luận án y học từ Research Passport và target profile. Orchestrates section writers and gates. Không thay section writer, không tự quyết bố cục hay bịa phần còn thiếu.
metadata:
  version: 2.0.0-alpha.1
  role: orchestrator
  locale: [vi, en]
  document_types: [journal-article, thesis, dissertation]
---

# Viết bản thảo y học

Read [references/assembly-workflow.md](references/assembly-workflow.md). Confirm the Research Passport, document type, target profile, locale profile, approved outline, source ledger, verified analysis artifacts, depth, and budget. Route prose to the matching section writer; route semantic order to `bo-cuc-tai-lieu`, Word mechanics to `dinh-dang-tai-lieu`, and analysis to `phan-tich-so-lieu`.

Assemble only completed section artifacts. Run one full `kiem-van-phong` gate on the first complete assembly; after substantive revision, re-audit affected chunks and run one final document gate. Then call `kiem-chung-ban-thao`. Never resolve conflicting facts by preference, and never draft missing Results.

Return a manuscript manifest, section states and hashes, dependency graph, unresolved markers, target-profile compliance state, gate history, and submission blockers.

