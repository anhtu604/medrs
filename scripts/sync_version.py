import argparse
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(DEFAULT_ROOT / "src"))

from medical_research_skills_vn.release import apply_version, canonical_version, version_drift  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Propagate .claude-plugin/plugin.json version to every carrier.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    version = canonical_version(root)
    if args.check:
        drift = version_drift(root)
        if drift:
            for entry in drift:
                print(f"Version drift: {entry}", file=sys.stderr)
            return 1
        print(f"Version {version} is consistent")
        return 0
    written = apply_version(root)
    for path in written:
        print(f"Updated {path.relative_to(root).as_posix()}")
    print(f"Version {version} applied to {len(written)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
