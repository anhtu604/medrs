# Exposure follow-up and systematic-review appraisal

Use for a specific exposure-effect estimate or the methodological appraisal of an intervention systematic review. These targets differ from intervention-effect appraisal, diagnostic accuracy, prevalence and certainty of a body of evidence. Start with the Research Passport, protocol, design, estimand, comparison and outcome. An instrument name does not supply missing evidence.

## Official-source loading across all expanded instruments

Every expanded manifest requires the original at use time. `../scripts/official_tool.py::load_official_tool` checks the locally supplied DOCX/PDF hash and returns complete text with paragraph/table/page locators. It neither downloads nor redistributes originals, performs appraisal, executes official algorithms or establishes legal permission. Read the resulting original, not just its summary or item-name list. Retain the original use record privately with the appraisal. Do not publish returned original text in the repository or hand it to an external AI without scoped authority.

The `authorized_use` flag records a separately established lawful-use scope; it is not a waiver of license restrictions. Consult actual terms where purpose is uncertain. Once the scope is recorded, reuse it only for the same purpose rather than ask every paragraph. If the original is absent, wrong-hash, unreadable or the reader unavailable, report `OFFICIAL_TOOL_REQUIRED`, `SOURCE_HASH_MISMATCH` or the explicit runtime/OCR limitation. Do not fill the missing checklist from memory. A successful load means source text was read, not that the study has passed appraisal.

## ROBINS-E, 24 March 2024

Primary: https://www.riskofbias.info/welcome/robins-e-tool. Coverage: `../../../coverage/robins-e-2024.yaml`. Source checked 2026-10-11; reverify within 365 days or when an update is reported. Original license CC BY-NC-ND 4.0; no official wording, translation or algorithm is redistributed. Use-time original/guidance remain required.

Define the causal contrast, exposure metric, exposure window, outcome period and population before selecting the domain variants. Complete the original preliminary sections, including exposure measurement and confounder evaluation. Baseline confounding and baseline-plus-time-varying confounding use different Domain 1 variants. Domain 2 has three distinct variants: one measurement, repeated measurements combined into an exposure summary, and follow-up split by changing exposure. Repeated official question numbers are namespaced A/B/C in navigation; do not deduplicate away a branch or mix its guidance with another exposure structure.

There are seven domains and forty-eight branch-specific navigation entries across the complete set of variants. An individual estimate uses its applicable variant and the official conditional questions, not every incompatible branch. The remaining domains concern selection, post-exposure interventions, missing information, outcome measurement and reported-result selection. Link each question to the exact estimate and source evidence, distinguish measured from imputed completeness, and keep uncertainty visible. Do not treat post-exposure adjustment as automatically protective; inspect its relationship with the chosen causal target through the official guidance.

For each domain retain the source's three distinct judgments: bias risk, likely direction, and whether the bias could threaten the exposure-effect conclusion. Do not substitute one traffic-light color for all three. The original source labels in some fields can be inconsistent; preserve and flag anomalies rather than silently invent repaired official text. Explain each overall conclusion and hand selection/missingness/confounding uncertainties to sensitivity planning and synthesis. This is result-specific assessment, not a blanket clinical conclusion.

## AMSTAR 2

Primary checklist: https://www.amstar.ca/docs/AMSTAR-2.pdf. Guidance: https://www.amstar.ca/docs/AMSTAR%202-Guidance-document.pdf. Coverage: `../../../coverage/amstar-2-2017.yaml`. The 2017 instrument is currently linked on the official site; retrieval in 2026 does not make it a new edition. Original site copyright is retained; package content is independent navigation, not copied response criteria.

Complete all sixteen items against the review, protocols, supplements, search record and excluded-study list. Load the official response criteria including partial responses and applicable RCT/nonrandomized branches. Do not reduce review quality to an arithmetic total score. Explain consequential flaws using the official guidance; a count of yes answers can conceal a failure in an important domain. Document justified context-specific variations rather than design a new scoring system after seeing the review's conclusion.

Keep review-level and primary-study funding/conflicts distinct. Duplicate screening/extraction needs actual reviewer evidence; asking the same model twice is not automatically duplicate independent review. Where no meta-analysis was performed, use the official not-applicable route rather than invent a quantitative-synthesis judgment. Appraisal of review methods is neither PRISMA reporting completeness nor GRADE certainty of its pooled outcomes.

## Output and continuity

Return instrument/version/hash, original loading evidence, target, applicable branch, all item responses and rationale, source locators, domain/overall judgments, unresolved issues and synthesis implications. Preserve first judgments and corrections in dated history. If authors update results or the protocol, invalidate dependent appraisals and recheck affected targets. Never report completed official appraisal merely because coverage validation, original loading or navigation succeeded.
