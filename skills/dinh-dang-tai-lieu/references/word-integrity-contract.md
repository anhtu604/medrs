# Word integrity through revision and refresh

Read before formatting an existing draft, accepting a file returned by another editor/AI, or approving a final Word deliverable. Apply this together with the Zotero field contract, not in place of it.

## What the actual file must retain

Fields are XML objects, not their visible numbers. Preserve complex-field boundaries and instruction fragments, simple fields, relationships, bookmarks, footnote/endnote targets and comment IDs/anchors. Replacing `paragraph.text` or a whole run can discard these objects even when displayed prose seems unchanged. Move complete XML nodes for authorized restructuring; maintain schema child order. Positional text offsets are unstable after edits: identify comments by ID, surrounding content and anchors, and confirm the intended passage after a move.

Use [../scripts/docx_integrity.py](../scripts/docx_integrity.py) to inspect saved packages. `audit_docx_integrity(path)` returns structural issues and protected fingerprints. It is read-only, rejects malformed/unsafe XML and missing targets, checks field boundaries across each part, and preserves duplicate-object multiplicity in fingerprints. It does not prove full XSD compliance, visual appearance or the semantic position of an anchor. A changed fingerprint calls for scope-aware comparison: adding a legitimate PAGE/TOC field is different from losing a Zotero citation. It must not simply be waived because the number of fields is unchanged.

## Styles, not repeated local formatting

The canonical runtime is [../scripts/medrs_word_runtime/docx_formatting.py](../scripts/medrs_word_runtime/docx_formatting.py); actual-file validation is [../scripts/medrs_word_runtime/docx_validation.py](../scripts/medrs_word_runtime/docx_validation.py). These ship in Cowork and do not import repository-only `src/`. Third-party Python libraries are still required and capability-probed; portable code does not make unavailable libraries available.

Manage Normal/Body Text/headings, Caption, table text, bibliography, generated TOC/table-of-figures and list styles. Explicit style fonts remove conflicting same-element theme selectors. For ordinary managed paragraphs remove spacing/font overrides that defeat the selected style, while retaining intended bold/italic/emphasis. Field-bearing runs are protected; normalize generated field-result appearance after refresh only through a scope-aware backend. Do not assume docDefaults determine body text if Normal or a paragraph style overrides them.

For cover pages and nonstandard paragraph roles, require a role mapping/profile rather than applying body line spacing to every paragraph. Empty Heading paragraphs containing pictures and body text mistakenly assigned a Heading are reported for semantic review, not silently deleted or retagged from a heuristic. Style gallery presence is not proof that paragraphs use those styles.

Font precedence reference: Microsoft [MS-OI29500 §17.3.2.26](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oi29500/aef3c9a6-5d6c-434b-90b7-85e761fd8e62), last-updated 2023-03-09, checked 2026-10-11, Microsoft documentation terms. Same-element attributes and style-hierarchy precedence differ; inspect both instead of searching only for a font-name string.

## Tables and lists

Set both table grid and cell widths, account for merged cells and actual available page width. Content demand is a bounded layout heuristic; long text columns should normally receive more space than row numbers, but many narrow columns must still have positive widths and sum to the usable total. Recheck wrapped headers and captions after rendering. A schema-valid table can still be unreadable. Border choices follow the actual institution/journal profile; never impose no-vertical-lines on every thesis.

Use numbering definitions for automatic bullets, with level-specific tab/hanging indent and correct XML property order. Preserve author-selected nesting and non-bullet numbering. Direct paragraph indents must not override numbering levels. Custom configured indents should be validated against the profile rather than one hard-coded value.

## Refresh, render, inspect, then accept

Save → refresh fields/indexes through a genuinely available backend → save again → reopen → inspect the changed actual file → render PDF/page images → visually review. Conversion alone does not establish that all indexes/fields were updated. Word COM may be reached through PowerShell even without Python's win32com; test that bridge instead of equating those capabilities. LibreOffice existence does not prove UNO Python bindings or index-update success.

Use hash-bound evidence for the refreshed document and rendered outputs. Any subsequent edit invalidates affected evidence. Where a renderer/field backend is unavailable, keep conditional drafting possible and return unperformed checks; do not claim content and form jointly accepted. Preserve pre/post-refresh packages to detect footnote, citation or comment loss by a backend.
