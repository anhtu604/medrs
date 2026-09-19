# Changelog

## 2.0.0-alpha.6 — Four further reporting guidelines

- Added coverage manifests for SPIRIT 2025 (53 identifiers, trial protocols), STARD 2015 (34, diagnostic accuracy), COREQ 2007 (32, interview and focus-group research) and CARE 2013 (13, clinical case reports). SPIRIT 2025 supersedes SPIRIT 2013, which the superseded-edition test now also excludes.
- Encoded each instrument at the depth its licence allows. SPIRIT 2025 and STARD 2015 are CC BY 4.0, so their item wording is reproduced with attribution. CARE is CC BY-NC-ND 3.0 and COREQ is closed access, so both carry identifiers and item names only, with independently written operational prompts and no official wording; a test enforces that their licence fields say so.
- COREQ identifiers, domains and topic grouping were retrieved from the EQUATOR-hosted validated Portuguese translation because no open-access edition of the original exists; the provenance is recorded in the manifest and in ATTRIBUTION.md rather than implied.
- `kiem-chuan-bao-cao` now routes eight designs and states which manifests carry official wording and which carry independently written prompts, so an author knows when to consult the official document.

## 2.0.0-alpha.5 — Reporting-guideline coverage and time-to-event analysis

- Added `kiem-chuan-bao-cao`, which checks a manuscript against the reporting guideline matching its study design, item by item, and judges each item as reported, partially reported, not reported or not applicable with a required location in the manuscript.
- Added four source-governed coverage manifests retrieved from the primary statements on 2026-09-19 and reproduced under their CC BY licences with attribution: CONSORT 2025 (42 identifiers), STROBE 2007 (34), PRISMA 2020 (42) and TRIPOD+AI 2024 (52). CONSORT 2025 and TRIPOD+AI replace the superseded 2010 and 2015 editions, and a test keeps the superseded editions out of the package.
- Designs without an encoded manifest now return `GUIDELINE_UNAVAILABLE` and name the applicable statement, instead of being checked against a near-enough instrument.
- Added a time-to-event and prediction-model contract to `phan-tich-so-lieu` covering index-date and censoring definitions, competing risks, immortal-time bias, proportional-hazards checking, events-per-variable limits, and the rule that discrimination and calibration are reported together.
- Made context budgets read their thresholds from `config/canonical-skills.yaml` rather than duplicating them in code, and raised the aggregate description budget for the larger inventory.

## 2.0.0-alpha.4 — Citation management, publication figures, single-source releases

- Added `quan-ly-trich-dan`: read-only access to Zotero, BibTeX, RIS and CSL-JSON libraries with a declared backend, runtime field resolution, trash exclusion, and a retraction check that runs before any other verdict.
- Added citation-faithfulness verification judged per citation × claim across faithful, overstated, misattributed and unsupported, with a separate unverifiable state, and a statistic-provenance rule that treats a figure relayed by a review as misattributed.
- Added `bieu-do-cong-bo`: an evidence contract that must be settled before plotting, a claim-to-figure map covering survival, ROC, calibration, agreement, forest and funnel forms, and a publication QA pass covering grayscale, downscaling, colour accessibility and error-bar disclosure.
- Routed both new skills from the `/medrs` entrypoint and raised the canonical inventory to 26 accepted skills.
- Made releases single-source: the version is written only in `.claude-plugin/plugin.json` and propagated by `scripts/sync_version.py`, and the canonical skill count only in `config/canonical-skills.yaml`. The Cowork package name now follows the manifest version instead of a pinned filename, and packaging refuses to build while any carrier disagrees.
- Shortened installer staging directories, which had pushed staged skill paths past the 260-character Windows limit and broken installation under deep user profiles.

## 2.0.0-alpha.3 — Refresh-safe Word formatting

- Replaced direct run-level typography with an authoritative Word paragraph-style system covering body text, four heading levels, captions, tables, lists, TOC entries, lists of figures/tables, and bibliography output.
- Added refresh-safe field settings and post-refresh mechanical validation so regenerated TOCs and lists retain profile typography and line spacing.
- Added bounded content-weighted table column sizing, fixed OOXML table grids, and a dedicated table-text style.
- Added deterministic three-level automatic bullet numbering with controlled tab stops and hanging indents.
- Added an HMU style-carrier DOCX, a local Word COM field-refresh/PDF bridge, expanded QA guidance, idempotence checks, and Cowork packaging coverage.

## 2.0.0-alpha.2 — MedRS single entrypoint

- Renamed the canonical `co-van` router to `medrs`, exposed as `/medrs` on Claude-compatible hosts and `$medrs` on Codex.
- Added manifest-scoped retirement of renamed skills during upgrades so the old entrypoint is removed without touching user-owned skills.
- Renamed the Claude/Cowork plugin and regenerated the minimal Cowork upload package as MedRS.

## 2.0.0-alpha.1 — All 24 skills accepted

- Added a four-pass scoped academic-style gate with explicit integrity and authorship boundaries.
- Added traceable R/Stata analysis orchestration, backend-specific reproducibility contracts, execution-state schemas, artifact hashing, and hard refusals for significance-driven selection or fabricated output.
- Added citation-network mode requirements to the planned literature-retrieval vertical.
- Added the complete article-writing vertical: document orchestration, Introduction, thematic review, verified Results, source-bounded Discussion reverse engineering, conclusions, abstract lifecycle, and artifact-level manuscript validation.
- Added reproducible literature retrieval and evidence synthesis, including source-dated query logs, lawful-access states, typed citation networks, correction/retraction relations, GraphML export, contradiction retention, and hard systematic/meta-analysis readiness gates.
- Added source-traceable RoB 2, GRADE and GRADE-CERQual appraisal contracts with exact identifier coverage and unresolved-evidence safeguards.
- Added an executable HMU thesis semantic-structure profile, author-approved DOCX reordering, source-overwrite protection, and validation of the generated artifact.
- Added host-aware Word mechanics with source-governed HMU styles, margins, fields, page-number restart declarations, generated-artifact inspection, and explicit visual-validation limits.
- Added traceable peer review, point-by-point response matrices, revision commitments, numeric propagation checks, thesis examination, and hash-triggered re-review.
- Added six offline acceptance exemplars covering protocol, journal article, systematic review, qualitative synthesis, meta-analysis readiness failure, and HMU thesis handling.
- Added repository-first PowerShell install, update, doctor and manifest-scoped uninstall workflows for Codex, Claude Code and generic Agent Skills directories, plus a parameterized web bootstrap with optional archive checksum pinning.

## 2.0.0-alpha.1 — Slice 1

- Added six canonical foundation/protocol skills and a generated portable skill index.
- Added Research Passport creation, validation, author confirmation, and safe intake of existing DOCX/Markdown/text projects.
- Added protocol design and prespecified sample-size/analysis boundaries.
- Added source-verified ethics/data-governance routing with freshness and exact-scope manifests.
- Added distinct Vietnamese and English academic locale profiles and protocol/completed-study Methods contracts.
- Added offline end-to-end acceptance, capability probing, deterministic packaging, and support for a separately supplied, uninstalled 1.3.0 rollback archive.
- Recorded official HMU sources and deferred executable profile encoding to Slice 4.

## 2.0.0-alpha.1 — unreleased

- Begin the greenfield foundation-and-protocol slice.
- Add repo-first Claude marketplace packaging and portable agent entry instructions.
- Add Research Passport, source freshness, context-budget validation, and in-progress project intake.
- Keep legacy skill names outside discovery descriptions.
