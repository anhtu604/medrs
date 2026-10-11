# Identity before interpretation

Read for any table, figure, statistical observation, Results paragraph, abstract result or Discussion claim. The result key is not a p-value. Use a stable ID plus variable, indicator, analysis set/denominator, group, time pair, test and adjustment. Retain planned versus achieved sample size separately. Different indicators calculated from one questionnaire are different results; an overall test is not a pairwise comparison. When a table changes, reconcile all dependent observations, figure labels and embedded data, abstract, Discussion and conclusions through the leader's work order.

## Trace actual results

Each numerical claim must link to verified runtime output, or explicitly labelled author-supplied output with unresolved provenance. Record script/data/output hashes, software version, missing-data policy, denominator and units. Do not choose the row with a matching p and then infer its comparison. With longitudinal measures, state the actual visits/intervals, which pair is compared, whether pairing is valid, and whether the test assesses a distribution, mean, median, proportion or change. Follow the confirmed design and analysis plan. A requested short manuscript does not authorize an invalid simplification.

Check signs, scales and display rounding against the unrounded results. Distinguish a proportion, percentage-point change, relative percentage change, risk ratio, odds ratio and standardized score. The allowable CI domain belongs to the estimand: a proportion is bounded, a score change can cross zero, and an odds ratio has a different domain. If an inappropriate CI method produces an impossible bound, flag it and correct the estimator/code with justification; never cosmetically clip it to 0 or 100. P-values must be within their domain and must retain the correct test and multiplicity adjustment. Do not substitute exact p with an unsupported threshold.

## Minimal readable presentation

For every new or materially changed table provide a short observation naming its main comparison, denominator and direction, plus a legend for symbols, abbreviations, tests, units and adjusted p when applicable. Do not silently replace existing author observations or put process codes such as Task 4 into the manuscript. Verify that table title, column headings and prose refer to the same variable and time pair. Inspect chart labels and embedded workbook data, not just surrounding captions. Numeric OOXML checks do not read raster figures or establish visual quality.

Non-significance alone does not establish equivalence, absence of effect or successful adjustment. Interpret effect size and uncertainty first; causal conclusions require a design and assumptions that support them. Explain a difference between studies only using comparable population, indicator, baseline, setting and time horizon; differences in baseline do not by themselves prove the direction of a mechanism. Basic CK2/institutional reports need only analyses that answer the confirmed question, but must retain valid denominators, uncertainty, clinical detail and ethical limitations.

## Release evidence

Use `leader-nghien-cuu/scripts/quality_checks.py` for full keyed comparisons and explicit CI bounds. It is a mechanical comparator, not a statistical runtime or a replacement for expert review. The content reviewer must independently reconcile the actual saved file with output and codebook. After repairs, repeat affected checks and update final hashes; an old pass cannot certify a new file. Missing identity, unknown output provenance or unexplained calculation discrepancy remains unresolved in the closing checklist.
