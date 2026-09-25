# MedRS 3.0 — Design Specification

Status: approved in brainstorming on 2026-09-25; awaiting written-spec review.
Target release: `3.0.0-rc.1`, then `3.0.0` after acceptance on a real manuscript.

## 1. Purpose

MedRS 2.0.0-alpha.8 is accurate but behaves like a compliance officer. It demands proof for what the author states, stops when a regulation source is overdue for re-checking, undercuts every Discussion paragraph with its own limitations, scatters status codes through drafts, and destroys Zotero citations whenever it edits a Word file.

Version 3.0 keeps the accuracy and changes the posture. MedRS works for the author: it trusts what the author states, asks only what it cannot default, writes each finding at the full strength its evidence supports, answers weaknesses before an examiner raises them, writes in the author's own voice, and keeps Zotero citations alive.

One boundary does not move: MedRS never invents approval numbers, data, statistics, or citations the author has not supplied. It leaves a slot and keeps writing.

## 2. Problems observed in 2.0.0-alpha.8

| Problem | Evidence |
|---|---|
| Every Discussion argument ends by listing bias, confounding, chance and a limitation | `skills/viet-ban-luan/SKILL.md:17` |
| The ethics skill demands evidence for approvals the author states | `skills/dao-duc-va-quan-tri-du-lieu/SKILL.md:13` |
| The ethics skill stops when a regulation source is marked `STALE` or `UNVERIFIED` | `skills/dao-duc-va-quan-tri-du-lieu/SKILL.md:22` |
| Every writing skill requires "depth, and budget", but nothing defines depth per document type, so the author is asked each time | `skills/viet-ket-qua/SKILL.md:13`, `skills/viet-ban-thao-y-hoc/SKILL.md:13` |
| Status codes appear 35 times across 28 skill files and leak into drafts | `UNRESOLVED`, `DRAFT_INFERRED`, `AUTHOR_APPROVAL_REQUIRED`, `OFFICIAL_RULE_REQUIRED` |
| Refusal clauses repeat in skill descriptions, so tone drifts skill by skill | the `Không …` tail of most `description` fields |
| Two skills check the same things before submission | round 1 of `tu-phan-bien` duplicates `kiem-chung-ban-thao` |
| Only one structure profile exists: the HMU master's thesis | `profiles/institution/hmu/` |
| Prose rewriting follows generic good style, not the author's voice | `skills/kiem-van-phong/references/prose-rewriting.md` |
| No code recognises Zotero fields; `quan-ly-trich-dan` never inserts citations | no `ZOTERO_ITEM` handling in `src/` |

Formatting is not the cause of lost citations. `format_docx` clears only run font name and size (`src/medical_research_skills_vn/docx_formatting.py:132-135`), which leaves field codes intact. Citations break when MedRS rewrites paragraph content and flattens each field into its displayed text.

## 3. Working principles

A new shared file, `skills/medrs/references/working-principles.md`, holds the posture that every skill follows. Each `SKILL.md` links it exactly once: `medrs` as `references/working-principles.md`, every other skill as `../medrs/references/working-principles.md`. `structure.py` enforces the link the same way it enforces the shared writing preflight.

1. **The author's word is enough.** A fact the author states — approval body and number, consent arrangement, design, data provenance — is recorded as `CONFIRMED` and used at once. No proof is requested. This changes what qualifies as `CONFIRMED`; the Research Passport schema does not change.
2. **Ask as little as possible.** Ask only when a missing choice would materially change the output and no sensible default exists. Otherwise choose the default, state it in one line, and continue. Ask at most one question at a time. Never ask the author to justify a request.
3. **Do it the author's way.** When a request is unusual, carry it out. Note a concern once if it matters; do not block and do not lecture.
4. **Never invent — the only hard boundary.** Do not create approval numbers or dates, data values, statistical results, citations, or consent statements the author has not supplied. Write a short slot such as `[Số QĐ]` and keep drafting. A slot is not a refusal.
5. **Lead with strength.** Interpret each finding at the full strength its evidence supports, not below it. State contributions plainly. Gather limitations into one section placed by the document-type profile, strengths first, and pair each limitation with how it was mitigated or why it does not overturn the finding. Observational designs still report associations, stated with confidence.
6. **Keep drafts clean.** Body text carries only short slots. Every item the author must supply goes into one closing checklist headed `Việc cần bổ sung` / `Items to complete`. Status codes such as `UNRESOLVED` and `DRAFT_INFERRED` live in artifacts and that checklist, never in prose.

For ethics specifically, an overdue regulation source no longer stops work. The skill drafts against the most recent known rule and adds "re-check the current rule" to the closing checklist.

## 4. Structure

### 4.1 Merge `kiem-chung-ban-thao` into `tu-phan-bien`

The inventory drops from 28 to 27 skills. `tu-phan-bien` becomes the single pre-submission reviewer:

- **Round 1 — evidence soundness:** numeric consistency across abstract, text, tables and figures; claim–citation support; objective–method–result–conclusion alignment; reporting-guideline coverage through `kiem-chuan-bao-cao`. `skills/kiem-chung-ban-thao/references/validation-contract.md` moves to `skills/tu-phan-bien/references/validation-contract.md` and becomes this round's lens.
- **Round 2 — sceptical reader:** questions an examiner or reviewer will ask, alternative explanations, and argument quality through `kiem-van-phong`.

The independence rules of 2.0.0-alpha.8 stay: a hash-locked manuscript, no edits between rounds, and a second round that never reads the first.

`kiem-van-phong` and `kiem-chuan-bao-cao` remain callable on their own for a focused check. `phan-bien-va-chinh-sua` keeps its separate job: answering comments from real reviewers.

Routing: requests matching `kiểm chứng bản thảo`, `validate the manuscript`, `submission readiness`, or `kiểm tra trước khi nộp` route to `tu-phan-bien` in mode `pre-submission-review`. `skills/medrs/references/legacy-skill-map.yaml` maps `kiem-chung-ban-thao` to `tu-phan-bien`, and the installer retires the old directory through its existing manifest-scoped retirement, as it did for `co-van` in 2.0.0-alpha.2.

Eighteen files reference `kiem-chung-ban-thao`, including `tests/cases/end-to-end/journal-article.yaml`; all move to the new name.

### 4.2 Capability-led descriptions

All 27 `description` fields are rewritten to open with what the skill does. One disambiguation clause may remain when it helps routing ("use this for X; use Y for Z"). Moral refusals move to the working principles. Each description stays within the existing 60-word, 640-byte budget.

## 5. Document-type profiles

A new layer, `profiles/document-type/`, defines six document types:

| File | Type |
|---|---|
| `journal-article-vn.yaml` | Vietnamese journal article |
| `journal-article-intl.yaml` | International journal article |
| `thesis-master.yaml` | Master's thesis (luận văn thạc sĩ) |
| `thesis-specialist.yaml` | Specialist thesis (luận văn BSCK I/II) |
| `dissertation-doctoral.yaml` | Doctoral dissertation (luận án tiến sĩ) |
| `protocol.yaml` | Study protocol (đề cương) |

Each profile has two layers.

**Convention layer** (`convention`, status `CONVENTION`) — defaults that save the author from being asked, freely overridden:

| Field | Vietnamese article | International article | Master's / specialist thesis | Doctoral dissertation |
|---|---|---|---|---|
| Frame | Đặt vấn đề with explicit objectives → Đối tượng và phương pháp → Kết quả → Bàn luận → separate Kết luận mirroring the objectives | Strict IMRaD; aim in the last Introduction paragraph; conclusion as the final Discussion paragraph | Institution chapter structure | Institution chapter structure plus a new-contributions section |
| Abstract | Vietnamese and English | English, structured | Institution rule | Institution rule |
| Discussion scope | Follows the result groups, close to thesis style | Three to five principal findings: principal findings → comparison → strengths and limitations → implications | Every objective, covering each result group | As the thesis, with deeper mechanism and alternative-explanation work |
| Analysis depth | Descriptive studies widely accepted | Multivariable adjustment and sensitivity analysis expected | Descriptive, comparative, and multivariable where appropriate | Multivariable models and sensitivity analysis |
| Literature comparison | Vietnamese and international studies | Mainly international, stressing what the study adds | Broad, domestic and international | Broad and critical |
| Strengths and limitations | Short subsection in Bàn luận | `Strengths and limitations` subsection | End of the Discussion chapter | End of the Discussion chapter, plus `Những đóng góp mới của luận án` |
| Submission package | Per the journal's author instructions | Reporting checklist, ethics, data availability, funding, conflicts, author contributions | — | — |

The protocol profile carries planning depth only: no results, no Discussion.

**Rule layer** (`rules`) — mandatory chapters, mandatory sections, and page limits, taken only from official documents and governed like the existing HMU profile (source URL, version, licence, last-verified date, checksum). When an official document cannot be retrieved, `rules` is `null` with a `rules_note` telling the author to consult the original. A missing rule layer never blocks a release or a draft.

The Research Passport's existing `document_type` field selects the profile by file stem, for example `thesis-master`. Projects created before 3.0 hold coarser values, which map without asking: `thesis` → `thesis-master`, `dissertation` → `dissertation-doctoral`, `protocol` → `protocol`, and `journal-article` or `manuscript` → `journal-article-vn` under the Vietnamese locale profile or `journal-article-intl` under the English one. The chosen profile is stated in one line, and the author can change it. An institution profile, such as HMU, layers its rules on top. Writing skills take depth and length from the profile and ask only when the author wants something different.

Because a thesis and an article now differ only by profile, converting a thesis into an article means switching profiles and reassembling from the same verified results.

## 6. Skill rewrites

- **`viet-ban-luan`:** the argument template becomes finding → meaning → contribution → comparison with the literature. Bias, confounding, chance and limitations leave the per-paragraph template and move into one strengths-and-limitations section, strengths first, placed by the document-type profile. Each limitation states how it was mitigated or why it does not overturn the finding.
- **`phan-tich-so-lieu`:** interpretation leads with clinical meaning and effect size, and uses a minimal clinically important difference when the author supplies one. P-values support interpretation rather than lead it. The rules against significance-driven model selection, outcome switching and post-hoc sample-size changes stay; they protect the author under review.
- **`viet-ket-luan-khuyen-nghi`:** conclusions state what the evidence supports, affirmatively, at its full strength.
- **`dao-duc-va-quan-tri-du-lieu`:** remove the evidence demand and the stop on overdue sources. The ethics section affirms how the study complied and protected participants, instead of listing risks defensively.

`viet-ket-qua` keeps its rule against interpretation. Results sections report; Discussion interprets. That is the convention of articles and theses alike.

## 7. Author style profile

MedRS learns the author's voice from the author's own writing and uses it both to draft and to rewrite.

**Input:** three to five documents the author wrote, preferably including Discussion sections. Below 8,000 words of source text the profile is still built and marked `LOW_CONFIDENCE`.

**Measured layer** — computed by `src/medical_research_skills_vn/style_profile.py` through `scripts/build_style_profile.py`:

- sentence and paragraph length distributions;
- preferred connectors and sentence openers, such as `Tuy nhiên`, `Bên cạnh đó`, `Như vậy`;
- person and voice: frequency of `chúng tôi` against passive constructions;
- number conventions: decimal comma or point, `p < 0,05` style, percentage format;
- citation placement within sentences, Vietnamese or English terms, abbreviation habits.

**Pattern layer** — extracted by the model, each pattern illustrated by a verbatim excerpt of at most 40 words from the author's own text: how the author opens a literature comparison, states a strength, states a limitation, and moves from a number to its clinical meaning.

**Storage:** `author-style-profile.json` beside the Research Passport in the author's project folder, validated by `schemas/author-style-profile.schema.json`. The Passport points to it. The profile never enters the repository or a release package. One profile per author, so an author who supervises or writes for several researchers keeps each voice separate.

**Use:**

1. Every writing skill drafts in the author's voice from the start.
2. `prose-rewriting.md` targets the profile and reports deviations concretely, for example "mean sentence 38 words; profile 24".

**Precedence:** the author profile overrides the Vietnamese and English composition guides. Numbers, citations, and claim strength follow §3 and are never changed for voice.

## 8. Zotero citations

### 8.1 Preservation through token round-trip

The model never touches Zotero field XML.

1. **Before an edit**, `tokenize` replaces each Zotero field in the paragraph with a stable token `⟦Z:n⟧`. The model sees and edits text only.
2. **After the edit**, `detokenize` restores the original field XML byte for byte at each token.
3. **Audit** compares the field inventory before and after the edit, identifying each field by its full concatenated instruction text, since older fields may lack a `citationID`. A single missing field is a blocking error, and the file is not delivered.

Recognised fields are complex fields whose instruction begins `ADDIN ZOTERO_ITEM CSL_CITATION` or `ADDIN ZOTERO_BIBL`. Word splits long instructions across several runs, so the extractor concatenates every `w:instrText` between `begin` and `separate` before matching. The audit also confirms that the `ZOTERO_PREF_*` custom document properties survive.

Preservation is pure XML handling and needs no library access. It therefore works on every host, including Cowork on the web.

### 8.2 Generation of live citations

When drafting, the model writes `⟦cite:ITEMKEY⟧`, or `⟦cite:KEY1;KEY2⟧` for several items. `insert` resolves each key read-only against the author's Zotero library and emits a live `ADDIN ZOTERO_ITEM CSL_CITATION` field holding the item URI, minimal CSL item data, and placeholder display text. The author opens the document in Word and clicks **Zotero → Refresh**; Zotero renders every citation in the chosen style and rebuilds the bibliography. MedRS points at the right items; Zotero does the formatting.

Item URIs take one of three forms, to be confirmed against a real Zotero-produced field before release:

- synced personal library: `http://zotero.org/users/<userID>/items/<itemKey>`;
- unsynced local library: `http://zotero.org/users/local/<localUserKey>/items/<itemKey>`;
- group library: `http://zotero.org/groups/<groupID>/items/<itemKey>`.

When no library is readable, as on Cowork, or a key does not resolve, the draft carries `[CẦN TRÍCH DẪN: Nguyễn 2020]` and the closing checklist lists it. MedRS never emits a field it could not resolve.

| Host | Preserve existing fields | Generate new fields |
|---|---|---|
| Claude Code or Codex on the author's machine | Yes | Yes, reads `zotero.sqlite` |
| Cowork on the web | Yes | No library access; slot plus checklist item |

### 8.3 Code and contract

- `src/medical_research_skills_vn/zotero_fields.py` provides `extract`, `tokenize`, `detokenize`, `insert`, and `audit`.
- `skills/quan-ly-trich-dan/references/zotero-field-contract.md` states the token formats, the audit rule, and host behaviour. `quan-ly-trich-dan` gains an insert mode.
- Every skill that writes or edits manuscript text links the contract exactly once, enforced by `structure.py`: the seven `viet-*` section writers, `viet-ban-thao-y-hoc`, `kiem-van-phong`, `phan-bien-va-chinh-sua`, `tu-phan-bien`, and `bo-cuc-tai-lieu`.
- The library read-only invariant stays. MedRS writes to the manuscript, never to the Zotero library.

## 9. Migration from 2.0.0-alpha.8

- **PowerShell install:** the installer retires `kiem-chung-ban-thao` through its manifest; `legacy-skill-map.yaml` routes the old name to `tu-phan-bien`.
- **Cowork:** uploading the new ZIP is enough, because it contains only the 27 skills.
- **Existing projects:** the Research Passport schema is unchanged, so projects in progress open as before. Drafts that still carry inline status codes keep working; new output uses the closing checklist.

## 10. Testing and acceptance

- The 179 existing tests and six end-to-end exemplars pass after updating for the merge.
- New automated tests:
  - every skill links `working-principles.md` exactly once;
  - every manuscript-editing skill links `zotero-field-contract.md` exactly once;
  - all six document-type profiles validate, and a profile with `rules: null` validates;
  - Zotero round-trip preserves field XML byte for byte, including an instruction split across three runs;
  - a deleted token makes the audit fail;
  - a generated field parses back to the requested item URI;
  - `ZOTERO_PREF_*` properties survive an edit;
  - the style extractor reproduces known statistics on a fixture text;
  - routing sends pre-submission requests to `tu-phan-bien`.
- New end-to-end exemplar: a Discussion places its limitations in one section rather than in every argument paragraph.
- **Human acceptance:** run `3.0.0-rc.1` on one anonymised real chapter and compare it with 2.0.0-alpha.8 output. Only a reader can judge flexibility, strength-led framing, and voice.

## 11. Implementation order

Each step runs and passes its tests on its own. Restructuring comes first so later edits land on the final layout.

1. Merge `kiem-chung-ban-thao` into `tu-phan-bien`.
2. Add `working-principles.md` and link it from all 27 skills.
3. Add the six document-type profiles and wire depth and length into the writing skills.
4. Rewrite the four skills in §6 and all 27 descriptions.
5. Build the author style profile.
6. Build Zotero preservation and generation.
7. Retrieve official rule layers; ship `rules: null` where a source is unavailable.
8. Release `3.0.0-rc.1`: sync the version, update the changelog and README, package, push.

## 12. Non-goals

- Optimising text against AI detectors, scoring human-likeness, or inferring authorship.
- Writing to the Zotero library.
- Hard-coding individual international journals; their author instructions are read at the time of use.
- New Research Passport states.
- EndNote or Mendeley field support.

## 13. Inputs needed during implementation

| Input | Needed for | From |
|---|---|---|
| One DOCX with Zotero citations inserted through the Word plugin | Test fixture; confirming URI forms (§8.2) | Author; only field XML structure is used |
| Three to five documents the author wrote | Author style profile (§7) | Author |
| One anonymised real chapter | Human acceptance (§10) | Author |
| Official doctoral-dissertation and specialist-thesis regulations | Rule layers (§5) | Retrieved publicly first; author supplies if not public |
| Author instructions of the Vietnamese journals the author targets | Rule layer of `journal-article-vn` | Retrieved publicly; default candidates are Tạp chí Nghiên cứu Y học and Tạp chí Y học Việt Nam |
