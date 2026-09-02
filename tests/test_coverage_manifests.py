from pathlib import Path

from medical_research_skills_vn.coverage import load_coverage_manifest, validate_coverage_manifest


ROOT = Path(__file__).parents[1]


def test_rob2_manifest_covers_all_five_domains_and_twenty_two_questions():
    manifest = load_coverage_manifest(ROOT / "coverage/rob2-parallel-2019.yaml")
    assert manifest["version"] == "22 August 2019"
    assert set(manifest["domains"]) == {"D1", "D2", "D3", "D4", "D5"}
    assert manifest["expected_ids"] == [
        "1.1", "1.2", "1.3",
        "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7",
        "3.1", "3.2", "3.3", "3.4",
        "4.1", "4.2", "4.3", "4.4", "4.5",
        "5.1", "5.2", "5.3",
    ]
    assert manifest["implemented_ids"] == manifest["expected_ids"]
    assert all(item["operational_prompt"] and item["source_locator"] for item in manifest["items"])
    assert validate_coverage_manifest(manifest) == []


def test_grade_and_cerqual_manifests_cover_every_adopted_component():
    grade = load_coverage_manifest(ROOT / "coverage/grade-interventions-6.5.1.yaml")
    cerqual = load_coverage_manifest(ROOT / "coverage/cerqual-2018.yaml")
    assert grade["expected_ids"] == [
        "risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias",
        "large_effect", "dose_response", "residual_confounding",
    ]
    assert cerqual["expected_ids"] == [
        "methodological_limitations", "coherence", "adequacy", "relevance"
    ]
    assert validate_coverage_manifest(grade) == []
    assert validate_coverage_manifest(cerqual) == []


def test_manifest_rejects_named_only_or_missing_items():
    manifest = load_coverage_manifest(ROOT / "coverage/rob2-parallel-2019.yaml")
    manifest["items"][0]["operational_prompt"] = ""
    manifest["implemented_ids"] = manifest["implemented_ids"][:-1]
    issues = validate_coverage_manifest(manifest)
    assert "COVERAGE_MISMATCH" in issues
    assert "ITEM_CONTENT_MISSING:1.1" in issues

