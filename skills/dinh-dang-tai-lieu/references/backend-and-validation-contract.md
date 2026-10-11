# Backend and generated-artifact contract

Choose the strongest backend actually available on the execution surface. Word COM belongs to a Windows Python process with `win32com`; it is not available merely because the user's computer runs Windows when the agent executes inside Linux. LibreOffice UNO requires a callable office executable and the UNO bridge. OOXML-only can change and inspect package mechanics but cannot calculate page layout, update a table of contents reliably, or prove visual pagination.

Every transformation has distinct source and output paths. Record source hash, output hash, profile/version, backend probe, requested operations and actual changes. Preserve comments, tracked revisions, relationships, embedded parts and unknown XML unless the approved operation explicitly replaces them. On backend failure, close documents/processes in `finally`, retain the source, and report the partial output as failed rather than passing it.

Validation reopens the generated DOCX. Mechanical checks include style definitions and assignment, margins/page size, section properties, field codes, page-number restart declarations, caption placement and numbering declarations. Render checks require a generated PDF plus page images. Field presence is not field update; a conversion command returning zero is not proof of correct pagination. Unsupported checks remain `HOST_CAPABILITY_UNAVAILABLE` or `AUTHOR_APPROVAL_REQUIRED`.

The final report separates `PASS`, `FAIL`, `UNPERFORMED`, and `AUTHOR_APPROVAL_REQUIRED`. A mechanical pass never upgrades an unperformed visual check. The author must review line/page breaks, orphan headings, clipped tables, figure resolution, TOC page numbers and institution-specific visual details before a submission-ready claim.

Use ../scripts/refresh_uno.py only with actual UNO Python and an available
LibreOffice executable. It disables macros (NEVER_EXECUTE=0) and external
link updates, rejects external update fields, uses a short isolated native
profile on Windows, updates document indexes and reopens the saved DOCX to
inspect persisted index content before exporting PDF. Retain its run log
and native-profile path. Its status is REFRESHED_REVIEW_REQUIRED, never PASS:
post-refresh style checks, protected-field/part fidelity and visual review
are separate. If conversion rewrites protected structures or strips style
definitions, retain both files and fail/defer the affected checks; do not
weaken comparison to make the renderer seem accepted.

Primary API references, verified 2026-10-11:
https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XDocumentIndexesSupplier.html
https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1text_1_1DocumentIndex.html
https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1document_1_1MacroExecMode.html
https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1document_1_1UpdateDocMode.html
