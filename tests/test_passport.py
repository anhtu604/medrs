from copy import deepcopy
from datetime import datetime, timezone

from medical_research_skills_vn.passport import confirm_field, new_passport, validate_passport


def test_new_passport_never_presents_unknowns_as_facts():
    passport = new_passport("p-001", "thesis", "vi-medical-academic")
    assert passport["research_question"]["status"] == "UNRESOLVED"
    assert passport["research_question"]["marker"] == "DATA_REQUIRED"
    assert passport["locale_profile"] == "vi-medical-academic"
    assert validate_passport(passport) == []


def test_confirm_field_creates_audit_event_without_mutating_input():
    passport = new_passport("p-001", "protocol", "en-medical-academic")
    original = deepcopy(passport)
    confirmed = confirm_field(
        passport,
        "/research_question",
        value="Does exposure X predict outcome Y?",
        author="researcher-01",
        timestamp="2026-08-29T10:00:00+00:00",
    )
    assert passport == original
    assert confirmed["research_question"]["status"] == "CONFIRMED"
    assert confirmed["research_question"]["confirmed_by"] == "researcher-01"
    assert confirmed["audit_log"][-1]["action"] == "CONFIRM_FIELD"


def test_validation_rejects_confirmed_field_without_author():
    passport = new_passport("p-001", "protocol", "vi-medical-academic")
    passport["research_question"].update(
        {"value": "Question", "status": "CONFIRMED", "confirmed_by": None, "marker": None}
    )
    codes = {issue.code for issue in validate_passport(passport)}
    assert "CONFIRMED_WITHOUT_AUTHOR" in codes

