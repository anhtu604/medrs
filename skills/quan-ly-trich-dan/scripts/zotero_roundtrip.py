"""Export Word paragraphs with field tokens, then apply edited text back safely.

    python zotero_roundtrip.py export draft.docx --out paragraphs.json
    python zotero_roundtrip.py apply draft.docx paragraphs.json --out revised.docx [--zotero-db PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from zotero_fields import ZoteroFieldError, apply_edits, export_paragraphs  # noqa: E402
from zotero_library import resolve_items  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export")
    export.add_argument("docx", type=Path)
    export.add_argument("--out", type=Path, required=True)
    apply = commands.add_parser("apply")
    apply.add_argument("docx", type=Path)
    apply.add_argument("paragraphs", type=Path)
    apply.add_argument("--out", type=Path, required=True)
    apply.add_argument("--zotero-db", type=Path)
    args = parser.parse_args()

    if args.command == "export":
        data = export_paragraphs(args.docx)
        args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{len(data['paragraphs'])} paragraphs -> {args.out}")
        return 0

    data = json.loads(args.paragraphs.read_text(encoding="utf-8"))
    edits = {row["index"]: row["text"] for row in data["paragraphs"]}
    resolver = partial(resolve_items, args.zotero_db) if args.zotero_db else None
    try:
        report = apply_edits(args.docx, edits, args.out, expected_sha256=data["source_sha256"], resolver=resolver)
    except ZoteroFieldError as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
