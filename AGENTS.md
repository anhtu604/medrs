# Medical Research Skills VN 2.0

This repository is the portable core and Claude package for a medical-research assistant. Start with `skills/co-van/SKILL.md`. Canonical content lives only under `skills/<name>/`; host adapters must remain thin.

Never reconstruct a reporting checklist, appraisal instrument, regulatory rule, citation, result, or institutional requirement from memory. Retrieve primary material, record source/version/license/retrieval/freshness metadata, and implement exact item coverage. If primary material is unavailable, create `BLOCKED.md`, leave the implemented item list empty, and let validation fail.

Research data and extracted draft fields are not verified by default. Use the Research Passport and preserve `DRAFT_INFERRED` or `UNRESOLVED` until the author confirms them.

Run validation in this order:

```text
claude plugin validate . --strict
python scripts/validate_skills.py
python -m pytest -q
python tests/eval_runner.py --offline
```

Do not install version 1.3.0 alongside 2.0. The old release is an archival rollback artifact only.

