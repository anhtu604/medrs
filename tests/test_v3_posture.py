from pathlib import Path

from medical_research_skills_vn.budgets import load_frontmatter


ROOT = Path(__file__).parents[1]


def test_descriptions_lead_with_capability_not_refusal():
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        description = str(load_frontmatter(path)[0]["description"])
        assert not description.startswith(("Không", "Use when")), path.parent.name
        for word in ("bịa", "invent", "fabricat"):
            assert word not in description.casefold(), (path.parent.name, word)


def test_discussion_keeps_limitations_in_one_section():
    skill = (ROOT / "skills/viet-ban-luan/SKILL.md").read_text(encoding="utf-8")
    workflow = (ROOT / "skills/viet-ban-luan/references/discussion-workflow.md").read_text(encoding="utf-8")
    assert "finding → meaning → contribution → comparison" in skill
    assert "Limitations do not appear in argument paragraphs." in workflow
    assert "bias/confounding/chance → limitation" not in skill


def test_interpretation_leads_with_clinical_meaning():
    text = (ROOT / "skills/phan-tich-so-lieu/SKILL.md").read_text(encoding="utf-8")
    assert "clinical meaning" in text
    assert "Refuse significance-driven model selection" in text


def test_ethics_skill_no_longer_halts_or_demands_proof():
    text = (ROOT / "skills/dao-duc-va-quan-tri-du-lieu/SKILL.md").read_text(encoding="utf-8")
    assert "dừng áp quy tắc" not in text
    assert "chưa cung cấp bằng chứng" not in text
