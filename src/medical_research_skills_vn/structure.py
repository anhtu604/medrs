"""Structural validation for cross-skill contracts."""

from pathlib import Path

from .budgets import ValidationIssue


WRITING_SKILLS = {
    "viet-phuong-phap",
    "viet-dat-van-de",
    "viet-tong-quan",
    "viet-ket-qua",
    "viet-ban-luan",
    "viet-ket-luan-khuyen-nghi",
    "viet-tom-tat",
}
SHARED_LINK_SUFFIX = "viet-phuong-phap/references/writing-preflight.md"


def validate_shared_preflight(root):
    root = Path(root)
    issues: list[ValidationIssue] = []
    shared = root / "skills/viet-phuong-phap/references/writing-preflight.md"
    if not shared.exists():
        issues.append(ValidationIssue("SHARED_PREFLIGHT_MISSING", str(shared), "shared contract not found"))
    for name in WRITING_SKILLS:
        path = root / "skills" / name / "SKILL.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        expected = "references/writing-preflight.md" if name == "viet-phuong-phap" else f"../{SHARED_LINK_SUFFIX}"
        if text.count(expected) != 1:
            issues.append(
                ValidationIssue("SHARED_PREFLIGHT_NOT_CALLED", str(path), "writer must call shared contract exactly once")
            )
        if "PREFLIGHT_RULE:" in text:
            issues.append(ValidationIssue("PREFLIGHT_RULE_DUPLICATED", str(path), "move rule to shared contract"))
    return issues
