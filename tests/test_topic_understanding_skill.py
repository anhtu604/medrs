import json
import subprocess
import sys
from pathlib import Path

import yaml

from medical_research_skills_vn.budgets import validate_context_budget


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills/tim-hieu-de-tai"
CLI = SKILL / "scripts/topic_understanding.py"
DAY = "2026-10-23"


def run_cli(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True,
                          text=True, encoding="utf-8")


def test_next_part_resumes_at_first_unfinished():
    from topic_understanding import next_part

    parts = {"background": "DONE", "question": "CHECKED_BACK", "methods": "NOT_STARTED", "expected": "NOT_STARTED"}
    assert next_part({"parts": parts}) == "question"
    assert next_part({"parts": {name: "DONE" for name in parts}}) is None


def test_cli_status_on_empty_folder(tmp_path):
    result = run_cli("status", tmp_path)
    assert result.returncode == 0, result.stderr
    status = json.loads(result.stdout)
    assert status["workspace"] is False
    assert status["state"] == "NOT_STARTED"
    assert status["next_part"] == "background"


def test_cli_confirm_refuses_unfinished_parts(tmp_path):
    import project_workspace

    project_workspace.initialize_project(tmp_path, "p", DAY)
    result = run_cli("confirm", tmp_path, DAY, "Tôi đã hiểu rõ")
    assert result.returncode == 2
    assert "PARTS_NOT_DONE" in result.stderr


def test_cli_walks_a_part_and_reports_progress(tmp_path):
    import project_workspace

    project_workspace.initialize_project(tmp_path, "p", DAY)
    for value in ("EXPLAINED", "CHECKED_BACK", "DONE"):
        assert run_cli("part", tmp_path, DAY, "background", value).returncode == 0
    assert run_cli("open-items", tmp_path, DAY, 1).returncode == 0
    status = json.loads(run_cli("status", tmp_path).stdout)
    assert status["state"] == "IN_PROGRESS"
    assert status["next_part"] == "question"
    assert status["open_items"] == 1
    assert run_cli("defer", tmp_path, DAY).returncode == 0
    assert json.loads(run_cli("status", tmp_path).stdout)["state"] == "DEFERRED_BY_AUTHOR"


def test_skill_contract_covers_the_four_parts_and_check_back():
    contract = (SKILL / "references/conversation-contract.md").read_text(encoding="utf-8")
    for phrase in ("Kiến thức nền", "Câu hỏi nghiên cứu", "Phương pháp dự kiến", "Kết quả mong đợi",
                   "có nguồn", "giả thuyết", "cần tìm hiểu thêm", "hỏi ngược"):
        assert phrase in contract, phrase
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for link in ("references/conversation-contract.md", "../tim-y-van/SKILL.md", "../ho-so-nghien-cuu/SKILL.md",
                 "../leader-nghien-cuu/references/project-workspace.md", "../medrs/references/working-principles.md",
                 "scripts/topic_understanding.py"):
        assert f"]({link})" in skill, link


def test_inventory_has_29_skills_within_budget():
    inventory = yaml.safe_load((ROOT / "config/canonical-skills.yaml").read_text(encoding="utf-8"))
    assert inventory["final_count"] == 29
    assert "tim-hieu-de-tai" in {item["name"] for item in inventory["skills"]}
    legacy = yaml.safe_load((ROOT / "skills/medrs/references/legacy-skill-map.yaml").read_text(encoding="utf-8"))
    assert validate_context_budget(ROOT, set(legacy.get("legacy", {}))) == []
