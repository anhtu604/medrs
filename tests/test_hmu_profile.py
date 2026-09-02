from pathlib import Path

from medical_research_skills_vn.structure_profiles import load_structure_profile, verify_profile_source


ROOT = Path(__file__).parents[1]
PROFILE = ROOT / "profiles/institution/hmu/thesis-master-2020-current-2026.yaml"


def test_hmu_profile_is_source_traceable_to_registered_official_docx():
    profile = load_structure_profile(PROFILE)
    result = verify_profile_source(ROOT, profile)

    assert result["status"] == "VERIFIED"
    assert result["sha256"] == "6FAFDBB41FD09AE6D506661D2F7D9C0AC02B6B7DE6A3FF9A147CD551C125054F"
    assert result["verification_basis"] in {
        "LOCAL_SOURCE_HASH_AND_LOCATORS",
        "REGISTERED_PROVENANCE_SOURCE_NOT_BUNDLED",
    }
    assert all(rule["source_locator"].startswith("P") for rule in profile["semantic_rules"])


def test_hmu_profile_encodes_semantic_order_without_word_mechanics():
    profile = load_structure_profile(PROFILE)
    ids = [item["id"] for item in profile["sections"]]

    assert ids.index("introduction") < ids.index("chapter-1-literature-review")
    assert ids.index("chapter-1-literature-review") < ids.index("chapter-2-methods")
    assert ids.index("chapter-2-methods") < ids.index("chapter-3-results")
    assert ids.index("chapter-3-results") < ids.index("chapter-4-discussion")
    assert ids.index("chapter-4-discussion") < ids.index("conclusion")
    forbidden = {"font", "margin", "line_spacing", "page_number", "toc_field"}
    assert forbidden.isdisjoint(profile)
