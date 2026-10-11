# Basic statistical decisions and interpretation ceilings

Read before selecting/altering a test, threshold or model, interpreting supplied outputs, or handing findings to a writer. Apply the analysis-deviation and result-identity contracts alongside this one. CK2/institutional projects use the simplest analysis answering their objectives; complexity is not a quality criterion.

## Establish the question before choosing the command

Identify the estimand, outcome type, independent/paired/clustered/repeated structure, timing, analysis set, missingness and intended effect measure. A small p-value cannot choose these. Inspect the actual observations/output and assumptions; do not use one normality-test p-value as an automatic switch between methods or assume the before/after raw distributions determine paired inference. Distinguish hypotheses, descriptive reporting and exploratory analyses.

For paired continuous data, mean-difference inference depends on the differences and their sampling behavior. A paired t candidate requires the mean-difference estimand and adequate inference support; signed-rank procedures have their own assumptions and do not automatically estimate the same quantity. Independent mean comparisons require support for their mean inference; equal variance must be justified before pooled variance is used. Do not ignore clustering by routing every two-column dataset to a two-sample test.

For independent categorical count tables consider exact inference when the asymptotic approximation is unsupported, with fixed-marginal interpretation and computational limits documented. Paired categorical data are not independent-table Fisher data: use the appropriate paired design/discordant counts. Record test name, sidedness, exact/asymptotic or Monte Carlo setting and analysis denominator. Simulation used for an exact-test approximation is a computational method, not evidence that patient data were simulated.

## Effect measures, intervals and sample accounting

An odds ratio is not a risk ratio or prevalence ratio. Preserve the fitted measure, unit, reference group, adjustment and confidence interval when explaining it. Common outcomes make casual substitution particularly misleading. Choose proportion confidence-interval method explicitly; Wilson/score is an available option, not a mandatory rule for every design. Do not silently use a symmetric Wald interval at boundaries, clip impossible intervals, or change the estimate to agree with a label. Survey/cluster designs need design-consistent estimation, not an independent-binomial formula by default.

Recruitment target, achieved recruited N, eligible N and outcome-available N are separate. Use the correct denominator for each group/outcome/time/model; record complete-case or imputed analysis membership. Number of events, fitted parameters, separation, missingness and model stability matter; no universal events-per-variable threshold guarantees validity. Report imprecision/under-recruitment honestly, do not retroactively shrink the planned target.

## Thresholds and searching

Keep a continuous variable continuous unless the question/protocol justifies categorization. For a cutoff record whether it comes from consensus, a reference range or one study, plus source, applicable population/measurement and timing. Source existence is not applicability. An approved before-outcome protocol can support a prespecified threshold; otherwise classify it as exploratory/deviation and report all tried thresholds/specifications. A sensitivity grid is a transparent analysis choice, not permission to pick the best-looking p. No label can erase prior outcome inspection.

## Runtime, PH and interpretation

Use [../scripts/statistics_policy.py](../scripts/statistics_policy.py) for candidate decisions, extraction checks, p display and interpretation qualifiers. It never runs a statistical test or proves an assumption. R/Stata perform execution and must retain command/path/version, source/code/output hashes, log, timestamps and warnings. Supplied output remains conditional until linked to its data/code; unknown multiplicity is not silently treated as handled. Prespecified/exploratory classification passes unchanged to Results/Discussion/abstract.

Cox proportional-hazards checking includes the residual-based test/plots and clinical time pattern, not only crossing KM lines or a binary global p cutoff. Non-proportional effects cannot be summarized unconditionally as a constant hazard ratio; discuss the approved alternative, retain the original estimand and record deviations. KM survivor, failure and hazard functions are distinct; ensure label, command and event coding match.

Display p below chosen precision as an inequality, not zero; retain raw precision and do not infer extra digits from a screenshot. Confidence intervals, clinical magnitude and design limitations remain primary. The machine-readable qualifier belongs in a sidecar; the manuscript expresses its meaning in cautious academic prose.

## Primary-source register

Checked 2026-10-11; `source_cutoff` 2026-10-11; reverify by 2027-10-11 or when installed versions/profile differ. These are paraphrased operational rules, not redistributed manuals.

- R stats development manual, version 4.6.0: [t.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html), Usage/Arguments/Details; R documentation license applies. Installed R can differ; record local help/version separately.
- R stats development manual, version 4.6.0: [fisher.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html), Description/Details/Value; R documentation license applies.
- R survival documentation: [cox.zph](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cox.zph.html), Description/Details; survival package license applies, confirm installed package version.
- Cochrane current [Handbook chapter 6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06), binary effect measures; Cochrane copyright, no copied prose.
- NIST/SEMATECH [7.2.4.1](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm), proportion confidence intervals; NIST site terms, no copied tables/formulas here.
- StataCorp Stata 19 [Programming manual](https://www.stata.com/manuals/p.pdf), capture/program/macro sections, and [sts graph](https://www.stata.com/manuals/ststsgraph.pdf), survival/failure/hazard options; copyright 1985–2025, all rights reserved; links and original implementation guidance only.
