"""Canonical skill-inventory lifecycle validation."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from .budgets import ValidationIssue


VALID_STATUSES = {"planned", "active", "accepted"}


@dataclass(frozen=True)
class SkillRecord:
    name: str
    slice: int
    status: str


def load_inventory(root: Path) -> list[SkillRecord]:
    path = Path(root) / "config/canonical-skills.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [
        SkillRecord(
            name=str(item["name"]),
            slice=int(item["slice"]),
            status=str(item.get("status", "accepted" if item.get("active") else "planned")),
        )
        for item in data.get("skills", [])
    ]


def validate_inventory(root: Path) -> list[ValidationIssue]:
    root = Path(root)
    issues: list[ValidationIssue] = []
    for record in load_inventory(root):
        if record.status not in VALID_STATUSES:
            issues.append(
                ValidationIssue("SKILL_STATUS_INVALID", record.name, record.status)
            )
            continue
        entrypoint = root / "skills" / record.name / "SKILL.md"
        if record.status in {"active", "accepted"} and not entrypoint.is_file():
            issues.append(
                ValidationIssue(
                    "ACCEPTED_SKILL_MISSING",
                    str(entrypoint),
                    f"{record.name} is {record.status} but has no entrypoint",
                )
            )
    return issues
