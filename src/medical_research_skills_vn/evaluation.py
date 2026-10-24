"""Deterministic offline acceptance scenarios."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from .contracts import load_contract, planning_decision
from .document_types import load_document_type
from .ethics import build_ethics_artifact
from .evidence import EvidenceContractError, synthesize_evidence
from .methods import draft_methods
from .passport import confirm_field, new_passport, validate_passport
from .quality import assess_cerqual
from .routing import RoutingRequest, route_request
from .structure_profiles import load_structure_profile, verify_profile_source
from .writing import build_discussion_blueprint


@dataclass
class ScenarioResult:
    name: str
    artifacts: dict
    errors: list[str]


def run_scenario(path: Path, root: Path) -> ScenarioResult:
    case = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    active = set(case["active_skills"])
    route = route_request(RoutingRequest(text=case["request"], attachments=tuple(case.get("attachments", ()))), {}, active)
    workflow = case.get("workflow", "protocol")
    expected = case.get("expect", {})
    if workflow != "protocol":
        errors = []
        if route.canonical != expected.get("route"):
            errors.append(f"route: expected {expected.get('route')}, got {route.canonical}")
        if route.mode != expected.get("mode"):
            errors.append(f"mode: expected {expected.get('mode')}, got {route.mode}")
        artifacts = {"route": route}
        if workflow == "topic-understanding":
            artifacts["understanding"] = _run_understanding_steps(root, case.get("steps", []))
            for key in ("next_part", "status", "error"):
                if key in expected and artifacts["understanding"][key] != expected[key]:
                    errors.append(f"understanding {key}: expected {expected[key]}, got {artifacts['understanding'][key]}")
        elif workflow == "systematic-empty":
            synthesis = _empty_systematic_synthesis("systematic")
            artifacts["synthesis"] = synthesis
            if synthesis["systematic_completeness"] != expected["systematic_completeness"]:
                errors.append("systematic completeness mismatch")
        elif workflow == "meta-analysis-guard":
            try:
                _empty_systematic_synthesis("meta-analysis")
                errors.append("meta-analysis unexpectedly passed without effect data")
            except EvidenceContractError as exc:
                artifacts["blocked_by"] = str(exc)
                if str(exc) != expected["blocked_by"]:
                    errors.append(f"meta-analysis: expected {expected['blocked_by']}, got {exc}")
        elif workflow == "cerqual":
            components = {
                name: {"concern": "none-or-very-minor", "rationale": "fixture evidence", "source_locator": f"fixture:{name}"}
                for name in ("methodological_limitations", "coherence", "adequacy", "relevance")
            }
            appraisal = assess_cerqual(finding_id="finding-1", components=components)
            artifacts["appraisal"] = appraisal
            if appraisal["confidence"] != expected["confidence"]:
                errors.append("CERQual confidence mismatch")
        elif workflow == "hmu-profile":
            profile = load_structure_profile(Path(root) / "profiles/institution/hmu/word-format-master-2020-current-2026.yaml")
            verification = verify_profile_source(root, profile)
            artifacts["profile_verification"] = verification
            if verification["status"] != expected["source_status"]:
                errors.append("HMU source verification failed")
        elif workflow == "discussion-blueprint":
            blueprint = build_discussion_blueprint(
                document_type_profile=load_document_type(root, case["document_type"])
            )
            artifacts["blueprint"] = blueprint
            if "limitation" in blueprint["moves"]:
                errors.append("discussion: limitations repeated in every argument paragraph")
            closing = blueprint["closing_sections"][0]
            if closing["id"] != "strengths_and_limitations" or closing["order"] != ["strengths", "limitations"]:
                errors.append("discussion: strengths and limitations are not one strength-first section")
        return ScenarioResult(name=case["name"], artifacts=artifacts, errors=errors)

    passport = new_passport(case["project_id"], "protocol", case["locale_profile"])
    for field, value in case.get("author_confirmed_fields", {}).items():
        passport = confirm_field(
            passport,
            f"/{field}",
            value=value,
            author=case["author_id"],
            timestamp=case["confirmation_timestamp"],
        )

    ethics = build_ethics_artifact(**case["ethics"])
    methods = draft_methods(
        mode="protocol",
        planned_procedures=case["planned_procedures"],
        confirmed_procedures=[],
        deviations=[],
        locale_profile=case["locale_profile"],
        multi_section=True,
    )
    boundaries = {
        "design_sampling": planning_decision(
            load_contract(root, "de-cuong-va-thiet-ke"), "define_sampling_strategy"
        ),
        "analysis_power": planning_decision(
            load_contract(root, "co-mau-va-ke-hoach-phan-tich"), "sample_size_calculation"
        ),
    }

    errors = [f"passport:{issue.code}" for issue in validate_passport(passport)]
    expected = case.get("expect", {})
    if route.canonical != expected.get("route"):
        errors.append(f"route: expected {expected.get('route')}, got {route.canonical}")
    if expected.get("approval_number") is None and ethics["approval_number"] is not None:
        errors.append("ethics: approval number was invented")
    if expected.get("all_procedures") == "PLANNED" and any(
        claim["execution_status"] != "PLANNED" for claim in methods["procedure_claims"]
    ):
        errors.append("methods: protocol procedure presented as completed")
    if boundaries != {"design_sampling": "ALLOW", "analysis_power": "ALLOW"}:
        errors.append("planning: ownership contract failed")

    return ScenarioResult(
        name=case["name"],
        artifacts={
            "route": route,
            "passport": passport,
            "ethics": ethics,
            "methods": methods,
            "planning_boundaries": boundaries,
        },
        errors=errors,
    )


def _run_understanding_steps(root: Path, steps: list) -> dict:
    """Replay conversation steps on a throwaway workspace; stop at the first refusal."""
    import sys
    import tempfile

    for folder in ("skills/leader-nghien-cuu/scripts", "skills/tim-hieu-de-tai/scripts"):
        if str(Path(root) / folder) not in sys.path:
            sys.path.insert(0, str(Path(root) / folder))
    from project_workspace import initialize_project, set_understanding
    from topic_understanding import status

    day = "2026-10-23"
    with tempfile.TemporaryDirectory() as folder:
        project = Path(folder)
        initialize_project(project, "eval", day)
        error = None
        for kind, value in steps:
            try:
                if kind == "status":
                    set_understanding(project, day, status=value)
                elif kind == "confirm":
                    set_understanding(project, day, status="CONFIRMED", confirmation=value)
                else:
                    set_understanding(project, day, part=kind, part_state=value)
            except ValueError as exc:
                error = str(exc)
                break
        current = status(project)
    return {"next_part": current["next_part"], "status": current["state"], "error": error}


def _empty_systematic_synthesis(mode: str) -> dict:
    log = {
        "database": "fixture-db",
        "platform": "offline-fixture",
        "query": "fixture-query",
        "question_version": "v1",
        "searched_at": "2026-09-02T10:00:00+07:00",
        "request_id": "fixture-request",
        "request_artifact_hash": "a" * 64,
        "result_count": 0,
        "status": "EXECUTED_VERIFIED",
    }
    return synthesize_evidence(
        records=[],
        mode=mode,
        search_logs=[log],
        screening_complete=True,
        extracted_effects=[],
        protocol_id="fixture-protocol",
        eligibility_criteria_id="fixture-eligibility",
        deduplication_log_id="fixture-deduplication",
        screening_ledger={"artifact_id": "fixture-screening", "record_ids": [], "unresolved_ids": []},
        analysis_plan={"artifact_id": "fixture-analysis", "artifact_hash": "b" * 64},
    )
