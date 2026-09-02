# Medical Research Skills VN 2.0 Slices 2–4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the remaining eighteen canonical skills, executable references, host-aware R/Stata and Word workflows, HMU profile, end-to-end acceptance cases, and repository-first installation.

**Architecture:** Keep `skills/<name>/` as the only canonical portable core. Deterministic Python modules validate contracts and parse real artifacts; thin host adapters install or expose the same skills without duplicating medical instructions. Work proceeds as three accepted vertical slices, never as eighteen simultaneous scaffolds.

**Tech Stack:** Python 3.11+, pytest, PyYAML, jsonschema, python-docx, OOXML, optional Word COM/LibreOffice UNO, R, Stata, PowerShell, portable Agent Skills.

**Spec:** `docs/medical-research-skills-vn-v2-design.md`

## Global Constraints

- Exactly 24 canonical skills; no legacy alias directories and no cross-plugin runtime dependency.
- Each description is at most 60 words/640 UTF-8 bytes; aggregate descriptions are at most 1,200 words/12 KiB.
- Every new skill is introduced by a failing routing or behavioral case before its directory is created.
- Never reconstruct a checklist, appraisal instrument, regulatory rule, or reporting guideline from memory.
- Checklist coverage must identify every adopted item/domain/subitem and pass source, version, license, freshness, and caller validation.
- R/Stata/Word execution is claimed only after runtime evidence and generated-artifact validation.
- Writers use the one shared writing preflight; full `kiem-van-phong` runs at the lifecycle points defined by the spec.
- Source files are never overwritten. Transformations write a new artifact, change log, and validation report.
- ZIP is not the primary release. Repository installation and update are the final distribution gate.

---

### Task 1: Activate full-inventory contracts without creating empty skills

**Files:**
- Modify: `config/canonical-skills.yaml`
- Modify: `src/medical_research_skills_vn/routing.py`
- Modify: `src/medical_research_skills_vn/structure.py`
- Create: `tests/test_full_inventory_contract.py`
- Modify: `tests/test_routing.py`

**Interfaces:**
- Produces: inventory state `planned | active | accepted` per skill and slice.
- Produces: route decisions that distinguish unavailable dependencies from accepted skills.

- [ ] Write a failing test asserting the eventual inventory is exactly the 24 names in spec §5 and that an `active` skill must have `SKILL.md`, at least one positive case, one nearest-boundary negative case, and explicit reference callers.
- [ ] Run `python -m pytest tests/test_full_inventory_contract.py -q`; confirm failure because only six skills exist.
- [ ] Add slice acceptance state and validation primitives without marking absent skills active.
- [ ] Run inventory tests and the existing 58-test regression suite.
- [ ] Commit as `test: define full inventory acceptance contract`.

### Task 2: Complete the mandatory style gate

**Files:**
- Create: `skills/kiem-van-phong/SKILL.md`
- Create: `skills/kiem-van-phong/references/scientific-integrity.md`
- Create: `skills/kiem-van-phong/references/argument-quality.md`
- Create: `skills/kiem-van-phong/references/composition-vi.md`
- Create: `skills/kiem-van-phong/references/composition-en.md`
- Create: `skills/kiem-van-phong/references/formulaic-writing-audit.md`
- Create: `schemas/style-audit.schema.json`
- Create: `src/medical_research_skills_vn/style_gate.py`
- Create: `tests/cases/kiem-van-phong/routing.yaml`
- Create: `tests/test_style_gate.py`

**Interfaces:**
- Produces: `StyleAuditState(document_hash, section_hashes, locale_profile_version, source_ledger_version, reference_versions)`.
- Produces: four independent pass results and scoped invalidation decisions.

- [ ] Write failing cases for fabricated citations, unsupported causal language, Vietnamese/English locale leakage, formulaic phrasing, unchanged-section reuse, and changed-source invalidation.
- [ ] Run `python -m pytest tests/test_style_gate.py -q`; confirm missing implementation failure.
- [ ] Create the concise entrypoint and conditionally loaded references. Adapt composition rules from verified *Elements of Style* and the AI-writing field guide without detector-evasion claims.
- [ ] Implement deterministic audit-state hashing and invalidation; prose judgments remain explicit review outputs, not fake classifier scores.
- [ ] Run style, shared-preflight, budget, caller, and routing tests.
- [ ] Commit as `feat: complete scoped medical writing gate`.

### Task 3: Implement the R/Stata analysis vertical

**Files:**
- Create: `skills/phan-tich-so-lieu/SKILL.md`
- Create: `skills/phan-tich-r/SKILL.md`
- Create: `skills/phan-tich-stata/SKILL.md`
- Create: `skills/phan-tich-so-lieu/references/analysis-deviation-contract.md`
- Create: `skills/phan-tich-r/references/reproducibility-contract.md`
- Create: `skills/phan-tich-stata/references/reproducibility-contract.md`
- Create: `src/medical_research_skills_vn/statistics.py`
- Create: `schemas/analysis-run.schema.json`
- Create: `tests/fixtures/statistics/`
- Create: `tests/cases/phan-tich-so-lieu/boundaries.yaml`
- Create: `tests/test_statistics_workflow.py`

**Interfaces:**
- Produces: `AnalysisRun(backend, runtime_verified, command, code_hash, input_hash, output_paths, deviations, status)`.
- Consumes only a confirmed analysis plan plus verified data or author-supplied real output.

- [ ] Write failing tests for significance-driven model selection, absent runtime, supplied-output interpretation, R script provenance, Stata do-file provenance, output hash mismatch, and assumption-reporting artifacts.
- [ ] Confirm red with `python -m pytest tests/test_statistics_workflow.py -q`.
- [ ] Implement orchestration and traceability; generate code when a runtime is missing and mark execution `NOT_RUN`.
- [ ] Add small checked fixtures for descriptive statistics, one regression family, missing-data reporting, confidence intervals, and publication tables; smoke-run only when the matching executable is callable.
- [ ] Run statistics, capability-probe, planning-boundary, budget, and routing tests.
- [ ] Commit as `feat: add traceable R and Stata workflows`.

### Task 4: Implement the journal-article writing vertical

**Files:**
- Create: `skills/viet-ban-thao-y-hoc/`
- Create: `skills/viet-dat-van-de/`
- Create: `skills/viet-tong-quan/`
- Create: `skills/viet-ket-qua/`
- Create: `skills/viet-ban-luan/`
- Create: `skills/viet-ket-luan-khuyen-nghi/`
- Create: `skills/viet-tom-tat/`
- Create: `skills/kiem-chung-ban-thao/`
- Create: `src/medical_research_skills_vn/writing.py`
- Create: `src/medical_research_skills_vn/manuscript.py`
- Create: `schemas/section-artifact.schema.json`
- Create: `schemas/discussion-blueprint.schema.json`
- Create: `tests/cases/writing/`
- Create: `tests/test_article_writing.py`

**Interfaces:**
- Every writer consumes Passport, target/locale profile, approved outline, verified facts/results, source ledger, depth, and budget.
- Every writer produces draft, claim–evidence rows, markers, dependencies, approval requests, preflight, and gate state.

- [ ] Write failing positive/negative bilingual routes for each skill plus cases that reject invented Results, interpretation in Results, author-by-author literature catalogs, unsupported novelty, new findings in conclusions, and an abstract drafted before full-text consistency is available.
- [ ] Add Discussion cases for lawful comparator access, paragraph-function maps, blueprint approval, phrase-copy rejection, evidence-needs markers, and observational causal ceilings.
- [ ] Confirm red with `python -m pytest tests/test_article_writing.py -q`.
- [ ] Create and verify one writer at a time, stopping after its focused cases pass; every writer names the shared preflight once.
- [ ] Implement document assembly and manuscript validation after all section writers pass independently.
- [ ] Run article, style-gate, shared-preflight, routing, context-budget, and reference-caller tests.
- [ ] Commit each verified writer separately, then commit the accepted article vertical as `feat: accept journal article workflow`.

### Task 5: Add journal-profile structure handling for article acceptance

**Files:**
- Create: `profiles/journal/schema.yaml`
- Create: `src/medical_research_skills_vn/document_profiles.py`
- Create: `tests/fixtures/journal/incorrect-order.md`
- Create: `tests/test_journal_structure.py`
- Modify: `skills/viet-ban-thao-y-hoc/SKILL.md`
- Modify: `skills/kiem-chung-ban-thao/SKILL.md`

**Interfaces:**
- Produces a source-dated profile and semantic restructuring plan; it does not perform Word styling.

- [ ] Write failing tests that require source URL/version/date, article type, submission stage, required order, headings, and author approval before moving sections.
- [ ] Implement profile parsing and actual Markdown section reordering against a controlled fixture.
- [ ] Run article end-to-end: Passport → verified results → all sections → style gate → validation → structurally ordered manuscript.
- [ ] Mark Slice 2 accepted only after all commands pass and commit `test: accept analysis and article slice`.

### Task 6: Implement reproducible literature retrieval and evidence mapping

**Files:**
- Create: `skills/tim-y-van/`
- Create: `skills/tong-hop-bang-chung/`
- Create: `src/medical_research_skills_vn/evidence.py`
- Create: `schemas/search-log.schema.json`
- Create: `schemas/evidence-map.schema.json`
- Create: `schemas/citation-network.schema.json`
- Create: `tests/cases/evidence/`
- Create: `tests/test_evidence_workflow.py`

**Interfaces:**
- Produces query/source/date/deduplication provenance, lawful-access state, study records, evidence map, citation-network nodes/edges, and synthesis mode.

- [ ] Write failing cases for unverifiable citations, inaccessible full text, embedded prompt injection, duplicate records, missing search dates, narrative versus systematic claims, and meta-analysis requested without extractable study data.
- [ ] Add `citation-network` mode to `tim-y-van`: seed records, backward/forward citation chasing, typed edges, discovery provenance, explicit stopping criteria, and JSON/GraphML export. Citation count is descriptive only; title-only design classification remains `UNRESOLVED` with `LOW` confidence, and a graph alone never supports a claim of systematic completeness.
- [ ] Write failing graph cases for a title-only node, missing seed provenance, duplicate DOI/PMID nodes, correction/retraction links, a citation-count quality claim, and no prespecified stopping rule.
- [ ] Create `tim-y-van`, verify it, then create `tong-hop-bang-chung`; do not batch their entrypoints.
- [ ] Implement offline fixture import plus host-connector contracts; no database is claimed searched unless a real query record exists.
- [ ] Run evidence routing, provenance, privacy, budget, and end-to-end tests.
- [ ] Commit the two verified skills separately.

### Task 7: Implement reporting-guideline and evidence-quality coverage

**Files:**
- Create: `skills/danh-gia-chat-luong-bang-chung/`
- Create: `skills/kiem-chung-ban-thao/references/reporting/`
- Create: `coverage/`
- Create: `src/medical_research_skills_vn/coverage.py`
- Create: `tests/fixtures/coverage/`
- Create: `tests/test_coverage_manifests.py`
- Create: `tests/test_evidence_quality.py`

**Interfaces:**
- Produces exact coverage manifests with expected and implemented identifiers, source/version/license/freshness, and caller reference.
- Produces design-matched risk-of-bias judgments and certainty assessments with unresolved signalling questions visible.

- [ ] Retrieve current primary artifacts and licenses for STROBE, PRISMA 2020, CONSORT current, RoB 2, GRADE, and CERQual; block rather than approximate any inaccessible artifact.
- [ ] Write failing manifest tests for missing item, subitem, signalling question, decision rule, source metadata, and reference-content floor.
- [ ] Implement coverage validation before adding operational references.
- [ ] Populate one framework at a time from its verified source and run its focused coverage/appraisal cases before proceeding.
- [ ] Run the systematic-review exemplar and mark Slice 3 accepted only when every named instrument is substantive and green.
- [ ] Commit each framework independently and finish with `test: accept evidence synthesis slice`.

### Task 8: Implement semantic thesis structure and the HMU profile

**Files:**
- Create: `skills/bo-cuc-tai-lieu/`
- Create: `profiles/institution/hmu/`
- Create: `src/medical_research_skills_vn/structure_profiles.py`
- Create: `tests/fixtures/hmu/`
- Create: `tests/test_hmu_profile.py`
- Create: `tests/test_document_structure.py`

**Interfaces:**
- Produces profile, comparison, author-approved restructuring plan, and a structurally reordered artifact.
- Consumes the verified HMU DOCX registered in `sources/hmu/source-register.yaml`.

- [ ] Parse the official HMU document into traceable rule fields with source paragraph/table provenance; mark ambiguous requirements for author review.
- [ ] Write failing golden tests for section order, heading hierarchy, preliminary matter, lists, captions, and numbering transitions before implementing transformations.
- [ ] Implement semantic move/rename/split/merge on a generated DOCX fixture without deciding fonts or margins in this skill.
- [ ] Validate the transformed artifact and commit `feat: add source-traceable HMU structure profile`.

### Task 9: Implement Word mechanics and generated-artifact validation

**Files:**
- Create: `skills/dinh-dang-tai-lieu/`
- Create: `src/medical_research_skills_vn/docx_formatting.py`
- Create: `src/medical_research_skills_vn/docx_validation.py`
- Create: `src/medical_research_skills_vn/word_backends.py`
- Create: `scripts/format_docx.py`
- Create: `scripts/validate_docx.py`
- Create: `tests/test_docx_formatting.py`
- Create: `tests/test_word_backends.py`

**Interfaces:**
- Produces a new DOCX, change log, validation report, optional PDF/render images, and explicit unperformed-check markers.

- [ ] Write failing tests for source overwrite, style assignment, section properties, fields, captions, page-number restarts, comments/tracked changes preservation, leaked processes, and false rendered-pass claims.
- [ ] Implement OOXML-only formatting/validation first and require `AUTHOR_APPROVAL_REQUIRED` for pagination and visual checks.
- [ ] Add Word COM behind a passing local capability probe and `finally` cleanup; inspect the generated DOCX/PDF.
- [ ] Add LibreOffice UNO contract and fixture only where UNO is callable; unsupported adapters fail clearly.
- [ ] Run generated-artifact tests and representative visual inspection where rendering exists.
- [ ] Commit `feat: add host-aware Word formatting and validation`.

### Task 10: Implement review, revision, and full release acceptance

**Files:**
- Create: `skills/phan-bien-va-chinh-sua/`
- Create: `schemas/revision-commitment.schema.json`
- Create: `src/medical_research_skills_vn/revision.py`
- Create: `tests/cases/phan-bien-va-chinh-sua/`
- Create: `tests/cases/end-to-end/{journal-article,systematic-review,thesis-hmu}.yaml`
- Create: `tests/test_revision.py`
- Create: `tests/test_full_release_e2e.py`
- Modify: `README.md`, `CHANGELOG.md`, `ATTRIBUTION.md`, `docs/migration-1.3-to-2.0.md`

**Interfaces:**
- Produces review findings, response matrix, commitments, changed-artifact links, disclosure updates, and re-review state.

- [ ] Write failing cases for reviewer-request tracking, unsupported concession, changed-number propagation, response-without-change, thesis examination, and re-review of committed edits.
- [ ] Implement and verify the final skill.
- [ ] Activate all 24 inventory entries, rebuild `skills/index.json`, and assert exactly 24 discoverable skills.
- [ ] Run the protocol, article, systematic-review, qualitative, meta-analysis, and HMU thesis exemplars.
- [ ] Run `claude plugin validate . --strict`, `python scripts/validate_skills.py`, `python -m pytest -q`, and `python tests/eval_runner.py --offline`.
- [ ] Commit `feat: accept all 24 medical research skills`.

### Task 11: Replace ZIP-first packaging with repository installation

**Files:**
- Create: `install.ps1`, `uninstall.ps1`, `update.ps1`
- Create: `adapters/claude/`, `adapters/codex/`, `adapters/generic-agent-skills/`
- Create: `.codex-plugin/plugin.json`
- Create: `src/medical_research_skills_vn/installer.py`
- Create: `tests/test_installer.py`
- Modify: `README.md`, `.gitignore`, `.claude-plugin/marketplace.json`
- Remove from primary workflow: `scripts/package_plugin.py`, `src/medical_research_skills_vn/packaging.py`, ZIP assertions

**Interfaces:**
- PowerShell bootstrap installs a pinned repository revision into a versioned local source directory and exposes canonical skills through host-specific links/copies.
- Supports `install`, `update`, `doctor`, and `uninstall`; never installs 1.3.0 beside 2.0.

- [ ] After the public GitHub URL is known, write isolated-home failing tests for install, idempotent update, rollback after failed validation, uninstall, path quoting, and Claude/Codex/generic discovery.
- [ ] Implement verified download/clone, staged validation, atomic activation, and previous-version recovery. The one-line `irm ... | iex` is documented only for the public raw URL; a pinned-SHA command is also provided.
- [ ] Do not claim ChatGPT chat-only support from local installation; publish only adapters that pass their own host tests.
- [ ] Run installer tests in temporary user profiles and the complete release acceptance suite.
- [ ] Commit `build: add repository-first multi-host installer`.

---

## Completion Gate

The work is complete only when all 24 skill directories are active, every named checklist/instrument passes exact coverage, the six end-to-end workflows pass, HMU structure/format fixtures inspect generated artifacts, R/Stata claims remain runtime-traceable, and supported host installers pass isolated installation tests. A missing primary source or unavailable rendering/runtime remains an explicit blocker or capability degradation, never a simulated pass.
