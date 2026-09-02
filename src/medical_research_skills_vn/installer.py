"""Validation helpers for repository-first installation."""

import json
from pathlib import Path


def validate_install_source(root: Path) -> dict:
    root = Path(root)
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    index_path = root / "skills/index.json"
    if not index_path.is_file():
        return {"status": "INVALID", "reason": "SKILL_INDEX_MISSING"}
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"status": "INVALID", "reason": "SKILL_INDEX_INVALID"}
    disk_names = {path.parent.name for path in skill_files}
    index_names = {item.get("name") for item in index.get("skills", [])}
    if len(disk_names) != 24 or len(index_names) != 24 or disk_names != index_names:
        return {"status": "INVALID", "reason": "CANONICAL_SKILL_SET_MISMATCH"}
    required = ("coverage", "profiles", "schemas", "config/canonical-skills.yaml")
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        return {"status": "INVALID", "reason": "SHARED_RESOURCE_MISSING", "missing": missing}
    return {"status": "VALID", "skills": sorted(disk_names)}
