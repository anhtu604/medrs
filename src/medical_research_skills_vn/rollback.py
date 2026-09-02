"""Isolated rollback simulation; never touches a live plugin cache."""

import shutil
from pathlib import Path
import zipfile
import json

from .packaging import build_package


def _safe_extract(archive: Path, destination: Path) -> None:
    destination = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            target.relative_to(destination)
        bundle.extractall(destination)


def _skill_count(installation: Path) -> int:
    return len(list((installation / "skills").glob("*/SKILL.md")))


def _v2_present(installation: Path) -> bool:
    manifest = installation / ".claude-plugin/plugin.json"
    if not manifest.exists():
        return False
    version = str(json.loads(manifest.read_text(encoding="utf-8-sig")).get("version", ""))
    return version.startswith("2.")


def simulate_rollback(root: Path, workspace: Path, rollback_archive: Path) -> dict:
    root = Path(root).resolve()
    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    install = (workspace / "plugin-install").resolve()
    install.relative_to(workspace)
    package = build_package(root, workspace / "v2.zip")
    _safe_extract(package, install)
    v2_count = _skill_count(install)

    if install.exists():
        install.relative_to(workspace)
        shutil.rmtree(install)
    install.mkdir(parents=True)
    _safe_extract(Path(rollback_archive), install)
    v1_count = _skill_count(install)
    v2_present = _v2_present(install)
    return {
        "v2_skill_count": v2_count,
        "v1_skill_count": v1_count,
        "simultaneous_install_detected": bool(v2_present and v1_count),
        "v2_present_after_rollback": v2_present,
    }
