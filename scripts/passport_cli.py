import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.passport import confirm_field, new_passport, validate_passport  # noqa: E402
from medical_research_skills_vn.intake import draft_passport_from_project, extract_project  # noqa: E402


def write_new(path: Path, data: dict, forbidden_input: Path | None = None) -> None:
    if forbidden_input and path.resolve() == forbidden_input.resolve():
        raise ValueError("Refusing to overwrite the input Passport")
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("new")
    create.add_argument("--project-id", required=True)
    create.add_argument("--document-type", required=True)
    create.add_argument("--locale-profile", required=True)
    create.add_argument("--output", type=Path, required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("path", type=Path)
    confirm = sub.add_parser("confirm")
    confirm.add_argument("path", type=Path)
    confirm.add_argument("--field", required=True)
    confirm.add_argument("--value", required=True)
    confirm.add_argument("--author", required=True)
    confirm.add_argument("--timestamp", required=True)
    confirm.add_argument("--output", type=Path, required=True)
    intake = sub.add_parser("intake")
    intake.add_argument("path", type=Path)
    intake.add_argument("--project-id", required=True)
    intake.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "new":
        write_new(args.output, new_passport(args.project_id, args.document_type, args.locale_profile))
        return 0
    if args.command == "intake":
        data = draft_passport_from_project(extract_project(args.path), args.project_id)
        write_new(args.output, data, args.path)
        return 0
    data = json.loads(args.path.read_text(encoding="utf-8"))
    if args.command == "validate":
        issues = validate_passport(data)
        for issue in issues:
            print(f"{issue.code}: {issue.path}: {issue.message}")
        return int(bool(issues))
    updated = confirm_field(data, f"/{args.field}", args.value, args.author, args.timestamp)
    write_new(args.output, updated, args.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
