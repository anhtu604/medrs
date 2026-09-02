"""Traceable peer-review, revision-commitment, and re-review contracts."""


class RevisionContractError(ValueError):
    pass


def _by_comment(items: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for item in items:
        grouped.setdefault(item.get("comment_id", ""), []).append(item)
    return grouped


def build_response_matrix(*, comments: list[dict], changes: list[dict], evidence: list[dict]) -> dict:
    identifiers = [comment.get("id") for comment in comments]
    if len(identifiers) != len(set(identifiers)):
        raise RevisionContractError("DUPLICATE_COMMENT_ID")
    changes_by_id = _by_comment(changes)
    evidence_by_id = _by_comment(evidence)
    rows = []
    allowed = {"accept", "partial", "decline", "clarify"}
    for comment in comments:
        identifier = comment.get("id")
        if not identifier or not comment.get("reviewer") or not comment.get("verbatim"):
            raise RevisionContractError("COMMENT_PROVENANCE_REQUIRED")
        decision = comment.get("decision")
        if decision not in allowed or not comment.get("rationale"):
            raise RevisionContractError("DECISION_AND_RATIONALE_REQUIRED")
        linked_changes = changes_by_id.get(identifier, [])
        linked_evidence = evidence_by_id.get(identifier, [])
        if decision in {"accept", "partial"} and not linked_changes:
            raise RevisionContractError(f"RESPONSE_WITHOUT_CHANGE:{identifier}")
        if decision in {"partial", "decline"} and not linked_evidence:
            raise RevisionContractError(f"DECISION_EVIDENCE_REQUIRED:{identifier}")
        for change in linked_changes:
            if not change.get("artifact") or not change.get("locator") or len(str(change.get("artifact_hash", ""))) != 64:
                raise RevisionContractError(f"CHANGE_PROVENANCE_REQUIRED:{identifier}")
        commitment = linked_changes[0] if linked_changes else None
        rows.append(
            {
                "comment_id": identifier,
                "reviewer": comment["reviewer"],
                "verbatim": comment["verbatim"],
                "classification": comment.get("classification", "unclassified"),
                "decision": decision,
                "rationale": comment["rationale"],
                "evidence": linked_evidence,
                "changes": linked_changes,
                "commitment": commitment,
            }
        )
    known_ids = set(identifiers)
    orphan_ids = sorted((set(changes_by_id) | set(evidence_by_id)) - known_ids)
    if orphan_ids:
        raise RevisionContractError(f"ORPHAN_REVISION_RECORD:{','.join(orphan_ids)}")
    return {"status": "READY_FOR_RE_REVIEW", "rows": rows}


def check_numeric_propagation(*, claim_id: str, new_value: str, expected_locations: list[str], observed_values: dict) -> dict:
    mismatches = [
        {"locator": locator, "observed": observed_values.get(locator)}
        for locator in expected_locations
        if observed_values.get(locator) != new_value
    ]
    return {
        "claim_id": claim_id,
        "new_value": new_value,
        "status": "PASS" if not mismatches else "PROPAGATION_INCOMPLETE",
        "mismatches": mismatches,
    }


def re_review_commitments(matrix: dict, current_artifact_hashes: dict[str, str]) -> dict:
    stale = []
    missing = []
    for row in matrix.get("rows", []):
        commitment = row.get("commitment")
        if not commitment:
            continue
        artifact = commitment["artifact"]
        current = current_artifact_hashes.get(artifact)
        if current is None:
            missing.append(row["comment_id"])
        elif current != commitment["artifact_hash"]:
            stale.append(row["comment_id"])
    status = "RE_REVIEW_REQUIRED" if stale or missing else "COMMITMENTS_VERIFIED"
    return {"status": status, "stale_comments": stale, "missing_artifacts": missing}
