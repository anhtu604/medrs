# Passport scope, compatibility and conflicting evidence

Read for an existing project, a new objective-specific manuscript/subproject, or inconsistent source files. Portable helpers are `../scripts/project_scope.py`; repository Passport functions delegate to these helpers. Schema version 2.0.0 remains compatible with existing files and is independent of the package version. Preserve unknown extension fields on ordinary updates; never rewrite the Passport from a smaller newly extracted dictionary.

Optional `workspace` points to the project README/history/final root, `parent_project_id` identifies a subproject, `data_provenance` records the author decision and receipt from `data_provenance.py`, and `writing_policy` records the shared gate mode/dependencies. These fields do not themselves prove that a workspace, data verification or audit exists. Link underlying artifacts and hashes; initialize the workspace before substantive work using the leader contract.

## Adoption and extraction

Read the author-designated current draft, objectives, design, results tables, codebook and logs before asking for information already present. Create a draft Passport with `DRAFT_INFERRED` fields and source locations. Confirm only through an explicit author decision; retain unknowns as `UNRESOLVED`. Distinguish intended protocol from performed methods. Do not treat filenames, a past-tense sentence or a duplicate number as independent verification.

`reconcile_project_evidence` leaves an existing value intact when a source disagrees, records both values and the source in `conflicts`, and requires author approval. Agreement is not an opportunity to erase uncertainty or upgrade inference to confirmation. After the author resolves a conflict, record who decided, the scope and superseded value, propagate the agreed change through affected manuscript surfaces, then recheck. A helper's reconciliation output is not automatic author resolution.

## Child project

`create_child_passport` requires a distinct ID. Inherit the schema and locale only; reset objectives, design, population, results, decisions and verification. Never copy the parent result N into a child paper: an objective-specific outcome may have fewer available patients, different timepoints or a distinct analysis set. Reuse parent sources and data only by explicit scoped reference with provenance and eligibility confirmation. A parent approval does not automatically authorize another purpose or external transfer. Parent custom extensions are not automatically inherited because their scope is unknown; keep the parent unchanged and let the author select what applies.

For data replacement follow `data_provenance.md`, preserving old simulated lineage while removing obsolete labels only from the confirmed updated working draft. Before drafting, read effective decisions; ask one grouped set only about consequential unknowns. Preserve all original source files and logs in dated history. Never convert unresolved data provenance into verified results to avoid another question.
