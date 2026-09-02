import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from medical_research_skills_vn.evaluation import run_scenario  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--host")
    args = parser.parse_args()
    if args.host:
        print(f"adapter not implemented: {args.host}", file=sys.stderr)
        return 2
    if not args.offline:
        parser.error("choose --offline or --host")

    failed = False
    case_root = ROOT / "tests/cases/end-to-end"
    for path in sorted(case_root.glob("*.yaml")):
        result = run_scenario(path, ROOT)
        if result.errors:
            failed = True
            print(f"{result.name}: FAIL")
            for error in result.errors:
                print(f"  {error}")
        else:
            print(f"{result.name}: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
