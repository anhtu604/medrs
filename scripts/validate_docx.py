import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.docx_validation import validate_docx  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--backend", default="ooxml-only")
    parser.add_argument("--rendered", type=Path, action="append", default=[])
    args = parser.parse_args()
    profile = yaml.safe_load(args.profile.read_text(encoding="utf-8"))
    result = validate_docx(args.document, profile, rendered_artifacts=args.rendered, backend=args.backend)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    mechanical_pass = all(value == "PASS" for value in result["mechanical_checks"].values())
    return 0 if mechanical_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
