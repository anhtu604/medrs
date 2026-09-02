import json
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]


def test_inventory_lifecycle_matches_current_slice_four_progress():
    inventory = yaml.safe_load((ROOT / "config/canonical-skills.yaml").read_text(encoding="utf-8"))
    accepted = [skill["name"] for skill in inventory["skills"] if skill["status"] == "accepted"]
    active = [skill["name"] for skill in inventory["skills"] if skill["status"] == "active"]
    assert accepted == [
        "co-van",
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
    ]
    assert active == []
    assert inventory["active_slice"] == 4
    assert inventory["final_count"] == 24


def test_claude_manifest_and_marketplace_are_repo_first():
    claude_manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    assert not (ROOT / "plugin.json").exists()
    assert claude_manifest["name"] == "medrs"
    assert claude_manifest["version"] == "2.0.0-alpha.1"
    assert claude_manifest["license"] == "CC-BY-NC-4.0"
    assert claude_manifest["repository"] == "https://github.com/anhtu604/medrs"
    assert marketplace["plugins"][0]["source"] == "./"
    assert marketplace["plugins"][0]["name"] == claude_manifest["name"]


def test_portable_repository_entry_files_exist():
    for relative in (
        "AGENTS.md",
        "ATTRIBUTION.md",
        "CHANGELOG.md",
        "requirements.txt",
        "docs/medical-research-skills-vn-v2-design.md",
    ):
        assert (ROOT / relative).is_file(), relative
