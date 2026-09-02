import argparse
import json
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(DEFAULT_ROOT / "src"))

from medical_research_skills_vn.indexing import build_index  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / "skills/index.json"
    rendered = json.dumps(build_index(root), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not destination.exists() or destination.read_text(encoding="utf-8") != rendered:
            print(f"Skill index drift: regenerate {destination}", file=sys.stderr)
            return 1
        print("Skill index is current")
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
