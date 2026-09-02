"""Methods-section artifact construction without prose fabrication."""

from pathlib import Path

import yaml


VALID_MODES = {"protocol", "completed-study"}


def load_locale_profile(root: Path, profile_id: str) -> dict:
    path = Path(root) / "profiles" / "locale" / f"{profile_id}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def draft_methods(
    *,
    mode: str,
    planned_procedures: list[str],
    confirmed_procedures: list[str],
    deviations: list[str],
    locale_profile: str,
    multi_section: bool,
) -> dict:
    if mode not in VALID_MODES:
        raise ValueError(f"Unsupported Methods mode: {mode}")

    markers = []
    if mode == "protocol":
        claims = [{"text": text, "execution_status": "PLANNED"} for text in planned_procedures]
        completed = False
    else:
        claims = [{"text": text, "execution_status": "CONFIRMED_EXECUTED"} for text in confirmed_procedures]
        completed = bool(claims)
        unconfirmed = set(planned_procedures) - set(confirmed_procedures)
        if unconfirmed:
            markers.append("DATA_REQUIRED")

    return {
        "mode": mode,
        "locale_profile": locale_profile,
        "procedure_claims": claims,
        "claims_procedure_completed": completed,
        "deviations": list(deviations),
        "markers": markers,
        "preflight": {"status": "PENDING_EXECUTION", "scope": "section"},
        "full_gate": {
            "status": "PENDING",
            "reason": "kiem-van-phong is not active in slice 1",
        },
        "document_context": "multi-section" if multi_section else "standalone",
    }
