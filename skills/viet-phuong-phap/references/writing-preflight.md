# Shared writing preflight

Every section writer reads this reference by relative path before returning a draft. The rules live here only.

## Inputs

- Research Passport and active locale-profile version
- section draft and section hash
- claim/evidence table
- unresolved markers

## Checks

1. `FABRICATION`: every fact, citation, number, approval, policy, and completed procedure is traceable to a confirmed Passport value or source. Otherwise emit the applicable unresolved marker.
2. `UNRESOLVED`: unresolved scientific or administrative decisions remain visible and are not converted into fluent prose that appears final.
3. `CAUSALITY`: causal verbs do not exceed the design and estimand. Observational association is not rewritten as intervention effect.
4. `LOCALE`: language, terminology, attribution, tense, forms of address, and section conventions match the active locale profile rather than literal translation.

## Output

Return `status` as `PASS` or `REVISE`, one record per check, markers, locale-profile identifier, Passport hash, and section hash. In a multi-section draft, the complete `kiem-van-phong` gate remains `PENDING`; this preflight is not a substitute for the assembled-document audit.
