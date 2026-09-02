from datetime import date
from pathlib import Path

import yaml

from medical_research_skills_vn.ethics import (
    build_ethics_artifact,
    load_source_register,
    validate_source_registers,
    validate_sources,
)


ROOT = Path(__file__).parents[1]
REGISTER = ROOT / "skills/dao-duc-va-quan-tri-du-lieu/references/source-register.yaml"


def test_missing_approval_number_is_marked_and_never_invented():
    artifact = build_ethics_artifact(
        jurisdiction="VN",
        study_stage="protocol",
        data_class="health_data",
        destination="institutional_repository",
        approval_number=None,
        consent_state="UNRESOLVED",
        registration_state="NOT_APPLICABLE_PENDING_CONFIRMATION",
    )

    assert "OFFICIAL_RULE_REQUIRED" in artifact["unresolved_approvals"]
    assert artifact["approval_number"] is None
    assert artifact["invented_values"] == []


def test_stale_regulatory_source_produces_a_visible_banner(tmp_path):
    register_path = tmp_path / "source-register.yaml"
    register_path.write_text(
        yaml.safe_dump(
            {
                "sources": [
                    {
                        "id": "example-rule",
                        "title": "Example rule",
                        "source_url": "https://example.org/rule",
                        "source_version": "2024",
                        "source_license": "UNKNOWN",
                        "source_cutoff": "2024-01-01",
                        "last_verified": "2024-01-01",
                        "expires_after_days": 90,
                        "verification_status": "CURRENT",
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    report = validate_sources(load_source_register(register_path), as_of=date(2026, 8, 31))

    assert report.has("SOURCE_STALE")
    assert report.banners == ["SOURCE_STALE: example-rule"]


def test_checked_in_sources_have_primary_urls_and_current_computed_status():
    register = load_source_register(REGISTER)
    report = validate_sources(register, as_of=date(2026, 8, 31))

    assert not report.issues
    assert {source["id"] for source in register["sources"]} == {
        "vn-tt43-2024-byt",
        "wma-helsinki-2024",
        "ich-e6-r3-2025",
    }
    assert all(source["source_type"] == "PRIMARY" for source in register["sources"])


def test_register_requires_exact_nonempty_coverage_identifiers(tmp_path):
    register = {
        "sources": [
            {
                "id": "empty-instrument",
                "title": "Empty instrument",
                "source_type": "PRIMARY",
                "source_url": "https://example.org/instrument",
                "source_version": "1",
                "source_license": "UNKNOWN",
                "source_cutoff": "2026-01-01",
                "last_verified": "2026-08-31",
                "expires_after_days": 365,
                "verification_status": "CURRENT",
                "coverage": {"expected_identifiers": [], "implemented_identifiers": []},
            }
        ]
    }

    report = validate_sources(register, as_of=date(2026, 8, 31))

    assert report.has("SOURCE_COVERAGE_EMPTY")


def test_register_rejects_coverage_count_that_does_not_match_identifiers():
    register = {
        "sources": [
            {
                "id": "miscounted-instrument",
                "title": "Miscounted instrument",
                "source_type": "PRIMARY",
                "source_url": "https://example.org/instrument",
                "source_version": "1",
                "source_license": "UNKNOWN",
                "source_cutoff": "2026-01-01",
                "last_verified": "2026-08-31",
                "expires_after_days": 365,
                "verification_status": "CURRENT",
                "coverage": {
                    "expected_count": 3,
                    "implemented_count": 2,
                    "expected_identifiers": ["1", "2", "3"],
                    "implemented_identifiers": ["1", "2"],
                },
            }
        ]
    }

    report = validate_sources(register, as_of=date(2026, 8, 31))

    assert report.has("SOURCE_COVERAGE_COUNT_MISMATCH")


def test_repository_validator_discovers_nested_source_registers(tmp_path):
    path = tmp_path / "skills/example/references/source-register.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("sources: []\n", encoding="utf-8")

    issues = validate_source_registers(tmp_path, as_of=date(2026, 8, 31))

    assert [issue.code for issue in issues] == ["SOURCE_REGISTER_EMPTY"]
