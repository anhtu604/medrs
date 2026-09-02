from pathlib import Path

import pytest

from medical_research_skills_vn.quality import (
    QualityContractError,
    appraise_rob2,
    assess_cerqual,
    assess_grade,
    select_appraisal_framework,
)
from medical_research_skills_vn.quality import ROB2_ARTIFACT_SHA256


ROOT = Path(__file__).parents[1]


def test_design_matched_framework_routing():
    assert select_appraisal_framework("individually randomized parallel trial") == "ROB2_PARALLEL_2019"
    assert select_appraisal_framework("qualitative evidence synthesis") == "GRADE_CERQUAL_2018"
    assert select_appraisal_framework("retrospective cohort intervention") == "ROBINS_I_OFFICIAL_TOOL_REQUIRED"
    assert select_appraisal_framework("cluster randomized parallel trial") == "ROB2_DESIGN_SPECIFIC_MODULE_REQUIRED"


def test_rob2_missing_questions_remain_unresolved_not_low():
    result = appraise_rob2(
        outcome_id="mortality-30d",
        estimand="effect-of-assignment",
        answers={"1.1": {"response": "NI", "rationale": "Not reported", "source_locator": "report:p4"}},
        official_algorithm={"version": "22 August 2019", "artifact_hash": ROB2_ARTIFACT_SHA256, "domain_judgments": {}},
    )
    assert result["status"] == "INCOMPLETE"
    assert result["overall_judgment"] == "UNRESOLVED"
    assert "5.3" in result["missing_question_ids"]


def test_assignment_manifest_cannot_be_reused_for_adherence_estimand():
    with pytest.raises(QualityContractError, match="OFFICIAL_ADHERENCE_MODULE_REQUIRED"):
        appraise_rob2(
            outcome_id="mortality-30d",
            estimand="effect-of-adhering",
            answers={},
            official_algorithm={},
        )


def test_rob2_cannot_claim_low_without_evidence_or_official_algorithm_output():
    answers = {
        item: {"response": "Y", "rationale": "", "source_locator": ""}
        for item in ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2", "4.3", "4.4", "4.5", "5.1", "5.2", "5.3"]
    }
    with pytest.raises(QualityContractError, match="EVIDENCE_LOCATOR_REQUIRED"):
        appraise_rob2(
            outcome_id="mortality-30d", estimand="effect-of-assignment", answers=answers,
            official_algorithm={"version": "22 August 2019", "artifact_hash": "a" * 64, "domain_judgments": {"D1": "Low", "D2": "Low", "D3": "Low", "D4": "Low", "D5": "Low", "overall": "Low"}},
        )


def test_grade_is_outcome_specific_and_rct_is_not_automatically_high():
    with pytest.raises(QualityContractError, match="GRADE_DOMAIN_EVIDENCE_REQUIRED"):
        assess_grade(outcome_id="mortality", starting_design="RCT", domain_judgments={})
    judgments = {
        name: {"rating": "not-serious", "rationale": "Reviewed", "source_locator": f"grade:{name}"}
        for name in ("risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias")
    }
    judgments["risk_of_bias"] = {"rating": "unresolved", "rationale": "RoB incomplete", "source_locator": "rob2:pending"}
    result = assess_grade(outcome_id="mortality", starting_design="RCT", domain_judgments=judgments)
    assert result["certainty"] == "UNRESOLVED"


def test_grade_rejects_unknown_rating_and_fake_locator():
    judgments = {
        name: {"rating": "banana", "rationale": "x", "source_locator": "fake:1"}
        for name in ("risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias")
    }
    with pytest.raises(QualityContractError, match="GRADE_DOMAIN_EVIDENCE_REQUIRED"):
        assess_grade(outcome_id="mortality", starting_design="RCT", domain_judgments=judgments)


def test_cerqual_high_requires_all_four_supported_component_judgments():
    components = {
        name: {"concern": "none-or-very-minor", "rationale": "Supported", "source_locator": f"cerqual:{name}"}
        for name in ("methodological_limitations", "coherence", "adequacy", "relevance")
    }
    assert assess_cerqual(finding_id="finding-1", components=components)["confidence"] == "HIGH"
    components["adequacy"] = {"concern": "unresolved", "rationale": "Thin data", "source_locator": "cerqual:adequacy"}
    assert assess_cerqual(finding_id="finding-1", components=components)["confidence"] == "UNRESOLVED"
