"""Design-matched, evidence-traceable quality and certainty contracts."""

from pathlib import Path

from .coverage import load_coverage_manifest


ROOT = Path(__file__).parents[2]
ROB2_PATH = ROOT / "coverage/rob2-parallel-2019.yaml"
ROB2_RESPONSES = {"Y", "PY", "PN", "N", "NI", "NA"}
ROB2_ARTIFACT_SHA256 = "B79474C4FED5CFD666110EBF118F8DB9C36747F97362C2D4E93ECB540B294BF6"
GRADE_RATINGS = {"not-serious", "serious", "very-serious", "unresolved"}
CERQUAL_CONCERNS = {"none-or-very-minor", "minor", "moderate", "serious", "unresolved"}


def _valid_locator(value: str) -> bool:
    return isinstance(value, str) and ":" in value and len(value.split(":", 1)[0].strip()) >= 2 and "fake" not in value.casefold()


class QualityContractError(ValueError):
    pass


def select_appraisal_framework(study_design: str) -> str:
    design = study_design.casefold()
    if any(term in design for term in ("cluster randomized", "cluster-randomized", "crossover", "cross-over")):
        return "ROB2_DESIGN_SPECIFIC_MODULE_REQUIRED"
    if "random" in design and "parallel" in design:
        return "ROB2_PARALLEL_2019"
    if "qualitative evidence synthesis" in design or "tổng hợp định tính" in design:
        return "GRADE_CERQUAL_2018"
    if any(term in design for term in ("cohort", "case-control", "non-random")):
        return "ROBINS_I_OFFICIAL_TOOL_REQUIRED"
    return "OFFICIAL_TOOL_REQUIRED"


def appraise_rob2(*, outcome_id: str, estimand: str, answers: dict, official_algorithm: dict) -> dict:
    if not outcome_id or estimand not in {"effect-of-assignment", "effect-of-adhering"}:
        raise QualityContractError("OUTCOME_AND_ESTIMAND_REQUIRED")
    if estimand == "effect-of-adhering":
        raise QualityContractError("OFFICIAL_ADHERENCE_MODULE_REQUIRED")
    manifest = load_coverage_manifest(ROB2_PATH)
    expected = manifest["expected_ids"]
    missing = [identifier for identifier in expected if identifier not in answers]
    if missing:
        return {
            "framework": "ROB2_PARALLEL_2019",
            "outcome_id": outcome_id,
            "estimand": estimand,
            "status": "INCOMPLETE",
            "missing_question_ids": missing,
            "domain_judgments": {},
            "overall_judgment": "UNRESOLVED",
        }
    for identifier in expected:
        answer = answers[identifier]
        if answer.get("response") not in ROB2_RESPONSES:
            raise QualityContractError(f"ROB2_RESPONSE_INVALID:{identifier}")
        if not answer.get("rationale") or not _valid_locator(answer.get("source_locator")):
            raise QualityContractError(f"EVIDENCE_LOCATOR_REQUIRED:{identifier}")
    if (
        official_algorithm.get("version") != manifest["version"]
        or str(official_algorithm.get("artifact_hash", "")).upper() != ROB2_ARTIFACT_SHA256
    ):
        raise QualityContractError("OFFICIAL_ALGORITHM_REQUIRED")
    judgments = official_algorithm.get("domain_judgments", {})
    if set(judgments) != {"D1", "D2", "D3", "D4", "D5", "overall"} or any(
        value not in {"Low", "Some concerns", "High"} for value in judgments.values()
    ):
        raise QualityContractError("OFFICIAL_ALGORITHM_OUTPUT_INCOMPLETE")
    if any(answer["response"] == "NI" for answer in answers.values()) and judgments.get("overall") == "Low":
        raise QualityContractError("LOW_JUDGMENT_UNSUPPORTED_WITH_NO_INFORMATION")
    return {
        "framework": "ROB2_PARALLEL_2019",
        "outcome_id": outcome_id,
        "estimand": estimand,
        "status": "COMPLETE",
        "missing_question_ids": [],
        "domain_judgments": {key: judgments[key] for key in ("D1", "D2", "D3", "D4", "D5")},
        "overall_judgment": judgments["overall"],
        "algorithm_artifact_hash": official_algorithm["artifact_hash"],
    }


def assess_grade(*, outcome_id: str, starting_design: str, domain_judgments: dict) -> dict:
    required = {"risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias"}
    if not outcome_id or set(domain_judgments) & required != required:
        raise QualityContractError("GRADE_DOMAIN_EVIDENCE_REQUIRED")
    for domain in required:
        judgment = domain_judgments[domain]
        if judgment.get("rating") not in GRADE_RATINGS or not judgment.get("rationale") or not _valid_locator(judgment.get("source_locator")):
            raise QualityContractError(f"GRADE_DOMAIN_EVIDENCE_REQUIRED:{domain}")
    if any(domain_judgments[domain]["rating"] == "unresolved" for domain in required):
        certainty = "UNRESOLVED"
    else:
        levels = ["VERY_LOW", "LOW", "MODERATE", "HIGH"]
        index = 3 if starting_design.casefold() == "rct" else 1
        for domain in required:
            rating = domain_judgments[domain]["rating"]
            index -= 2 if rating == "very-serious" else 1 if rating == "serious" else 0
        upgrades = sum(
            1 for key in ("large_effect", "dose_response", "residual_confounding")
            if domain_judgments.get(key, {}).get("rating") == "upgrade"
            and domain_judgments[key].get("rationale")
            and _valid_locator(domain_judgments[key].get("source_locator"))
        )
        index = min(3, index + upgrades)
        certainty = levels[max(0, index)]
    return {"framework": "GRADE_6.5.1", "outcome_id": outcome_id, "certainty": certainty, "domains": domain_judgments}


def assess_cerqual(*, finding_id: str, components: dict) -> dict:
    required = {"methodological_limitations", "coherence", "adequacy", "relevance"}
    if not finding_id or set(components) != required:
        raise QualityContractError("CERQUAL_COMPONENTS_REQUIRED")
    for component, judgment in components.items():
        if judgment.get("concern") not in CERQUAL_CONCERNS or not judgment.get("rationale") or not _valid_locator(judgment.get("source_locator")):
            raise QualityContractError(f"CERQUAL_COMPONENT_EVIDENCE_REQUIRED:{component}")
    concerns = [components[name]["concern"] for name in required]
    if "unresolved" in concerns:
        confidence = "UNRESOLVED"
    elif all(value == "none-or-very-minor" for value in concerns):
        confidence = "HIGH"
    elif "serious" in concerns:
        confidence = "LOW"
    else:
        confidence = "MODERATE"
    return {"framework": "GRADE_CERQUAL_2018", "finding_id": finding_id, "confidence": confidence, "components": components}
