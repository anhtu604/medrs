---
name: kiem-chung-ban-thao
description: "Kiểm chứng bản thảo y học trước nộp: claim–citation, số liệu xuyên phần, reporting guideline, liêm chính, disclosure và target profile. Validates actual artifacts. Không sửa ngầm nội dung hoặc cho qua checklist chưa nạp đủ."
metadata:
  version: 2.0.0-alpha.2
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, journal-article, review]
---

# Kiểm chứng bản thảo

Read [references/validation-contract.md](references/validation-contract.md). Inspect the generated manuscript and its artifacts, not the configuration or formatting script. Require the Passport, target/locale profiles, source ledger, analysis runs, section manifests, style-gate state, reporting-guideline coverage, disclosures, and output file.

Check citation existence and support, numeric and terminology consistency, objective–method–result–conclusion alignment, causal ceiling, table/figure/text agreement, marker leakage, authorship/contribution/funding/conflict/AI disclosures, target structure, and exact applicable reporting items. Missing or stale substantive references block the corresponding pass.

Return findings with artifact locator, severity, evidence, owner and required action; consistency matrix; reporting coverage; unresolved approvals; readiness verdict; and a revalidation plan. Do not silently rewrite the manuscript.
