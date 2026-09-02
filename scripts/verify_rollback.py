import argparse
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.rollback import simulate_rollback  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--isolated", action="store_true")
    args = parser.parse_args()
    if not args.isolated:
        parser.error("--isolated is required; live plugin caches are never modified")
    with tempfile.TemporaryDirectory(prefix="medical-research-rollback-") as temporary:
        workspace = Path(temporary)
        archive = workspace / "synthetic-v1.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("skills/legacy-skill/SKILL.md", "---\nname: legacy-skill\ndescription: test fixture\n---\n")
        report = simulate_rollback(ROOT, workspace, archive)
    for key, value in report.items():
        print(f"{key}: {value}")
    return 1 if report["simultaneous_install_detected"] or report["v2_present_after_rollback"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
