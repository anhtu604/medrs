from pathlib import Path
import shutil

from medical_research_skills_vn.structure import validate_shared_preflight
from medical_research_skills_vn.budgets import issue_codes


FIXTURES = Path(__file__).parent / "fixtures/shared-preflight"


def make_tree(tmp_path, fixture_name):
    writer = tmp_path / "skills/viet-phuong-phap"
    writer.mkdir(parents=True)
    shutil.copy(FIXTURES / fixture_name / "SKILL.md", writer / "SKILL.md")
    return tmp_path


def test_missing_shared_preflight_fails_validation(tmp_path):
    tree = make_tree(tmp_path, "valid-writer")
    assert "SHARED_PREFLIGHT_MISSING" in issue_codes(validate_shared_preflight(tree))


def test_valid_writer_calls_single_shared_preflight(tmp_path):
    tree = make_tree(tmp_path, "valid-writer")
    shared = tree / "skills/viet-phuong-phap/references"
    shared.mkdir(parents=True)
    (shared / "writing-preflight.md").write_text("# Preflight\n", encoding="utf-8")
    assert validate_shared_preflight(tree) == []


def test_copied_preflight_rules_are_rejected(tmp_path):
    tree = make_tree(tmp_path, "copied-rules-writer")
    shared = tree / "skills/viet-phuong-phap/references"
    shared.mkdir(parents=True)
    (shared / "writing-preflight.md").write_text("# Preflight\n", encoding="utf-8")
    codes = issue_codes(validate_shared_preflight(tree))
    assert "PREFLIGHT_RULE_DUPLICATED" in codes
    assert "SHARED_PREFLIGHT_NOT_CALLED" in codes
