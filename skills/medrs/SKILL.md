---
name: medrs
description: Điểm vào duy nhất `/medrs` cho dự án nghiên cứu y học; định tuyến yêu cầu Việt–Anh đến đúng skill chuyên môn. Không dùng cho tư vấn điều trị hoặc khi tác giả chỉ yêu cầu thao tác ngoài nghiên cứu.
metadata:
  version: 2.0.0-alpha.2
  role: entry-point
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript, evidence-synthesis]
---

# MedRS

Treat `/medrs` as the single user-facing entrypoint. Classify the request, preserve the Research Passport, and route to one canonical skill. Do not perform specialist work inside this entrypoint.

## Routing

Resolve document type, target language and locale profile, requested section, study design, project stage, data sensitivity, and available artifacts. Ask only for information not already present. Use one bounded question at a time when a missing choice changes the route.

If the user provides a legacy skill name, read [references/legacy-skill-map.yaml](references/legacy-skill-map.yaml), report the canonical destination and whether it is active, then route or explain the unavailable slice. Legacy names never appear in frontmatter descriptions.

If the user has an existing DOCX, Markdown, or text draft, route to `ho-so-nghien-cuu` in `adopt-existing-project` mode before asking them to re-enter objectives or design details.

## Safety

- Do not diagnose or recommend treatment.
- Do not invent data, sources, approvals, policies, institutional rules, or completed work.
- Record unavailable capabilities and unresolved decisions with stable markers.
- Before external transfer, identify the data class, destination, fields, authorization, and local alternative.

## Output

Return the routing decision, known Passport context, open questions, capability limitations, and the named handoff. A route to a future slice is reported as unavailable; it is not simulated.
