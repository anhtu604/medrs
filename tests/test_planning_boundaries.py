from pathlib import Path

from medical_research_skills_vn.contracts import load_contract, planning_decision


ROOT = Path(__file__).parents[1]


def test_design_skill_does_not_own_sample_size_calculation():
    contract = load_contract(ROOT, "de-cuong-va-thiet-ke")
    assert "sample_size_calculation" not in contract["owns"]
    assert "sample_size_calculation" in contract["forbids"]


def test_analysis_plan_rejects_observed_outcome_model_selection():
    decision = planning_decision(
        load_contract(ROOT, "co-mau-va-ke-hoach-phan-tich"),
        requested_action="select_model_from_observed_p_values",
    )
    assert decision == "REFUSE_AND_EXPLAIN"


def test_analysis_plan_owns_estimand_and_power():
    contract = load_contract(ROOT, "co-mau-va-ke-hoach-phan-tich")
    assert {"estimand", "sample_size_calculation", "sensitivity_plan"} <= set(contract["owns"])


def test_design_skill_owns_sampling_strategy_not_numeric_size():
    contract = load_contract(ROOT, "de-cuong-va-thiet-ke")
    assert "sampling_strategy" in contract["owns"]
    assert planning_decision(contract, "define_sampling_strategy") == "ALLOW"
