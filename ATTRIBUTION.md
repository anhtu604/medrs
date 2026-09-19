# Attribution and license audit

| Source | Snapshot | License | Integration status |
|---|---|---|---|
| `medical-research-skills-vn` 1.3.0 | SHA-256 `C3AD0C20385BD8B7AEE0C93FEE4303F3CF4499E586C06978CF4689E4443F6231` | CC BY-NC 4.0 | Architecture and Vietnam-specific workflow lineage; rollback archive retained locally and not redistributed |
| `academic-research-skills` | `5debcd2efb686dce0205ba9094b6413dae5f89c0` | CC BY-NC 4.0 | Human checkpoints, source ledger, consistency and integrity concepts adapted |
| `scientific-agent-skills` | `895b4be37ef0ca1cd55c6e628e7ff937ba5a1cf1` | Root MIT; child licenses vary | No child file may be reused until entered in the per-file audit below |
| `obra/the-elements-of-style` | commit `05fc4f0d2b97b7c042dd9949ad658568e4a1324e`; verified 2026-08-31 | Strunk 1918 text is public domain; repository identifies Project Gutenberg #37134 | Independently adapted composition principles in `composition-en.md`; no source prose copied |
| Wikipedia “Signs of AI writing” | revision `1372013638`, 2026-08-29; verified 2026-08-31 | CC BY-SA for copied/adapted expression | Categories and caveats adapted in `formulaic-writing-audit.md`; no examples copied and no detector evasion |
| `codelabr/easy-map` installer | `main` inspected 2026-09-02 | MIT, copyright Nguyen Tuan Anh (2026) | Web-bootstrap/local-installer separation, temporary-download cleanup and multi-target installation pattern adapted; medical plugin adds staging, manifests, rollback, shared resources and checksum pinning |
| `dougwyu/claude-zotero-skills` | `main` inspected 2026-09-19 | Apache 2.0 | Read-only reference-library invariants, runtime field resolution, trash exclusion and the four-verdict citation-faithfulness taxonomy independently rewritten in `quan-ly-trich-dan`; no source prose, SQL or code copied |
| `Galaxy-Dawn/claude-scholar` | `main` inspected 2026-09-19 | MIT | Pre-plot evidence contract and publication QA concepts independently rewritten and re-scoped to R/Stata medical figures in `bieu-do-cong-bo`; no source prose or code copied, and the upstream Python figure toolchain is not adopted |
| `joshzyj/open-scholar-skill` | `main` inspected 2026-09-19 | No license file; rights reserved by default | Excluded. Nothing consulted for reuse and nothing derived from it |

## Per-file upstream audit

No upstream file has been copied verbatim. New entries must record source path, commit, license, destination, and whether content is copied, adapted, or independently implemented.

## Primary instruments consulted in Slice 1

Operational summaries are independently written and bounded by the exact scope in each source register.

| Source | Version verified | Rights note | Local use |
|---|---|---|---|
| Vietnam Ministry of Health, Circular 43/2024/TT-BYT | Effective 2025-02-01; checked 2026-08-31 | Official legal text; redistribution status not asserted | Routing metadata and approval-form identifiers only |
| WMA Declaration of Helsinki | 2024 revision; checked 2026-08-31 | Copyright WMA, all rights reserved | Non-verbatim operational routing across paragraphs 1–37 |
| ICH E6(R3) | Step 4, 2025-01-06; corrections 2025-10-24 | ICH permits reuse/adaptation with acknowledgment and change labelling; third-party content excluded | Explicit routing subset, not a full compliance instrument |
| HMU “Yêu cầu đối với luận văn”, linked by the official 2026 process page | DOCX SHA-256 `6FAFDBB41FD09AE6D506661D2F7D9C0AC02B6B7DE6A3FF9A147CD551C125054F`; checked 2026-08-31 | Official institutional document; redistribution permission unknown | Executable semantic structure profile with paragraph provenance; binary excluded from redistributed package |
| NCBI E-utilities ELink documentation | current online documentation; checked 2026-09-02 | US Government/NCBI documentation terms; no text redistributed | Independently implemented linked-record provenance contract |
| PMC Open Access Subset terms | page modified 2026-08-24; checked 2026-09-02 | Article-level licenses vary; automated retrieval restricted to named PMC services | Lawful-access and reuse boundary only |
| Crossref REST API relation filters | current online documentation; checked 2026-09-02 | Documentation consulted; no source prose copied | Correction/retraction relation metadata model |
| Cochrane RoB 2 tool for individually randomized parallel-group trials | 22 August 2019; checked 2026-09-02 | CC BY-NC-ND 4.0 | Exact 22-question identifier coverage and independently written operational summaries; official wording/algorithm not redistributed |
| Cochrane Handbook Chapter 14 (GRADE) | Version 6.5.1, May 2025; checked 2026-09-02 | Cochrane rights apply | Outcome-specific five-domain certainty contract and three upgrading considerations |
| GRADE-CERQual official guidance | 2018 guidance set; checked 2026-09-02 | Official site states all rights reserved | Finding-specific four-component operational contract; worksheets not redistributed |
| CONSORT 2025 statement | BMJ 2025;389:e081123; retrieved 2026-09-19; supersedes CONSORT 2010 | CC BY 4.0 | Exact 42-identifier coverage with item wording reproduced under the licence and attributed in `coverage/consort-2025.yaml` |
| STROBE statement | PLoS Med 2007;4(10):e296; retrieved 2026-09-19 | CC BY | Exact 34-identifier coverage with item wording reproduced under the licence and attributed in `coverage/strobe-2007.yaml` |
| PRISMA 2020 statement | BMJ 2021;372:n71; retrieved 2026-09-19 | CC BY 4.0 | Exact 42-identifier coverage with item wording reproduced under the licence and attributed in `coverage/prisma-2020.yaml` |
| TRIPOD+AI statement | BMJ 2024;385:e078378; retrieved 2026-09-19; supersedes TRIPOD 2015 | CC BY 4.0 | Exact 52-identifier coverage with item wording reproduced under the licence and attributed in `coverage/tripod-ai-2024.yaml` |
| SPIRIT 2025 statement | BMJ 2025;389:e081660; retrieved 2026-09-19; supersedes SPIRIT 2013 | CC BY 4.0 | Exact 53-identifier coverage with item wording reproduced under the licence and attributed in `coverage/spirit-2025.yaml` |
| STARD 2015 statement | BMJ 2015;351:h5527; retrieved 2026-09-19 | CC BY 4.0 | Exact 34-identifier coverage with item wording reproduced under the licence and attributed in `coverage/stard-2015.yaml` |
| CARE statement | BMJ Case Reports 2013;2013:bcr-2013-201554; retrieved 2026-09-19 | CC BY-NC-ND 3.0 | No-derivatives term respected: `coverage/care-2013.yaml` encodes the 13 identifiers and item names with independently written operational prompts; official wording not reproduced |
| COREQ | Int J Qual Health Care 2007;19(6):349-57; checked 2026-09-19 | Closed access, copyright Oxford University Press | Original unavailable and not redistributed. Identifiers, three domains and topic grouping retrieved from the EQUATOR-hosted validated Portuguese translation (Acta Paul Enferm 2021;34:eAPE02631); operational prompts in `coverage/coreq-2007.yaml` are independently written |
| PRISMA-P 2015 statement | Syst Rev 2015;4:1; retrieved 2026-09-19 | CC BY 4.0 | Exact 26-identifier coverage with item wording reproduced under the licence and attributed in `coverage/prisma-p-2015.yaml` |
| CHEERS 2022 statement | BMC Med 2022;20:23 co-publication; retrieved 2026-09-19; supersedes CHEERS 2013 | CC BY 4.0 | Exact 28-identifier coverage with item wording reproduced under the licence and attributed in `coverage/cheers-2022.yaml` |
| ARRIVE 2.0 guidelines | PLoS Biol 2020;18(7):e3000410; retrieved 2026-09-19; supersedes ARRIVE 2010 | CC0 public domain dedication | Exact 21-identifier coverage in `coverage/arrive-2-0.yaml`; attribution retained as good practice although CC0 does not require it |

This distribution is CC BY-NC 4.0. Commercial or for-profit use, including some hospital, institute, consultancy, or sponsored settings, may require permission and legal review.
