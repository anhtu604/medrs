# MedRS Comprehensive Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver every P0–P3 requirement in the confirmed specification, with content and presentation acceptance on the actual final artifacts.

**Architecture:** Keep one plugin and 28 canonical skills. Reuse existing routers, Passport, revision guards, formatters and validators; put portable runtime ownership inside the responsible skill and keep repository adapters thin. Deliver sequential, independently tested increments; no concurrent expansion of all skills.

**Tech Stack:** Python, pytest, JSON Schema, OOXML/python-docx, PowerShell, existing R/Stata adapters, capability-probed Word COM/LibreOffice UNO, source-governed Markdown/JSON references.

**Spec:** `docs/superpowers/specs/2026-10-11-medrs-comprehensive-upgrade.md`

## Global Constraints

- Một plugin, 28 skill canonical, `/medrs` là cổng vào duy nhất.
- Runtime cần cho Cowork nằm trong skill `scripts/`.
- Description tối đa 60 từ/skill, gộp 1300 từ; frontmatter gộp 16384 byte. Mục tiêu thực tế là 45 từ/skill.
- Không tự gửi dữ liệu sang AI khác.
- Bản thảo riêng, dữ liệu người bệnh và log riêng không được xuất bản trong repo.
- Thiếu nguồn/kiểm chứng có thể tiếp tục viết nháp có điều kiện và marker, không khẳng định chắc chắn.
- Nguồn thiếu không được fake pass; còn mục chặn thì báo phạm vi chưa hoàn thành, không tuyên bố full xong.
- Use synthetic fixtures, preserve local private audit reports, never paste them into public documentation.
- Do not change installed packages or public branches during planning. Version is assigned at release by the existing single-manifest workflow, not by manually editing every carrier.

## Review Focus

1. Author changes the source while a round is running: refuse promotion, preserve both versions and stale the old evidence. Task 1 owns this race test.
2. Renamed/reordered simulation later described as real: retain lineage, distinguish author declaration from replacement evidence, request resolution without accusing the author. Task 4 owns the transition test.
3. Externally edited Word file contains live Zotero fields, footnotes and comment anchors: merge only authorized changes, preserve object identity and require fresh final-hash review. Tasks 2 and 3 own the fixture tests.
4. Old Passport has conflicting design/unknown extensions: preserve extensions and surface the contradiction; do not silently infer a new design. Task 6 owns compatibility tests.
5. Official source expires or rendering runtime is absent: neither profile nor presentation can pass, but a conditional draft may continue. Tasks 7, 9 and 11 own negative acceptance tests.

---

## Execution layout and recordkeeping

Worktree: `work/medical-research-skills-vn-v2/.worktrees/medrs-3.1` on `feature/medrs-comprehensive-upgrade`, starting at `60bdd98`.

Local project record: `work/medrs-upgrade-2026-10-11/README.md`, `final/`, `history/YYYY-MM-DD/`. Before each task update the daily note; save command transcripts, test reports and source-verification receipts there. Commit only synthetic fixtures and public-safe documentation. The existing session transcript is not a replacement for stored execution logs.

Each task follows RED → implementation → GREEN → review → explicit-path commit. Do not commit unrelated author edits. An executable test passing does not establish clinical truth, full guideline coverage, permission to reproduce content or rendered appearance.

## Task 1: Project lifecycle, daily archive and final promotion

**Files:** create `skills/leader-nghien-cuu/scripts/project_workspace.py`, `skills/leader-nghien-cuu/references/project-workspace.md`, `schemas/project-state.schema.json`, `tests/test_project_workspace.py`; modify `skills/leader-nghien-cuu/SKILL.md`, `skills/ho-so-nghien-cuu/SKILL.md`, `skills/medrs/SKILL.md`.

**Interfaces:** `initialize_project(root: Path, project_id: str, date: str) -> dict`; `record_event(root: Path, date: str, event: dict) -> Path`; `promote_final(root: Path, staged: Path, source_snapshot: dict, date: str) -> dict`. Use existing `revision_guard.py` snapshot/locking primitives. Managed README blocks must not replace text authored outside those blocks.

- [ ] Write RED tests importing the new module via its skill scripts path:

```python
def test_initialize_is_idempotent(tmp_path):
    from project_workspace import initialize_project
    initialize_project(tmp_path, "fixture", "2026-10-11")
    note = tmp_path / "README.md"
    note.write_text(note.read_text(encoding="utf-8") + "\nAuthor note\n", encoding="utf-8")
    initialize_project(tmp_path, "fixture", "2026-10-11")
    assert "Author note" in note.read_text(encoding="utf-8")
    assert (tmp_path / "history/2026-10-11/README.md").exists()
    assert (tmp_path / "final").is_dir()
```

Add collision, path traversal, interrupted promotion, two same-day rounds and changed-source tests using the actual revision guard API. Expect no loss of either file or event. Final promotion must reject changed-source hash and leave final untouched.

- [ ] Run `python -m pytest tests/test_project_workspace.py -q`; expect missing module before implementation.
- [ ] Implement initialization with exclusive creation, strict ISO dates and resolved paths under root; append JSONL events without raw participant values. Under a project lock, snapshot previous final to a unique dated round, stage the new version, verify source unchanged, atomically replace only the managed final target. On failure retain recovery files and mark promotion incomplete. Generate README progress from state, not unverified filenames.

```python
from pathlib import Path

def project_path(root: Path, relative: str) -> Path:
    root = root.resolve()
    candidate = (root / relative).resolve()
    if candidate == root or root not in candidate.parents:
        raise ValueError("Path outside project")
    return candidate
```

- [ ] Run project tests plus `tests/test_v31_revision_quality.py`; inspect actual archive contents.
- [ ] Commit explicit task files with message `feat: add recoverable project workspace and daily logs`.

## Task 2: Word structural safety and durable styles

**Files:** modify `src/medical_research_skills_vn/docx_formatting.py`, `src/medical_research_skills_vn/docx_validation.py`, `src/medical_research_skills_vn/structure_profiles.py`, `skills/dinh-dang-tai-lieu/SKILL.md`; create `skills/dinh-dang-tai-lieu/scripts/docx_integrity.py`, `skills/dinh-dang-tai-lieu/scripts/docx_formatting.py`, `skills/dinh-dang-tai-lieu/scripts/docx_validation.py`, `skills/dinh-dang-tai-lieu/references/word-integrity-contract.md`, `tests/fixtures/docx_traps.py`, `tests/test_docx_revision_traps.py`. Move reusable formatter/validator code into these skill scripts and retain the original module names as thin import adapters; test both entry paths before removing duplicated implementation.

**Interfaces:** preserve existing public formatter/validator signatures. Add `audit_docx_integrity(path: Path) -> dict` in `skills/dinh-dang-tai-lieu/scripts/docx_integrity.py`; result keys `status`, `issues`, `protected_fingerprints`. Fingerprints cover live field instructions, relationship targets, footnote IDs and comment anchors; not merely text offsets.

- [ ] Create synthetic DOCX fixtures with theme font, direct font override, paragraph spacing override, Caption/TOC/bibliography styles, empty picture-heading, body-as-heading, narrow numeric and long text columns, nested bullets, section numbering, footnotes and bookmarks.

```python
def test_integrity_rejects_missing_footnote_target(tmp_path):
    from docx_integrity import audit_docx_integrity
    from tests.fixtures.docx_traps import make_missing_footnote_docx
    path = make_missing_footnote_docx(tmp_path / "broken.docx")
    report = audit_docx_integrity(path)
    assert report["status"] == "FAIL"
    assert any(item["code"] == "MISSING_FOOTNOTE_TARGET" for item in report["issues"])
```

Define `make_missing_footnote_docx(path: Path) -> Path` in new `tests/fixtures/docx_traps.py`: produce a normal package with `w:footnoteReference w:id="9"` but no matching footnote. Include `tests/__init__.py` and `tests/fixtures/__init__.py` only if needed for fixture import, not a runtime dependency.

- [ ] Run `python -m pytest tests/test_docx_revision_traps.py -q`; expect RED for missing audit/uncaught traps.
- [ ] Parse package XML and preserve child order/relationships; never assign paragraph/run text across fields. Resolve effective font/spacing through style chain and direct formatting; apply profile overrides to stable named styles including generated lists. Retain intended inline emphasis. Heading repair requires semantic confirmation, not regex alone. Allocate bounded content-aware column widths; use OOXML numbering with consistent hanging indent, not Unicode bullets. Table-border policy must come from task 7 profile, never thesis-wide assumption.

```python
def missing_targets(reference_ids: set[str], defined_ids: set[str]) -> list[str]:
    return sorted(reference_ids - defined_ids)
```

- [ ] Run existing DOCX/structure tests plus trap tests; inspect saved then refreshed/reopened/rendered artifacts on available backend. Missing backend remains unperformed, not PASS.
- [ ] Commit `fix: preserve Word structure and effective styles through revisions`.

## Task 3: Zotero, author-returned revisions and external handoff

**Files:** modify `skills/quan-ly-trich-dan/scripts/zotero_fields.py`, `skills/quan-ly-trich-dan/scripts/zotero_roundtrip.py`, `skills/quan-ly-trich-dan/references/zotero-field-contract.md`, `skills/leader-nghien-cuu/references/revision-and-acceptance.md`; create `skills/leader-nghien-cuu/scripts/external_revision.py`, `schemas/external-handoff.schema.json`, `tests/test_external_revision.py`; extend `tests/test_zotero_fields.py`.

**Interfaces:** `prepare_handoff(source: Path, tasks: list[dict], authorization: dict) -> dict`; `inspect_returned_revision(source: Path, returned: Path, handoff: dict) -> dict`. Returns source/returned hashes, task IDs, protected-object diffs, scope/consent status, stale evidence list; no network operation. Consume task 2 `audit_docx_integrity` and task 1 event recorder.

- [ ] RED tests for changed citation JSON item identity despite identical displayed numbers; lost field under Track Changes; footnote/comment deletion; new handwritten author paragraph; unrequested design change; unauthorized external destination.

```python
def test_no_external_transfer_without_consent(tmp_path):
    from external_revision import prepare_handoff
    source = tmp_path / "draft.txt"
    source.write_text("Synthetic draft", encoding="utf-8")
    report = prepare_handoff(source, [], {"confirmed": False})
    assert report["status"] == "AUTHOR_APPROVAL_REQUIRED"
    assert report["transfer_permitted"] is False
```

- [ ] Run `python -m pytest tests/test_external_revision.py tests/test_zotero_fields.py -q`; new behavior must fail before implementation.
- [ ] Generate a local handoff manifest/prompts with selected fields, destination, author scope and source hash. Compare returned file with last delivered source, not an arbitrary older draft. Preserve comment IDs/anchors and Zotero instructions; require author choice for substantive out-of-scope edits. Add library/refresh locks and recoverable typed-to-live conversion mapping using confirmed item keys; do not invent references or automatically accept Track Changes.

```python
def transfer_permitted(authorization: dict) -> bool:
    return (authorization.get("confirmed") is True
            and bool(authorization.get("destination"))
            and bool(authorization.get("data_class")))
```

- [ ] Run Zotero and revision suites; accept only fresh evidence for returned-file hash. Document refresh as actual backend-specific operation, not cached bibliography appearance.
- [ ] Commit `feat: add consent-bound handoff and protected revision intake`.

## Task 4: Simulation lineage and confirmed replacement

**Files:** create `skills/ho-so-nghien-cuu/scripts/data_provenance.py`, `schemas/data-provenance.schema.json`, `skills/ho-so-nghien-cuu/references/data-provenance.md`, `tests/test_data_provenance.py`; modify `skills/medrs/references/working-principles.md`, `skills/leader-nghien-cuu/references/revision-and-acceptance.md`.

**Interfaces:** `transition_data_state(previous: dict, replacement: dict, author_decision: dict) -> dict`; `fingerprint_records(rows: list[dict], columns: list[str], key: bytes) -> str`. States: SIMULATED, UNRESOLVED, AUTHOR_DECLARED_REAL, VERIFIED_REAL. Verified state requires an independent verification receipt; author declaration alone does not produce it.

- [ ] RED tests:

```python
def test_real_declaration_is_not_independent_verification():
    from data_provenance import transition_data_state
    report = transition_data_state(
        {"state": "SIMULATED", "digest": "a"},
        {"digest": "b", "replacement_received": True},
        {"confirmed": True, "data_updated_to_real": True})
    assert report["state"] == "AUTHOR_DECLARED_REAL"
    assert report["author_recheck_required"] is True
    assert report["history_preserved"] is True
```

Also test no confirmation, explicit still-simulated, identical digest after rename/reorder, partial column replacement, duplicate rows and missing verification receipt. Same digest signals unresolved transition, not an accusation; do not relabel unchanged simulation as verified real.

- [ ] Run `python -m pytest tests/test_data_provenance.py -q`; expect RED.
- [ ] Implement keyed canonical value digests retaining duplicate counts and normalization version. Keep keys local, never log rows/identifiers. Author-confirmed replacement allows updating obsolete labels in current manuscript plus rechecking dependent results; archive original evidence and emit a concise author check notice.

```python
def replacement_confirmed(decision: dict, replacement: dict) -> bool:
    return (decision.get("confirmed") is True
            and decision.get("data_updated_to_real") is True
            and replacement.get("replacement_received") is True)
```

- [ ] Run provenance/revision suites and inspect notices for both privacy and non-accusatory language.
- [ ] Commit `fix: preserve data lineage across author-confirmed replacement`.

## Task 5: Statistical decisions, extraction and R/Stata runs

**Files:** modify `skills/phan-tich-so-lieu/references/analysis-deviation-contract.md`, `skills/phan-tich-r/SKILL.md`, `skills/phan-tich-stata/SKILL.md`, `skills/viet-ket-qua/SKILL.md`, `skills/viet-ban-luan/SKILL.md`, `schemas/analysis-plan.schema.json`, `schemas/analysis-run.schema.json`; create `skills/phan-tich-so-lieu/scripts/statistics_policy.py`, `skills/phan-tich-so-lieu/references/basic-statistics-contract.md`, `skills/tong-hop-bang-chung/references/extraction-identity.md`, `tests/test_statistics_safeguards.py`.

**Interfaces:** add `interpretation_ceiling(plan: dict, run: dict) -> dict` in `skills/phan-tich-so-lieu/scripts/statistics_policy.py`; keys `causal_allowed`, `confirmatory_allowed`, `qualifications`, `unresolved`. No function runs a statistical test without an actual runtime.

- [ ] RED tests:

```python
def test_posthoc_unadjusted_result_not_confirmatory():
    from statistics_policy import interpretation_ceiling
    report = interpretation_ceiling(
        {"design": "cross-sectional", "prespecified": False},
        {"multiple_tests": True, "multiplicity_addressed": False})
    assert report["confirmatory_allowed"] is False
    assert report["causal_allowed"] is False
    assert "EXPLORATORY" in report["qualifications"]
```

Add outcome-available N vs recruited N, OR mislabelled PR, denominator/group/time swaps, paired-difference assumptions, PH failure, missing runtime, threshold sources, and analysis specification ledger tests. Define fixture expected outcomes from primary statistical references with source receipts, not reviewer heuristics alone.

- [ ] Run `python -m pytest tests/test_statistics_safeguards.py tests/test_statistics_workflow.py -q`; confirm failing new safeguards.
- [ ] Encode operational decision tables with evidence/version metadata. Keep continuous variables default; approved protocol deviations and all tried specifications visible. Preserve exact estimates/CI/p without fabricated precision. Reference sample-size heuristics as qualified context, not mandatory fixed thresholds. R/Stata use task 1 daily run directories, real runtime/date/exit/output logs, reproducible seeds when applicable and cautious KM/Cox interpretations.

```python
def confirmatory_allowed(plan: dict, run: dict) -> bool:
    return (plan.get("prespecified") is True
            and (run.get("multiple_tests") is not True
                 or run.get("multiplicity_addressed") is True))
```

- [ ] Run suites and actual R/Stata fixture only where installed. Optional agreed cross-validation is reported separately; no Python substitution labelled Stata.
- [ ] Commit `fix: enforce analysis and extraction interpretation ceilings`.

## Task 6: Shared writing gate, Passport compatibility and routing

**Files:** modify `skills/medrs/scripts/router.py`, `skills/medrs/references/legacy-skill-map.yaml`, `skills/medrs/references/routing-contract.md`, `src/medical_research_skills_vn/passport.py`, `schemas/research-passport.schema.json`, all seven section-writer `SKILL.md` files, shared preflight reference under `skills/viet-phuong-phap/references/writing-preflight.md`; create `skills/kiem-van-phong/scripts/gate_lifecycle.py`, `skills/kiem-van-phong/references/gate-lifecycle.md`, `tests/test_upgrade_routing_and_gate.py`, `tests/test_passport_project_scope.py`.

**Interfaces:** preserve router API and Passport 2.0 compatibility. Add optional project workspace, parent scope and policy fields without forcing schema/package version equality. Add `required_gate_scope(mode: str, changed_sections: list[str]) -> dict` in `skills/kiem-van-phong/scripts/gate_lifecycle.py`, consumed by writers/leader; output `full`, `local`, `consistency`.

- [ ] RED tests:

```python
def test_assembled_draft_has_one_full_gate():
    from gate_lifecycle import required_gate_scope
    report = required_gate_scope("assembled", [])
    assert report == {"full": ["document"], "local": [], "consistency": True}
```

Add standalone and revision-scope tests, CLI legacy-name and `/medrs:skill` tests, explicit negative triggers, compound tasks, old Passport unknown-extension roundtrip, conflicting designs and child objective-specific populations. Unknown legacy name must not invent a future available skill.

- [ ] Run `python -m pytest tests/test_upgrade_routing_and_gate.py tests/test_passport_project_scope.py -q`; expect RED.
- [ ] Implement one gate policy, references with explicit callers and short entrypoints. Use author confirmed decisions to avoid repeated questions; ask a concise grouped list only for consequential unresolved choices. Carry task 5 qualifications into writing, preserving conditional markers rather than confident prose. Load migration map in CLI and chat contract; fix protocol destination; remove stale slice promises. New subproject cannot silently inherit parent result N.

```python
def required_gate_scope(mode: str, changed_sections: list[str]) -> dict:
    if mode == "assembled":
        return {"full": ["document"], "local": [], "consistency": True}
    if mode == "revision":
        return {"full": [], "local": sorted(set(changed_sections)), "consistency": True}
    if mode == "standalone":
        return {"full": sorted(set(changed_sections)), "local": [], "consistency": False}
    raise ValueError("Unknown writing mode")
```

- [ ] Run routing, Passport, shared-preflight, style and methods tests; pressure-test realistic prompts without prescribing the expected skill in the prompt.
- [ ] Commit `fix: unify routing, writing gates and project scope`.

## Task 7: Official HMU profiles and document conventions

**Files:** modify `src/medical_research_skills_vn/document_types.py`, `src/medical_research_skills_vn/profiles.py`, `skills/bo-cuc-tai-lieu/references/hmu-profile-use.md`; create `skills/bo-cuc-tai-lieu/scripts/profile_policy.py`, source registers under `sources/hmu/`, profile fixtures under `tests/fixtures/profiles/`, `tests/test_official_profile_requirements.py`; add source-backed profiles under `profiles/` only after retrieval.

**Interfaces:** retain `load_document_type(root, name)` and existing validation API. Define `profile_readiness(profile: dict, today: str) -> str` in `skills/bo-cuc-tai-lieu/scripts/profile_policy.py` with OFFICIAL_RULE_REQUIRED, STALE, READY statuses. Training regulations do not satisfy presentation-rule source kind.

- [ ] RED test:

```python
def test_training_regulation_cannot_certify_presentation():
    from profile_policy import profile_readiness
    assert profile_readiness({"source_kind": "training-regulation"}, "2026-10-11") == "OFFICIAL_RULE_REQUIRED"
```

Add expired source, missing source hash, missing locator, approved institution exception, journal grid vs no-vertical borders and CK2 basic-depth fixtures.

- [ ] Run `python -m pytest tests/test_official_profile_requirements.py -q`; expect RED.
- [ ] Retrieve HMU CKII/BSNT presentation primary attachments first; record title/version/source/license/hash/date/locators. If absent create `BLOCKED.md`, do not mark READY or invent margins. Encode undergraduate/institutional/ministry reports, council response and defense conventions separately from official formatting. Caller selects convention for provisional writing but official format acceptance remains blocked.

```python
def official_presentation_source(profile: dict) -> bool:
    return (profile.get("source_kind") == "presentation-rules"
            and bool(profile.get("source_hash"))
            and bool(profile.get("requirements_locators")))
```

- [ ] Run profile/HMU/freshness/structure tests against source-backed fixtures; visually check actual profile-rendered documents where possible.
- [ ] Commit `feat: add source-governed document profiles` only for retrieved verified content; missing sources remain documented blockers.

## Task 8: Observational appraisal instruments

**Files:** modify `skills/danh-gia-chat-luong-bang-chung/SKILL.md`, `src/medical_research_skills_vn/coverage.py`; create instrument-specific references and coverage manifests under existing `skills/danh-gia-chat-luong-bang-chung/references/` and `coverage/`; create `tests/test_appraisal_expansion.py`.

**Interfaces:** extend existing coverage validator, not an independent parallel checklist loader. Each registered instrument consumes `instrument`, `version`, `source_url`, `license`, `last_verified`, exact expected/implemented IDs and operational item text/locators. Add source hash and applicability where required without silently bypassing older manifests.

- [ ] RED tests derive exact expected IDs from retrieved primary instruments. Add mismatched legacy/current version and missing signalling-question cases. For unavailable source pin the failure:

```python
def test_blocked_instrument_cannot_pass_with_empty_coverage():
    from medical_research_skills_vn.coverage import validate_coverage_manifest
    manifest = {"instrument": "Synthetic blocked fixture", "version": "fixture",
                "source_url": "https://example.invalid/fixture", "license": "fixture",
                "last_verified": "2026-10-11", "caller": "skills/medrs/SKILL.md",
                "status": "BLOCKED", "expected_ids": [], "implemented_ids": [], "items": []}
    assert "SOURCE_BLOCKED" in validate_coverage_manifest(manifest)
```

Extend coverage validation to emit SOURCE_BLOCKED before evaluating empty item equality; never allow two empty lists to certify completeness.

- [ ] Run `python -m pytest tests/test_appraisal_expansion.py tests/test_coverage_manifests.py -q`; expect missing registered instruments to fail.
- [ ] Retrieve official ROBINS-I current, ROBINS-E, JBI analytical cross-sectional/prevalence, QUADAS-3 and AMSTAR2. QUADAS-2 is only explicit legacy when protocol pins it. Verify JBI 2026 versus legacy applicability. Implement exact operational domains/signalling items under permitted licenses; if reproduction rights unavailable, licensed retrieval/reference strategy must still provide item coverage at use time, not memory reconstruction.
- [ ] Run exact-coverage tests plus design-selection cases. Independent review compares items with primary documents; word count is not evidence of completeness.
- [ ] Commit `feat: extend verified observational appraisal coverage` for verified tools only, leave missing tools explicitly blocked.

## Task 9: Reporting guidelines and journals

**Files:** modify `skills/kiem-chuan-bao-cao/SKILL.md`, `skills/bo-cuc-tai-lieu/SKILL.md`, `tests/test_coverage_manifests.py`; create source-backed guideline references/coverage, VJPM/VJPH profiles and `tests/test_reporting_and_journal_expansion.py`.

**Interfaces:** reuse task 8 coverage and task 7 profile readiness. Profile must distinguish article type, real section layout, word limits, reference style, tables, supplements and provenance. Formatting-only adjustments cannot satisfy section-layout requirements.

- [ ] Write exact guideline ID tests from retrieved PRISMA-ScR, RECORD, CROSS/CHERRIES, SRQR and SQUIRE2 sources, plus journal section-order test on an actual transformed document. For an expired otherwise valid profile:

```python
def test_expired_profile_requires_reverification():
    from profile_policy import profile_readiness
    profile = {"source_kind": "presentation-rules", "source_hash": "fixture",
               "requirements_locators": ["section 1"], "expires": "2026-10-10"}
    assert profile_readiness(profile, "2026-10-11") == "STALE"
```

- [ ] Run `python -m pytest tests/test_reporting_and_journal_expansion.py -q`; missing coverage/section remap must fail.
- [ ] Retrieve journal-owned author guidance (VJPM discovery URL `https://tcyhdp.vjpm.vn/cho-tac-gia/`), locate VJPH official source and guideline original publications via EQUATOR. Verify rights/version/freshness before encoding. Source inaccessible is a blocker for official acceptance, not permission to invent constraints. Update existing journal profiles under same process.
- [ ] Run coverage, journal structure and freshness suites; compare generated outline and styled DOCX with source requirements.
- [ ] Commit `feat: add verified reporting and journal profiles`.

## Task 10: Retrieval fallback and extraction traceability

**Files:** modify `skills/tim-y-van/SKILL.md`, `skills/tong-hop-bang-chung/SKILL.md`; create `skills/tim-y-van/references/access-fallback.md`, `skills/tim-y-van/scripts/access_policy.py`, `tests/test_literature_access_policy.py`; extend existing evidence-workflow tests.

**Interfaces:** `access_state(attempts: list[dict]) -> str`; attempt fields `provider`, `query`, `time`, `http_status`, `access_level`, `hits`, `error`. States distinguish SEARCHED_NO_HITS, INACCESSIBLE, ABSTRACT_ONLY, FULL_TEXT. Discovery graph edges are citation/relevance links, not appraisal or verified evidence strength.

- [ ] RED test:

```python
def test_forbidden_access_does_not_mean_absent_literature():
    from access_policy import access_state
    attempts = [{"provider": "pubmed", "http_status": 403, "hits": None}]
    assert access_state(attempts) == "INACCESSIBLE"
```

Add zero hits after valid query, conflicting providers, abstract-only limitation, duplicate DOI/title normalization, Vietnamese sources, retraction/update flags and citation-network expansion with recorded seed/edge provenance.

- [ ] Run `python -m pytest tests/test_literature_access_policy.py -q`; expect RED.
- [ ] Probe current host before choosing lawful fallback Europe PMC/OpenAlex/publisher/library/user-supplied PDF. Preserve query ledger, blocked attempts and dates. Never bypass access controls; no fixed quota of Vietnamese comparisons regardless of relevance. Extraction uses task 5 identity contract and returns source locator/access ceiling.

```python
def inaccessible(attempt: dict) -> bool:
    return attempt.get("http_status") in {401, 403, 429} or bool(attempt.get("error"))
```

- [ ] Run mocked access tests and one permission-safe live query with dated log; live success is host-specific, not a universal guarantee.
- [ ] Commit `fix: distinguish retrieval failures and preserve extraction provenance`.

## Task 11: Status registry, portable packages and final acceptance

**Files:** create `schemas/status-codes.json`, `docs/cowork-README.md`, `tests/test_upgrade_status_and_package.py`; modify `src/medical_research_skills_vn/packaging.py`, `skills/leader-nghien-cuu/scripts/revision_guard.py`, `README.md`, `.claude-plugin/marketplace.json`, `AGENTS.md`, existing installer/version/eval tests and `docs/medrs-3.1-upgrade.md`.

**Interfaces:** keep `build_cowork_package(root: Path, destination: Path) -> Path` and `final_acceptance` signatures compatible. Cowork ZIP root README must be the user-facing document, not a root developer instruction relying on excluded scripts. Status registry specifies contexts and evidence requirements; it does not erase distinctions between NOT_RUN and UNPERFORMED.

- [ ] RED package test:

```python
def test_cowork_contains_portable_runtime(tmp_path):
    import zipfile
    from medical_research_skills_vn.packaging import build_cowork_package
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    archive = build_cowork_package(root, tmp_path / "cowork.zip")
    with zipfile.ZipFile(archive) as bundle:
        assert "skills/dinh-dang-tai-lieu/scripts/docx_integrity.py" in bundle.namelist()
        assert "skills/leader-nghien-cuu/scripts/project_workspace.py" in bundle.namelist()
        assert bundle.read("README.md") == (root / "docs/cowork-README.md").read_bytes()
```

Add isolated extracted-ZIP execution without repo PYTHONPATH/root src, expired source, absent Word/UNO and stale final-hash acceptance tests. CLI fallback must not masquerade as chat-native command support.

- [ ] Run `python -m pytest tests/test_upgrade_status_and_package.py -q`; expect missing portable files/user README to fail.
- [ ] Update package inclusion/README mapping and status validation; retire old slice promises, synchronize user-facing marketplace text. Audit every new shared reference has a named caller. Source-gap/capability warnings remain visible after packaging. Shared preflight and optional clarity pass reference the actual author-style schema; no writer rule duplication.
- [ ] Run validators in AGENTS order: `claude plugin validate . --strict`; `python scripts/validate_skills.py`; `python scripts/sync_version.py --check`; `python -m pytest -q`; `python tests/eval_runner.py --offline`. Save full logs locally and concise public synthetic summaries.
- [ ] Run end-to-end standalone section, assembled manuscript, CK2 basic project, author-returned DOCX and existing-project migration scenarios. Review semantic content and rendered appearance of final exact hashes; a renderer missing means presentation incomplete even if unit tests pass.
- [ ] Commit `feat: finalize portable package and evidence-bound acceptance`.
- [ ] Obtain independent whole-branch review using the execution method chosen by the author. Resolve defects; any repair reruns affected suites and invalidates affected receipts.
- [ ] Only after complete scope acceptance, set release version in `.claude-plugin/plugin.json`, run `python scripts/sync_version.py`, repeat all release validations, build repository/ZIP artifacts and verify hash/contents. Promote accepted artifacts through task 1 lifecycle. Publish GitHub/copy ZIP/install only within prior user authorization, never publish private logs or reports. If sources/runtime prevent complete acceptance, report exact remaining items and do not label the release fully complete.

## Requirement ownership and self-review

| Spec IDs | Tasks |
|---|---|
| P0.1 | 4 |
| P0.2 | 5, 6 |
| P0.3–4 | 6 |
| P1.1 | 1, 6 |
| P1.2 | 3 |
| P1.3–4 | 2 |
| P1.5 | 3 |
| P1.6 | 4 |
| P1.7–9 | 5 |
| P1.10 | 10 |
| P1.11 | 1, 5 |
| P1.12 | 2, 6, 7 |
| P2.1 | 7 |
| P2.2 | 8 |
| P2.3 | 9 |
| P2.4 | 6 |
| P3 | 6, 11 |

Shared functions are defined in their owning task before use; existing API signatures are preserved. Source-derived exact checklist IDs and formatting numbers are intentionally obtained from verified primary documents, not fabricated in this plan. Their retrieval failure has an explicit blocked behavior and prevents full acceptance. Review Focus cases each have task owners and negative tests. No unit-test count is a completion criterion by itself.

## Handoff

Read this plan and the spec before editing production files. Author review is required before execution under the writing-plans skill. Suggested execution: Native implementation in this session, followed by independent whole-branch review; task-by-task delegated implementation/review is an alternative when the author prefers more frequent independent gates.
