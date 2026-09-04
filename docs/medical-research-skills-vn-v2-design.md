# Medical Research Skills VN 2.0 — Design Specification

## 1. Purpose

Version 2.0 is a greenfield rebuild of `medical-research-skills-vn` as one medical-first plugin with a portable Agent Skills core. Claude Chat and Claude Cowork are the first packaging target. ChatGPT Chat, ChatGPT Work, and Codex receive explicit host adapters in later phases; they are not assumed to read Claude manifests. The plugin supports clinical research, epidemiology, public health, laboratory medicine, qualitative health research, theses, dissertations, systematic reviews, and journal manuscripts.

The plugin remains human-led. It may analyze, outline, draft, edit, validate, and execute local document or statistical workflows when the host permits. It must not invent data, citations, approvals, policies, or completed procedures. The accountable researcher approves scientific decisions and final text.

## 2. Design goals

1. Keep one plugin so every skill can call the other skills it needs.
2. Remove duplicated coordinators and language-specific copies.
3. Preserve deep, section-specific writing workflows.
4. Use progressive disclosure so only relevant instructions enter context.
5. Treat official institutional and journal requirements as executable document profiles.
6. Separate document structure from Word mechanics.
7. Preserve R and Stata as the primary statistical backends.
8. Operate safely across chat-only and file-capable hosts.
9. Record evidence, decisions, missing inputs, and author approvals.
10. Provide a replacement and rollback path from version 1.3.0 without preserving duplicate runtime aliases.

## 3. Non-goals

- The plugin will not absorb all skills from either reference repository.
- It will not become a general-purpose scientific or drug-discovery suite.
- It will not diagnose, recommend treatment, or replace ethics committees, statisticians, supervisors, editors, or peer reviewers.
- It will not claim that prose is human-written, optimize for detector scores, or conceal AI use.
- It will not apply generic formatting when an official target profile is required but unavailable.
- It will not execute R, Stata, Word, or external database operations on a host that lacks those capabilities.

## 4. Architectural model

### 4.1 Four layers

| Layer | Responsibility |
|---|---|
| Entry and state | `medrs` classifies the request, checks privacy, opens the Research Passport, and selects a workflow. |
| Medical workflows | Planning, evidence, analysis, section writing, document assembly, review, and revision. |
| Target profiles | Study-design, language, institution, journal, reporting-guideline, and document-depth rules. |
| Quality gates | Evidence, citation, consistency, causal-language, privacy, integrity, structure, and author approval checks. |

### 4.2 Research Passport

Every substantial project uses one Research Passport. It is a local Markdown or JSON artifact when files are available and a structured conversation block on chat-only hosts.

`ho-so-nghien-cuu` also supports `adopt-existing-project`. It reads an author-supplied DOCX, Markdown, or text draft; extracts candidate research questions, objectives, design, variables, and source-ledger entries with artifact/section/paragraph provenance; and creates a draft Passport. Extracted values are `DRAFT_INFERRED`, never verified. Conflicts and fields that cannot be derived remain unresolved markers and are presented to the author for confirmation rather than silently filled or requested again from scratch.

Required fields:

- project identifier and document type;
- target language and audience;
- research question, objectives, hypotheses, and study design;
- population, setting, exposure/intervention, comparator, and outcomes;
- data-sensitivity classification and allowed destinations;
- target institution or journal profile and verification date;
- first-class locale profile for academic rhetoric, terminology, address, attribution, tense, and section conventions;
- reporting guideline and risk-of-bias framework;
- verified results and their provenance;
- source ledger and claim–citation links;
- author decisions and approvals;
- unresolved markers;
- AI-use and external-service disclosure record.

Every dynamic profile, checklist, API reference, regulatory source, and journal or institution rule also carries:

- `source_url` or local source identifier;
- `source_version`;
- `source_license`;
- `source_cutoff`;
- `last_verified`;
- `expires_after_days`;
- `verification_status`: `CURRENT`, `STALE`, or `UNVERIFIED`.

Default freshness windows are 90 days for journal, institution, legal, regulatory, and ethics profiles; 365 days for reporting guidelines and appraisal tools; and 180 days for API/package references. A workflow may require a shorter window, especially immediately before submission. A stale source remains visible but produces an expiry banner and requires author approval. An unverified source cannot support a claim that the current rule or version has been confirmed. On a host without browsing, the plugin must preserve the last verified date and display `STALE` or `UNVERIFIED`; it must not silently refresh the date.

No workflow may silently convert an unresolved item into a fact.

### 4.3 Standard unresolved markers

Markers use stable language-neutral codes and locale-specific display text:

| Code | Vietnamese | English |
|---|---|---|
| `DATA_REQUIRED` | `[CẦN DỮ LIỆU]` | `[DATA REQUIRED]` |
| `VERIFIED_RESULTS_REQUIRED` | `[CẦN KẾT QUẢ ĐÃ XÁC NHẬN]` | `[VERIFIED RESULTS REQUIRED]` |
| `SOURCE_REQUIRED` | `[CẦN TÌM NGUỒN: mô tả loại bằng chứng]` | `[SOURCE REQUIRED: evidence needed]` |
| `OFFICIAL_RULE_REQUIRED` | `[CẦN QUY ĐỊNH CHÍNH THỨC]` | `[OFFICIAL REQUIREMENT REQUIRED]` |
| `AUTHOR_APPROVAL_REQUIRED` | `[CẦN TÁC GIẢ DUYỆT]` | `[AUTHOR APPROVAL REQUIRED]` |
| `HOST_CAPABILITY_UNAVAILABLE` | `[KHÔNG THỂ THỰC THI TRÊN NỀN TẢNG NÀY]` | `[HOST CAPABILITY UNAVAILABLE]` |
| `SOURCE_STALE` | `[NGUỒN ĐÃ HẾT HẠN XÁC MINH]` | `[SOURCE VERIFICATION EXPIRED]` |
| `SOURCE_UNVERIFIED` | `[CHƯA XÁC MINH NGUỒN HIỆN HÀNH]` | `[CURRENT SOURCE NOT VERIFIED]` |

The output shows the language that matches the active locale profile. Machine-readable artifacts store the stable code.

## 5. Canonical skill inventory

Version 2.0 contains 24 canonical skills.

### 5.1 Entry, planning, and governance

1. `medrs` — single entrypoint and workflow router.
2. `ho-so-nghien-cuu` — creates, validates, updates, and summarizes the Research Passport.
3. `de-cuong-va-thiet-ke` — develops the research question, objectives, hypotheses, design, target population, eligibility, sampling frame and strategy, variables, bias controls, and protocol structure. It does not calculate sample size or choose a final fitted model.
4. `co-mau-va-ke-hoach-phan-tich` — defines estimands, effect-size assumptions, alpha/power, sample-size calculations, planned model families, analysis sets, missing-data strategy, sensitivity analyses, and prespecified tables/figures. It does not inspect observed outcomes to select models or interpret results.
5. `dao-duc-va-quan-tri-du-lieu` — Vietnam and international ethics profiles, consent, privacy, registration, data governance, and disclosure preparation.

### 5.2 Evidence workflows

6. `tim-y-van` — reproducible literature and authoritative-database retrieval with query provenance.
7. `tong-hop-bang-chung` — narrative, scoping, systematic-review, and meta-analysis modes; protocol output when study data are absent.
8. `danh-gia-chat-luong-bang-chung` — design-matched risk-of-bias appraisal, GRADE/CERQual, and evidence limitations.

### 5.3 Statistical workflows

9. `phan-tich-so-lieu` — after verified data or output exist, coordinates execution through `phan-tich-r` or `phan-tich-stata`, selects justified adjustments within the prespecified plan, checks assumptions, records deviations, and interprets effect estimates and uncertainty. Without a callable R/Stata runtime it produces code and an execution plan or interprets supplied real output; it never claims to have executed an analysis. It cannot silently redesign sampling, recalculate the target sample to fit observed results, or select models for significance.
10. `phan-tich-r` — generates and audits R scripts, reads real output, and prepares reproducible tables and figures.
11. `phan-tich-stata` — generates and audits Stata do-files, reads real output, and prepares reproducible tables and figures.

Python may support bounded document or validation utilities but is not a third user-facing statistical backend.

### 5.4 Writing workflows

12. `viet-ban-thao-y-hoc` — document-level writing orchestrator. It assembles section plans from the Research Passport and target profile but delegates section prose.
13. `viet-dat-van-de` — problem, evidence gap, rationale, and objectives without generic significance claims.
14. `viet-tong-quan` — thematic or conceptual synthesis driven by an evidence map; it must not produce an author-by-author catalogue.
15. `viet-phuong-phap` — protocol mode describes planned work; completed-study mode describes what was actually done and records deviations.
16. `viet-ket-qua` — writes only from verified tables, figures, datasets, or statistical output; it does not interpret results.
17. `viet-ban-luan` — target-journal reverse engineering, Discussion Blueprint, evidence-needs matrix, cautious interpretation, and limitations.
18. `viet-ket-luan-khuyen-nghi` — answers the objectives without new findings or unsupported extrapolation.
19. `viet-tom-tat` — produces the abstract last and verifies consistency with the full text.
20. `kiem-van-phong` — mandatory post-writing quality gate for scientific reasoning, author voice, English composition, Vietnamese academic prose, and formulaic AI-writing patterns.

### 5.5 Validation and completion

21. `kiem-chung-ban-thao` — claim–citation support, citation existence, cross-section consistency, reporting-guideline coverage, integrity, disclosure, and submission readiness.
22. `bo-cuc-tai-lieu` — builds and applies an official institution or journal structure profile, including actual section reordering, renaming, splitting, and merging.
23. `dinh-dang-tai-lieu` — performs Word mechanics: styles, heading levels, section breaks, tables of contents, lists of tables/figures, captions, page numbering, margins, fonts, and spacing.
24. `phan-bien-va-chinh-sua` — thesis examination, journal peer review, revision coaching, response letters, commitment tracking, and re-review.

## 6. Writing system

### 6.1 Shared writing contract

Every section writer receives:

- the Research Passport;
- document and target profiles;
- an approved section outline;
- verified facts and results permitted for that section;
- the source ledger and claim-strength limits;
- target language, depth, and word budget;
- a first-class locale profile identifier and content covering academic rhetoric, terminology, forms of address, attribution, tense, citation integration, paragraphing, and section conventions.

Every section writer returns:

- draft text;
- a claim–evidence table;
- unresolved markers;
- consistency dependencies on other sections;
- an author-approval request for scientific interpretations;
- a compact local preflight result and `kiem-van-phong` gate status. Initial section drafting records the full gate as `PENDING`; it does not invoke the complete gate once per section.

### 6.2 Mandatory `kiem-van-phong` gate

The gate has four independent passes:

1. **Scientific integrity:** no fabricated facts, sources, results, approvals, policies, causal claims, or novelty claims.
2. **Argument quality:** each substantive claim must attach to verified results, a source, explicit reasoning, or an unresolved marker.
3. **Composition:** paragraph unity, useful topic sentences, concrete wording, concise syntax, appropriate active voice, parallel construction, related words kept together, and emphasis placed deliberately.
4. **Formulaic-writing audit:** flags generic significance, promotional tone, vague attribution, superficial participial analysis, mechanical rule-of-three phrasing, repeated negative parallelism, canned challenges/future-prospects conclusions, excessive headings, boldface, em dashes, and templated user-facing language.

The fourth pass treats these patterns as possible symptoms, not proof of AI authorship. Corrections must improve specificity, evidence, logic, and author voice. The plugin must not promise detector evasion.

The gate has an explicit execution lifecycle:

1. Every section writer calls one named shared preflight reference for fabricated facts/citations, unresolved markers, causal overreach, and locale mismatch. The rules exist in that reference only; writers link it by relative path and do not embed copies. This preflight uses the shared writing contract and does not load the complete `kiem-van-phong` skill or all of its references.
2. A standalone section request invokes the full gate once before delivery.
3. A multi-section document invokes the full gate once after first assembly. Passes 1–2 operate on the document-wide claim/evidence and consistency artifacts; passes 3–4 operate in bounded section chunks using only the active locale and named composition references.
4. If substantive revisions follow that audit, affected chunks receive scoped re-audits and the assembled document receives one final full gate before submission. With no substantive revision, the first assembly audit is the final audit. Thus the normal document lifecycle has one full-document gate, or two when revision invalidates the first result—not one complete invocation per writer.

The gate stores an audit state keyed by document hash, section hashes, locale-profile version, source-ledger version, and reference versions. Unchanged sections are reused; any changed dependency invalidates only the affected scoped result plus document-wide consistency checks. A full gate may load only the reference modules named for its current pass and locale.

### 6.3 Discussion workflow

`viet-ban-luan` proceeds through five stages:

1. Verify the exact target journal, article type, and current author instructions. Quartile is optional metadata, never an entry gate. If recorded, it must include ranking system, category, year, source, access status, and verification state; user-supplied institutional JCR/Scopus information is accepted but is not silently presented as independently verified.
2. Select two or three legally accessible comparator papers from that journal, prioritizing the same topic and design. Permitted routes are author-supplied PDFs, publisher or repository open access, PubMed Central, Unpaywall or equivalent lawful discovery, and manual use of the author's institutional access. The plugin never bypasses a paywall, copies credentials, or automates access outside the user's authorization. If full Discussion text is unavailable, use fewer full-text comparators or a generic evidence-based framework; do not reverse engineer a Discussion from its abstract.
3. With author approval, map each Discussion paragraph by rhetorical function, source result, literature comparison, proposed mechanism, handling of agreement/disagreement, and role in the overall argument.
4. Derive a reusable Discussion Blueprint from common rhetorical moves without copying sentences or imitating one author's distinctive voice.
5. Draft each argument as: finding → meaning → literature comparison → explanation → limitation → proportionate implication, then validate against Results, study design, source ledger, claim-strength ladder, target profile, and `kiem-van-phong`.

Required artifacts are the benchmark-paper register, lawful-access record, paragraph-function maps, Discussion Blueprint, evidence-needs matrix, draft, and audit report. Stored maps contain DOI/citation metadata and functional summaries, not full copyrighted text or long excerpts. Source retention follows the author's authorization and applicable access terms. Author checkpoints occur after paper selection and after the Blueprint.

### 6.4 Planning-boundary contract

| Skill | Owns | Must not do |
|---|---|---|
| `de-cuong-va-thiet-ke` | Research question, objectives, hypotheses, design, target population, eligibility, sampling frame/strategy, variable operationalization, bias controls | Calculate sample size; fit or interpret the final model |
| `co-mau-va-ke-hoach-phan-tich` | Estimand, assumptions, alpha/power, sample-size calculation, planned model family, analysis sets, missing/sensitivity plan | Use observed outcomes to choose models; interpret study results |
| `phan-tich-so-lieu` | Coordinate the prespecified analysis through `phan-tich-r`/`phan-tich-stata`, diagnose verified output, document justified deviations, report estimates and uncertainty | Claim execution without a runtime; silently change the design or target sample; data-dredge or optimize for significance |

## 7. Document structure and Word execution

### 7.1 `bo-cuc-tai-lieu`

This skill owns semantic document architecture. It must:

1. retrieve or receive the current official institution or journal instructions;
2. record their source and verification date;
3. construct a machine-readable document profile;
4. compare the current document with the required section order and hierarchy;
5. produce a restructuring plan;
6. move, rename, merge, or split sections after author approval;
7. hand the structurally correct document to `dinh-dang-tai-lieu`.

For theses and dissertations, an official institutional template overrides observed convention. For journal manuscripts, current author instructions, article type, submission stage, and official template override generic IMRaD assumptions. Without an official profile, the skill stops at `[CẦN QUY ĐỊNH CHÍNH THỨC]`.

### 7.2 `dinh-dang-tai-lieu`

This skill owns Word mechanics and never decides scientific section order. It must preserve content, numbers, citations, comments, tracked changes, and embedded objects unless the approved operation requires a bounded change.

It supports specification, diagnosis, apply, table-of-contents, and validation modes. It writes a new output file, a change log, and a validation report; it never overwrites the source document.

Validation must inspect the generated file, not merely the script configuration. It checks style assignments, heading hierarchy, fields, captions, section breaks, page numbering, margins, font/spacing rules, and rendered-page anomalies where rendering is available.

Word validation has four capability levels:

1. **Windows Word COM backend:** on a local Windows execution surface with Microsoft Word and COM access, open a copy in a hidden Word instance; update fields, tables of contents and other indexes; repaginate; save the resulting DOCX; export PDF; and close documents and the Word process in a `finally` path. Tests must detect leaked processes and confirm that the inspected DOCX/PDF is the generated artifact. This backend applies to a Windows terminal or local Codex execution surface, not to a Linux Cowork VM merely because it mounts files from a Windows device.
2. **Preinstalled LibreOffice UNO backend:** when LibreOffice and UNO are already callable, update document indexes through UNO, save, and then export PDF. A bare `soffice --convert-to pdf` call is not treated as proof that fields or indexes were refreshed.
3. **Provisioned LibreOffice UNO sandbox backend:** a Linux Cowork or cloud adapter may install or supply a pinned LibreOffice/UNO runtime inside its sandbox or image, then perform the same index-update, save, export, and render workflow. Provisioning must pass an executable capability probe for package/image availability, UNO import, writable temporary storage, fonts, and PDF rendering. Installation is never assumed from the client device's operating system. If the sandbox forbids provisioning, this backend is unavailable rather than silently skipped.
4. **Structural-only fallback:** when no rendering backend is callable, inspect OOXML relationships, style assignments, field instructions, section properties, headers/footers, numbering definitions, and package integrity. Computed TOC page numbers, final pagination, line/page breaks, cross-reference display, and visual layout remain `AUTHOR_APPROVAL_REQUIRED`; the report must not mark them as passed.

The local Windows development-host audit on 2026-08-29 found Microsoft Word COM available and `soffice` unavailable. That result applies only to the Windows host. It says nothing about a Cowork Linux VM, a cloud sandbox, or a mounted Windows directory. For the first Claude Cowork package, provisioned LibreOffice UNO is the target for level-2 document automation; if its adapter capability test fails, Cowork must advertise structural-only formatting until the backend is supplied.

PDF pages from a successful rendering backend are rasterized with an available PDF renderer for representative visual inspection. The validator records the backend, version, commands/API path, files inspected, checks performed, skipped checks, and unresolved approvals.

| Property | OOXML-only | Word COM | LibreOffice UNO, preinstalled or provisioned | Human review still required |
|---|---:|---:|---:|---:|
| Styles, hierarchy, section properties, field instructions | Yes | Yes | Yes | For ambiguous semantic intent |
| Updated TOC/index values and page numbers | No | Yes | Yes, after explicit UNO index update | If backend unavailable or compatibility differs |
| Final pagination and PDF export | No | Yes | Yes | For target-environment fidelity |
| Visual defects, widows/orphans, clipping, awkward breaks | No | Render for inspection | Render for inspection | Yes; automation may flag but not certify aesthetics |
| Tracked changes, comments, equations, embedded-object fidelity | Structural checks only | Best fidelity on Word | Compatibility-dependent | Yes for material or unsupported objects |

## 8. Cross-platform behavior and release order

The plugin uses portable Agent Skills as its core. Host-specific capabilities are detected at runtime.

| Execution surface | Typical runtime and file access | Word automation | R/Stata and persistent artifacts |
|---|---|---|---|
| Chat-only | No shell; user uploads or pastes redacted inputs | Specification and instructions only | Code generation and supplied-output interpretation; conversation-block Passport |
| Claude Cowork VM | Linux VM/sandbox with host files exposed through a mounted path; the client device may be Windows but COM is not inherited | Provisioned or preinstalled LibreOffice UNO after a passing capability probe; otherwise OOXML-only with explicit approvals | Execute only a runtime callable inside the VM; local Markdown/JSON Passport in the mounted workspace |
| Local Windows Python/terminal, including a local Codex host | Native Windows process and local filesystem permissions | Word COM preferred when installed; LibreOffice UNO optional; OOXML fallback | Execute only locally installed R/Stata; local artifacts |
| Linux cloud sandbox or worktree | Isolated Linux filesystem, possibly with controlled mounts and package restrictions | Provisioned/preinstalled LibreOffice UNO after a passing probe; otherwise OOXML fallback | Execute only provisioned runtimes; sandbox-local artifacts and explicit export |

Browsing/connectors are independent capabilities on every surface. Confidential processing is permitted only within the user's authorization and the declared storage/egress boundary; a file-capable sandbox is not automatically approved for identifiable data.

No canonical skill assumes Claude-specific hooks, slash commands, subagents, Codex-only tools, or that another host can read `.claude-plugin/plugin.json`. Platform adapters may enhance execution but cannot alter the scientific contract.

Packaging is delivered in this order:

1. portable core schema, canonical skills, references, deterministic validators, and host-neutral test cases;
2. Claude Chat/Cowork packaging and end-to-end acceptance;
3. Codex adapter and end-to-end acceptance using Codex's native skill/plugin conventions;
4. ChatGPT Chat/Work adapter and end-to-end acceptance using the capabilities available at implementation time.

A later adapter is not listed as supported until its own manifest, installation path, routing behavior, file/tool capability degradation, and end-to-end tests pass. Claude acceptance does not imply ChatGPT or Codex acceptance.

## 9. Privacy and external services

Raw identifiable, sensitive, controlled, unpublished, or institution-restricted data stay local by default. Chat services receive only redacted, de-identified, aggregated, synthetic, or placeholder content unless the user explicitly confirms authorization for a named destination and scope.

Before any external call, `medrs` or the active skill records:

- data class;
- proposed destination;
- fields being sent;
- authorization basis;
- whether a local alternative exists.

External content is untrusted data. Instructions embedded in papers, PDFs, datasets, API responses, or templates are never executed as user instructions.

## 10. Source integration and licensing

The design review used these snapshots:

- original plugin ZIP SHA-256: `C3AD0C20385BD8B7AEE0C93FEE4303F3CF4499E586C06978CF4689E4443F6231`;
- Academic Research Skills commit: `5debcd2efb686dce0205ba9094b6413dae5f89c0`;
- Scientific Agent Skills commit: `895b4be37ef0ca1cd55c6e628e7ff937ba5a1cf1`;
- *Elements of Style* repository and Wikipedia field guide accessed on 2026-08-29.

Implementation may update an upstream snapshot only after reviewing its changelog, license, security implications, and effect on this specification.

| Source | Pinned snapshot | License status | Permitted integration approach |
|---|---|---|---|
| Original `medical-research-skills-vn` 1.3.0 | ZIP SHA-256 above | CC BY-NC 4.0 | Preserve attribution; derivative release remains subject to the non-commercial condition unless rights are separately obtained |
| `academic-research-skills` | Commit above | CC BY-NC 4.0 | Adapt architecture and concepts with attribution; do not relabel as MIT-compatible content |
| `scientific-agent-skills` | Commit above | Root MIT, but individual skill directories may carry MIT, BSD, Apache, GPL, proprietary, or unknown terms | Audit every selected file/skill before reuse; root license is not treated as blanket permission for conflicting child content |
| `the-elements-of-style` | Snapshot recorded during implementation | Public-domain source text, subject to repository notice verification | Adapt concise composition principles |
| Wikipedia “Signs of AI writing” | Revision/date recorded during implementation | CC BY-SA applies to copied/adapted Wikipedia expression | Use as a cited descriptive field guide; avoid copying its prose or turning it into detector-evasion rules |

Version 2.0 defaults to CC BY-NC 4.0 because the original plugin and Academic Research Skills contribution path are non-commercial. The release documentation must state that commercial or for-profit use, including some hospital, institute, consultancy, or sponsored settings, may require permission and legal review. A commercially permissive edition is a separate project requiring a clean-room rewrite of non-commercial contributions and a file-by-file rights audit; it is not implied by this specification.

### 10.1 Original plugin

Preserve Vietnam-specific medical research workflows, bilingual output, R/Stata support, ethics profiles, reporting-guideline selection, risk-of-bias tools, Word formatting, and anti-fabrication constraints.

### 10.2 Academic Research Skills

Adapt the useful architecture: human checkpoints, source ledger, claim verification, cross-document consistency, revision commitments, disclosure records, integrity gates, and staged research-to-publication flow. Claude-specific orchestration, hooks, and command infrastructure are not copied into the portable core.

### 10.3 Scientific Agent Skills

Adapt deterministic retrieval contracts, authoritative database selection, experimental design, statistical power, local exploratory checks, publication-quality visualization, evidence-bounded hypothesis generation, and security boundaries. General science, chemistry, omics, laboratory automation, and unrelated package skills remain outside the core.

### 10.4 Elements of Style and AI-writing field guide

Use composition principles from the public-domain *Elements of Style*. Use Wikipedia's signs of AI writing only as a descriptive quality checklist, with its caveats retained. Do not transform either source into detector-evasion rules.

The release records exact upstream commit identifiers, selected file paths, license findings, adaptation method, and third-party notices. Verbatim content is included only when its license permits and its maintenance value exceeds a concise adaptation.

## 11. Greenfield replacement of version 1.3.0

Version 2.0 is a major greenfield rebuild, not a directory remap. Only the plugin name and `medrs` entrypoint remain stable. Approximately seven of the twenty-four canonical roles have close predecessors; the writing system expands into section-specific skills while six legacy coordinators collapse into one stateful orchestration path.

| Version 1.3.0 area | Version 2.0 destination |
|---|---|
| Six `dieu-phoi-*` skills | `medrs`, document profiles, and `viet-ban-thao-y-hoc` |
| `viet-phan-vn` / `viet-phan-en` | Section-specific writers with `locale` profiles |
| `viet-dinh-tinh-vn` | Qualitative design profile plus section writers |
| `dao-duc-vn` / `dao-duc-en` | `dao-duc-va-quan-tri-du-lieu` jurisdiction profiles |
| `tim-tai-lieu` | `tim-y-van` |
| Systematic-review coordinator | `tong-hop-bang-chung` systematic/scoping/meta modes |
| Multiple `kiem-*` skills | `kiem-van-phong`, `kiem-chung-ban-thao`, and design-matched references |
| Thesis/manuscript reviewers and rebuttal | `phan-bien-va-chinh-sua` modes |
| `kiem-dinh-dang` | Validation modes in `bo-cuc-tai-lieu` and `dinh-dang-tai-lieu` |

No legacy alias skill directories are shipped. Claude loads skill descriptions for routing and does not provide a reliable “explicit-only alias” contract, so alias directories would consume context and create duplicate triggers. Legacy names appear only in the migration guide and the lookup reference owned by `medrs`; they are forbidden in canonical descriptions so the full description budget remains available for bilingual positive and negative routing triggers. Direct invocation of a removed legacy `$skill` name is an intentional major-version break and receives a documented lookup path through `medrs`.

Version 1.3.0 is retained only as a checksummed archival ZIP and migration fixture; it is not installed or discoverable while 2.0 is under test or active. Rollback is a two-step operation: uninstall 2.0, then reinstall the archived 1.3.0 package. Tests verify that only one version contributes skill descriptions to routing at a time.

### 11.1 Vertical implementation slices

Implementation proceeds as four independently runnable end-to-end slices. A slice is accepted before the next one opens; all twenty-four skills are never developed concurrently.

1. **Foundation and protocol:** `medrs`, Research Passport, source freshness, ethics/data governance, design, sample size/analysis planning, protocol Methods, core integrity and routing validators.
2. **Analysis, Results, and journal article:** R/Stata execution, verified Results, section writers, Discussion reverse engineering, abstract, journal structure, style gate, manuscript validation.
3. **Evidence synthesis:** literature retrieval, evidence maps, narrative/scoping/systematic review, meta-analysis, reporting-guideline coverage, design-matched risk of bias, GRADE/CERQual.
4. **Thesis/dissertation, document execution, and revision:** thesis profiles, full document assembly, semantic restructuring, Word backends, rendered validation, examination/peer review, response and commitment tracking. HMU work has two milestones. First, the maintainer owns obtaining and archiving the authoritative current thesis/dissertation presentation rules of Hanoi Medical University by 2026-09-30, independently of the coding schedule, with source snapshot/checksum, `last_verified`, and license/redistribution note. Second, the document-profile workstream encodes rule-level profile fields, builds the golden DOCX fixture, and passes structure/format tests before slice-4 acceptance. If an authoritative source is unavailable, the maintainer must resolve the source or formally remove HMU from release scope rather than leave it indefinitely `PENDING LOCAL SOURCE`.

Each slice includes its canonical skills, substantive references, fixtures, automated tests, one end-to-end exemplar, migration notes, and rollback point. A skill may begin only when its dependencies from an accepted slice exist.

## 12. Context and packaging budget

These limits are self-imposed engineering budgets, not documented platform limits. They control routing context and maintenance cost and may be changed only through an explicit design decision with updated tests.

- One plugin contains all callable skills; no runtime cross-plugin dependency is permitted.
- Canonical `SKILL.md` files contain routing, essential constraints, inputs, outputs, and reference-selection rules only.
- Each canonical frontmatter `description` is at most 60 words and 640 UTF-8 bytes. Across all 24 skills, descriptions are at most 1,200 words and 12 KiB, and complete YAML frontmatter is at most 16 KiB.
- Each canonical `SKILL.md`, including frontmatter, is at most 1,200 words and 16 KiB; `medrs` has the tighter limit of 900 words and 12 KiB. A larger workflow must move conditional detail into named references rather than request an undocumented exception.
- Detailed procedures, profiles, examples, and checklists live under `references/`. Placement alone is insufficient: every checklist-bearing or instrument-bearing skill must contain operational item-level content, not a list of framework names.
- Scripts implement deterministic repeated operations rather than prose instructions.
- Each reference has at least one explicit caller.
- Tests reject duplicate canonical triggers, broken links, unused references, oversize entrypoints, and circular routing.
- No alias skill directories are permitted. Legacy names may appear only in the migration guide and `medrs` lookup reference, never in canonical descriptions.

Every checklist or appraisal instrument has a machine-readable coverage manifest containing framework name, adopted version, source, source license, retrieval date, `last_verified`, exact expected item/domain identifiers and counts, implemented identifiers, and the reference file that supplies each item. Operational coverage means:

- STROBE coverage includes all 22 numbered items and applicable subitems for the adopted checklist;
- PRISMA 2020 coverage includes all 27 numbered items and applicable subitems;
- RoB 2 coverage includes all five domains, every signalling question in the adopted tool, response options, decision rules or algorithm references, domain judgments, and overall judgment logic;
- CONSORT coverage matches the complete adopted current official version. A legacy 2010 profile may be retained only when a target requires it, must be labeled legacy, and must account for all 25 legacy items; the default must not silently hard-code the superseded count;
- other named guidelines or instruments meet the same exact item/domain accounting rule.

The initial authoritative registries are the [STROBE Statement](https://www.strobe-statement.org/), [PRISMA 2020 checklist](https://www.prisma-statement.org/prisma-2020-checklist), [Cochrane Handbook risk-of-bias chapter](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08), and [CONSORT/SPIRIT official explanation-and-elaboration registry](https://www.consort-spirit.org/published-e-es). Implementation must verify the adopted artifact at its primary source rather than reconstruct it from memory or a secondary summary.

Where the source license permits redistribution, the reference may include the full checklist wording. Where it does not, the plugin stores a faithful item-level operational paraphrase with the official item identifier and source link; it must not reproduce protected wording without permission. As a coarse guard, a checklist-bearing leaf skill must have at least 500 words across its operational references, excluding metadata and citations. Word count is necessary but never sufficient: a coverage-manifest mismatch, missing subitem, name-only entry, or unimplemented decision rule fails validation regardless of length.

## 13. Testing strategy

The test suite is executable, not a collection of Markdown trigger examples. Its primary runner is `pytest`:

- deterministic structural and unit cases live in `tests/`;
- routing and safety scenarios live as YAML or JSON under `tests/cases/<skill>/`;
- `scripts/validate_skills.py` checks manifests, frontmatter, graph boundaries, references, coverage manifests, freshness metadata, context budgets, licenses, and forbidden aliases;
- `tests/eval_runner.py` runs offline deterministic assertions by default and optional live-model evaluations through explicit `claude`, `codex`, or later ChatGPT adapters;
- golden DOCX/PDF, R, and Stata fixtures are versioned or generated reproducibly with checksums.

Required local commands are:

```text
claude plugin validate . --strict
python scripts/validate_skills.py
python -m pytest -q
python tests/eval_runner.py --offline
```

The official Claude validator runs first for manifest schema, component paths, path traversal, frontmatter parsing, and encoding. It does not replace `scripts/validate_skills.py`, which owns medical coverage, context budgets, freshness, reference reachability, and license audit.

Live model evaluation is opt-in, requires an explicitly configured host and credentials, records model/version/date, and cannot replace deterministic checks. Typical commands are `python tests/eval_runner.py --host claude` and `python tests/eval_runner.py --host codex`; unsupported adapters fail clearly rather than being skipped as passes.

### 13.1 Structural tests

- Validate plugin manifests, YAML frontmatter, names, links, scripts, licenses, and version metadata.
- Enforce per-description word/byte limits, aggregate description/frontmatter budgets, per-`SKILL.md` limits, and progressive-disclosure rules using UTF-8 byte counts and a documented Unicode-aware word tokenizer.
- Detect circular calls and overlapping automatic triggers.
- Reject any alias skill directory, checklist coverage mismatch, name-only checklist, reference-content floor failure, missing source/version/license/freshness metadata, or unreviewed per-file upstream license.

### 13.2 Behavioral routing tests

- Positive, negative, ambiguous, bilingual, and locale-leakage cases for every canonical skill.
- End-to-end cases for protocol, thesis, dissertation, journal article, qualitative study, systematic review, and meta-analysis.
- Host-capability degradation tests for chat-only and file-capable environments.

### 13.3 Scientific safety tests

- Missing results, contradictory numbers, fabricated citations, invalid DOI/PMID, unsupported mechanisms, causal overreach, invented ethics approval, stale policy, and confidential-data prompts.
- Discussion reverse engineering must preserve rhetorical abstraction while avoiding phrase copying.
- Results writing must refuse invented numbers and interpretation.
- Methods writing must distinguish planned from executed procedures.

### 13.4 Writing-quality tests

- Paragraph unity, evidence specificity, attribution, claim strength, concise composition, language-appropriate grammar, author voice, and formulaic-writing patterns.
- Tests assess improvements in reasoning and prose; they never score detector evasion.

### 13.5 R and Stata tests

- Syntax and smoke tests where runtimes are available.
- Golden output-parsing fixtures.
- Missing-data, model-assumption, effect-size, confidence-interval, and table/figure reporting cases.
- No result may be reported unless traceable to actual data or supplied output.

### 13.6 Word and structure tests

- Golden thesis and journal fixtures with incorrect section order and incorrect styles.
- Verify actual section restructuring before Word formatting.
- Inspect heading hierarchy, table of contents, captions, section breaks, page numbering, margins, fonts, spacing, and output preservation on the generated artifact.
- Exercise Word COM on supported Windows CI or a declared local validation host. Exercise both preinstalled and provisioned LibreOffice UNO paths on a Linux fixture. The Claude Cowork adapter must run its own capability probe and an end-to-end index-update/PDF-render fixture before advertising rendered Word automation. Exercise OOXML-only degradation unconditionally on every host adapter.
- Confirm field/index refresh and repagination through the backend output, not through script settings or field-code presence alone.
- Render successful PDF exports to page images and visually inspect representative documents. When rendering is unavailable, assert `AUTHOR_APPROVAL_REQUIRED` for every unperformed visual or pagination check.
- Test safe cleanup after exceptions, no leaked Word/LibreOffice processes, preservation of tracked changes/comments/embedded objects within declared support, and explicit warnings for compatibility losses.

## 14. Acceptance criteria

The release is ready only when:

1. all 24 canonical skills validate and pass their routing tests;
2. no canonical skill duplicates another's responsibility;
3. all references are reachable and loaded only by named conditions, and every checklist/instrument passes exact item-level coverage, minimum-content, version, source, license, and freshness validation;
4. all end-to-end workflows preserve the Research Passport and author checkpoints;
5. scientific safety tests pass without silent fabrication;
6. journal and institutional fixtures are structurally reorganized, not merely restyled;
7. Word outputs are new files with change logs and generated-file validation reports; computed fields, page numbers, and visual layout are either verified through Word COM/LibreOffice UNO plus rendering or explicitly marked `AUTHOR_APPROVAL_REQUIRED`;
8. R/Stata outputs remain traceable to code and real output;
9. chat-only hosts degrade explicitly rather than pretending to execute;
10. upstream attribution, file-level license audits, commit pins, third-party notices, non-commercial-use notice, and the security review are complete;
11. version 1.3.0 remains recoverable as a checksummed, uninstalled archival package, and rollback tests prove that 2.0 is removed before 1.3.0 is reinstalled;
12. each vertical slice passes its executable offline suite and end-to-end exemplar before the next slice begins;
13. no legacy alias directory ships and no legacy name appears in a canonical description;
14. locale-profile tests demonstrate materially distinct Vietnamese and English academic conventions beyond translation;
15. source-expiry tests display stale/unverified banners and never claim a current version without verification;
16. each host is advertised only after its own adapter passes installation, routing, degradation, and end-to-end smoke tests; Cowork rendered Word automation additionally requires a passing provisioned/preinstalled LibreOffice UNO fixture;
17. description, aggregate frontmatter, and `SKILL.md` budgets pass the exact word-and-byte limits in section 12;
18. the HMU profile is source-verified and passes its golden structure/format fixtures by 2026-09-30, or HMU support is explicitly removed from release scope before slice-4 acceptance.

## 15. Planned deliverables

- Versioned source tree for `medical-research-skills-vn` 2.0.
- Git repository plus `.claude-plugin/marketplace.json` as the primary distribution channel, allowing ref/SHA pinning, update history, and repo-first installation; Codex and ChatGPT Chat/Work adapters remain separately accepted later deliverables.
- Twenty-four canonical skill directories with routing-only descriptions, legacy lookup through `medrs`, and no alias directories.
- Research Passport schema and templates.
- Institution, journal, study-design, first-class locale, and reporting profiles with source freshness metadata.
- Substantive checklist/instrument references, exact coverage manifests, source/version/license records, and stale-source banners.
- Word restructuring and formatting scripts with local-Windows Word COM, preinstalled/provisioned LibreOffice UNO for Linux/Cowork surfaces, OOXML-only degradation, PDF rendering, capability probes, and explicit human-approval reports.
- A source-verified HMU thesis/dissertation profile owned by the document-profile workstream, due 2026-09-30, with a golden DOCX fixture and executable structure/format tests.
- R/Stata workflow references and tests.
- Executable `pytest` structural, behavioral, safety, context, coverage, source-freshness, host-adapter, and document tests.
- Migration guide, attribution/license audit, changelog, and rollback package. A checksum-pinned ZIP is a secondary marketplace `archive` distribution, not the primary installer.
