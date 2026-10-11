import json
from pathlib import Path
import subprocess
import sys
import pytest
from medical_research_skills_vn.routing import RoutingRequest, route_request, route_plan

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/kiem-van-phong/scripts"))


@pytest.mark.parametrize("mode,sections,expected", [
    ("assembled", [], {"full": ["document"], "local": [], "consistency": True}),
    ("standalone", ["Discussion"], {"full": ["Discussion"], "local": [], "consistency": False}),
    ("revision", ["Methods", "Results", "Methods"], {"full": [], "local": ["Methods", "Results"], "consistency": True}),
])
def test_gate_scope(mode, sections, expected):
    from gate_lifecycle import required_gate_scope
    assert required_gate_scope(mode, sections) == expected


def test_empty_revision_cannot_silently_skip_local_audit():
    from gate_lifecycle import required_gate_scope
    with pytest.raises(ValueError):
        required_gate_scope("revision", [])


def test_medrs_colon_explicit_selection_wins():
    result = route_request(RoutingRequest("/medrs:viet-ban-luan có nhắc Zotero"), {}, {"medrs", "viet-ban-luan", "quan-ly-trich-dan"})
    assert result.canonical == "viet-ban-luan"
    assert result.mode == "explicit"


def test_unknown_explicit_skill_needs_clarification():
    result = route_request(RoutingRequest("/medrs:not-a-skill"), {}, {"medrs"})
    assert result.availability == "UNAVAILABLE"
    assert result.mode == "unknown-explicit-skill"


def test_cli_loads_legacy_map_and_routes_protocol_to_design():
    process = subprocess.run([sys.executable, str(ROOT / "skills/medrs/scripts/router.py"), "dieu-phoi-de-cuong-vn"], capture_output=True, text=True, encoding="utf-8", check=True)
    result = json.loads(process.stdout)
    assert result["tasks"][0]["skill"] == "de-cuong-va-thiet-ke"


def test_negated_word_action_does_not_claim_execution():
    result = route_request(RoutingRequest("không sửa mục lục"), {}, {"medrs", "dinh-dang-tai-lieu"})
    assert result.canonical == "medrs"


def test_compound_request_preserves_requested_order():
    result = route_plan(RoutingRequest("Viết bàn luận rồi căn bảng rồi nghiệm thu"), {}, {"medrs", "viet-ban-luan", "dinh-dang-tai-lieu", "leader-nghien-cuu"})
    assert [task["skill"] for task in result["tasks"]] == ["viet-ban-luan", "dinh-dang-tai-lieu", "leader-nghien-cuu"]
