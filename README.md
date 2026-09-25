# MedRS 3.0 release candidate

This development branch contains all 27 canonical medical-research skills, spanning protocol design, analysis, medical writing, evidence retrieval/synthesis/appraisal, reporting-guideline compliance, citation management, publication figures, document structure/formatting, two-round self-review, and peer-review revision.

All 27 skills are indexed in `skills/index.json`. Version 1.3.0 must remain uninstalled while this package is active. The license is CC BY-NC 4.0; commercial use may require separate permission and legal review.

Start with `skills/medrs/SKILL.md`. Non-Claude agents can enumerate the present skills from the generated `skills/index.json`.

The single user-facing entrypoint is `/medrs` on Claude-compatible hosts and `$medrs` in Codex. The other 26 skills are specialist handoff targets selected by MedRS.

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

The installer validates the exact declared skill inventory before mutation, stages each target, preserves a managed manifest, and restores the previous managed paths if activation fails. `uninstall.ps1` removes only paths listed by that manifest.

Install the current public release from GitHub:

```powershell
irm https://raw.githubusercontent.com/anhtu604/medrs/main/install/web.ps1 | iex
```

Inspect the downloaded script before piping it to `iex`. Override `MEDICAL_RESEARCH_SKILLS_REPO` only for a fork. For a reproducible install, invoke the downloaded script block with a commit SHA in `-Ref` and the downloaded archive's `-ArchiveSha256`.

Targets `codex`, `claude`, and `generic` install into local `.codex/skills`, `.claude/skills`, and `.agents/skills`. This does not make local files discoverable to ChatGPT web, Claude Chat, or a remote Cowork sandbox; those surfaces require their own published plugin/app adapter.

For Claude Cowork manual installation, run `python scripts/package_plugin.py`; it validates the skills, refuses to build while any version carrier disagrees with `.claude-plugin/plugin.json`, and writes `dist/medrs-cowork-<version>.zip` plus its `.sha256`. Upload that ZIP from the Claude organization plugin settings. The upload contains only the Cowork manifest, every canonical skill, shared coverage/profile/schema resources, public documentation, and the HMU Word style carrier.

Word formatting in alpha.3 is style-driven and refresh-safe: built-in TOC/list/bibliography styles are defined explicitly, tables use bounded content-weighted widths, and bullets use deterministic OOXML numbering. On local Windows with Microsoft Word, `scripts/refresh_word_fields.ps1` refreshes all fields into a new DOCX and can export a PDF; Cowork keeps field refresh and pagination marked for author review when no rendering backend is available.

## Zotero citations

Citations inserted with the Zotero Word plugin survive MedRS edits. To edit a draft or add citations yourself:

```powershell
python skills/quan-ly-trich-dan/scripts/zotero_roundtrip.py export draft.docx --out paragraphs.json
python skills/quan-ly-trich-dan/scripts/zotero_roundtrip.py apply draft.docx paragraphs.json --out revised.docx --zotero-db "$env:USERPROFILE\Zotero\zotero.sqlite"
```

Then open `revised.docx` in Word and click **Zotero → Refresh**.

## Writing in your own voice

Build a style profile from three to five documents you wrote and keep it beside the Research Passport:

```powershell
python skills/kiem-van-phong/scripts/style_profile.py --author "Tên" --out author-style-profile.json bai-bao-1.docx luan-van.docx
```

## Upgrading from 2.0.0-alpha.8

`kiem-chung-ban-thao` is merged into `tu-phan-bien`; reinstalling retires it. Research Passports need no change.

## Validation

Validation commands:

```text
claude plugin validate . --strict
python scripts/validate_skills.py
python scripts/sync_version.py --check
python -m pytest -q
python tests/eval_runner.py --offline
```

To cut a release, edit the version in `.claude-plugin/plugin.json` only, then run `python scripts/sync_version.py` to propagate it to `pyproject.toml`, the package `__version__`, and every skill's frontmatter.
