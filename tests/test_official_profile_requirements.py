from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/bo-cuc-tai-lieu/scripts"))


def valid_source():
    return {"source_kind": "presentation-rules", "source_hash": "a" * 64,
            "requirements_locators": ["P44"], "source_url": "https://example.invalid/official",
            "source_version": "Synthetic fixture v1", "source_license": "Fixture only",
            "last_verified": "2026-10-11", "expires_after_days": 365,
            "applicable_document_types": ["master-thesis"], "document_type": "master-thesis"}


def readiness(profile):
    from profile_policy import profile_readiness
    return profile_readiness(profile, "2026-10-11")


def test_training_regulation_cannot_certify_presentation():
    assert readiness(valid_source() | {"source_kind": "training-regulation"}) == "OFFICIAL_RULE_REQUIRED"


@pytest.mark.parametrize("field", ["source_hash", "requirements_locators", "source_version", "source_license", "last_verified"])
def test_missing_source_evidence_fails(field):
    profile = valid_source()
    profile.pop(field)
    assert readiness(profile) == "OFFICIAL_RULE_REQUIRED"


def test_expired_source_is_stale_not_ready():
    assert readiness(valid_source() | {"last_verified": "2024-10-11"}) == "STALE"


def test_future_verification_not_accepted():
    assert readiness(valid_source() | {"last_verified": "2027-10-11"}) == "OFFICIAL_RULE_REQUIRED"


def test_master_source_does_not_certify_ckii():
    assert readiness(valid_source() | {"document_type": "ckii-thesis"}) == "OFFICIAL_RULE_REQUIRED"


def test_complete_applicable_source_can_be_ready():
    assert readiness(valid_source()) == "READY"


def test_border_rule_is_profile_specific_not_universal():
    from profile_policy import table_border_policy
    assert table_border_policy({"table_borders": "grid"}) == "grid"
    assert table_border_policy({"table_borders": "no-vertical"}) == "no-vertical"
    assert table_border_policy({}) == "AUTHOR_APPROVAL_REQUIRED"


def test_exception_cannot_replace_missing_source():
    assert readiness({"institution_exception": {"approved_by": "author", "scope": "table", "reason": "local convention"}}) == "OFFICIAL_RULE_REQUIRED"


def test_exception_must_be_scoped_and_approved():
    from profile_policy import table_border_policy
    assert table_border_policy({"table_borders": "grid", "institution_exception": {"scope": "table-borders", "value": "no-vertical", "approved_by": "author", "reason": "confirmed local instruction"}}) == "no-vertical"


def test_ck2_basic_depth_preserved():
    from medical_research_skills_vn.document_types import load_document_type
    assert load_document_type(ROOT, "project-ck2")["convention"]["complexity"] == "basic-question-led"


def test_source_governed_profile_adapter_preserves_applicability():
    from datetime import date
    import yaml
    from medical_research_skills_vn.profiles import official_profile_readiness
    profile = yaml.safe_load((ROOT / "profiles/institution/hmu/word-format-master-2020-current-2026.yaml").read_text(encoding="utf-8"))
    assert official_profile_readiness(profile, date(2026, 10, 11)) == "READY"
    profile["document_type"] = "ckii-thesis"
    assert official_profile_readiness(profile, date(2026, 10, 11)) == "OFFICIAL_RULE_REQUIRED"
