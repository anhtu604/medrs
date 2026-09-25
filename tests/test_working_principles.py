from pathlib import Path

from medical_research_skills_vn.budgets import issue_codes
from medical_research_skills_vn.structure import validate_working_principles


ROOT = Path(__file__).parents[1]


def test_every_skill_links_the_shared_working_principles_exactly_once():
    assert validate_working_principles(ROOT) == []


def test_skill_without_the_link_is_reported(tmp_path):
    principles = tmp_path / "skills/medrs/references/working-principles.md"
    principles.parent.mkdir(parents=True)
    principles.write_text("# Nguyên tắc làm việc\n", encoding="utf-8")
    (tmp_path / "skills/medrs/SKILL.md").write_text(
        "---\nname: medrs\ndescription: x\n---\n\n[p](references/working-principles.md)\n", encoding="utf-8"
    )
    orphan = tmp_path / "skills/viet-ket-qua/SKILL.md"
    orphan.parent.mkdir(parents=True)
    orphan.write_text("---\nname: viet-ket-qua\ndescription: x\n---\n\n# Viết Kết quả\n", encoding="utf-8")

    issues = validate_working_principles(tmp_path)

    assert issue_codes(issues) == {"WORKING_PRINCIPLES_NOT_LINKED"}
    assert issues[0].path.endswith("viet-ket-qua\\SKILL.md") or issues[0].path.endswith("viet-ket-qua/SKILL.md")


def test_principles_keep_the_single_hard_boundary():
    text = (ROOT / "skills/medrs/references/working-principles.md").read_text(encoding="utf-8")
    assert "Lời tác giả là đủ" in text
    assert "Không bịa" in text
    assert "Việc cần bổ sung" in text


def test_every_manuscript_editing_skill_links_the_zotero_contract():
    from medical_research_skills_vn.structure import validate_zotero_contract

    assert validate_zotero_contract(ROOT) == []
