# Project workspace and retained history

Read before starting or adopting any substantial project, before each revision round, and before replacing a current final artifact. This contract covers local files; chat-only hosts must supply a downloadable README and archive instructions instead of claiming a folder was created.

## Before work

Always create the project README first. `initialize_project` adds the fixed context sections (overview, topic understanding, background, question, methods, expected results, background literature, agreed terms, open points, author decisions, next steps) and appends missing ones to an existing README without touching author text. While topic understanding is not `CONFIRMED`, hand the author to `tim-hieu-de-tai` for the conversation; it does not ask again about confirmed decisions. A new collaborator should be able to identify the question, objectives, design, project type, intended institution/journal, source/data status, input versions, effective author decisions, current stage, completed work, unresolved issues and next action without reading the conversation. Populate these from the Passport and existing files, with unresolved markers where unknown; do not ask again about author-confirmed decisions. Keep detailed private content local. The generated progress block provides storage/status/hash information, not the entire research narrative: fill the contextual sections outside that block and preserve them on updates.

Use one `final/` directory for the current accepted data, manuscript and other deliverables, with stable names and distinct roles. A draft with unresolved checks stays in the day's working area, not in final merely because its filename says final. Internal acceptance and the author's approval are separate.

Create `history/YYYY-MM-DD/` for every active work day. Keep inputs, intermediate outputs, executable scripts, analysis outputs, all logs, checks and notes in this dated area. Each day's README states what was done and what changed versus the preceding day; multiple rounds in one day use separate identifiers. Do not silently overwrite an earlier round or omit a failed run from the log. Store complete execution transcripts under `logs/` and retain their exit states. Logs must exclude participant records, credentials and unnecessary identifiers; protected data themselves stay in an access-controlled project location, not progress prose or public GitHub.

## Portable mechanical helper

Use [../scripts/project_workspace.py](../scripts/project_workspace.py):

```python
from pathlib import Path
from project_workspace import initialize_project, record_event, promote_final
from revision_guard import snapshot

root = Path("project")
initialize_project(root, "study-id", "2026-10-11")
record_event(root, "2026-10-11", {
    "action": "REVISED", "summary": "Updated table styles",
    "changes": "Replaced conflicting direct formatting versus yesterday"})
```

Date is the actual execution date, not a date copied from the example. This helper maintains only its delimited README progress block. It refuses ambiguous markers rather than overwriting author content. Event fields accept redacted strings only; the allowlist is not a personal-data detector. The caller must redact free text before logging. The state contract is [../../../schemas/project-state.schema.json](../../../schemas/project-state.schema.json).

## Replacing a final artifact

Call `promote_final(root, staged, source_snapshot, date, acceptance=receipt)` only after the leader's evidence-bound acceptance for that exact staged hash. The receipt needs status `ACCEPTED_INTERNAL` and `artifact_sha256` from the existing leader receipt (`sha256` is accepted for simple callers). This utility does not supply semantic, visual or author review by itself.

A project lease serializes MedRS writes. Before replacement, check the current author source and the existing final hash against the managed registry; an unregistered collision or author-modified final requires revision intake, not overwrite. Save the staged version and prior final in the day's unique round, then publish. A failed promotion retains staged, prior and pending files with `PROMOTION_INCOMPLETE`; inspect the actual target and receipts before retrying. Do not clean these files automatically.

The lease does not lock Microsoft Word or another editor. If the author edits concurrently after a hash check, no multi-file OS transaction is guaranteed; avoid editing the source during promotion and perform a final reopen/hash review. On detecting a later source change, invalidate dependent evidence and re-review rather than claiming a complete atomic transaction across unrelated files.

Keep all history when the project ends. Archived v1.3/other installations must remain uninstalled rollback packages to avoid duplicate routing. A README or folder created by this helper is infrastructure, not proof of research completion.
