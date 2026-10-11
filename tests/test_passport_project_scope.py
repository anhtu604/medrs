from copy import deepcopy
from medical_research_skills_vn import passport as api


def test_old_passport_extensions_survive_confirmation():
    old = api.new_passport("parent", "thesis", "vi-medical-academic")
    old["custom_extension"] = {"local": [1, 2]}
    result = api.confirm_field(old, "/study_design", "cohort", "author", "2026-10-11")
    assert result["custom_extension"] == old["custom_extension"]
    assert result["schema_version"] == "2.0.0"
    assert api.validate_passport(result) == []


def test_child_never_inherits_parent_results_population_or_objectives():
    parent = api.new_passport("parent", "thesis", "vi-medical-academic")
    parent["verified_results"] = [{"N": 120}]
    parent["population"]["value"] = "All patients"
    original = deepcopy(parent)
    child = api.create_child_passport(parent, "child", "manuscript")
    assert child["parent_project_id"] == "parent"
    assert child["verified_results"] == []
    assert child["population"]["status"] == "UNRESOLVED"
    assert child["population"]["value"] is None
    assert child["objectives"]["status"] == "UNRESOLVED"
    assert parent == original
    assert api.validate_passport(child) == []


def test_conflicting_design_retained_not_silently_overwritten():
    passport = api.new_passport("p", "thesis", "vi-medical-academic")
    passport = api.confirm_field(passport, "/study_design", "cohort", "author", "2026-10-11")
    original = deepcopy(passport)
    result = api.reconcile_project_evidence(passport, [{"field": "study_design", "value": "cross-sectional", "source": "draft.docx"}])
    assert result["study_design"]["value"] == "cohort"
    assert result["conflicts"][0]["field"] == "study_design"
    assert "AUTHOR_APPROVAL_REQUIRED" in result["unresolved_markers"]
    assert passport == original


def test_new_extracted_value_remains_inferred():
    passport = api.new_passport("p", "thesis", "vi-medical-academic")
    result = api.reconcile_project_evidence(passport, [{"field": "study_design", "value": "cohort", "source": "draft.docx"}])
    assert result["study_design"]["status"] == "DRAFT_INFERRED"
    assert result["study_design"]["confirmed_by"] is None
    assert result["study_design"]["marker"] == "AUTHOR_APPROVAL_REQUIRED"
