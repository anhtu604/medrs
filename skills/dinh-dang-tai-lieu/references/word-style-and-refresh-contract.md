# Word style and refresh contract

Load this reference whenever the task creates, repairs, or validates a DOCX. If the host supplies a native DOCX/Word artifact skill, use it together with this contract. The institution or journal profile remains authoritative for dimensions and typography; the rules below define how MedRS implements those requirements without accumulating direct-formatting drift.

## Styles are the source of truth

Never format every occurrence of a heading, body paragraph, caption, list item, TOC entry, or table cell independently. Define or repair a named paragraph style, then assign that style to every member of the semantic class. Clear conflicting direct font name, font size, paragraph spacing, line spacing, tab, and indentation properties after confirming that bold, italic, superscript, subscript, language, and tracked revisions carry meaning and must be preserved.

At minimum, the package must contain and validate: `Normal`, `Body Text`, `Heading 1` through `Heading 4`, `TOC Heading`, `TOC 1` through `TOC 4`, `Table of Figures`, `Caption`, `Bibliography`, `List Paragraph`, and `MedRS Table Text`. The built-in names matter because Word regenerates field results with those styles. A visually correct current TOC is not sufficient if its underlying `TOC 1`–`TOC 4` styles are wrong.

Each style contract records font family for ASCII, high ANSI, East Asian, and complex-script slots; size; line spacing; spacing before and after; indentation; keep-with-next; and whether the style appears in the Quick Style gallery. Heading styles must use keep-with-next. Body, TOC, list-of-figures/tables, and bibliography styles normally inherit the profile's body line spacing. Table text and captions may use a profile-authorized compact spacing. Do not invent a journal or institution rule: label MedRS layout defaults separately from sourced requirements.

## Refresh-safe fields

Create real field codes, not typed page numbers or a pasted table of contents. Set `w:updateFields` in `word/settings.xml`, and use the appropriate built-in result styles:

- `TOC \\o "1-4" \\h \\z \\u` for a four-level table of contents, or the profile's declared depth.
- `TOC Heading` for the table-of-contents heading and `TOC 1`–`TOC 4` for generated entries.
- `Table of Figures` for generated lists of tables, figures, charts, or diagrams.
- `Caption` for source captions; preserve the required placement and chapter-linked numbering.
- `Bibliography` for a generated bibliography when Word's bibliography field is used. A manually managed reference list must have its own named profile style rather than direct formatting.

After Word or LibreOffice refreshes fields, reopen the refreshed DOCX and revalidate style definitions and assignments. Field presence does not prove that page numbers were recalculated. A successful conversion process does not prove correct typography. Inspect the refreshed TOC and lists for font family, font size, line spacing, hanging indents, tab leaders, page-number alignment, and unexpected direct formatting. Render all pages and visually inspect them before claiming pagination or layout success.

## Content-weighted tables

Do not assign equal widths by default. Compute a content demand score for each column from the maximum and typical text lengths, then allocate the usable page width proportionally with lower and upper bounds. A robust default is 8% minimum and 65% maximum per column. Compact identifier, ordinal, yes/no, and short numeric columns; give more width to descriptions, definitions, outcomes, and notes. Apply widths to both `tblGrid` and each cell's `tcW`, and use fixed layout after calculation so Word does not silently redistribute the grid.

Treat the algorithm as a starting point, not a semantic oracle. Recheck tables with merged cells, nested tables, rotated headers, wide confidence intervals, long unbreakable tokens, or landscape sections. Keep units and their values together where possible. Never shrink below readable typography merely to keep a table on one page. If a table remains crowded, prefer landscape orientation, a deliberate split, or an appendix after author approval.

Every cell paragraph uses `MedRS Table Text`; header rows may add bold emphasis without changing the base paragraph style. Remove fixed row heights that clip wrapped text. Repeat header rows only when supported and verify the repeat in rendered pages. Check cell margins, vertical alignment, orphan units, border consistency, and whether the table stays within the section's text width.

## Deterministic bullets and numbered lists

Use OOXML numbering definitions, never literal bullet characters plus spaces. MedRS bullet lists use one named multilevel abstract numbering definition and one numbering instance for a contiguous list. Each level defines its bullet glyph, tab stop, left indent, and hanging indent. A stable baseline is 720 twips left at level 1, a 540-twip increment per nested level, and a 360-twip hanging indent. Paragraphs use `List Paragraph`; direct paragraph indentation and tabs are removed so numbering controls alignment.

Detect existing automatic bullets by their numbering definition, not only by English style names. Preserve true numbered/ordered lists and heading numbering; do not convert them to bullets. Confirm that wrapped lines align with the text after the bullet, nested levels are visibly distinct, list continuation versus restart is intentional, and copy/paste did not create multiple conflicting numbering definitions.

## Required post-format QA

The mechanical report must separately state whether these checks passed: required style definitions, style assignment, direct-formatting drift, `updateFields`, TOC field, TOC result styles, table-of-figures style, bibliography style, margins, section/page numbering, adaptive table grids, table text style, numbering definition, list paragraph assignment, and hanging indents. A failed or unavailable item remains `FAIL`, `UNPERFORMED`, `HOST_CAPABILITY_UNAVAILABLE`, or `AUTHOR_APPROVAL_REQUIRED`; it must not be collapsed into a generic pass.

The visual report checks every rendered page for hierarchy consistency, TOC/list refresh typography, line and page breaks, widows/orphans, bullets, tables, captions, headers/footers, page-number transitions, blank pages, and clipped or overflowed content. Compare the refreshed DOCX—not the pre-refresh input—against the active source profile.
