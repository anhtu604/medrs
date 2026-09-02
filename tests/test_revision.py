import pytest

from medical_research_skills_vn.revision import (
    RevisionContractError,
    build_response_matrix,
    check_numeric_propagation,
    re_review_commitments,
)


def _comment(decision="accept"):
    return {
        "id": "R1-C1",
        "reviewer": "Reviewer 1",
        "verbatim": "Clarify the adjusted effect estimate.",
        "classification": "methods-and-results",
        "decision": decision,
        "rationale": "The request improves reproducibility.",
    }


def test_every_reviewer_request_is_tracked_with_a_verbatim_source():
    matrix = build_response_matrix(
        comments=[_comment()],
        changes=[{"comment_id": "R1-C1", "artifact": "manuscript-v2.docx", "locator": "P12", "artifact_hash": "a" * 64}],
        evidence=[{"comment_id": "R1-C1", "source": "analysis-log", "locator": "model-2"}],
    )
    assert matrix["status"] == "READY_FOR_RE_REVIEW"
    assert matrix["rows"][0]["comment_id"] == "R1-C1"
    assert matrix["rows"][0]["commitment"]["artifact_hash"] == "a" * 64


def test_acceptance_without_changed_artifact_is_blocked():
    with pytest.raises(RevisionContractError, match="RESPONSE_WITHOUT_CHANGE"):
        build_response_matrix(comments=[_comment()], changes=[], evidence=[])


def test_declining_or_partially_accepting_requires_evidence():
    comment = _comment(decision="decline")
    with pytest.raises(RevisionContractError, match="DECISION_EVIDENCE_REQUIRED"):
        build_response_matrix(comments=[comment], changes=[], evidence=[])


def test_changed_number_must_propagate_to_all_registered_locations():
    result = check_numeric_propagation(
        claim_id="primary-effect",
        new_value="1.42",
        expected_locations=["abstract:P4", "results:T2", "discussion:P2"],
        observed_values={"abstract:P4": "1.42", "results:T2": "1.42", "discussion:P2": "1.31"},
    )
    assert result["status"] == "PROPAGATION_INCOMPLETE"
    assert result["mismatches"] == [{"locator": "discussion:P2", "observed": "1.31"}]


def test_changed_artifact_hash_forces_re_review():
    matrix = build_response_matrix(
        comments=[_comment()],
        changes=[{"comment_id": "R1-C1", "artifact": "manuscript-v2.docx", "locator": "P12", "artifact_hash": "a" * 64}],
        evidence=[{"comment_id": "R1-C1", "source": "analysis-log", "locator": "model-2"}],
    )
    result = re_review_commitments(matrix, {"manuscript-v2.docx": "b" * 64})
    assert result["status"] == "RE_REVIEW_REQUIRED"
    assert result["stale_comments"] == ["R1-C1"]


def test_duplicate_comment_ids_are_rejected():
    with pytest.raises(RevisionContractError, match="DUPLICATE_COMMENT_ID"):
        build_response_matrix(comments=[_comment(), _comment()], changes=[], evidence=[])
