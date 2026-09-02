# Adopt an existing project

Use this mode when the researcher already has a proposal, thesis, dissertation, or manuscript draft.

1. Preserve the source file; extraction is read-only.
2. Extract headings, paragraphs, tables, and source-citation candidates with artifact and paragraph/line provenance.
3. Create candidates for title, research question, objectives, study design, population, setting, variables, exposure/intervention, comparator, outcomes, and source ledger.
4. Mark candidates `DRAFT_INFERRED`; confidence describes extraction strength, not scientific truth.
5. Keep ethics approval, verified results, and institutional rules unresolved unless the author supplies verifiable evidence.
6. Group conflicts and ask one author-confirmation question at a time. Do not ask the author to type an unambiguous extracted value again; show it for confirmation or correction.
7. Append confirmation and correction events without deleting the original provenance.

Supported deterministic formats in slice 1 are DOCX, Markdown, and plain text. Unsupported or encrypted artifacts receive `HOST_CAPABILITY_UNAVAILABLE` or `AUTHOR_APPROVAL_REQUIRED` rather than fabricated extraction.

