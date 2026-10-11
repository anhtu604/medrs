"""Privacy-aware simulation lineage; author declarations and verification differ."""

from copy import deepcopy
import hashlib
import hmac
import json
import unicodedata


def fingerprint_records(rows: list[dict], columns: list[str], key: bytes) -> str:
    if not rows or not columns or len(set(columns)) != len(columns) or not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("ROWS_COLUMNS_AND_PRIVATE_KEY_REQUIRED")
    encoded = []
    for row in rows:
        if any(column not in row for column in columns):
            raise ValueError("FINGERPRINT_COLUMN_MISSING")
        record = {column: unicodedata.normalize("NFC", row[column]) if isinstance(row[column], str) else row[column] for column in sorted(columns)}
        encoded.append(json.dumps(record, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(",", ":")))
    payload = json.dumps({"normalization": "medrs-records-v1", "rows": sorted(encoded)}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def transition_data_state(previous: dict, replacement: dict, author_decision: dict) -> dict:
    simulated_digests = set()
    for entry in [previous, *previous.get("history", [])]:
        for state_key, digest_key in (("state", "digest"), ("previous_state", "previous_digest"),
                                      ("new_state", "replacement_digest")):
            if entry.get(state_key) == "SIMULATED" and entry.get(digest_key):
                simulated_digests.add(entry[digest_key])
    resolution = author_decision.get("conflict_resolution") or {}
    resolved = (resolution.get("status") == "CONFIRMED" and resolution.get("scope") == "dataset-replacement"
                and resolution.get("digest") == replacement.get("digest")
                and bool(resolution.get("author") and resolution.get("reason") and resolution.get("timestamp")))
    result = {"state": previous.get("state", "UNRESOLVED"), "digest": previous.get("digest"),
              "remove_current_simulation_labels": False, "author_recheck_required": False,
              "history_preserved": True, "history": deepcopy(previous.get("history", [])),
              "qualifications": [], "author_declaration": None}
    confirmed = author_decision.get("confirmed") is True
    if confirmed and author_decision.get("still_simulated") is True:
        result.update(state="SIMULATED", author_declaration="STILL_SIMULATED")
    elif confirmed and author_decision.get("data_updated_to_real") is True and replacement.get("replacement_received") is True:
        result.update(author_recheck_required=True, author_declaration="REAL_UPDATED")
        if not replacement.get("digest"):
            result.update(state="UNRESOLVED", qualifications=["REPLACEMENT_DIGEST_REQUIRED"])
        elif replacement.get("partial") is True:
            result.update(state="UNRESOLVED", qualifications=["PARTIAL_REPLACEMENT_REQUIRES_SCOPE"])
        elif replacement["digest"] in simulated_digests and not resolved:
            result.update(state="UNRESOLVED", qualifications=["SAME_VALUES_REQUIRE_REVIEW"])
        else:
            result.update(state="AUTHOR_DECLARED_REAL", digest=replacement["digest"], remove_current_simulation_labels=True)
            receipt = replacement.get("verification") or {}
            if receipt.get("status") == "PASS" and receipt.get("reviewer") and receipt.get("digest") == replacement["digest"]:
                result["state"] = "VERIFIED_REAL"
            else:
                result["qualifications"].append("AUTHOR_DECLARATION_NOT_INDEPENDENT_VERIFICATION")
    elif confirmed and author_decision.get("data_updated_to_real") is True:
        result["qualifications"].append("REPLACEMENT_NOT_RECEIVED")
    result["history"].append({"previous_state": previous.get("state", "UNRESOLVED"), "previous_digest": previous.get("digest"),
                              "new_state": result["state"], "replacement_digest": replacement.get("digest"),
                              "author": author_decision.get("author"), "timestamp": author_decision.get("timestamp"),
                              "author_declaration": result["author_declaration"],
                              "conflict_resolution": deepcopy(resolution) if resolved else None})
    return result
