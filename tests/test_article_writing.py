import json
from pathlib import Path

import pytest
from jsonschema import validate

from medical_research_skills_vn.writing import (
    WritingContractError,
    build_discussion_blueprint,
    build_section_artifact,
    stable_snapshot_hash,
    validate_abstract_consistency,
)
from medical_research_skills_vn.manuscript import assemble_manuscript


ROOT = Path(__file__).parents[1]


def verified_inputs():
    return {
        "passport_hash": "passport-sha256",
        "target_profile": "journal-example-2026",
        "locale_profile": "vi-medical-academic@1.0.0",
        "outline_approved": True,
        "source_ledger_version": "ledger-3",
        "word_budget": 500,
    }


def test_results_refuses_unverified_numbers_and_never_interprets():
    with pytest.raises(WritingContractError, match="VERIFIED_RESULTS_REQUIRED"):
        build_section_artifact(
            section="results",
            inputs=verified_inputs(),
            claims=[{"text": "Tỷ lệ đáp ứng là 61%", "result_verified": False}],
        )

    with pytest.raises(WritingContractError, match="RESULT_ARTIFACT_LOCATOR_REQUIRED"):
        build_section_artifact(
            section="results",
            inputs=verified_inputs(),
            claims=[{"text": "Tỷ lệ đáp ứng là 61%", "result_verified": True}],
        )

    with pytest.raises(WritingContractError, match="RESULTS_INTERPRETATION_NOT_ALLOWED"):
        build_section_artifact(
            section="results",
            inputs=verified_inputs(),
            claims=[
                {
                    "text": "Tỷ lệ đáp ứng là 61%, chứng tỏ can thiệp rất hiệu quả",
                    "result_verified": True,
                    "artifact_id": "run-1",
                    "locator": "table-2:row-3",
                    "kind": "interpretation",
                }
            ],
        )


def test_results_blocks_causal_mechanism_recommendation_and_value_judgment_flags():
    for forbidden_flag in ("causal", "mechanism", "recommendation", "value_judgment"):
        with pytest.raises(WritingContractError, match="RESULTS_INTERPRETATION_NOT_ALLOWED"):
            build_section_artifact(
                section="results",
                inputs=verified_inputs(),
                claims=[
                    {
                        "text": "Verified result",
                        "result_verified": True,
                        "artifact_id": "run-1",
                        "locator": "table-2:row-3",
                        forbidden_flag: True,
                    }
                ],
            )


def test_literature_review_rejects_author_by_author_catalogue():
    with pytest.raises(WritingContractError, match="THEMATIC_SYNTHESIS_REQUIRED"):
        build_section_artifact(
            section="literature-review",
            inputs=verified_inputs(),
            claims=[
                {"text": "Nguyễn et al. found A.", "source_verified": True, "theme": None},
                {"text": "Smith et al. found B.", "source_verified": True, "theme": None},
            ],
        )


def test_discussion_blueprint_requires_lawful_full_text_and_author_approval():
    with pytest.raises(WritingContractError, match="FULL_TEXT_REQUIRED"):
        build_discussion_blueprint(
            comparators=[{"doi": "10.1/example", "access": "abstract-only"}],
            paper_selection_approved=True,
            blueprint_approved=True,
        )


def test_discussion_requires_inferential_and_audit_artifacts():
    with pytest.raises(WritingContractError, match="DISCUSSION_PREFLIGHT_REQUIRED"):
        build_section_artifact(
            section="discussion",
            inputs=verified_inputs() | {"discussion_blueprint_approved": True},
            claims=[],
        )

    with pytest.raises(WritingContractError, match="AUTHOR_APPROVAL_REQUIRED"):
        build_discussion_blueprint(
            comparators=[{"doi": "10.1/example", "access": "author-supplied-full-text"}],
            paper_selection_approved=True,
            blueprint_approved=False,
        )


def test_discussion_rejects_phrase_copy_and_observational_causal_overreach():
    inputs = verified_inputs() | {
        "discussion_blueprint_approved": True,
        "study_design": "cohort",
        "inferential_ceiling": "association",
    }
    with pytest.raises(WritingContractError, match="PHRASE_COPY_NOT_ALLOWED"):
        build_section_artifact(
            section="discussion",
            inputs=inputs,
            claims=[{"text": "copied phrase", "copied_from_comparator": True}],
        )
    with pytest.raises(WritingContractError, match="CAUSAL_OVERREACH"):
        build_section_artifact(
            section="discussion",
            inputs=inputs,
            claims=[
                {
                    "text": "Phơi nhiễm gây ra kết cục",
                    "result_verified": True,
                    "source_verified": True,
                    "causal": True,
                }
            ],
        )


def test_conclusion_rejects_new_findings_and_unsupported_recommendations():
    with pytest.raises(WritingContractError, match="NEW_FINDING_NOT_ALLOWED"):
        build_section_artifact(
            section="conclusion",
            inputs=verified_inputs() | {"study_design": "randomized-trial", "inferential_ceiling": "causal"},
            claims=[{"text": "Một phân tích mới cho thấy...", "present_in_results": False}],
        )

    with pytest.raises(WritingContractError, match="OVERCLAIM_BLOCKED"):
        build_section_artifact(
            section="conclusion",
            inputs=verified_inputs() | {"study_design": "randomized-trial", "inferential_ceiling": "causal"},
            claims=[
                {
                    "text": "Nên triển khai thường quy",
                    "present_in_results": True,
                    "recommendation": True,
                    "recommendation_basis": {
                        "design": True,
                        "certainty": False,
                        "benefit_harm": True,
                        "feasibility": True,
                        "scope": True,
                    },
                }
            ],
        )

    with pytest.raises(WritingContractError, match="CAUSAL_OVERREACH"):
        build_section_artifact(
            section="conclusion",
            inputs=verified_inputs() | {"study_design": "cohort", "inferential_ceiling": "association"},
            claims=[{"text": "Phơi nhiễm gây bệnh", "present_in_results": True, "causal": True}],
        )


def test_abstract_is_last_and_must_match_verified_full_text():
    with pytest.raises(WritingContractError, match="FULL_TEXT_REQUIRED"):
        build_section_artifact(
            section="abstract",
            inputs=verified_inputs() | {"full_text_ready": False},
            claims=[],
        )

    issues = validate_abstract_consistency(
        abstract_facts={"n": 120, "primary_effect": "RR 0.80"},
        full_text_facts={"n": 118, "primary_effect": "RR 0.80"},
    )
    assert issues == ["ABSTRACT_FULL_TEXT_MISMATCH:n"]


def test_abstract_skeleton_is_allowed_but_not_submission_ready():
    artifact = build_section_artifact(
        section="abstract",
        inputs=verified_inputs()
        | {"full_text_ready": False, "abstract_state": "SKELETON"},
        claims=[],
    )
    assert artifact["lifecycle_state"] == "SKELETON"
    assert artifact["submission_verdict"] == "BLOCKED_INCOMPLETE_MANUSCRIPT"


def test_final_abstract_requires_snapshot_consistency_numeric_provenance_and_novelty():
    snapshot = {"n": 118, "primary_effect": "RR 0.80"}
    base = verified_inputs() | {
        "full_text_ready": True,
        "abstract_state": "FINAL_VERIFIED",
        "manuscript_hash": stable_snapshot_hash(snapshot),
        "manuscript_snapshot": snapshot,
        "manuscript_version": "v7",
        "generation_timestamp": "2026-09-02T10:00:00+07:00",
        "abstract_facts": {"n": 120},
        "full_text_facts": {"n": 118},
        "required_consistency_fields": ["n"],
    }
    with pytest.raises(WritingContractError, match="BLOCKED_CONFLICT"):
        build_section_artifact(section="abstract", inputs=base, claims=[])

    consistent = base | {"abstract_facts": {"n": 118}}
    with pytest.raises(WritingContractError, match="NUMERIC_PROVENANCE_REQUIRED"):
        build_section_artifact(
            section="abstract",
            inputs=consistent,
            claims=[{"text": "N = 118", "numeric": True}],
        )

    with pytest.raises(WritingContractError, match="NOVELTY_VERIFICATION_REQUIRED"):
        build_section_artifact(
            section="abstract",
            inputs=consistent,
            claims=[{"text": "Đây là nghiên cứu đầu tiên.", "full_text_locator": "conclusion:p1"}],
        )


def test_section_artifact_uses_shared_preflight_and_matches_schema():
    artifact = build_section_artifact(
        section="introduction",
        inputs=verified_inputs(),
        claims=[
            {
                "text": "Khoảng trống bằng chứng đã được xác định.",
                "source_verified": True,
                "evidence_id": "doi:10.1/source",
            }
        ],
    )
    schema = json.loads((ROOT / "schemas" / "section-artifact.schema.json").read_text(encoding="utf-8"))

    validate(instance=artifact, schema=schema)
    assert artifact["preflight"]["contract"] == "shared-writing-preflight"
    assert artifact["full_gate"]["status"] == "PENDING"


def test_manuscript_assembly_runs_one_document_gate_not_one_per_writer():
    sections = [
        {"section": "introduction", "draft": "Intro", "full_gate": {"status": "PENDING"}},
        {"section": "methods", "draft": "Methods", "full_gate": {"status": "PENDING"}},
        {"section": "results", "draft": "Results", "full_gate": {"status": "PENDING"}},
        {"section": "discussion", "draft": "Discussion", "full_gate": {"status": "PENDING"}},
    ]

    manuscript = assemble_manuscript(sections=sections, substantive_revision=False)

    assert manuscript["full_gate_invocations"] == 1
    assert manuscript["full_gate_scope"] == "assembled-document"


def test_manuscript_assembly_propagates_section_blockers():
    manuscript = assemble_manuscript(
        sections=[
            {
                "section": "abstract",
                "draft": "",
                "markers": ["NOVELTY_VERIFICATION_REQUIRED"],
                "preflight": {"status": "REVISE"},
                "full_gate": {"status": "PENDING"},
            }
        ],
        substantive_revision=False,
    )
    assert manuscript["status"] == "BLOCKED"
    assert "NOVELTY_VERIFICATION_REQUIRED" in manuscript["blockers"]
