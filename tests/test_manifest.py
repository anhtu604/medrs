import json
from pathlib import Path

import yaml

from medical_research_skills_vn.release import canonical_version, expected_skill_count, version_drift


ROOT = Path(__file__).parents[1]


def test_inventory_lifecycle_matches_current_slice_four_progress():
    inventory = yaml.safe_load((ROOT / "config/canonical-skills.yaml").read_text(encoding="utf-8"))
    accepted = [skill["name"] for skill in inventory["skills"] if skill["status"] == "accepted"]
    active = [skill["name"] for skill in inventory["skills"] if skill["status"] == "active"]
    assert accepted == [
        "medrs",
        "ho-so-nghien-cuu",
        "de-cuong-va-thiet-ke",
        "co-mau-va-ke-hoach-phan-tich",
        "dao-duc-va-quan-tri-du-lieu",
        "viet-phuong-phap",
        "kiem-van-phong",
        "tim-y-van",
        "tong-hop-bang-chung",
        "danh-gia-chat-luong-bang-chung",
        "phan-tich-so-lieu",
        "phan-tich-r",
        "phan-tich-stata",
        "viet-ban-thao-y-hoc",
        "viet-dat-van-de",
        "viet-tong-quan",
        "viet-ket-qua",
        "viet-ban-luan",
        "viet-ket-luan-khuyen-nghi",
        "viet-tom-tat",
        "kiem-chung-ban-thao",
        "bo-cuc-tai-lieu",
        "dinh-dang-tai-lieu",
        "phan-bien-va-chinh-sua",
        "quan-ly-trich-dan",
        "bieu-do-cong-bo",
    ]
    assert active == []
    assert inventory["active_slice"] == 4
    assert inventory["final_count"] == len(inventory["skills"])


def test_claude_manifest_and_marketplace_are_repo_first():
    claude_manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    assert not (ROOT / "plugin.json").exists()
    assert claude_manifest["name"] == "medrs"
    assert claude_manifest["license"] == "CC-BY-NC-4.0"
    assert claude_manifest["repository"] == "https://github.com/anhtu604/medrs"
    assert marketplace["plugins"][0]["source"] == "./"
    assert marketplace["plugins"][0]["name"] == claude_manifest["name"]


def test_every_version_carrier_matches_the_plugin_manifest():
    assert version_drift(ROOT) == []
    assert canonical_version(ROOT) in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_declared_skill_count_matches_the_skills_on_disk():
    assert len(list((ROOT / "skills").glob("*/SKILL.md"))) == expected_skill_count(ROOT)


def test_portable_repository_entry_files_exist():
    for relative in (
        "AGENTS.md",
        "ATTRIBUTION.md",
        "CHANGELOG.md",
        "requirements.txt",
        "docs/medical-research-skills-vn-v2-design.md",
    ):
        assert (ROOT / relative).is_file(), relative
