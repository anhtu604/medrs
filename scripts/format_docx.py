import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.docx_formatting import format_docx  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--approved", action="store_true")
    args = parser.parse_args()
    profile = yaml.safe_load(args.profile.read_text(encoding="utf-8"))
    result = format_docx(args.source, args.output, profile, author_approved=args.approved)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "FORMATTED_WITH_UNPERFORMED_CHECKS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
