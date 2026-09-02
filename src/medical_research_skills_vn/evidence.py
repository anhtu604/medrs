"""Reproducible literature retrieval, citation graphs, and bounded synthesis."""

from copy import deepcopy
from datetime import datetime
from html import escape
import re


class EvidenceContractError(ValueError):
    pass


def _normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip().casefold()
    normalized = re.sub(r"^https?://(dx\.)?doi\.org/", "", normalized)
    return normalized.removeprefix("doi:")


def create_search_log(
    *, database: str, query: str, searched_at: str, connector_evidence: dict | None,
    platform: str | None = None, question_version: str | None = None,
    filters: list | None = None, coverage_dates: dict | None = None,
    export_format: str | None = None, retriever: str | None = None,
    errors: list | None = None,
) -> dict:
    required = (database, query.strip(), searched_at, platform, question_version, coverage_dates, export_format, retriever)
    if not all(required) or filters is None or errors is None or not connector_evidence:
        raise EvidenceContractError("SEARCH_PROVENANCE_REQUIRED")
    try:
        parsed_date = datetime.fromisoformat(searched_at)
    except ValueError as exc:
        raise EvidenceContractError("SEARCH_DATE_INVALID") from exc
    if parsed_date.tzinfo is None:
        raise EvidenceContractError("SEARCH_DATE_TIMEZONE_REQUIRED")
    if (
        not connector_evidence.get("request_id")
        or not connector_evidence.get("artifact_hash")
        or not isinstance(connector_evidence.get("result_count"), int)
        or connector_evidence["result_count"] < 0
    ):
        raise EvidenceContractError("SEARCH_CONNECTOR_EVIDENCE_REQUIRED")
    return {
        "database": database,
        "platform": platform,
        "query": query,
        "question_version": question_version,
        "filters": filters,
        "coverage_dates": coverage_dates,
        "searched_at": searched_at,
        "export_format": export_format,
        "retriever": retriever,
        "errors": errors,
        "request_id": connector_evidence["request_id"],
        "request_artifact_hash": connector_evidence["artifact_hash"],
        "result_count": int(connector_evidence["result_count"]),
        "status": "EXECUTED_VERIFIED",
    }


def _record_key(record: dict) -> str:
    doi = _normalize_doi(record.get("doi"))
    if doi:
        return f"doi:{doi}"
    if record.get("pmid"):
        return f"pmid:{str(record['pmid']).strip()}"
    title = re.sub(r"\W+", " ", str(record.get("title", "")).casefold()).strip()
    year = str(record.get("year", ""))
    return f"title-year:{title}:{year}"


def deduplicate_records(records: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for source_record in records:
        record = deepcopy(source_record)
        if record.get("doi"):
            record["doi"] = _normalize_doi(record["doi"])
        key = _record_key(record)
        route = record.pop("discovered_by", None)
        if key not in merged:
            record["discovery_routes"] = []
            merged[key] = record
        if route and route not in merged[key]["discovery_routes"]:
            merged[key]["discovery_routes"].append(route)
        for field, value in record.items():
            if field != "discovery_routes" and not merged[key].get(field) and value:
                merged[key][field] = value
    return list(merged.values())


def _evidence_level(record: dict) -> tuple[str, str, str]:
    content = record.get("content_evidence") or {}
    valid_content = (
        content.get("type") in {"abstract", "full-text"}
        and content.get("verification_status") == "VERIFIED"
        and content.get("artifact_id")
        and re.fullmatch(r"[0-9a-fA-F]{64}", str(content.get("artifact_hash", "")))
        and re.fullmatch(r"[^:]+:.+", str(content.get("source_locator", "")))
    )
    if not valid_content:
        return "UNRESOLVED", "LOW", "ABSTRACT_OR_FULL_TEXT_REQUIRED"
    design = str(record.get("study_design", "")).casefold()
    if not design:
        return "UNRESOLVED", "LOW", "STUDY_DESIGN_REQUIRED"
    mapping = {
        "systematic-review": "L1",
        "meta-analysis": "L1",
        "guideline": "L1",
        "randomized-trial": "L2",
        "rct": "L2",
        "cohort": "L3",
        "case-control": "L4",
    }
    return mapping.get(design, "L5"), "MEDIUM", "ABSTRACT_OR_FULL_TEXT_CLASSIFICATION"


def build_citation_network(
    *,
    seed_ids: list[str],
    records: list[dict],
    edges: list[dict],
    stopping_rule: dict,
    ranking_basis: str = "discovery_relevance",
) -> dict:
    if ranking_basis not in {"discovery_relevance", "chronology", "none"}:
        raise EvidenceContractError("CITATION_COUNT_NOT_QUALITY")
    allowed_stops = {"two_rounds_no_new_eligible", "date_cutoff", "all_key_papers_chased", "resource_limit"}
    if not stopping_rule.get("type"):
        raise EvidenceContractError("STOPPING_RULE_REQUIRED")
    if stopping_rule.get("type") not in allowed_stops or stopping_rule.get("prespecified") is not True:
        raise EvidenceContractError("STOPPING_RULE_INVALID")
    if stopping_rule["type"] == "date_cutoff" and not stopping_rule.get("value"):
        raise EvidenceContractError("STOPPING_RULE_INVALID")
    if stopping_rule["type"] == "two_rounds_no_new_eligible" and stopping_rule.get("rounds", 0) < 2:
        raise EvidenceContractError("STOPPING_RULE_INVALID")

    deduped = deduplicate_records(records)
    required_node_fields = {"id", "source", "retrieved_at", "access_state", "screening_decision", "publication_status_check"}
    for record in deduped:
        if not required_node_fields <= set(record) or not record.get("discovery_routes"):
            raise EvidenceContractError("NODE_PROVENANCE_REQUIRED")
        status_check = record.get("publication_status_check", {})
        if (
            status_check.get("status") not in {"clear", "corrected", "expression-of-concern", "retracted", "unresolved"}
            or not status_check.get("source")
            or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(status_check.get("checked_at", "")))
        ):
            raise EvidenceContractError("PUBLICATION_STATUS_CHECK_REQUIRED")
    known_ids = {
        identifier
        for record in deduped
        for identifier in (
            record.get("id"),
            f"doi:{record['doi']}" if record.get("doi") else None,
            f"pmid:{record['pmid']}" if record.get("pmid") else None,
        )
        if identifier
    }
    seed_records = [
        record
        for record in deduped
        if set(seed_ids)
        & {
            record.get("id"),
            f"doi:{record['doi']}" if record.get("doi") else None,
            f"pmid:{record['pmid']}" if record.get("pmid") else None,
        }
    ]
    if set(seed_ids) - known_ids or any(
        "seed" not in record.get("discovery_routes", []) or not record.get("source") or not record.get("retrieved_at")
        for record in seed_records
    ):
        raise EvidenceContractError("SEED_PROVENANCE_REQUIRED")

    nodes = []
    canonical_by_any_id: dict[str, str] = {}
    for record in deduped:
        node = deepcopy(record)
        canonical_id = (
            f"doi:{record['doi']}" if record.get("doi") else f"pmid:{record['pmid']}" if record.get("pmid") else record.get("id")
        )
        node["id"] = canonical_id
        level, confidence, reason = _evidence_level(node)
        node["evidence_level"] = level
        node["classification_confidence"] = confidence
        node["classification_reason"] = reason
        node["citation_count_use"] = "DESCRIPTIVE_ONLY"
        nodes.append(node)
        for any_id in (record.get("id"), canonical_id):
            if any_id:
                canonical_by_any_id[any_id] = canonical_id

    allowed_edges = {"cites", "cited_by", "updates", "corrects", "retracts", "related_by_source"}
    normalized_edges = []
    for edge in edges:
        if edge.get("type") not in allowed_edges:
            raise EvidenceContractError("CITATION_EDGE_TYPE_INVALID")
        edge_required = ("source", "target", "source_system", "retrieved_at", "request_id")
        if edge.get("verification_status") != "VERIFIED" or not all(edge.get(field) for field in edge_required):
            raise EvidenceContractError("CITATION_EDGE_PROVENANCE_REQUIRED")
        source_id = canonical_by_any_id.get(edge["source"], edge["source"])
        target_id = canonical_by_any_id.get(edge["target"], edge["target"])
        canonical_node_ids = {node["id"] for node in nodes}
        if source_id not in canonical_node_ids or target_id not in canonical_node_ids:
            raise EvidenceContractError("CITATION_EDGE_ENDPOINT_REQUIRED")
        normalized_edges.append(
            {
                **edge,
                "source": source_id,
                "target": target_id,
            }
        )
    return {
        "mode": "citation-network-exploration",
        "nodes": nodes,
        "edges": normalized_edges,
        "seed_ids": seed_ids,
        "stopping_rule": stopping_rule,
        "systematic_completeness": False,
        "limitations": ["Citation-network exploration does not establish systematic completeness."],
    }


def export_graphml(network: dict) -> str:
    node_xml = "".join(
        f'<node id="{escape(str(node["id"]))}" />' for node in network.get("nodes", [])
    )
    edge_xml = "".join(
        f'<edge source="{escape(str(edge["source"]))}" target="{escape(str(edge["target"]))}"><data key="relation">{escape(str(edge["type"]))}</data></edge>'
        for edge in network.get("edges", [])
    )
    return f'<?xml version="1.0" encoding="UTF-8"?><graphml><graph edgedefault="directed">{node_xml}{edge_xml}</graph></graphml>'


def synthesize_evidence(
    *,
    records: list[dict],
    mode: str,
    search_logs: list[dict],
    screening_complete: bool,
    extracted_effects: list[dict] | None = None,
    protocol_id: str | None = None,
    eligibility_criteria_id: str | None = None,
    deduplication_log_id: str | None = None,
    screening_ledger: dict | None = None,
    analysis_plan: dict | None = None,
) -> dict:
    normalized_mode = mode.casefold()
    if normalized_mode not in {"narrative", "systematic", "scoping", "meta-analysis", "evidence-map-only"}:
        raise EvidenceContractError("SYNTHESIS_MODE_INVALID")
    systematic_modes = {"systematic", "scoping", "meta-analysis"}
    if normalized_mode in systematic_modes:
        required_search_fields = {
            "database", "platform", "query", "question_version", "searched_at", "request_id",
            "request_artifact_hash", "result_count", "status",
        }
        logs_valid = bool(search_logs) and all(
            log.get("status") == "EXECUTED_VERIFIED" and required_search_fields <= set(log)
            for log in search_logs
        )
        ledger_valid = bool(screening_ledger and screening_ledger.get("artifact_id") and "record_ids" in screening_ledger and "unresolved_ids" in screening_ledger)
        if not all((logs_valid, screening_complete, protocol_id, eligibility_criteria_id, deduplication_log_id, ledger_valid)):
            raise EvidenceContractError("SYSTEMATIC_WORKFLOW_REQUIRED")
        if set(screening_ledger["record_ids"]) != {record.get("id") for record in records}:
            raise EvidenceContractError("SCREENING_LEDGER_COVERAGE_REQUIRED")
    included = [record for record in records if record.get("screening_decision") == "include"]
    def citation_is_verified(record):
        verification = record.get("citation_verification", {})
        return (
            verification.get("status") == "VERIFIED"
            and verification.get("artifact_id")
            and verification.get("artifact_hash")
            and (record.get("doi") or record.get("pmid") or record.get("pmcid"))
            and record.get("title")
        )
    if any(not citation_is_verified(record) for record in included):
        raise EvidenceContractError("CITATION_VERIFICATION_REQUIRED")
    excluded = [record for record in records if record.get("screening_decision") == "exclude"]
    if any(
        not all(record.get(field) for field in ("exclusion_reason", "eligibility_rule_id", "screening_artifact_id"))
        for record in excluded
    ):
        raise EvidenceContractError("EXCLUSION_PROVENANCE_REQUIRED")
    if normalized_mode == "meta-analysis":
        required_effect_fields = {
            "study_id", "outcome", "metric", "time_point", "population", "effect",
            "standard_error", "denominator", "analysis_unit", "source_locator", "extraction_artifact_hash",
        }
        effects = extracted_effects or []
        if (
            len(effects) < 2
            or not analysis_plan
            or not analysis_plan.get("artifact_id")
            or not analysis_plan.get("artifact_hash")
            or any(not required_effect_fields <= set(effect) for effect in effects)
            or len({effect.get("study_id") for effect in effects}) != len(effects)
            or any(record.get("access_state") != "full-text" for record in included)
        ):
            raise EvidenceContractError("EXTRACTABLE_EFFECT_DATA_REQUIRED")

    prepared = []
    for record in included:
        item = deepcopy(record)
        item["source_text_trust"] = "UNTRUSTED_CONTENT"
        prepared.append(item)
    theme_directions: dict[str, set[str]] = {}
    for record in prepared:
        if record.get("theme") and record.get("direction"):
            theme_directions.setdefault(record["theme"], set()).add(record["direction"])
    contradictions = [
        {"theme": theme, "directions": sorted(directions)}
        for theme, directions in sorted(theme_directions.items())
        if len(directions) > 1
    ]
    return {
        "mode": normalized_mode,
        "records": prepared,
        "contradictions": contradictions,
        "systematic_completeness": normalized_mode in {"systematic", "scoping", "meta-analysis"},
        "meta_analysis_ready": normalized_mode == "meta-analysis",
        "excluded_records": excluded,
        "unresolved_records": [record for record in records if record.get("screening_decision") == "unresolved"],
    }
