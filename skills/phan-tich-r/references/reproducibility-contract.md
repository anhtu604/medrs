# R reproducibility contract

A verified R bundle contains the `.R` script, analysis-plan hash, immutable input hash, R and package versions from `sessionInfo()` or an equivalent machine-readable record, command, start/end times, exit code, complete console log, warnings/errors, random seed when applicable, and hashes for every table, figure, diagnostic, and exported model summary.

The script must make analysis-set filters, variable coding, factor reference levels, transformations, missing-data handling, model formulae, confidence level, multiplicity handling, and output paths visible. It must produce denominator and missingness accounting plus model-appropriate assumption or diagnostic artifacts.

A script that parses is not a completed analysis. Without a callable R runtime and captured artifacts, use `NOT_RUN`. Author-supplied output uses `USER_SUPPLIED_OUTPUT_UNVERIFIED` until its script and input linkage is confirmed. Never manufacture a model object, coefficient, standard error, interval, p-value, fit statistic, table, plot, or console log.

The allowed state machine is closed: `NOT_RUN` may become `RUN_FAILED` or `RUN_VERIFIED` only after a callable runtime is invoked; `USER_SUPPLIED_OUTPUT_UNVERIFIED` may become `RUN_VERIFIED` only after code, input, runtime, and artifact linkage passes validation. Store the sidecar against `schemas/analysis-run.schema.json`.

If simulation is needed solely to exercise code, mark the script and every derived title, table, figure, and interpretation: `DỮ LIỆU MÔ PHỎNG — KHÔNG PHẢI KẾT QUẢ NGHIÊN CỨU — KHÔNG DÙNG ĐỂ NỘP/CÔNG BỐ`. A request to fabricate output for submission triggers refusal, not a simulation workaround.
