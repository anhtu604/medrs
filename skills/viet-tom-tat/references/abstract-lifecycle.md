# Abstract lifecycle

Allowed states are `SKELETON`, `DRAFT_FROM_INCOMPLETE_MANUSCRIPT`, `SYNCED_DRAFT`, and `FINAL_VERIFIED`. Only `FINAL_VERIFIED` is submission-ready. Store the source manuscript hash/version and generation time. A change to objective, Methods, sample, outcome, estimate, conclusion, title, or keywords invalidates a synced/final abstract.

Every number records its full-text and analysis-artifact locator. A conflict becomes `BLOCKED_CONFLICT` with both values and locations; do not choose the more attractive value. Distinguish screened, enrolled, allocated, followed, and analyzed counts. Rounding follows a declared rule only after underlying values agree.

Priority words such as first, novel, unprecedented, or only require a dated novelty search with sources/databases, terms, cutoff, scope, candidate precedents, and freshness. An inaccessible full text or empty result does not prove priority. Otherwise omit the claim or emit `[CẦN XÁC MINH TÍNH MỚI]` / `[NOVELTY VERIFICATION REQUIRED]`.

