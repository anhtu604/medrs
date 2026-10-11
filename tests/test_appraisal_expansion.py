from medical_research_skills_vn.coverage import validate_coverage_manifest
from medical_research_skills_vn.coverage import load_coverage_manifest
from pathlib import Path


def manifest():
    return {"instrument": "Synthetic fixture", "version": "fixture", "source_url": "https://example.invalid/fixture",
            "license": "Fixture", "last_verified": "2026-10-11", "caller": "skills/medrs/SKILL.md",
            "expected_ids": ["1"], "implemented_ids": ["1"],
            "items": [{"id": "1", "operational_prompt": "Check fixture evidence", "source_locator": "Fixture item 1"}]}


def test_blocked_instrument_cannot_pass_with_empty_coverage():
    source = manifest() | {"status": "BLOCKED", "expected_ids": [], "implemented_ids": [], "items": []}
    assert "SOURCE_BLOCKED" in validate_coverage_manifest(source)


def test_empty_unblocked_coverage_cannot_certify_completeness():
    source = manifest() | {"expected_ids": [], "implemented_ids": [], "items": []}
    assert "EMPTY_COVERAGE" in validate_coverage_manifest(source)


def test_duplicate_item_record_not_silently_collapsed():
    source = manifest()
    source["items"].append(source["items"][0].copy())
    assert "DUPLICATE_ITEM_IDS" in validate_coverage_manifest(source)


def test_null_source_metadata_not_treated_as_nonempty_string():
    source = manifest() | {"source_url": None}
    assert "METADATA_EMPTY:source_url" in validate_coverage_manifest(source)


def test_source_and_implementation_version_mismatch_fails():
    source = manifest() | {"source_version": "new", "implemented_version": "legacy"}
    assert "SOURCE_VERSION_MISMATCH" in validate_coverage_manifest(source)


def test_jbi_current_analytical_and_prevalence_coverage():
    root = Path(__file__).resolve().parents[1]
    for name, count in (("jbi-analytical-2026.yaml", 8), ("jbi-prevalence-current-2026.yaml", 9)):
        source = load_coverage_manifest(root / "coverage" / name)
        assert source["expected_ids"] == [str(i) for i in range(1, count + 1)]
        assert source["implemented_ids"] == source["expected_ids"]
        assert source["source_sha256"]
        assert source["official_tool_required_at_use"] is True
        assert validate_coverage_manifest(source) == []
