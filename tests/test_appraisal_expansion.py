from medical_research_skills_vn.coverage import validate_coverage_manifest
from medical_research_skills_vn.coverage import load_coverage_manifest
from pathlib import Path
import pytest


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


def test_robins_i_v2_keeps_both_confounding_variants():
    root = Path(__file__).resolve().parents[1]
    source = load_coverage_manifest(root / "coverage/robins-i-v2-draft-2025.yaml")
    assert source["draft"] is True
    assert source["version"] == "20 November 2025 draft"
    assert source["expected_ids"] == ([f"1A.{i}" for i in range(1, 5)] + [f"1B.{i}" for i in range(1, 6)] +
                                         [f"2.{i}" for i in range(1, 6)] + [f"3.{i}" for i in range(1, 9)] +
                                         [f"4.{i}" for i in range(1, 12)] + [f"5.{i}" for i in range(1, 4)] +
                                         [f"6.{i}" for i in range(1, 5)])
    assert source["official_tool_required_at_use"] is True
    assert source["coverage_scope"] == "domain-signalling-navigation-not-official-algorithms"
    assert validate_coverage_manifest(source) == []


def test_quadas3_does_not_reuse_quadas2_domain_structure():
    root = Path(__file__).resolve().parents[1]
    source = load_coverage_manifest(root / "coverage/quadas-3-1.2.yaml")
    assert source["version"] == "1.2"
    assert list(source["domains"]) == ["participants", "index-test", "target-condition", "analysis"]
    assert len(source["expected_ids"]) == 20
    assert len(source["phases"]) == 6
    assert validate_coverage_manifest(source) == []


def test_robins_e_preserves_three_exposure_variants():
    root = Path(__file__).resolve().parents[1]
    source = load_coverage_manifest(root / "coverage/robins-e-2024.yaml")
    assert len(source["domains"]) == 7
    assert len(source["expected_ids"]) == 48
    for variant in ("A", "B", "C"):
        assert all(f"2{variant}.{i}" in source["expected_ids"] for i in range(1, 5))
    assert validate_coverage_manifest(source) == []


def test_amstar2_has_all_sixteen_entries_not_a_total_score():
    root = Path(__file__).resolve().parents[1]
    source = load_coverage_manifest(root / "coverage/amstar-2-2017.yaml")
    assert source["expected_ids"] == [str(i) for i in range(1, 17)]
    assert source["numerical_total_score"] is False
    assert source["official_tool_required_at_use"] is True
    assert validate_coverage_manifest(source) == []


@pytest.mark.parametrize("text", ["Đánh giá ROBINS-I V2", "Đánh giá ROBINS-E", "Appraise JBI prevalence", "Đánh giá QUADAS-3", "Appraise AMSTAR 2"])
def test_named_appraisal_request_routes_to_appraisal_owner(text):
    from medical_research_skills_vn.routing import RoutingRequest, route_request
    result = route_request(RoutingRequest(text), {}, {"medrs", "danh-gia-chat-luong-bang-chung"})
    assert result.canonical == "danh-gia-chat-luong-bang-chung"
