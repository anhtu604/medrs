from datetime import date
from pathlib import Path

from medical_research_skills_vn.profiles import validate_profiles


ROOT = Path(__file__).parents[1]


def test_checked_in_locale_profiles_have_complete_current_metadata():
    assert validate_profiles(ROOT, as_of=date(2026, 8, 31)) == []


def test_profile_without_source_metadata_fails(tmp_path):
    path = tmp_path / "profiles/locale/incomplete.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("profile_id: incomplete\n", encoding="utf-8")

    issues = validate_profiles(tmp_path, as_of=date(2026, 8, 31))

    assert {issue.code for issue in issues} == {"PROFILE_SOURCE_METADATA_MISSING"}
