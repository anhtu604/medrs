# Revision and final acceptance

For author-returned or external-AI revisions use [../scripts/external_revision.py](../scripts/external_revision.py) and [../../../schemas/external-handoff.schema.json](../../../schemas/external-handoff.schema.json). Prepare a local, source-hash-bound prompt/manifest for selected fields, destination, data class and confirmed scope. It does not send anything. Compare the returned file with the last delivered hash before another round. Protected-field/footnote/comment loss prevents acceptance; numerical, study-design and scope changes require semantic review even when mechanical checks pass. `REVIEW_REQUIRED` is not acceptance. Use its event recorder for the dated project log without copying manuscript text into that log.

## Effective work order

If data are replaced, apply the [data-provenance contract](../../ho-so-nghien-cuu/references/data-provenance.md): reuse author confirmation, receive the replacement, archive prior simulation lineage and propagate current label/results changes. Author declaration alone is not an independent verification receipt. Notify the author to recheck; unresolved provenance or partial replacement prevents unconditional final claims, not independent conditional drafting.

At the start of a substantive round, inspect the author's designated input and its comments, headings, live citations, tracked revisions and modified time. Record the source path/hash, work-order revision, all requested items, owners, expected tables/figures, output destination and protected regions. An explicitly replaced assignment is superseded; unrelated additions remain active. An ambiguous source/comment mismatch warrants one bounded clarification. Continue independent items while it is pending.

Author edits and decisions persist. Store terminology with its scope and allowed exceptions, codebook labels, clinical definitions, typography, punctuation, decimal/p display, table layout, removed notes/sections, and arguments/sources to retain. Apply the latest confirmed decision across every dependent item; do not resurrect removed material when rerunning a script. Institutional requirements and author exceptions must have their provenance recorded. Do not treat the ROP project's 13 pt, LPR project's 14 pt, personal vocabulary, or number of references as universal defaults.

An instruction to shorten does not authorize new tables, tests, models or appendices. Flag a necessary missing analysis and route it to the analysis plan; do not manufacture p values during layout. Statistical method choice is justified by the research question and design, never by a preferred p value. Do not force both R and Stata for every project: run and verify the backend(s) actually requested, and reconcile them if cross-validation was commissioned.

## Version and writer ownership

Create a new output for every round; refuse source overwrite and refuse an already existing output. Capture source hash and mtime before work and verify both before commit. If the author edits during work, do not commit a stale revision: rebase scoped edits onto the newly designated source or report the conflict. A lease uses exclusive file creation for one writer. Never auto-delete another writer's lease; diagnose stale leases before a human-authorized release. Keep Word's owner-lock file and the author’s open original out of the write path.

Never accept/reject revisions, delete comments or change revision authors without explicit instruction. For changes that Word cannot track (chart labels, embedded workbook, style/field updates), record exact objects and before/after in a separate change ledger. Hash protected sections/parts and compare after edits. Source preservation alone does not prove all out-of-scope content survived in the new file.

## Dependencies and propagation

Each changed object has a stable ID, independent of its display number. A table split, removal or renumbering affects the title, row/column labels, its own observations, footnotes, symbols, chart data, all textual mentions, cross-reference fields, TOC/list entries and appendices. A changed result affects abstract, Results, Discussion, conclusions, recommendations and response letter. A terminology change also affects table cells, captions, chart labels and abbreviation lists.

After repairing one instance, search analogous instances in the authorized scope. Record those checked and any outside-scope defect. Every reviewer comment retains its verbatim text, original anchor/source, action, exact changed locator and after-save verification. Match by content and anchor as well as comment ID because IDs can move.

## Content acceptance

The leader reads the final content rather than repeating worker verdicts. Require objective coverage, clinically complete Methods, matching definitions/design across chapters, claim-to-cell identity (variable, indicator, denominator, group, time/pair, test, adjustment), numerical validity, relevant source support, preserved valuable arguments and recommendations grounded in Results/Discussion. Check the direction of a proposed explanation; a baseline difference does not establish the cause of a final difference.

Review clear prose separately: each sentence supplies a concrete finding, explanation, comparison or useful implication. Remove filler and repeated caveats while keeping necessary qualification at the claim. A basic project should be intelligible to its clinical readers. Avoid ornate terminology and technical operational codes. Source or result gaps can remain in a draft as short placeholders; they cannot be silently counted as final content passes.

Scan body paragraphs, tables, footnotes, headers, captions and chart/embedded-data labels for workflow language. Project-specific banned terms use the project dictionary and exceptions. Never delete a clinically valid abbreviation automatically because it appeared on another project's banned list.

## Presentation acceptance after the final save

Open the saved DOCX; check package integrity, live Zotero/REF fields, bookmarks, comments/revision preservation and reference metadata. Refresh through an available actual Word/UNO backend, save, reopen and audit style definitions plus direct overrides. Render the exact refreshed artifact and inspect all affected pages; for final assembly inspect every page, cover, chapter transition, table, bibliography and appendix. Check numbering, blank pages, caption/header placement, table width/row wrapping, bullets, font/spacing, abbreviation list and TOC/list-of-tables/figures.

Bind backend logs, mechanical/semantic findings, PDF/page images and the human/agent visual report to the final DOCX hash. A PDF existing is evidence of rendering, not evidence that it was inspected or that fields were updated. Evidence hashes are rechecked at acceptance. A subsequent edit or Zotero refresh invalidates the old receipt. Track what was actually performed; an unavailable check is UNPERFORMED, never PASS.

## Verdicts and delivery

When defects coexist, primary verdict priority is: stale final-hash evidence → RE_REVIEW_REQUIRED; known failed content/task/source/propagation checks → NEEDS_REVISION; missing evidence → VERIFICATION_INCOMPLETE; only a complete passing set → ACCEPTED_INTERNAL. Preserve separate content and presentation verdicts so a stale review and an unavailable renderer remain visible together. A numerical contradiction blocks acceptance, not independent draft delivery. Do not clip an invalid CI or invent a correct result to satisfy a deadline.

Filename collisions are routine: select the next vacant version in the intended output directory and record it; ask only if destination ownership or intended source is genuinely unclear. Implement requested comment edits while retaining their objects/anchors; deleting comments is a separate authorized action. A compact user message names the artifact, changes, verification state and gaps; the detailed receipt carries technical evidence and hashes.

Use NEEDS_REVISION for known failed checks, VERIFICATION_INCOMPLETE for missing evidence, RE_REVIEW_REQUIRED after hash changes, and ACCEPTED_INTERNAL only for a complete content-plus-presentation pass. Record author_acceptance separately as PENDING, ACCEPTED or CHANGES_REQUESTED; an agent must not infer author acceptance from internal checks. Drafts may be delivered promptly with their actual verification state. One closing checklist reports unresolved matters without polluting the manuscript with workflow text.
