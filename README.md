# MedRS 2.0

This development branch contains all 24 canonical medical-research skills, spanning protocol design, analysis, medical writing, evidence retrieval/synthesis/appraisal, document structure/formatting, and peer-review revision.

All 24 skills are accepted in this alpha and indexed in `skills/index.json`. Version 1.3.0 must remain uninstalled while this package is active. The license is CC BY-NC 4.0; commercial use may require separate permission and legal review.

Start with `skills/medrs/SKILL.md`. Non-Claude agents can enumerate the present skills from the generated `skills/index.json`.

The single user-facing entrypoint is `/medrs` on Claude-compatible hosts and `$medrs` in Codex. The other 23 skills are specialist handoff targets selected by MedRS.

Build and capability commands:

```text
python scripts/build_index.py --check
python scripts/capability_probe.py
```

The capability probe advertises R, Stata, Word COM, LibreOffice UNO, or DOCX support only when runtime evidence is present. Missing runtimes produce code or an explicit unavailable/unperformed state, never a simulated execution claim.

HMU note: the official “Yêu cầu đối với luận văn” source linked by the 2026 defense page is checksum-registered and encoded as semantic-structure and Word-mechanics profiles. OOXML checks do not claim visual pagination; PDF/page-image inspection remains required when no rendering backend is available.

## Install

From a local clone on Windows:

```powershell
.\install.ps1 -Targets codex,claude
.\doctor.ps1 -Targets codex,claude
```

The installer validates the exact 24-skill inventory before mutation, stages each target, preserves a managed manifest, and restores the previous managed paths if activation fails. `uninstall.ps1` removes only paths listed by that manifest.

Install the current public release from GitHub:

```powershell
irm https://raw.githubusercontent.com/anhtu604/medrs/main/install/web.ps1 | iex
```

Inspect the downloaded script before piping it to `iex`. Override `MEDICAL_RESEARCH_SKILLS_REPO` only for a fork. For a reproducible install, invoke the downloaded script block with a commit SHA in `-Ref` and the downloaded archive's `-ArchiveSha256`.

Targets `codex`, `claude`, and `generic` install into local `.codex/skills`, `.claude/skills`, and `.agents/skills`. This does not make local files discoverable to ChatGPT web, Claude Chat, or a remote Cowork sandbox; those surfaces require their own published plugin/app adapter.

For Claude Cowork manual installation, build `dist/medrs-cowork-2.0.0-alpha.2.zip` with `python scripts/package_plugin.py`, then upload that ZIP from the Claude organization plugin settings. The upload contains only the Cowork manifest, 24 skills, shared coverage/profile/schema resources, and public documentation.

Validation commands:

```text
claude plugin validate . --strict
python scripts/validate_skills.py
python -m pytest -q
python tests/eval_runner.py --offline
```
