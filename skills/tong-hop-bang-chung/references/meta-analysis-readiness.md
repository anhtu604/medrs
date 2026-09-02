# Meta-analysis readiness

Quantitative pooling is ready only when all included effects have a source locator and verified extraction; compatible outcome definition, metric, direction, time point and population; effect estimate plus SE/variance/CI or valid numerator-denominator data; analysis unit and denominator; and a stable link to the underlying study/report.

Detect multiple publications, overlapping cohorts, multiple arms, repeated time points and multiple effects from one study before treating observations as independent. Resolve conversions and unit harmonization explicitly. Keep the prespecified effect measure, fixed/random framework, heterogeneity assessment, subgroup/meta-regression rules, multiplicity handling and sensitivity analyses. Do not choose a model because it gives a preferred p-value.

Block pooling with `META_ANALYSIS_NOT_READY` when extraction is missing, full text is inadequate, outcome definitions are incompatible, uncertainty cannot be derived, cohort independence is unresolved, or fewer than two independent eligible effects remain. Return the exact missing fields and lawful retrieval/extraction steps. Never create effect sizes, variances, forest plots or heterogeneity statistics to fill gaps.

