"""Research Passport state management."""

from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

from .budgets import ValidationIssue


ROOT = Path(__file__).parents[2]
SCHEMA_PATH = ROOT / "schemas/research-passport.schema.json"


def unresolved_field(marker: str = "DATA_REQUIRED") -> dict:
    return {
        "value": None,
        "status": "UNRESOLVED",
        "confidence": None,
        "provenance": [],
        "confirmed_by": None,
        "marker": marker,
    }


def new_passport(project_id, document_type, locale_profile):
    return {
        "schema_version": "2.0.0",
        "project_id": project_id,
        "document_type": document_type,
        "locale_profile": locale_profile,
        "target_language": unresolved_field(),
        "research_question": unresolved_field(),
        "objectives": unresolved_field(),
        "hypotheses": unresolved_field(),
        "study_design": unresolved_field(),
        "population": unresolved_field(),
        "setting": unresolved_field(),
        "exposure_or_intervention": unresolved_field(),
        "comparator": unresolved_field(),
        "outcomes": unresolved_field(),
        "data_sensitivity": unresolved_field("AUTHOR_APPROVAL_REQUIRED"),
        "target_profile": unresolved_field("OFFICIAL_RULE_REQUIRED"),
        "reporting_guideline": unresolved_field("SOURCE_REQUIRED"),
        "risk_of_bias_framework": unresolved_field("SOURCE_REQUIRED"),
        "verified_results": [],
        "source_ledger": [],
        "author_decisions": [],
        "unresolved_markers": ["DATA_REQUIRED", "AUTHOR_APPROVAL_REQUIRED", "OFFICIAL_RULE_REQUIRED"],
        "disclosure_record": [],
        "audit_log": [],
    }


def confirm_field(passport, json_pointer, value, author, timestamp):
    if not json_pointer.startswith("/") or "/" in json_pointer[1:]:
        raise ValueError("Only top-level Passport fields may be confirmed")
    field_name = json_pointer[1:]
    if field_name not in passport or not isinstance(passport[field_name], dict):
        raise KeyError(field_name)
    updated = deepcopy(passport)
    updated[field_name].update(
        {
            "value": value,
            "status": "CONFIRMED",
            "confidence": 1.0,
            "confirmed_by": author,
            "marker": None,
        }
    )
    updated["audit_log"].append(
        {
            "action": "CONFIRM_FIELD",
            "path": json_pointer,
            "author": author,
            "timestamp": timestamp,
        }
    )
    return updated


def validate_passport(passport):
    issues: list[ValidationIssue] = []
    validator = Draft202012Validator({})
    if SCHEMA_PATH.exists():
        import json

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(passport), key=lambda item: list(item.path)):
        issues.append(ValidationIssue("PASSPORT_SCHEMA", "/".join(map(str, error.path)), error.message))
    for name, field in passport.items():
        if isinstance(field, dict) and field.get("status") == "CONFIRMED" and not field.get("confirmed_by"):
            issues.append(ValidationIssue("CONFIRMED_WITHOUT_AUTHOR", name, "confirmed_by is required"))
    return issues
