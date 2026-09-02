# Medical Research Skills VN 2.0 — Slice 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a runnable Claude-first foundation-and-protocol slice with a versioned Research Passport, safe intake of in-progress projects, bounded routing context, shared writing preflight, protocol planning, ethics/data governance, Methods drafting, and executable offline acceptance tests.

**Architecture:** Build only the seven canonical skills needed for this slice: `co-van`, `ho-so-nghien-cuu`, `de-cuong-va-thiet-ke`, `co-mau-va-ke-hoach-phan-tich`, `dao-duc-va-quan-tri-du-lieu`, `viet-phuong-phap`, and `kiem-van-phong`. Deterministic Python modules own schemas, validation, extraction, freshness, and test execution; skills own medical decisions and human checkpoints. Conditional detail lives in explicit references, including one shared preflight reference rather than seven copies.

**Tech Stack:** Python 3.11+, `pytest`, `jsonschema`, `PyYAML`, `python-docx`, Markdown/YAML/JSON, Claude plugin manifest, portable Agent Skills.

**Spec:** `docs/superpowers/specs/2026-08-29-medical-research-skills-vn-v2-design.md`

## Global Constraints

- Keep one plugin and no runtime dependency on another plugin.
- Do not create the other seventeen canonical skill directories during slice 1.
- Do not ship alias skill directories or put legacy skill names in frontmatter descriptions.
- Each description is at most 60 words and 640 UTF-8 bytes; all 24 final descriptions must remain within 1,200 words and 12 KiB, with a working target of at most 50 words per skill.
- Each `SKILL.md` is at most 1,200 words and 16 KiB; `co-van` is at most 900 words and 12 KiB.
- Never invent data, citations, ethics approval, institutional rules, completed procedures, or execution results.
- Every inferred Passport value records provenance and remains unconfirmed until the author accepts it.
- Version 1.3.0 remains an uninstalled, checksummed archive only.
- R and Stata remain the statistical backends; Python performs deterministic plugin utilities, not user-facing statistical analysis.
- Use TDD for every executable component and commit after each independently reviewable task.

---

## File Map

| Path | Responsibility |
|---|---|
| `.claude-plugin/plugin.json` | Claude Chat/Cowork package manifest for the accepted slice |
| `plugin.json` | Compatibility copy required by current Claude packaging, validated against the canonical manifest |
| `config/canonical-skills.yaml` | Final 24-skill inventory, slice ownership, active status, and description-budget allocation |
| `schemas/research-passport.schema.json` | Machine-readable Passport contract |
| `schemas/source-record.schema.json` | Freshness, version, license, and verification contract |
| `src/medical_research_skills_vn/passport.py` | Passport creation, validation, confirmation, and marker handling |
| `src/medical_research_skills_vn/freshness.py` | `CURRENT`/`STALE`/`UNVERIFIED` computation |
| `src/medical_research_skills_vn/intake.py` | DOCX/Markdown/text extraction for in-progress projects |
| `src/medical_research_skills_vn/budgets.py` | Unicode-aware word/byte accounting |
| `src/medical_research_skills_vn/routing.py` | Canonical and legacy-name lookup without alias skills |
| `scripts/passport_cli.py` | Create, intake, validate, confirm, and summarize Passport artifacts |
| `scripts/validate_skills.py` | Structural, routing, budget, reference, license, and freshness validator |
| `tests/eval_runner.py` | Offline scenario runner; live adapters remain opt-in |
| `shared/references/writing-preflight.md` | Single shared compact preflight called by every writer |
| `skills/co-van/references/legacy-skill-map.yaml` | Old-name lookup owned by `co-van`, never loaded into descriptions |
| `sources/hmu/source-register.yaml` | Official HMU source acquisition record for later slice-4 encoding |
| `tests/fixtures/in-progress/` | Synthetic DOCX/Markdown projects with known extraction ground truth |
| `tests/cases/<skill>/` | Positive, negative, ambiguous, bilingual, and safety scenarios |

---

### Task 1: Scaffold the Claude-first slice and executable test environment

**Files:**
- Create: `pyproject.toml`
- Create: `.claude-plugin/plugin.json`
- Create: `plugin.json`
- Create: `config/canonical-skills.yaml`
- Create: `src/medical_research_skills_vn/__init__.py`
- Create: `tests/test_manifest.py`
- Create: `LICENSE`
- Create: `THIRD_PARTY_NOTICES.md`
- Create: `README.md`

**Interfaces:**
- Produces: `config/canonical-skills.yaml` with `final_count`, `active_slice`, `skills[].name`, `skills[].slice`, and `skills[].description_target_words`.
- Produces: installable Python test dependencies without installing the plugin globally.

- [ ] **Step 1: Write failing manifest and inventory tests**

```python
def test_slice_one_activates_only_seven_skills(inventory):
    active = [s["name"] for s in inventory["skills"] if s["active"]]
    assert active == [
        "co-van", "ho-so-nghien-cuu", "de-cuong-va-thiet-ke",
        "co-mau-va-ke-hoach-phan-tich", "dao-duc-va-quan-tri-du-lieu",
        "viet-phuong-phap", "kiem-van-phong",
    ]

def test_manifests_have_same_name_and_version(root):
    assert load_json(root / "plugin.json") == load_json(root / ".claude-plugin/plugin.json")
```

- [ ] **Step 2: Run the tests and confirm they fail because the files do not exist**

Run: `python -m pytest tests/test_manifest.py -q`

- [ ] **Step 3: Create the project scaffold and canonical 24-name inventory**

Set version `2.0.0-alpha.1`, license `CC-BY-NC-4.0`, and activate only the seven slice-1 skills. Give every final skill a default target of 45 description words; retain a hard per-skill ceiling of 60 and aggregate ceiling of 1,200.

- [ ] **Step 4: Record source licenses and pinned commits**

List the original ZIP checksum, Academic Research Skills commit/license, Scientific Agent Skills commit with per-file audit requirement, Elements of Style status, and Wikipedia attribution rule. Do not copy source content in this task.

- [ ] **Step 5: Run manifest tests**

Run: `python -m pytest tests/test_manifest.py -q`
Expected: all tests pass.

- [ ] **Step 6: Commit**

```text
git add pyproject.toml .claude-plugin/plugin.json plugin.json config src tests LICENSE THIRD_PARTY_NOTICES.md README.md
git commit -m "build: scaffold medical research v2 slice one"
```

### Task 2: Enforce context budgets and remove migration names from discovery text

**Files:**
- Create: `src/medical_research_skills_vn/budgets.py`
- Create: `scripts/validate_skills.py`
- Create: `tests/test_context_budgets.py`
- Create: `skills/co-van/references/legacy-skill-map.yaml`
- Create: `docs/migration-1.3-to-2.0.md`

**Interfaces:**
- Produces: `count_words(text: str) -> int` and `utf8_size(text: str) -> int`.
- Produces: `validate_context_budget(root: Path) -> list[ValidationIssue]`.
- Produces: `lookup_legacy_skill(name: str) -> str | None` in Task 6 from the YAML map created here.

- [ ] **Step 1: Write failing tests for per-skill and aggregate limits**

```python
def test_description_limits(plugin_tree):
    issues = validate_context_budget(plugin_tree)
    assert not [i for i in issues if i.code.startswith("DESCRIPTION_")]

def test_legacy_names_are_forbidden_in_descriptions(plugin_tree, legacy_names):
    for description in all_descriptions(plugin_tree):
        assert not set(legacy_names) & set(description.split())

def test_budget_fixture_detects_aggregate_overflow(overbudget_tree):
    assert "DESCRIPTION_AGGREGATE_WORDS" in issue_codes(validate_context_budget(overbudget_tree))
```

- [ ] **Step 2: Verify the tests fail before the validator exists**

Run: `python -m pytest tests/test_context_budgets.py -q`

- [ ] **Step 3: Implement Unicode-aware accounting and YAML frontmatter parsing**

Use a documented tokenizer based on Unicode letter/number sequences, not ASCII whitespace alone. Validate 60 words/640 bytes per description, active aggregate plus reserved final allocation, 1,200 words/12 KiB final description budget, 16 KiB frontmatter budget, and `SKILL.md` limits.

- [ ] **Step 4: Create one authoritative old-to-new mapping outside descriptions**

The YAML keys are every 1.3.0 skill name. Values contain `canonical`, `mode`, and `note`. The migration guide renders a human-readable table from the same mapping; it does not become routing context.

- [ ] **Step 5: Run the budget and legacy-name tests**

Run: `python -m pytest tests/test_context_budgets.py -q`
Expected: pass, including the deliberately over-budget fixture failing validation.

- [ ] **Step 6: Commit**

```text
git add src/medical_research_skills_vn/budgets.py scripts/validate_skills.py tests/test_context_budgets.py skills/co-van/references/legacy-skill-map.yaml docs/migration-1.3-to-2.0.md
git commit -m "test: enforce routing context budgets"
```

### Task 3: Implement the Research Passport and source-freshness core

**Files:**
- Create: `schemas/research-passport.schema.json`
- Create: `schemas/source-record.schema.json`
- Create: `src/medical_research_skills_vn/passport.py`
- Create: `src/medical_research_skills_vn/freshness.py`
- Create: `scripts/passport_cli.py`
- Create: `tests/test_passport.py`
- Create: `tests/test_freshness.py`

**Interfaces:**
- Produces: `new_passport(project_id: str, document_type: str, locale_profile: str) -> dict`.
- Produces: `validate_passport(data: dict) -> list[ValidationIssue]`.
- Produces: `confirm_field(data: dict, json_pointer: str, author: str, timestamp: str) -> dict`.
- Produces: `verification_status(record: dict, as_of: date) -> Literal["CURRENT", "STALE", "UNVERIFIED"]`.

- [ ] **Step 1: Write failing tests for unresolved, inferred, and confirmed values**

```python
def test_new_passport_never_presents_unknowns_as_facts():
    passport = new_passport("p-001", "thesis", "vi-medical-academic")
    assert passport["research_question"]["status"] == "UNRESOLVED"
    assert passport["research_question"]["marker"] == "DATA_REQUIRED"

def test_stale_source_keeps_original_verification_date():
    record = source_record(last_verified="2025-01-01", expires_after_days=90)
    assert verification_status(record, date(2026, 8, 29)) == "STALE"
    assert record["last_verified"] == "2025-01-01"
```

- [ ] **Step 2: Run tests and confirm missing-module failures**

Run: `python -m pytest tests/test_passport.py tests/test_freshness.py -q`

- [ ] **Step 3: Implement schemas and immutable audit events**

Each substantive field stores `value`, `status` (`CONFIRMED`, `DRAFT_INFERRED`, `UNRESOLVED`), `confidence`, `provenance[]`, and `confirmed_by`. Preserve stable marker codes separately from localized labels.

- [ ] **Step 4: Implement CLI operations**

Commands: `new`, `validate`, `confirm`, `summarize`, and `freshness`. Every mutation writes a new file unless `--output` names a new path; no command overwrites its input.

- [ ] **Step 5: Run schema and freshness tests**

Run: `python -m pytest tests/test_passport.py tests/test_freshness.py -q`
Expected: pass.

- [ ] **Step 6: Commit**

```text
git add schemas src/medical_research_skills_vn/passport.py src/medical_research_skills_vn/freshness.py scripts/passport_cli.py tests/test_passport.py tests/test_freshness.py
git commit -m "feat: add research passport core"
```

### Task 4: Add intake for in-progress projects

**Files:**
- Create: `src/medical_research_skills_vn/intake.py`
- Create: `tests/fixtures/in-progress/thesis-partial.md`
- Create: `tests/fixtures/in-progress/build_docx_fixture.py`
- Create: `tests/test_in_progress_intake.py`
- Modify: `scripts/passport_cli.py`

**Interfaces:**
- Produces: `extract_project(path: Path) -> ExtractedProject`.
- Produces: `draft_passport_from_project(project: ExtractedProject, project_id: str) -> dict`.
- Consumes: Passport status/provenance types from Task 3.

- [ ] **Step 1: Generate a synthetic DOCX fixture with headings, tables, conflicting objectives, and missing design**

The fixture contains no real participant data. It includes a title, an Introduction objective, a Methods table with population variables, one citation-like string, and a later objective that conflicts with the first.

- [ ] **Step 2: Write failing intake tests**

```python
def test_docx_intake_builds_draft_not_confirmed_passport(docx_fixture):
    passport = draft_passport_from_project(extract_project(docx_fixture), "legacy-001")
    assert passport["objectives"]["status"] == "DRAFT_INFERRED"
    assert passport["objectives"]["provenance"][0]["artifact"].endswith(".docx")
    assert passport["study_design"]["status"] == "UNRESOLVED"

def test_conflicting_objectives_become_author_question(docx_fixture):
    passport = draft_passport_from_project(extract_project(docx_fixture), "legacy-001")
    assert "AUTHOR_APPROVAL_REQUIRED" in passport["unresolved_markers"]
    assert passport["intake_questions"]
```

- [ ] **Step 3: Run tests and confirm failure**

Run: `python -m pytest tests/test_in_progress_intake.py -q`

- [ ] **Step 4: Implement DOCX, Markdown, and text extraction**

Extract headings, paragraphs, tables, footnote/endnote presence, and section-local provenance. Infer only candidates for title, questions, objectives, design, population, variables, and cited-source strings. Do not infer ethics approval, completed procedures, verified results, or institutional profile from formatting alone.

- [ ] **Step 5: Add `passport_cli.py intake`**

Command example: `python scripts/passport_cli.py intake draft.docx --project-id legacy-001 --output passport.draft.json`. Output includes an intake report and ordered author questions; it never modifies the draft.

- [ ] **Step 6: Run intake tests**

Run: `python -m pytest tests/test_in_progress_intake.py -q`
Expected: pass for DOCX and Markdown; conflicts and unknowns remain explicit.

- [ ] **Step 7: Commit**

```text
git add src/medical_research_skills_vn/intake.py scripts/passport_cli.py tests/fixtures/in-progress tests/test_in_progress_intake.py
git commit -m "feat: intake in-progress research projects"
```

### Task 5: Create the shared writing preflight once

**Files:**
- Create: `shared/references/writing-preflight.md`
- Create: `schemas/writing-preflight-result.schema.json`
- Create: `tests/fixtures/shared-preflight/valid-writer/SKILL.md`
- Create: `tests/fixtures/shared-preflight/copied-rules-writer/SKILL.md`
- Create: `tests/test_shared_preflight.py`
- Modify: `scripts/validate_skills.py`

**Interfaces:**
- Produces: one reference path `shared/references/writing-preflight.md` called explicitly by every writing skill.
- Produces: result fields `status`, `checks[]`, `markers[]`, `locale_profile`, `passport_hash`, and `section_hash`.

- [ ] **Step 1: Write failing tests for a single source of truth**

```python
def test_shared_preflight_exists(plugin_tree):
    path = plugin_tree / "shared/references/writing-preflight.md"
    assert path.exists()
    assert {"FABRICATION", "UNRESOLVED", "CAUSALITY", "LOCALE"} <= preflight_check_ids(path)

def test_writers_reference_shared_preflight(plugin_tree):
    for name in writing_skills_present(plugin_tree):
        body = skill_body(plugin_tree, name)
        assert "../../shared/references/writing-preflight.md" in body

def test_preflight_rules_are_not_copied_into_writers(copied_rules_fixture):
    issues = validate_shared_preflight(copied_rules_fixture)
    assert "PREFLIGHT_RULE_DUPLICATED" in issue_codes(issues)
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_shared_preflight.py -q`

- [ ] **Step 3: Write the shared preflight contract**

Include only four compact checks: fabricated facts/citations, unresolved markers, causal-language ceiling, and locale mismatch. State that it is not the full `kiem-van-phong` audit and returns `PENDING` for the full gate during multi-section drafting.

- [ ] **Step 4: Extend structural validation**

Require every present writing skill to name the shared reference exactly once. Fail on copied preflight headings or missing caller links.

- [ ] **Step 5: Run shared-reference tests**

Run: `python -m pytest tests/test_shared_preflight.py -q`
Expected: pass.

- [ ] **Step 6: Commit**

```text
git add shared schemas/writing-preflight-result.schema.json tests/test_shared_preflight.py scripts/validate_skills.py
git commit -m "refactor: centralize writing preflight"
```

### Task 6: Implement `co-van` and `ho-so-nghien-cuu`

**Files:**
- Create: `src/medical_research_skills_vn/routing.py`
- Create: `skills/co-van/SKILL.md`
- Create: `skills/ho-so-nghien-cuu/SKILL.md`
- Create: `skills/ho-so-nghien-cuu/references/intake-existing-project.md`
- Create: `tests/cases/co-van/routing.yaml`
- Create: `tests/cases/ho-so-nghien-cuu/intake.yaml`
- Create: `tests/test_routing.py`

**Interfaces:**
- Produces: `RoutingRequest(text: str, attachments: tuple[str, ...] = ())`.
- Produces: `RoutingDecision(entrypoint: str, canonical: str, mode: str, availability: str)`.
- Produces: `route_request(request: RoutingRequest, legacy_map: dict) -> RoutingDecision`.
- Consumes: Task 2 legacy map; Task 3 Passport API; Task 4 intake API.

- [ ] **Step 1: Write failing routing tests**

```python
def test_old_skill_name_routes_through_co_van_without_alias(legacy_map):
    decision = route_request(RoutingRequest(text="dieu-phoi-luan-van"), legacy_map)
    assert decision.entrypoint == "co-van"
    assert decision.canonical == "viet-ban-thao-y-hoc"
    assert decision.availability == "NOT_IN_ACTIVE_SLICE"

def test_existing_draft_routes_to_intake():
    decision = route_request(RoutingRequest(text="Tôi có luận văn đang viết dở", attachments=["draft.docx"]), {})
    assert decision.canonical == "ho-so-nghien-cuu"
    assert decision.mode == "intake-existing-project"
```

- [ ] **Step 2: Run routing tests and confirm failure**

Run: `python -m pytest tests/test_routing.py -q`

- [ ] **Step 3: Implement concise descriptions and skill bodies**

Descriptions contain Vietnamese and English positive triggers plus the nearest negative boundary, but no legacy names. `co-van` reads the legacy map only when the user supplies an old skill name. `ho-so-nghien-cuu` offers `new`, `intake-existing-project`, `validate`, `confirm`, and `summarize` modes.

- [ ] **Step 4: Add the author-confirmation dialogue contract**

For intake, present extracted values with provenance, group conflicts, ask one bounded question at a time, and persist confirmation events. Never ask the user to re-enter a value already extracted and unambiguous; ask only for confirmation or correction.

- [ ] **Step 5: Run routing, budget, and Passport tests together**

Run: `python -m pytest tests/test_routing.py tests/test_context_budgets.py tests/test_passport.py tests/test_in_progress_intake.py -q`
Expected: pass.

- [ ] **Step 6: Commit**

```text
git add src/medical_research_skills_vn/routing.py skills/co-van skills/ho-so-nghien-cuu tests/cases tests/test_routing.py
git commit -m "feat: route new and in-progress projects"
```

### Task 7: Implement protocol design and analysis-planning boundaries

**Files:**
- Create: `skills/de-cuong-va-thiet-ke/SKILL.md`
- Create: `skills/de-cuong-va-thiet-ke/references/design-contract.md`
- Create: `skills/co-mau-va-ke-hoach-phan-tich/SKILL.md`
- Create: `skills/co-mau-va-ke-hoach-phan-tich/references/estimand-and-power.md`
- Create: `schemas/analysis-plan.schema.json`
- Create: `tests/cases/de-cuong-va-thiet-ke/boundaries.yaml`
- Create: `tests/cases/co-mau-va-ke-hoach-phan-tich/boundaries.yaml`
- Create: `tests/test_planning_boundaries.py`

**Interfaces:**
- Produces: design artifact with research question, objectives, hypotheses, population, eligibility, sampling frame/strategy, variables, and bias controls.
- Produces: analysis-plan artifact with estimand, assumptions, alpha/power, sample-size calculation trace, planned model family, analysis sets, missing-data plan, and sensitivity plan.

- [ ] **Step 1: Write failing ownership-boundary tests**

```python
def test_design_skill_does_not_claim_sample_size_ownership(skill_contracts):
    assert "sample_size_calculation" not in skill_contracts["de-cuong-va-thiet-ke"].owns

def test_analysis_plan_rejects_observed_outcome_model_selection(run_case):
    result = run_case("co-mau-va-ke-hoach-phan-tich", "choose-model-from-smallest-p")
    assert result.status == "REFUSE_AND_EXPLAIN"
```

- [ ] **Step 2: Run boundary tests and confirm failure**

Run: `python -m pytest tests/test_planning_boundaries.py -q`

- [ ] **Step 3: Write the two skills and substantive references**

Make protocol/completed-study state explicit. Sample-size outputs must show formula/method, assumptions, design effect or attrition where applicable, and R/Stata reproducibility route; they cannot use observed significance to revise the target.

- [ ] **Step 4: Validate schemas, context budgets, and boundary scenarios**

Run: `python -m pytest tests/test_planning_boundaries.py tests/test_context_budgets.py -q`
Expected: pass.

- [ ] **Step 5: Commit**

```text
git add skills/de-cuong-va-thiet-ke skills/co-mau-va-ke-hoach-phan-tich schemas/analysis-plan.schema.json tests/cases tests/test_planning_boundaries.py
git commit -m "feat: add protocol design and analysis planning"
```

### Task 8: Implement ethics and data-governance profiles

**Files:**
- Create: `skills/dao-duc-va-quan-tri-du-lieu/SKILL.md`
- Create: `skills/dao-duc-va-quan-tri-du-lieu/references/vietnam-profile.md`
- Create: `skills/dao-duc-va-quan-tri-du-lieu/references/international-profile.md`
- Create: `skills/dao-duc-va-quan-tri-du-lieu/references/data-governance.md`
- Create: `skills/dao-duc-va-quan-tri-du-lieu/references/source-register.yaml`
- Create: `tests/test_ethics_governance.py`

**Interfaces:**
- Produces: ethics/data-governance checklist with jurisdiction, study stage, data class, destination, authorization basis, consent/waiver state, registration state, and unresolved approvals.

- [ ] **Step 1: Write failing tests for stale and fabricated approval behavior**

```python
def test_missing_ethics_number_is_never_filled(run_case):
    result = run_case("dao-duc-va-quan-tri-du-lieu", "missing-approval-number")
    assert "OFFICIAL_RULE_REQUIRED" in result.markers
    assert not result.invented_values

def test_stale_regulatory_source_displays_banner(source_register):
    assert validate_sources(source_register, as_of="2026-08-29").has("SOURCE_STALE")
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_ethics_governance.py -q`

- [ ] **Step 3: Populate references from primary sources with version/license/freshness metadata**

Store operational rules and decisions needed by the skill, not framework names alone. Separate Vietnam and international conditions and require browsing or author-supplied current documents when a source is stale.

- [ ] **Step 4: Run ethics and source validators**

Run: `python -m pytest tests/test_ethics_governance.py tests/test_freshness.py -q && python scripts/validate_skills.py`
Expected: pass with no unverified current-rule claim.

- [ ] **Step 5: Commit**

```text
git add skills/dao-duc-va-quan-tri-du-lieu tests/test_ethics_governance.py
git commit -m "feat: add ethics and data governance"
```

### Task 9: Implement Methods writing and the full style-gate lifecycle

**Files:**
- Create: `skills/viet-phuong-phap/SKILL.md`
- Create: `skills/viet-phuong-phap/references/protocol-vs-completed.md`
- Create: `skills/kiem-van-phong/SKILL.md`
- Create: `skills/kiem-van-phong/references/scientific-integrity.md`
- Create: `skills/kiem-van-phong/references/composition-vi.md`
- Create: `skills/kiem-van-phong/references/composition-en.md`
- Create: `schemas/style-audit.schema.json`
- Create: `tests/test_methods_and_style_gate.py`

**Interfaces:**
- Consumes: Passport, design artifact, analysis plan, ethics artifact, locale profile, and shared preflight.
- Produces: Methods draft, claim/evidence table, preflight result, unresolved markers, and full-gate audit keyed by document/section/reference hashes.

- [ ] **Step 1: Write failing lifecycle tests**

```python
def test_multi_section_draft_uses_preflight_not_full_gate(run_case):
    result = run_case("viet-phuong-phap", "draft-inside-multi-section-document")
    assert result.preflight.status in {"PASS", "REVISE"}
    assert result.full_gate.status == "PENDING"

def test_standalone_methods_runs_full_gate_once(run_case):
    result = run_case("viet-phuong-phap", "standalone-methods")
    assert result.audit_invocations.full_document == 1

def test_protocol_never_changes_planned_work_to_past_tense(run_case):
    result = run_case("viet-phuong-phap", "protocol-with-unperformed-procedure")
    assert not result.claims_procedure_completed
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_methods_and_style_gate.py -q`

- [ ] **Step 3: Implement Methods modes and shared-reference call**

Protocol mode describes planned procedures; completed-study mode uses only confirmed executed procedures and records deviations. The writer links the single shared preflight rather than embedding its rules.

- [ ] **Step 4: Implement scoped full-gate references and cache contract**

Passes 1–2 use claim/evidence artifacts; passes 3–4 load only the active locale and composition reference. Store `document_hash`, `section_hashes`, `locale_profile_version`, `source_ledger_version`, and `reference_versions`; invalidate only changed chunks plus global consistency checks.

- [ ] **Step 5: Run lifecycle, shared-preflight, and budget tests**

Run: `python -m pytest tests/test_methods_and_style_gate.py tests/test_shared_preflight.py tests/test_context_budgets.py -q`
Expected: pass and no copied preflight block.

- [ ] **Step 6: Commit**

```text
git add skills/viet-phuong-phap skills/kiem-van-phong schemas/style-audit.schema.json tests/test_methods_and_style_gate.py
git commit -m "feat: add methods writing and scoped style gate"
```

### Task 10: Acquire the official HMU source independently of slice-4 coding

**Files:**
- Create: `sources/hmu/source-register.yaml`
- Create: `sources/hmu/README.md`
- Create: `tests/test_hmu_source_register.py`

**Interfaces:**
- Produces: source records with `title`, `issuing_body`, `document_number`, `effective_date`, `source_url`, `retrieved_at`, `sha256`, `license`, `redistribution`, `scope`, `last_verified`, and `verification_status`.
- Does not produce the HMU machine-readable formatting profile; that remains slice 4.

- [ ] **Step 1: Write a failing completeness test**

```python
def test_hmu_source_acquired_by_deadline(register):
    assert register["acquisition_due"] == "2026-09-30"
    assert register["status"] in {"ACQUIRED", "AUTHORITATIVE_ACCESS_CONFIRMED"}
    assert register["sources"]
    assert all(s["sha256"] and s["last_verified"] for s in register["sources"])
```

- [ ] **Step 2: Inspect the official HMU postgraduate legal-document index**

Start at `https://sdh.hmu.edu.vn/news/xc115_Van-ban-phap-quy.html`, record the page retrieval date, and follow only official HMU links. Treat the 2026 proposal/defense process pages and Decision 3589/QĐ-ĐHYHN references as discovery leads, not automatically as the presentation-format authority.

- [ ] **Step 3: Acquire or request the authoritative presentation document**

If public, save a lawful local snapshot and checksum it. If access is restricted, record the official access route and obtain an author-supplied copy; do not bypass authentication. Record redistribution as `PROHIBITED_OR_UNKNOWN` unless HMU states otherwise.

- [ ] **Step 4: Separate source acquisition from encoding**

Set `encoding_status: DEFERRED_TO_SLICE_4` and `encoding_acceptance_gate: slice-4`. The acquisition test must pass by 2026-09-30; profile implementation and golden DOCX fixtures are due only at slice-4 acceptance.

- [ ] **Step 5: Run source-register and freshness tests**

Run: `python -m pytest tests/test_hmu_source_register.py tests/test_freshness.py -q`
Expected: source acquisition passes without claiming the profile is encoded.

- [ ] **Step 6: Commit**

```text
git add sources/hmu tests/test_hmu_source_register.py
git commit -m "docs: register authoritative HMU sources"
```

### Task 11: Build the offline scenario runner and end-to-end protocol fixture

**Files:**
- Create: `tests/eval_runner.py`
- Create: `tests/cases/end-to-end/protocol-new-project.yaml`
- Create: `tests/cases/end-to-end/protocol-existing-project.yaml`
- Create: `tests/test_eval_runner.py`
- Create: `tests/test_slice_one_e2e.py`

**Interfaces:**
- Produces: `python tests/eval_runner.py --offline` with non-zero exit on failed assertions or unsupported requested adapter.
- Consumes: all seven active skills and all deterministic APIs from Tasks 1–9.

- [ ] **Step 1: Write failing runner tests**

```python
def test_unsupported_adapter_fails_clearly(run_cli):
    result = run_cli("python tests/eval_runner.py --host chatgpt")
    assert result.exit_code != 0
    assert "adapter not implemented" in result.stderr.lower()

def test_existing_project_e2e_preserves_inference_status(run_e2e):
    result = run_e2e("protocol-existing-project")
    assert result.passport["objectives"]["status"] != "CONFIRMED"
    assert result.author_questions
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_eval_runner.py tests/test_slice_one_e2e.py -q`

- [ ] **Step 3: Implement deterministic YAML scenario execution**

Support exact-match structural assertions, forbidden claims, marker presence, route decisions, artifact schema validation, and expected failure modes. Offline mode does not pretend to evaluate prose quality; it validates contracts and supplied golden outputs.

- [ ] **Step 4: Add two complete protocol journeys**

New-project journey: `co-van` → new Passport → design → sample size/analysis plan → ethics/data governance → Methods → preflight/full gate. Existing-project journey: DOCX intake → draft Passport → author questions → same workflow without retyping extracted facts.

- [ ] **Step 5: Run the complete offline suite**

Run: `python -m pytest -q && python scripts/validate_skills.py && python tests/eval_runner.py --offline`
Expected: all commands exit 0; unsupported live adapters are not counted as passes.

- [ ] **Step 6: Commit**

```text
git add tests/eval_runner.py tests/cases/end-to-end tests/test_eval_runner.py tests/test_slice_one_e2e.py
git commit -m "test: add slice one protocol acceptance"
```

### Task 12: Package, rollback-test, and accept slice 1

**Files:**
- Create: `scripts/package_plugin.py`
- Create: `scripts/verify_rollback.py`
- Create: `archive/README.md`
- Create: `tests/test_packaging.py`
- Modify: `README.md`
- Modify: `docs/migration-1.3-to-2.0.md`

**Interfaces:**
- Produces: `dist/medical-research-skills-vn-2.0.0-alpha.1.zip` with checksum report.
- Consumes: the user-supplied 1.3.0 ZIP as an external archival input; never installs it alongside 2.0.

- [ ] **Step 1: Write failing package-content tests**

```python
def test_zip_contains_only_active_slice_skills(package):
    skill_roots = package.skill_roots()
    assert skill_roots == set(ACTIVE_SLICE_ONE_SKILLS)

def test_no_alias_or_legacy_installation(package):
    assert not package.contains_legacy_skill_directories()
    assert not package.contains_nested_v1_installation()
```

- [ ] **Step 2: Run packaging tests and confirm failure**

Run: `python -m pytest tests/test_packaging.py -q`

- [ ] **Step 3: Implement deterministic packaging**

Sort archive entries, normalize timestamps, exclude caches/test outputs/confidential fixtures, include license/notices/manifests, emit SHA-256, and fail if structural validation is not clean.

- [ ] **Step 4: Implement rollback simulation in isolated temporary directories**

Simulate: install 2.0 → assert only seven slice-1 descriptions discoverable → uninstall 2.0 → install archived 1.3.0 → assert only 1.3.0 descriptions discoverable. Never touch the user's live plugin cache during this test.

- [ ] **Step 5: Run final acceptance commands**

Run:

```text
python -m pytest -q
python scripts/validate_skills.py
python tests/eval_runner.py --offline
python scripts/package_plugin.py
python scripts/verify_rollback.py --isolated
```

Expected: five zero exit codes; generated ZIP checksum recorded; Git working tree contains only expected deliverables.

- [ ] **Step 6: Commit**

```text
git add scripts/package_plugin.py scripts/verify_rollback.py archive/README.md tests/test_packaging.py README.md docs/migration-1.3-to-2.0.md
git commit -m "build: package and accept slice one"
```

---

## Slice-1 Exit Criteria

- Seven, and only seven, canonical skills are active and packageable.
- No description contains a legacy skill name; `co-van` resolves old names from one explicit reference.
- Description/frontmatter/entrypoint budgets pass both word and byte tests.
- Every writer calls the same shared preflight reference; no copied preflight block exists.
- New and in-progress projects both produce valid Passports; inferred values remain draft and traceable to source locations.
- Protocol design, sample-size/analysis planning, ethics/data governance, and Methods ownership boundaries pass negative tests.
- `kiem-van-phong` runs once for a stable assembled document and only reruns after invalidating changes.
- HMU authoritative-source acquisition is tracked separately with deadline 2026-09-30; encoding remains a slice-4 gate.
- Offline runner, structural validator, packaging, and isolated rollback simulation all exit 0.
- The 1.3.0 archive is checksummed and uninstalled whenever 2.0 is active.
