"""Topic-understanding conversation state: a thin CLI over the project workspace helper."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "leader-nghien-cuu/scripts"))

from project_workspace import PARTS, read_understanding, set_understanding  # noqa: E402


def next_part(understanding: dict) -> str | None:
    """First part still to finish; None once all four are done."""
    return next((part for part in PARTS if understanding["parts"][part] != "DONE"), None)


def status(root) -> dict:
    current = read_understanding(Path(root))
    return {"workspace": current["workspace"], "state": current["status"], "parts": current["parts"],
            "open_items": current["open_items"], "next_part": next_part(current)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status").add_argument("root")
    for name in ("part", "open-items", "defer", "confirm"):
        command = commands.add_parser(name)
        command.add_argument("root")
        command.add_argument("date")
        if name == "part":
            command.add_argument("part")
            command.add_argument("state")
        elif name == "open-items":
            command.add_argument("count", type=int)
        elif name == "confirm":
            command.add_argument("words")
    args = parser.parse_args(argv)
    try:
        if args.command == "part":
            set_understanding(Path(args.root), args.date, part=args.part, part_state=args.state)
        elif args.command == "open-items":
            set_understanding(Path(args.root), args.date, open_items=args.count)
        elif args.command == "defer":
            set_understanding(Path(args.root), args.date, status="DEFERRED_BY_AUTHOR")
        elif args.command == "confirm":
            set_understanding(Path(args.root), args.date, status="CONFIRMED", confirmation=args.words)
    except (ValueError, FileNotFoundError) as error:
        print(error.args[0] if isinstance(error, ValueError) else "PROJECT_NOT_INITIALIZED", file=sys.stderr)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(status(args.root), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
