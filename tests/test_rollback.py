import subprocess
import sys
from pathlib import Path
import zipfile

from medical_research_skills_vn.rollback import simulate_rollback


ROOT = Path(__file__).parents[1]


def test_isolated_rollback_never_discovers_both_versions(tmp_path):
    archive = tmp_path / "synthetic-v1.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr("skills/legacy-skill/SKILL.md", "---\nname: legacy-skill\ndescription: test fixture\n---\n")
    report = simulate_rollback(ROOT, tmp_path, archive)

    assert report["v2_skill_count"] == len(list((ROOT / "skills").glob("*/SKILL.md")))
    assert report["v1_skill_count"] > 0
    assert report["simultaneous_install_detected"] is False
    assert report["v2_present_after_rollback"] is False


def test_rollback_cli_runs_only_in_isolated_mode():
    completed = subprocess.run(
        [sys.executable, "scripts/verify_rollback.py", "--isolated"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert "simultaneous_install_detected: False" in completed.stdout
