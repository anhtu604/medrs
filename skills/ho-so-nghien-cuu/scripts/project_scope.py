"""Portable child scope and evidence conflicts; never auto-confirm extracted facts."""
from copy import deepcopy


def create_child_passport(parent: dict, project_id: str, document_type: str) -> dict:
    if not project_id or project_id == parent["project_id"]:
        raise ValueError("Distinct child project ID required")
    child = {key: deepcopy(parent[key]) for key in ("schema_version", "locale_profile")}
    child.update(project_id=project_id, document_type=document_type, parent_project_id=parent["project_id"])
    for name, field in parent.items():
        if isinstance(field, dict) and {"value", "status", "provenance"}.issubset(field):
            child[name] = {"value": None, "status": "UNRESOLVED", "confidence": None,
                           "provenance": [], "confirmed_by": None, "marker": "DATA_REQUIRED"}
    for name in ("verified_results", "source_ledger", "author_decisions", "disclosure_record", "audit_log"):
        child[name] = []
    child["unresolved_markers"] = ["DATA_REQUIRED", "AUTHOR_APPROVAL_REQUIRED", "OFFICIAL_RULE_REQUIRED"]
    child["audit_log"].append({"action": "CREATE_CHILD_SCOPE", "parent_project_id": parent["project_id"]})
    return child


def reconcile_project_evidence(passport: dict, evidence: list[dict]) -> dict:
    updated = deepcopy(passport)
    conflicts = updated.setdefault("conflicts", [])
    for record in evidence:
        name = record.get("field")
        field = updated.get(name)
        if not isinstance(field, dict) or "status" not in field or not record.get("source"):
            raise ValueError("Recognized Passport field and source required")
        if field.get("value") is not None and field["value"] != record.get("value"):
            conflict = {"field": name, "current": deepcopy(field["value"]),
                        "proposed": deepcopy(record.get("value")), "source": record["source"], "status": "UNRESOLVED"}
            if conflict not in conflicts:
                conflicts.append(conflict)
            if "AUTHOR_APPROVAL_REQUIRED" not in updated["unresolved_markers"]:
                updated["unresolved_markers"].append("AUTHOR_APPROVAL_REQUIRED")
        elif field.get("value") is None:
            field.update(value=deepcopy(record.get("value")), status="DRAFT_INFERRED", confirmed_by=None,
                         confidence=None, marker="AUTHOR_APPROVAL_REQUIRED")
            field["provenance"].append({"source": record["source"]})
    return updated
