"""Portable access receipts. A supplied outcome is not independently verified."""
from copy import deepcopy
from datetime import datetime


def inaccessible(attempt: dict) -> bool:
    code = attempt.get("http_status")
    return bool(attempt.get("error")) or (
        isinstance(code, int) and not isinstance(code, bool) and code >= 400)


def _executed(attempt):
    if inaccessible(attempt):
        return False
    code = attempt.get("http_status")
    if not isinstance(code, int) or isinstance(code, bool) or not 200 <= code < 300:
        return False
    if not all(str(attempt.get(k) or "").strip() for k in ("provider", "query", "time")):
        return False
    try:
        if datetime.fromisoformat(attempt["time"]).tzinfo is None:
            return False
    except (TypeError, ValueError):
        return False
    count = attempt.get("hits")
    return isinstance(count, int) and not isinstance(count, bool) and count >= 0


def access_state(attempts: list[dict]) -> str:
    if not attempts:
        return "UNPERFORMED"
    valid = [a for a in attempts if _executed(a)]
    for levels, state in [
        ({"full-text", "full_text", "FULL_TEXT"}, "FULL_TEXT"),
        ({"abstract", "abstract-only", "ABSTRACT_ONLY"}, "ABSTRACT_ONLY"),
    ]:
        if any(a["hits"] > 0 and a.get("access_level") in levels for a in valid):
            return state
    if any(a["hits"] > 0 for a in valid):
        return "METADATA_ONLY"
    # Failed or unresolved providers prohibit an overall absence claim.
    if any(inaccessible(a) for a in attempts):
        return "INACCESSIBLE"
    if len(valid) != len(attempts):
        return "UNRESOLVED"
    return "SEARCHED_NO_HITS"


def access_summary(attempts: list[dict]) -> dict:
    state = access_state(attempts)
    ceiling = {"FULL_TEXT": "READ_AVAILABLE_ORIGINAL_BEFORE_EXTRACTION",
               "ABSTRACT_ONLY": "ABSTRACT_CONTENT_ONLY",
               "METADATA_ONLY": "DISCOVERY_ONLY"}.get(state, "NO_CONTENT_CLAIM")
    return {
        "state": state, "attempts": deepcopy(attempts),
        "partial_failure": any(inaccessible(a) or not _executed(a) for a in attempts),
        "claim_ceiling": ceiling, "evidence_verified": False,
        "systematic_completeness": False, "required_vietnamese_count": None,
    }


def extraction_receipt(record: dict, attempts: list[dict]) -> dict:
    """Attempts must belong to THIS source, not an entire search result set."""
    import importlib.util
    from pathlib import Path
    path = Path(__file__).parents[2] / "phan-tich-so-lieu/scripts/statistics_policy.py"
    spec = importlib.util.spec_from_file_location("medrs_extraction_identity", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    access = access_summary(attempts)
    return {
        "source_locator": record.get("source_locator"),
        "access_ceiling": access["claim_ceiling"],
        "identity_issues": module.validate_extraction(record),
        "extraction_verified": False,
        "original_comparison_required": True,
        "access_receipt": access,
    }
