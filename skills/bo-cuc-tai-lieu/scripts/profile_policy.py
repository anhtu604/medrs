"""Source and scope gate; metadata readiness is not final-file acceptance."""
from datetime import date
import re


def profile_readiness(profile: dict, today: str) -> str:
    required = ("source_url", "source_version", "source_license", "last_verified")
    if profile.get("source_kind") != "presentation-rules":
        return "OFFICIAL_RULE_REQUIRED"
    if any(not isinstance(profile.get(k), str) or not profile[k].strip() for k in required):
        return "OFFICIAL_RULE_REQUIRED"
    if not re.fullmatch(r"[0-9a-fA-F]{64}", str(profile.get("source_hash", ""))):
        return "OFFICIAL_RULE_REQUIRED"
    locators = profile.get("requirements_locators")
    if not isinstance(locators, list) or not locators or any(not isinstance(x, str) or not x.strip() for x in locators):
        return "OFFICIAL_RULE_REQUIRED"
    applicable = profile.get("applicable_document_types")
    target = profile.get("document_type")
    if not target or not isinstance(applicable, list) or target not in applicable:
        return "OFFICIAL_RULE_REQUIRED"
    ttl = profile.get("expires_after_days")
    if type(ttl) is not int or ttl <= 0:
        return "OFFICIAL_RULE_REQUIRED"
    try:
        current, verified = date.fromisoformat(today), date.fromisoformat(profile["last_verified"])
    except (ValueError, TypeError):
        return "OFFICIAL_RULE_REQUIRED"
    age = (current - verified).days
    if age < 0:
        return "OFFICIAL_RULE_REQUIRED"
    return "STALE" if age > ttl else "READY"


def table_border_policy(profile: dict) -> str:
    exception = profile.get("institution_exception") or {}
    value = profile.get("table_borders")
    if (exception.get("scope") == "table-borders" and exception.get("approved_by")
            and exception.get("reason")):
        value = exception.get("value")
    return value if value in {"grid", "no-vertical", "minimal"} else "AUTHOR_APPROVAL_REQUIRED"
