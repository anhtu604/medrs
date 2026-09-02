import json
from pathlib import Path

import yaml

from medical_research_skills_vn.evaluation import run_scenario


ROOT = Path(__file__).parents[1]


def test_all_twenty_four_skills_are_accepted_and_discoverable():
    inventory = yaml.safe_load((ROOT / "config/canonical-skills.yaml").read_text(encoding="utf-8"))
    index = json.loads((ROOT / "skills/index.json").read_text(encoding="utf-8"))
    assert len(inventory["skills"]) == 24
    assert all(item["status"] == "accepted" for item in inventory["skills"])
    assert len(index["skills"]) == 24
    assert "all 24 canonical" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_six_release_exemplars_pass_offline():
    scenarios = sorted((ROOT / "tests/cases/end-to-end").glob("*.yaml"))
    assert {path.stem for path in scenarios} == {
        "protocol-new-project",
        "journal-article",
        "systematic-review",
        "qualitative-synthesis",
        "meta-analysis-guard",
        "thesis-hmu",
    }
    results = [run_scenario(path, ROOT) for path in scenarios]
    assert {result.name for result in results} == {
        "protocol-new-project",
        "journal-article",
        "systematic-review",
        "qualitative-synthesis",
        "meta-analysis-guard",
        "thesis-hmu",
    }
    assert all(result.errors == [] for result in results)
