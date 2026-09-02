# RoB 2 use contract

This workflow supports the 22 signalling-question identifiers in the 22 August 2019 tool for individually randomized parallel-group trials: domain 1 (1.1–1.3), domain 2 for effect of assignment (2.1–2.7), domain 3 (3.1–3.4), domain 4 (4.1–4.5), and domain 5 (5.1–5.3). The operational summaries live in `../../../coverage/rob2-parallel-2019.yaml`; their source locators point to the official template. They deliberately do not reproduce the full copyrighted wording.

Start with one specific result: outcome, time point, numerical result, comparison, and effect of assignment or adherence estimand. Use the trial report together with protocol, registry, statistical analysis plan and supplementary files when available. Answer only from located evidence. Valid response families include Yes, Probably yes, Probably no, No, No information, and instrument-defined Not applicable. Preserve the exact response code used by the official tool.

All five domains must be considered. Do not infer randomization quality merely from the word “randomized”; do not infer adherence deviations from attrition; do not equate a complete-case analysis with acceptable missingness; do not judge outcome measurement without assessor, method and differential-awareness evidence; and do not dismiss selective reporting without comparing prespecified and reported analyses.

The official algorithm determines Low risk, Some concerns or High risk for each domain and overall. Never substitute an improvised majority vote. Store the official tool version, algorithm/workbook provenance, completed question IDs, item rationales, domain results, overall result, and unresolved evidence. If the algorithm cannot be run or its provenance cannot be established, return `OFFICIAL_INSTRUMENT_REQUIRED` or `UNRESOLVED`, not a synthetic judgment.

RoB 2 is result-specific. A trial can receive different judgments across outcomes, time points or estimands. The output must therefore never claim a single permanent risk-of-bias grade for the whole publication unless explicitly presented only as a non-authoritative summary of multiple result-level assessments.
