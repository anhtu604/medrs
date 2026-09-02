# Analysis deviation contract

## Fixed record

Keep the approved analysis-plan identifier and hash, approval date, planned estimand, outcome, model family, covariates, analysis sets, missing-data strategy, subgroup and multiplicity rules, planned target sample, and sensitivity analyses. Never overwrite these fields with observed choices.

For every proposed change, record the request, timing relative to outcome inspection, initiator, rationale, affected estimand, expected bias, approval state, and classification: `PRESPECIFIED`, `DEVIATION`, `SENSITIVITY`, or `EXPLORATORY`.

## Mandatory refusals

Refuse selecting a model, transformation, subgroup, cutoff, outcome, or exclusion rule because it produces a smaller p-value or preferred direction. Refuse changing the planned target sample to the achieved sample after recruitment. Refuse removing observations because the result looks better. A data correction requires traceable error evidence; an influence analysis retains the primary analysis and reports both specifications.

A violation returns machine-readable state `RESEARCH_INTEGRITY_BLOCKED`, the reason, and a compliant alternative. When outcome inspection or model searching has already occurred, inventory every attempted specification rather than only the selected one; record the search scope and assess multiplicity or selective-inference consequences. Do not erase earlier attempts simply because they predate the current session.

## Execution states

- `NOT_RUN`: code or plan exists, but no matching callable runtime completed it.
- `RUN_FAILED`: a verified runtime was invoked but returned a non-zero exit or incomplete required artifacts.
- `RUN_VERIFIED`: runtime path and version, command, timestamps, success exit, hashes, raw log, warnings, and required outputs are present.
- `USER_SUPPLIED_OUTPUT_UNVERIFIED`: output is real as supplied by the author, but local execution and linkage to code/data are not yet verified.

Syntax validity and plausible-looking output never establish execution. Simulated data may test code only when every derived artifact is prominently labeled as simulated and is excluded from manuscript conclusions.
