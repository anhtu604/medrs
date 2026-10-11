# Shared gate lifecycle

Read when writing, assembling, revising or accepting a medical document. The canonical scope selector is `../scripts/gate_lifecycle.py::required_gate_scope`; scope selection is not an audit result. Writers, manuscript assembler and leader are explicit callers. All writers use the same preflight in `../../viet-phuong-phap/references/writing-preflight.md`; never copy its rules into seven entrypoints.

## Scope and reuse

- `standalone`: full four-pass audit of each named delivered section before handoff.
- `assembled`: preflight each section, then exactly one full four-pass audit of the assembled document; not seven full audits. Check transitions, objectives, denominators, terminology, contradictions and references across sections.
- `revision`: local four-pass audit of all changed or dependency-invalidated sections, plus whole-document consistency. Empty scope fails; unknown impact requires an assembled audit rather than guessing that nothing changed.

Passes 3/4 may read only affected prose in a revision. Passes 1/2 still inspect every affected claim and its dependencies. A source, result, locale, design or target-rule change expands scope; changed sections are not just those physically edited. Record document/section hashes, source ledger version, locale version, checklist versions, run status and unresolved markers. Unchanged evidence may be reused only if its dependencies remain valid. Any later edit invalidates the affected receipt. A cache is not blanket approval of a new file.

## Scientific ceiling and conditional drafts

Load `../../phan-tich-so-lieu/references/basic-statistics-contract.md` when interpreting results, and inherit the run's qualifications. Separate source verification, execution verification and author-declared data status. A simulated example is not a research finding; an author declaration is not independent verification. Conditional writing may proceed with explicit placeholders and qualified language, but unsupported causal or confirmatory statements must be revised, not made fluent. Do not claim an audit was executed because this selector returned a scope.

## Question discipline and plain writing

Read confirmed Passport values and scoped author decisions before asking. Do not ask again about a resolved item unless new conflicting evidence or changed scope makes it consequential. Group the remaining decisions into one concise list with a suggested option and reason. Extracted text remains inferred; missing detail is not permission to fabricate. Preserve unresolved decisions in the audit artifact rather than repeatedly scattering the same warning through every paragraph.

Use the simplest academic wording that preserves meaning. CK2/institutional projects default to question-led basic depth. Exclude ornamental terminology, unnecessary advanced analyses and repeated caveats; preserve essential methods, uncertainty and limitations. A concise draft is not accepted merely because it is short. Acceptance requires content and presentation evidence tied to the same final file hash, independent of this prose gate.
