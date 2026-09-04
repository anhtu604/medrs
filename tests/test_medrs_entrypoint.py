from pathlib import Path

import yaml

from medical_research_skills_vn.routing import RoutingRequest, route_request


ROOT = Path(__file__).parents[1]


def test_medrs_is_the_only_canonical_entrypoint():
    assert (ROOT / "skills/medrs/SKILL.md").is_file()
    assert not (ROOT / "skills/co-van").exists()

    inventory = yaml.safe_load((ROOT / "config/canonical-skills.yaml").read_text(encoding="utf-8"))
    names = [item["name"] for item in inventory["skills"]]
    assert names[0] == "medrs"
    assert "co-van" not in names

    decision = route_request(
        RoutingRequest(text="Tôi chưa biết nên bắt đầu nghiên cứu từ đâu"),
        {},
        active_skills=set(names),
    )
    assert decision.entrypoint == "medrs"
    assert decision.canonical == "medrs"
