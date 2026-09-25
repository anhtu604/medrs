"""Document-type profiles: convention defaults plus optional source-governed rules."""

from datetime import date
from pathlib import Path

import yaml

from .budgets import ValidationIssue
from .freshness import verification_status
from .profiles import REQUIRED_SOURCE_FIELDS


ROOT = Path(__file__).parents[2]
PROFILE_DIR = Path("profiles/document-type")
DOCUMENT_TYPES = (
    "journal-article-vn",
    "journal-article-intl",
    "thesis-master",
    "thesis-specialist",
    "dissertation-doctoral",
    "protocol",
)
LEGACY_DOCUMENT_TYPES = {"thesis": "thesis-master", "dissertation": "dissertation-doctoral", "protocol": "protocol"}
ARTICLE_ALIASES = {"journal-article", "manuscript"}
CONVENTION_FIELDS = {
    "status",
    "frame",
    "abstract_languages",
    "discussion_scope",
    "analysis_depth",
    "literature_comparison",
    "strengths_limitations",
    "contributions_section",
    "section_word_budget",
}


def resolve_document_type(value: str, locale_profile: str) -> str:
    normalized = value.strip().casefold()
    if normalized in DOCUMENT_TYPES:
        return normalized
    if normalized in LEGACY_DOCUMENT_TYPES:
        return LEGACY_DOCUMENT_TYPES[normalized]
    if normalized in ARTICLE_ALIASES:
        return "journal-article-intl" if locale_profile.casefold().startswith("en") else "journal-article-vn"
    raise ValueError(f"UNKNOWN_DOCUMENT_TYPE:{value}")


def load_document_type(root: Path, name: str) -> dict:
    return yaml.safe_load((Path(root) / PROFILE_DIR / f"{name}.yaml").read_text(encoding="utf-8"))


def section_word_budget(profile: dict, section: str) -> int | None:
    return (profile["convention"].get("section_word_budget") or {}).get(section)


def validate_document_type_profiles(root: Path, as_of: date) -> list[ValidationIssue]:
    issues = []
    for name in DOCUMENT_TYPES:
        path = Path(root) / PROFILE_DIR / f"{name}.yaml"
        if not path.exists():
            issues.append(ValidationIssue("DOCUMENT_TYPE_PROFILE_MISSING", str(path), name))
            continue
        profile = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if profile.get("profile_id") != name or profile.get("document_type") != name:
            issues.append(ValidationIssue("DOCUMENT_TYPE_ID_MISMATCH", str(path), name))
        convention = profile.get("convention") or {}
        missing = sorted(CONVENTION_FIELDS - set(convention))
        if missing:
            issues.append(ValidationIssue("DOCUMENT_TYPE_CONVENTION_INCOMPLETE", str(path), ", ".join(missing)))
        elif convention["status"] != "CONVENTION":
            issues.append(ValidationIssue("DOCUMENT_TYPE_CONVENTION_STATUS", str(path), str(convention["status"])))
        rules = profile.get("rules")
        if rules is None:
            if not profile.get("rules_note"):
                issues.append(ValidationIssue("DOCUMENT_TYPE_RULES_NOTE_MISSING", str(path), name))
            continue
        missing_source = sorted(REQUIRED_SOURCE_FIELDS - set(rules))
        if missing_source:
            issues.append(ValidationIssue("DOCUMENT_TYPE_RULES_SOURCE_MISSING", str(path), ", ".join(missing_source)))
            continue
        empty_source = sorted(
            field for field in ("source_url", "source_version", "source_license", "source_cutoff", "last_verified")
            if not isinstance(rules[field], str) or not rules[field].strip()
        )
        if rules["expires_after_days"] is None:
            empty_source.append("expires_after_days")
        if empty_source:
            issues.append(ValidationIssue("DOCUMENT_TYPE_RULES_SOURCE_EMPTY", str(path), ", ".join(empty_source)))
            continue
        if rules["verification_status"] == "UNVERIFIED":
            issues.append(ValidationIssue("DOCUMENT_TYPE_RULES_UNVERIFIED", str(path), name))
        computed = verification_status(rules, as_of)
        if computed != rules["verification_status"]:
            issues.append(
                ValidationIssue(
                    "DOCUMENT_TYPE_RULES_FRESHNESS_MISMATCH",
                    str(path),
                    f"declared {rules['verification_status']}, computed {computed}",
                )
            )
        if not rules.get("requirements") or any(
            not isinstance(item, dict)
            or not isinstance(item.get("source_locator"), str)
            or not item["source_locator"].strip()
            for item in rules["requirements"]
        ):
            issues.append(ValidationIssue("DOCUMENT_TYPE_RULES_UNLOCATED", str(path), name))
    return issues
