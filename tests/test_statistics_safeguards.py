from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/phan-tich-so-lieu/scripts"))


def api():
    import statistics_policy
    return statistics_policy


def test_posthoc_multiple_tests_never_confirmatory():
    report = api().interpretation_ceiling({"design": "cross-sectional", "prespecified": False}, {"multiple_tests": True, "multiplicity_addressed": False})
    assert report["confirmatory_allowed"] is False
    assert report["causal_allowed"] is False
    assert "EXPLORATORY" in report["qualifications"]


def test_unknown_multiplicity_is_not_implicitly_resolved():
    report = api().interpretation_ceiling({"design": "cross-sectional", "prespecified": True}, {})
    assert report["confirmatory_allowed"] is False
    assert "MULTIPLICITY_UNKNOWN" in report["unresolved"]


def test_adjustment_claim_cannot_resolve_unknown_test_family():
    report = api().interpretation_ceiling({"prespecified": True}, {"multiplicity_addressed": True})
    assert report["confirmatory_allowed"] is False


def test_clustered_observations_not_treated_as_independent():
    report = api().select_basic_test({"outcome_type": "continuous", "paired": False, "clustered": True, "mean_inference_supported": True})
    assert report["status"] == "SPECIALIST_REVIEW_REQUIRED"
    assert report["test"] is None


def test_missing_effect_measure_not_verified_identity():
    issues = api().validate_extraction({"source_locator": "Table 1", "outcome": "A", "group": "B", "time": "baseline", "adjustment": "unadjusted", "outcome_available_n": 10, "reported_n": 10})
    assert "EFFECT_MEASURE_REQUIRED" in issues


def test_unverified_runtime_and_failed_ph_have_explicit_ceiling():
    report = api().interpretation_ceiling({"prespecified": True, "design": "cohort"}, {"multiple_tests": False, "status": "NOT_RUN", "model": "cox", "ph_pass": False})
    assert "EXECUTION_UNVERIFIED" in report["unresolved"]
    assert "NONPROPORTIONAL_HAZARDS" in report["qualifications"]
    assert report["causal_allowed"] is False


def test_causal_language_requires_more_than_randomized_label():
    report = api().interpretation_ceiling({"prespecified": True, "design": "randomized-trial"}, {"multiple_tests": False})
    assert report["causal_allowed"] is False


def test_only_complete_assessed_randomized_inference_can_pass_causal_ceiling():
    report = api().interpretation_ceiling({"prespecified": True, "design": "randomized-trial", "randomization_verified": True}, {"multiple_tests": False, "status": "RUN_VERIFIED", "causal_assumptions_met": True})
    assert report["confirmatory_allowed"] is True
    assert report["causal_allowed"] is True


def test_paired_t_does_not_use_raw_before_after_normality_as_sufficient():
    problem = {"outcome_type": "continuous", "paired": True, "mean_difference_estimand": True, "raw_values_normal": True}
    assert api().select_basic_test(problem)["status"] == "ASSUMPTIONS_REQUIRED"
    problem["difference_mean_inference_supported"] = True
    assert api().select_basic_test(problem)["test"] == "paired-t"


def test_sparse_independent_count_table_routes_to_fisher_not_paired_test():
    report = api().select_basic_test({"outcome_type": "categorical", "paired": False, "sparse": True, "counts_verified": True})
    assert report["test"] == "fisher-exact"


def test_paired_categorical_data_not_routed_to_independent_fisher():
    report = api().select_basic_test({"outcome_type": "categorical", "paired": True, "sparse": True, "counts_verified": True})
    assert report["test"] == "paired-categorical-review"


def test_outcome_available_n_and_measure_identity_are_checked():
    issues = api().validate_extraction({"source_locator": "Table 2", "outcome": "Outcome A", "group": "Group A", "time": "6 months", "adjustment": "unadjusted", "outcome_available_n": 95, "recruited_n": 120, "reported_n": 120, "measure": "OR", "reported_measure": "PR"})
    assert "OUTCOME_DENOMINATOR_MISMATCH" in issues
    assert "EFFECT_MEASURE_MISMATCH" in issues


def test_secondary_table_and_missing_group_not_verified_extraction():
    issues = api().validate_extraction({"source_locator": "Secondary table", "secondary_only": True, "outcome_available_n": 20, "reported_n": 20})
    assert "PRIMARY_SOURCE_REQUIRED" in issues
    assert "IDENTITY_REQUIRED:group" in issues


def test_threshold_without_approved_protocol_is_exploratory():
    report = api().threshold_policy({"requested": True, "source_kind": "single-study", "source_url": "https://example.invalid/synthetic", "protocol_approved": False})
    assert report["classification"] == "EXPLORATORY"
    assert report["all_attempts_required"] is True


def test_no_requested_threshold_keeps_continuous_variable():
    assert api().threshold_policy({})["mode"] == "CONTINUOUS"


@pytest.mark.parametrize("value", [0, 0.0000002, 0.5, 1.0])
def test_p_format_never_reports_equal_zero(value):
    text = api().format_p(value, digits=3)
    assert text != "0.000"
    assert text == ("<0.001" if value < 0.001 else f"{value:.3f}")


@pytest.mark.parametrize("value", [-0.1, 1.1, float("nan")])
def test_invalid_p_not_clipped(value):
    with pytest.raises(ValueError):
        api().format_p(value)
