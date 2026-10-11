"""Retrieval outcomes, not clinical judgments or universal host capability."""
from pathlib import Path
import importlib.util
import pytest

ROOT = Path(__file__).parents[1]


def policy():
    spec = importlib.util.spec_from_file_location(
        "access_policy", ROOT / "skills/tim-y-van/scripts/access_policy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def attempt(**changes):
    return {"provider": "Europe PMC", "query": "hypertension AND cohort",
            "time": "2026-10-11T12:00:00+07:00", "http_status": 200,
            "access_level": "metadata", "hits": 0, "error": None} | changes


def test_forbidden_access_does_not_mean_absent_literature():
    assert policy().access_state([{"provider": "pubmed", "http_status": 403, "hits": None}]) == "INACCESSIBLE"


@pytest.mark.parametrize("status", [401,403,404,429,500])
def test_failed_request_never_becomes_success_even_with_claimed_hits(status):
    assert policy().access_state([attempt(http_status=status, hits=1, access_level="full-text")]) == "INACCESSIBLE"


def test_no_hits_requires_executed_query_and_aware_time():
    assert policy().access_state([attempt()]) == "SEARCHED_NO_HITS"
    assert policy().access_state([attempt(query="")]) == "UNRESOLVED"
    assert policy().access_state([attempt(time="2026-10-11")]) == "UNRESOLVED"
    assert policy().access_state([]) == "UNPERFORMED"


def test_partial_failures_are_preserved_not_called_exhaustive_absence():
    attempts = [attempt(), attempt(provider="PubMed", http_status=403, hits=None)]
    assert policy().access_state(attempts) == "INACCESSIBLE"
    receipt = policy().access_summary(attempts)
    assert receipt["attempts"] == attempts
    assert receipt["partial_failure"] is True
    assert receipt["systematic_completeness"] is False
    assert receipt["evidence_verified"] is False


def test_reachable_abstract_limits_claims_despite_other_failure():
    receipt = policy().access_summary([attempt(hits=2, access_level="abstract-only"),
                                      attempt(http_status=403)])
    assert receipt["state"] == "ABSTRACT_ONLY"
    assert receipt["claim_ceiling"] == "ABSTRACT_CONTENT_ONLY"
    assert receipt["partial_failure"] is True


def test_full_text_access_is_not_an_appraisal_or_verified_extraction():
    receipt = policy().access_summary([attempt(hits=1, access_level="full-text")])
    assert receipt["state"] == "FULL_TEXT"
    assert receipt["evidence_verified"] is False


def test_local_vietnamese_source_has_same_access_ceiling_no_quota():
    receipt = policy().access_summary([attempt(provider="VJOL", hits=1, access_level="abstract")])
    assert receipt["state"] == "ABSTRACT_ONLY"
    assert receipt["required_vietnamese_count"] is None


def test_metadata_and_empty_query_are_not_abstracts():
    assert policy().access_state([attempt(hits=3)]) == "METADATA_ONLY"
    assert policy().access_state([attempt(hits=True)]) == "UNRESOLVED"


def test_extraction_retains_identity_errors_locator_and_abstract_ceiling():
    record = {"source_locator": "Table 2", "outcome": "Outcome A", "group": "Group A",
              "time": "6 months", "adjustment": "unadjusted", "outcome_available_n": 95,
              "recruited_n": 120, "reported_n": 120, "measure": "OR", "reported_measure": "PR"}
    receipt = policy().extraction_receipt(record, [attempt(hits=1, access_level="abstract")])
    assert receipt["source_locator"] == "Table 2"
    assert receipt["access_ceiling"] == "ABSTRACT_CONTENT_ONLY"
    assert "OUTCOME_DENOMINATOR_MISMATCH" in receipt["identity_issues"]
    assert "EFFECT_MEASURE_MISMATCH" in receipt["identity_issues"]
    assert receipt["extraction_verified"] is False
