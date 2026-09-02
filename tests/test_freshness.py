from datetime import date

from medical_research_skills_vn.freshness import verification_status


def test_stale_source_keeps_original_verification_date():
    record = {"last_verified": "2025-01-01", "expires_after_days": 90}
    before = dict(record)
    assert verification_status(record, date(2026, 8, 29)) == "STALE"
    assert record == before


def test_current_source_is_current_on_expiry_boundary():
    record = {"last_verified": "2026-06-01", "expires_after_days": 89}
    assert verification_status(record, date(2026, 8, 29)) == "CURRENT"


def test_missing_verification_date_is_unverified():
    assert verification_status({"last_verified": None, "expires_after_days": 90}, date(2026, 8, 29)) == "UNVERIFIED"
