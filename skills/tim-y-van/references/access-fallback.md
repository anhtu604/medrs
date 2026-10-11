# Access fallback and honest search ceilings

Caller: tim-y-van for any failed, partial or abstract-only search; also
tong-hop-bang-chung before extraction. Helpers: ../scripts/access_policy.py
and ../scripts/record_identity.py (portable, without repository src).

Probe the actual execution surface: a Windows desktop is not evidence that
a Cowork VM can access PubMed or execute local tools. Record provider, exact
query, timezone-aware time, HTTP status, access level, hit count and error.
Keep the raw response separately with checksum, endpoint and filters.
Never fabricate a completed search record for an unsuccessful request.

Use access_state or access_summary on a set of attempts for the same search
scope. UNPERFORMED means no attempts. SEARCHED_NO_HITS requires a successful
query with a real zero count and no unresolved provider in that scope.
INACCESSIBLE is not evidence that literature does not exist. Partial success
retains failed attempts and does not prove exhaustive coverage. METADATA_ONLY,
ABSTRACT_ONLY and FULL_TEXT describe reported access, not verified content,
quality or successful appraisal. A DOI landing page alone is metadata,
not full text. Local receipts do not certify remote capabilities forever.

After a 401/403, unavailable connector or rate limit, report the limitation
and try a relevant lawful alternative: Europe PMC, OpenAlex, publisher open
access, authorized institutional library access, or an author-supplied PDF.
Respect service retry guidance for 429; do not rotate identities or evade
access controls. Do not paste credentials into logs. Never send identifiable
patient data as search text. A fixed Vietnamese-source quota is not an
inclusion criterion: use VJOL and journal/institution repositories when
relevant and retain their source, publication identity and access ceiling.

Deduplication normalizes DOI prefixes/URLs, title Unicode and punctuation,
then year. It retains discovery routes and publication-status history.
Title/year matching is a candidate merge, not proof that two different
reports or translations are the same study. Distinct DOI reports from one
study require study-level reconciliation, not DOI deletion. Unnamed records
must not collapse into one. Retraction/correction checks require source and
date; newer dated checks replace earlier ones, while same-date disagreements
remain unresolved. Absence of a known flag does not establish that a paper
is unretracted. Verify linked notices before treating findings as evidence.

Record seeds, expansion rounds, typed directed edges, retrieval source,
request evidence and stopping rule for citation chasing. Citation count,
node size and proximity are discovery aids, never risk-of-bias or certainty
ratings. Backward/forward discovery is not a systematic search by itself.
Keep correction, update and retraction relations distinct from citations.

Before extraction call extraction_receipt(record, attempts) with attempts
for THAT original source, not all records from a search. It calls the shared
statistics identity validator and retains source locator and access ceiling.
Identity errors block a verified estimate. Even zero errors only prove
metadata consistency; inspect original table, row/column/footnotes, numerical
values, time, outcome, group, adjustment and outcome-available N. A recruitment
total cannot fill an unavailable outcome denominator. Abstract-only sources
cannot support unseen methods, detailed bias appraisal or invented estimates.
Secondary tables remain pointers until the original comparison is recorded.
