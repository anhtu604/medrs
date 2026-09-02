import json
import subprocess
import sys
from pathlib import Path

from medical_research_skills_vn.indexing import build_index, validate_reference_callers


ROOT = Path(__file__).parents[1]


def test_generated_index_matches_present_canonical_skill_tree():
    generated = build_index(ROOT)
    checked_in = json.loads((ROOT / "skills/index.json").read_text(encoding="utf-8"))

    assert generated == checked_in
    present = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    assert {entry["name"] for entry in generated["skills"]} == present
    assert all(entry["skill_path"].endswith("/SKILL.md") for entry in generated["skills"])


def test_every_reference_has_an_explicit_caller():
    assert validate_reference_callers(ROOT) == []


def test_build_index_check_detects_drift(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_index.py"), "--check", "--root", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "index drift" in completed.stderr.lower()
