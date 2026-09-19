"""Single-source release version and inventory size.

`.claude-plugin/plugin.json` is the only place a release version is written by
hand; `config/canonical-skills.yaml` is the only place the canonical skill count
is written by hand. Everything else is derived or checked against them.
"""

import json
import re
from pathlib import Path

import yaml


PRERELEASE_TAGS = {"alpha": "a", "beta": "b", "rc": "rc"}


def canonical_version(root: Path) -> str:
    manifest = json.loads((Path(root) / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    return str(manifest["version"])


def pep440_version(version: str) -> str:
    match = re.fullmatch(r"(\d+\.\d+\.\d+)(?:-(alpha|beta|rc)\.(\d+))?", version)
    if not match:
        raise ValueError(f"Unsupported release version: {version}")
    base, tag, number = match.groups()
    return base if tag is None else f"{base}{PRERELEASE_TAGS[tag]}{number}"


def expected_skill_count(root: Path) -> int:
    inventory = yaml.safe_load((Path(root) / "config/canonical-skills.yaml").read_text(encoding="utf-8"))
    return int(inventory["final_count"])


def cowork_package_name(root: Path) -> str:
    return f"medrs-cowork-{canonical_version(root)}.zip"


def _carriers(root: Path) -> list[tuple[Path, str, str]]:
    """(path, pattern, replacement template) for every derived version carrier."""
    root = Path(root)
    carriers = [
        (root / "src/medical_research_skills_vn/__init__.py", r'(?m)^(__version__ = ")[^"]*(")', "{version}"),
        (root / "pyproject.toml", r'(?m)^(version = ")[^"]*(")', "{pep440}"),
    ]
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        carriers.append((skill, r"(?m)^(  version: )\S+()", "{version}"))
    return carriers


def _rendered(template: str, version: str) -> str:
    return template.format(version=version, pep440=pep440_version(version))


def version_drift(root: Path) -> list[str]:
    root = Path(root)
    version = canonical_version(root)
    drifted = []
    for path, pattern, template in _carriers(root):
        match = re.search(pattern, path.read_text(encoding="utf-8"))
        if match is None:
            drifted.append(f"{path.relative_to(root).as_posix()}: no version field found")
        elif match.group(0) != f"{match.group(1)}{_rendered(template, version)}{match.group(2)}":
            drifted.append(f"{path.relative_to(root).as_posix()}: expected {_rendered(template, version)}")
    return drifted


def apply_version(root: Path) -> list[Path]:
    root = Path(root)
    version = canonical_version(root)
    written = []
    for path, pattern, template in _carriers(root):
        original = path.read_text(encoding="utf-8")
        updated, count = re.subn(pattern, lambda m: f"{m.group(1)}{_rendered(template, version)}{m.group(2)}", original)
        if not count:
            raise ValueError(f"No version field to update in {path}")
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            written.append(path)
    return written
