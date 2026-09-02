# Appraisal routing

Use the appraisal target to choose the tool. RoB 2 evaluates risk of bias in a specific result from a randomized trial and requires the intended effect/estimand. GRADE rates certainty in a body of quantitative evidence for each outcome and comparison. GRADE-CERQual rates confidence in each qualitative evidence-synthesis finding. A reporting checklist such as CONSORT, STROBE or PRISMA asks whether reporting is complete; it does not replace appraisal.

Record study design, synthesis type, outcome or finding, time point, effect measure, comparison, estimand, and available source documents. If these fields do not identify an appraisal target, return `APPRAISAL_TARGET_REQUIRED`. If the requested instrument does not match the design, return `FRAMEWORK_MISMATCH` and propose a suitable family without inventing an assessment.

Every judgment needs an evidence excerpt or precise locator and the document's provenance. Absence of information is not evidence that a safeguard was absent or present. Mark the item `NI` or `UNRESOLVED` according to the official instrument. Do not collapse item-level uncertainty into a reassuring overall label.

Outputs are structured records suitable for synthesis: framework and version, target, sources, item responses, rationales, domain judgments, overall judgment, unresolved register, deviations from the official process, and date verified. Where an official algorithm or workbook is required, record its version and file hash or URL.
