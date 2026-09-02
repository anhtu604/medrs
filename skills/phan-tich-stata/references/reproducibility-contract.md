# Stata reproducibility contract

A verified Stata bundle contains the `.do` file, analysis-plan hash, immutable input hash, Stata edition/version from `about`, exact batch command, start/end times, exit code, complete unedited `.log`, warnings/errors, random seed when applicable, and hashes for every log, table, figure, diagnostic, and exported result.

The do-file must expose analysis-set filters, variable/value labels, base categories, transformations, missing-data handling, model commands, confidence level, survey/cluster settings, multiplicity handling, and output paths. It must create denominator and missingness reports and model-appropriate postestimation diagnostics.

A syntactically plausible do-file is not evidence of execution. Without a callable Stata runtime and captured artifacts, use `NOT_RUN`. Supplied logs remain `USER_SUPPLIED_OUTPUT_UNVERIFIED` until their do-file and data linkage is confirmed. Never create or clean up a fictional Stata log, and never choose commands because their p-values are more favorable.

The allowed state machine is closed: `NOT_RUN` may become `RUN_FAILED` or `RUN_VERIFIED` only after a callable runtime is invoked; `USER_SUPPLIED_OUTPUT_UNVERIFIED` may become `RUN_VERIFIED` only after code, input, runtime, and artifact linkage passes validation. Validate the provenance sidecar against `schemas/analysis-run.schema.json`.

If simulation is needed solely to exercise code, mark the do-file and every derived title, table, figure, log, and interpretation: `DỮ LIỆU MÔ PHỎNG — KHÔNG PHẢI KẾT QUẢ NGHIÊN CỨU — KHÔNG DÙNG ĐỂ NỘP/CÔNG BỐ`. A request to fabricate a submission log or result triggers refusal.
