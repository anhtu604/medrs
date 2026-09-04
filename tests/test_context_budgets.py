from pathlib import Path

from medical_research_skills_vn.budgets import (
    count_words,
    issue_codes,
    load_frontmatter,
    validate_context_budget,
)


def write_skill(root: Path, name: str, description: str, body: str = "# Skill\n") -> None:
    folder = root / "skills" / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(
        f'---\nname: {name}\ndescription: "{description}"\n---\n\n{body}',
        encoding="utf-8",
    )


def test_unicode_word_count_handles_vietnamese_and_english():
    assert count_words("Viết phương pháp cho cohort study") == 6


def test_frontmatter_parser_returns_description(tmp_path):
    write_skill(tmp_path, "sample", "Viết Methods; not Results.")
    frontmatter, _ = load_frontmatter(tmp_path / "skills/sample/SKILL.md")
    assert frontmatter["name"] == "sample"
    assert frontmatter["description"] == "Viết Methods; not Results."


def test_budget_fixture_detects_per_skill_and_aggregate_overflow(tmp_path):
    long_description = " ".join(f"word{i}" for i in range(61))
    write_skill(tmp_path, "too-long", long_description)
    issues = validate_context_budget(tmp_path, legacy_names=set())
    assert "DESCRIPTION_WORDS" in issue_codes(issues)


def test_legacy_names_are_forbidden_in_descriptions(tmp_path):
    write_skill(tmp_path, "medrs", "Routes dieu-phoi-luan-van requests safely.")
    issues = validate_context_budget(tmp_path, legacy_names={"dieu-phoi-luan-van"})
    assert "LEGACY_NAME_IN_DESCRIPTION" in issue_codes(issues)


def test_clean_skill_passes_context_budget(tmp_path):
    write_skill(tmp_path, "medrs", "Routes unclear medical research requests; not clinical advice.")
    assert validate_context_budget(tmp_path, legacy_names={"dieu-phoi-luan-van"}) == []
