from pathlib import Path

import yaml

import medical_research_skills_vn
from medical_research_skills_vn.budgets import issue_codes


ROOT = Path(__file__).parents[1]
EXPECTED_NAMES = {
    "co-van",
    "ho-so-nghien-cuu",
    "de-cuong-va-thiet-ke",
    "co-mau-va-ke-hoach-phan-tich",
    "dao-duc-va-quan-tri-du-lieu",
    "tim-y-van",
    "tong-hop-bang-chung",
    "danh-gia-chat-luong-bang-chung",
    "phan-tich-so-lieu",
    "phan-tich-r",
    "phan-tich-stata",
    "viet-ban-thao-y-hoc",
    "viet-dat-van-de",
    "viet-tong-quan",
    "viet-phuong-phap",
    "viet-ket-qua",
    "viet-ban-luan",
    "viet-ket-luan-khuyen-nghi",
    "viet-tom-tat",
    "kiem-van-phong",
    "kiem-chung-ban-thao",
    "bo-cuc-tai-lieu",
    "dinh-dang-tai-lieu",
    "phan-bien-va-chinh-sua",
}


def write_inventory(root: Path, skills: list[dict]) -> None:
    config = root / "config"
    config.mkdir(parents=True)
    (config / "canonical-skills.yaml").write_text(
        yaml.safe_dump({"final_count": 24, "skills": skills}, allow_unicode=True),
        encoding="utf-8",
    )


def test_repository_inventory_names_match_the_approved_twenty_four():
    records = medical_research_skills_vn.inventory.load_inventory(ROOT)

    assert {record.name for record in records} == EXPECTED_NAMES


def test_accepted_skill_must_have_a_real_entrypoint(tmp_path):
    write_inventory(tmp_path, [{"name": "missing-skill", "slice": 2, "status": "accepted"}])

    issues = medical_research_skills_vn.inventory.validate_inventory(tmp_path)

    assert "ACCEPTED_SKILL_MISSING" in issue_codes(issues)


def test_planned_skill_may_remain_absent_until_its_slice_opens(tmp_path):
    write_inventory(tmp_path, [{"name": "future-skill", "slice": 4, "status": "planned"}])

    assert medical_research_skills_vn.inventory.validate_inventory(tmp_path) == []


def test_current_repository_has_no_false_acceptance_claims():
    assert medical_research_skills_vn.inventory.validate_inventory(ROOT) == []
