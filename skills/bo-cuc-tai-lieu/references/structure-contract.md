# Semantic structure contract

This skill controls meaning and order: document class, required and optional sections, section sequence, heading hierarchy, section names, and the placement relationships of tables, figures, captions and appendices. It does not control typefaces, margins, line spacing, page-number fields, generated tables of contents, section-break mechanics, PDF rendering or visual pagination. Those are `dinh-dang-tai-lieu` responsibilities.

Inputs are the actual draft, a source-dated target profile, submission stage, language/locale profile and author decisions. Inspect the artifact rather than relying on a declared outline. Build a comparison containing current section identifiers, target identifiers, aliases used, unrecognized headings, missing required sections and order deviations. Never discard unknown XML blocks, comments, notes, tables or embedded objects merely because they are not classified.

The restructuring plan lists each move, rename, split or merge with source and destination and a reason tied to a profile rule. Renames that change meaning, and all splits or merges, require a content-level preview. No transformation proceeds until the author approves the plan. Missing substantive sections block output with `AUTHOR_INPUT_REQUIRED`; placeholders may appear in the plan but are not inserted as if they were content.

Transformations write a distinct output path. Validation reopens the new artifact and computes its recognized order; success cannot be inferred from script configuration. Report the source and output hashes, performed operations, preserved unknown blocks, missing sections, hierarchy findings and any checks not performed. A structural pass does not imply a formatting, pagination or visual-render pass.
