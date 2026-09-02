# Scientific integrity pass

Apply this pass to the claim–evidence artifact before sentence-level editing.

- A factual claim needs verified result provenance, a verified source, or an unresolved marker.
- A citation string is not evidence that the source exists or supports the sentence. Preserve it as `SOURCE_UNVERIFIED` until checked against the actual record.
- Numbers must match their source table, figure, dataset, or statistical output, including denominator, unit, time point, estimate, interval, and analysis population.
- An observational design supports association language unless a separately justified causal design and analysis are documented. Editing cannot upgrade the design.
- Ethics approval, registration, consent, software execution, and completed procedures require recorded provenance. Never improve prose by turning a plan into a completed event.
- Novelty, priority, safety, efficacy, policy, and clinical recommendations must stay within the evidence and target scope.

Return location, claim text, evidence state, ceiling breached, and the smallest safe correction. If the correct fact cannot be established, use the locale display for `SOURCE_REQUIRED`, `VERIFIED_RESULTS_REQUIRED`, or `AUTHOR_APPROVAL_REQUIRED` rather than guessing.
