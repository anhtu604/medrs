from datetime import date
from pathlib import Path

import pytest
import yaml

from medical_research_skills_vn.budgets import issue_codes
from medical_research_skills_vn.document_types import (
    DOCUMENT_TYPES,
    load_document_type,
    resolve_document_type,
    section_word_budget,
    validate_document_type_profiles,
)


ROOT = Path(__file__).parents[1]


def test_all_six_profiles_ship_and_validate():
    assert DOCUMENT_TYPES == (
        "journal-article-vn",
        "journal-article-intl",
        "thesis-master",
        "thesis-specialist",
        "dissertation-doctoral",
        "protocol",
    )
    assert validate_document_type_profiles(ROOT, date(2026, 9, 25)) == []


@pytest.mark.parametrize(
    ("value", "locale", "expected"),
    [
        ("thesis-master", "vi-medical-academic@1.0.0", "thesis-master"),
        ("thesis", "vi-medical-academic@1.0.0", "thesis-master"),
        ("dissertation", "vi-medical-academic@1.0.0", "dissertation-doctoral"),
        ("protocol", "en-medical-academic@1.0.0", "protocol"),
        ("journal-article", "vi-medical-academic@1.0.0", "journal-article-vn"),
        ("manuscript", "en-medical-academic@1.0.0", "journal-article-intl"),
    ],
)
def test_legacy_passport_values_map_without_asking(value, locale, expected):
    assert resolve_document_type(value, locale) == expected


def test_unknown_document_type_is_reported():
    with pytest.raises(ValueError, match="UNKNOWN_DOCUMENT_TYPE"):
        resolve_document_type("poster", "vi-medical-academic@1.0.0")


def test_depth_differs_between_article_and_thesis():
    article = load_document_type(ROOT, "journal-article-intl")
    thesis = load_document_type(ROOT, "thesis-master")
    assert section_word_budget(article, "discussion") < section_word_budget(thesis, "discussion")
    assert section_word_budget(load_document_type(ROOT, "protocol"), "discussion") is None


def test_only_the_doctoral_profile_carries_a_contributions_section():
    for name in DOCUMENT_TYPES:
        profile = load_document_type(ROOT, name)
        has_section = profile["convention"]["contributions_section"] is not None
        assert has_section == (name == "dissertation-doctoral"), name


def test_profile_without_rule_layer_needs_a_note(tmp_path):
    folder = tmp_path / "profiles/document-type"
    folder.mkdir(parents=True)
    profile = load_document_type(ROOT, "protocol")
    profile.pop("rules_note")
    for name in DOCUMENT_TYPES:
        (folder / f"{name}.yaml").write_text(
            yaml.safe_dump(profile | {"profile_id": name, "document_type": name}, allow_unicode=True),
            encoding="utf-8",
        )
    assert "DOCUMENT_TYPE_RULES_NOTE_MISSING" in issue_codes(
        validate_document_type_profiles(tmp_path, date(2026, 9, 25))
    )


def _write_profiles_with_protocol_override(tmp_path, change):
    folder = tmp_path / "profiles/document-type"
    folder.mkdir(parents=True)
    for name in DOCUMENT_TYPES:
        profile = load_document_type(ROOT, name)
        if name == "protocol":
            change(profile)
        (folder / f"{name}.yaml").write_text(
            yaml.safe_dump(profile, allow_unicode=True), encoding="utf-8"
        )


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("frame", [], "DOCUMENT_TYPE_CONVENTION_FRAME_INVALID"),
        ("frame", [" ", 2], "DOCUMENT_TYPE_CONVENTION_FRAME_INVALID"),
        ("frame", "Introduction", "DOCUMENT_TYPE_CONVENTION_FRAME_INVALID"),
        ("abstract_languages", [], "DOCUMENT_TYPE_CONVENTION_ABSTRACT_LANGUAGES_INVALID"),
        ("abstract_languages", ["vi", " "], "DOCUMENT_TYPE_CONVENTION_ABSTRACT_LANGUAGES_INVALID"),
        ("strengths_limitations", {}, "DOCUMENT_TYPE_CONVENTION_STRENGTHS_LIMITATIONS_INVALID"),
        ("strengths_limitations", {"placement": " "}, "DOCUMENT_TYPE_CONVENTION_STRENGTHS_LIMITATIONS_INVALID"),
        ("strengths_limitations", {"placement": "not-applicable"}, "DOCUMENT_TYPE_CONVENTION_STRENGTHS_LIMITATIONS_INVALID"),
        ("section_word_budget", {}, "DOCUMENT_TYPE_CONVENTION_SECTION_WORD_BUDGET_INVALID"),
        ("section_word_budget", {"methods": 0}, "DOCUMENT_TYPE_CONVENTION_SECTION_WORD_BUDGET_INVALID"),
        ("section_word_budget", {"methods": -1}, "DOCUMENT_TYPE_CONVENTION_SECTION_WORD_BUDGET_INVALID"),
        ("section_word_budget", {"methods": 1.5}, "DOCUMENT_TYPE_CONVENTION_SECTION_WORD_BUDGET_INVALID"),
        ("section_word_budget", {"methods": True}, "DOCUMENT_TYPE_CONVENTION_SECTION_WORD_BUDGET_INVALID"),
    ],
)
def test_convention_rejects_malformed_fields(tmp_path, field, value, expected_code):
    _write_profiles_with_protocol_override(
        tmp_path, lambda profile: profile["convention"].__setitem__(field, value)
    )
    assert expected_code in issue_codes(validate_document_type_profiles(tmp_path, date(2026, 9, 25)))


def test_convention_rejects_non_mapping_without_crashing(tmp_path):
    _write_profiles_with_protocol_override(tmp_path, lambda profile: profile.__setitem__("convention", []))
    assert "DOCUMENT_TYPE_CONVENTION_INVALID" in issue_codes(
        validate_document_type_profiles(tmp_path, date(2026, 9, 25))
    )


@pytest.mark.parametrize("source_sha256", [None, "not-a-hash", "a" * 63, " "])
def test_rule_layer_requires_valid_source_sha256(tmp_path, source_sha256):
    def change(profile):
        profile["rules"] = load_document_type(ROOT, "dissertation-doctoral")["rules"].copy()
        profile["rules"]["source_sha256"] = source_sha256

    _write_profiles_with_protocol_override(tmp_path, change)
    assert "DOCUMENT_TYPE_RULES_SOURCE_SHA256_INVALID" in issue_codes(
        validate_document_type_profiles(tmp_path, date(2026, 9, 25))
    )


def test_rule_layer_rejects_non_mapping_without_crashing(tmp_path):
    _write_profiles_with_protocol_override(tmp_path, lambda profile: profile.__setitem__("rules", []))
    assert "DOCUMENT_TYPE_RULES_INVALID" in issue_codes(
        validate_document_type_profiles(tmp_path, date(2026, 9, 25))
    )


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("source_url", None, "DOCUMENT_TYPE_RULES_SOURCE_EMPTY"),
        ("source_version", " ", "DOCUMENT_TYPE_RULES_SOURCE_EMPTY"),
        ("source_license", "", "DOCUMENT_TYPE_RULES_SOURCE_EMPTY"),
        ("source_cutoff", None, "DOCUMENT_TYPE_RULES_SOURCE_EMPTY"),
        ("verification_status", "UNVERIFIED", "DOCUMENT_TYPE_RULES_UNVERIFIED"),
        ("source_locator", " ", "DOCUMENT_TYPE_RULES_UNLOCATED"),
    ],
)
def test_rule_layer_requires_verified_source_and_substantive_locator(tmp_path, field, value, expected_code):
    folder = tmp_path / "profiles/document-type"
    folder.mkdir(parents=True)
    for name in DOCUMENT_TYPES:
        profile = load_document_type(ROOT, name)
        if name == "protocol":
            rules = {
                "source_url": "https://example.org/official-rules",
                "source_version": "2026",
                "source_license": "public",
                "source_cutoff": "2026-09-25",
                "last_verified": "2026-09-25",
                "expires_after_days": 365,
                "verification_status": "CURRENT",
                "requirements": [{"source_locator": "section 2"}],
            }
            if field == "source_locator":
                rules["requirements"][0][field] = value
            else:
                rules[field] = value
            profile["rules"] = rules
        (folder / f"{name}.yaml").write_text(
            yaml.safe_dump(profile, allow_unicode=True), encoding="utf-8"
        )
    assert expected_code in issue_codes(validate_document_type_profiles(tmp_path, date(2026, 9, 25)))
