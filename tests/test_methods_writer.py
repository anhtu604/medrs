from pathlib import Path

from medical_research_skills_vn.methods import draft_methods, load_locale_profile


ROOT = Path(__file__).parents[1]


def test_protocol_keeps_unperformed_procedures_planned():
    artifact = draft_methods(
        mode="protocol",
        planned_procedures=["đo huyết áp theo quy trình chuẩn"],
        confirmed_procedures=[],
        deviations=[],
        locale_profile="vi-medical-academic",
        multi_section=True,
    )

    assert artifact["procedure_claims"] == [
        {"text": "đo huyết áp theo quy trình chuẩn", "execution_status": "PLANNED"}
    ]
    assert artifact["claims_procedure_completed"] is False
    assert artifact["full_gate"]["status"] == "PENDING"


def test_completed_study_uses_only_confirmed_execution_and_flags_the_rest():
    artifact = draft_methods(
        mode="completed-study",
        planned_procedures=["lấy mẫu máu", "đo huyết áp"],
        confirmed_procedures=["đo huyết áp"],
        deviations=["Không lấy mẫu máu"],
        locale_profile="vi-medical-academic",
        multi_section=False,
    )

    assert artifact["procedure_claims"] == [
        {"text": "đo huyết áp", "execution_status": "CONFIRMED_EXECUTED"}
    ]
    assert artifact["deviations"] == ["Không lấy mẫu máu"]
    assert "DATA_REQUIRED" in artifact["markers"]


def test_standalone_methods_does_not_fake_unavailable_slice_two_style_gate():
    artifact = draft_methods(
        mode="protocol",
        planned_procedures=[],
        confirmed_procedures=[],
        deviations=[],
        locale_profile="en-medical-academic",
        multi_section=False,
    )

    assert artifact["full_gate"] == {
        "status": "PENDING",
        "reason": "kiem-van-phong is not active in slice 1",
    }


def test_locale_profiles_encode_distinct_academic_conventions():
    vi = load_locale_profile(ROOT, "vi-medical-academic")
    en = load_locale_profile(ROOT, "en-medical-academic")

    assert vi["academic_rhetoric"]["author_reference"] == "avoid_first_person_by_default"
    assert en["academic_rhetoric"]["author_reference"] == "first_person_permitted_when_clearer"
    assert vi["methods"]["protocol_tense"] == "future_or_planned_construction"
    assert en["methods"]["protocol_tense"] == "future_or_present_for_prespecified_methods"
    assert vi["profile_version"] != en["profile_version"]
