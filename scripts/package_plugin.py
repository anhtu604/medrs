import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.packaging import build_package  # noqa: E402


def main() -> int:
    validation = subprocess.run([sys.executable, "scripts/validate_skills.py"], cwd=ROOT, check=False)
    if validation.returncode:
        return validation.returncode
    destination = ROOT / "dist/medical-research-skills-vn-2.0.0-alpha.1.zip"
    build_package(ROOT, destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest().upper()
    checksum = destination.with_suffix(destination.suffix + ".sha256")
    checksum.write_text(f"{digest}  {destination.name}\n", encoding="ascii", newline="\n")
    print(destination)
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
