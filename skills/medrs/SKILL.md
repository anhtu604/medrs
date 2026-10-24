---
name: medrs
description: "Điểm vào duy nhất `/medrs` cho dự án nghiên cứu y học: hiểu yêu cầu tiếng Việt hoặc tiếng Anh và chuyển đến đúng skill chuyên môn. Routes medical research requests to the right specialist skill. Dùng cho nghiên cứu, không dùng để tư vấn điều trị."
metadata:
  version: 3.2.0
  role: entry-point
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript, evidence-synthesis]
---

# MedRS

Follow the [working principles](references/working-principles.md) in every response.

Treat `/medrs` as the single user-facing entrypoint. Classify every requested item, preserve the Research Passport and effective work order, and build a complete route plan. Do not perform specialist work inside this entrypoint.

At project start/adoption, hand off README, dated history/logs and accepted-final setup through [../leader-nghien-cuu/references/project-workspace.md](../leader-nghien-cuu/references/project-workspace.md) before substantive work. Reuse the existing workspace on later rounds.

Before writing work, check topic understanding with [../tim-hieu-de-tai/scripts/topic_understanding.py](../tim-hieu-de-tai/scripts/topic_understanding.py) `status <project folder>` (chat-only host: read the README section "Hiểu đề tài"). No workspace, or a new project not `CONFIRMED` → route to `tim-hieu-de-tai` first. A 3.1 project without that section, or one mid-revision → offer it in one line only. `DEFERRED_BY_AUTHOR` → one-line reminder, then do the requested work.

Read [references/routing-contract.md](references/routing-contract.md). Use [scripts/router.py](scripts/router.py) for reproducible candidate routing when Python exists; read the same contract and skill index on chat-only hosts. A candidate is not proof of execution.

## Routing

Resolve document type, target language and locale profile, requested section, study design, project stage, data sensitivity, and available artifacts. Ask only for information not already present. Use one bounded question at a time when a missing choice changes the route.

If the user provides a legacy skill name, read [references/legacy-skill-map.yaml](references/legacy-skill-map.yaml), report the canonical destination and whether it is active, then route or explain the unavailable slice. Legacy names never appear in frontmatter descriptions.

If adopting an existing draft, use `ho-so-nghien-cuu` before asking for objectives/design already in it. Do not redirect every scoped edit to adoption. For multi-domain work, planning, guidance, revision rounds or final acceptance, hand the complete plan to `leader-nghien-cuu`; it coordinates writers, reviewers and Word checks. Preserve all requested items even when a last instruction adds another task.

## Safety

- Do not diagnose or recommend treatment.
- Do not invent data, sources, approvals, policies, institutional rules, or completed work.
- Record unavailable capabilities and unresolved decisions with stable markers.
- Before external transfer, identify the data class, destination, fields, authorization, and local alternative.

## Output

Return the routing decision, known Passport context, open questions, capability limitations, and the named handoff. A route to a future slice is reported as unavailable; it is not simulated.
