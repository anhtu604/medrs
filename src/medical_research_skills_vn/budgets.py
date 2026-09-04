"""Context-budget validation primitives."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import yaml


WORD_PATTERN = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str


def count_words(text: str) -> int:
    return len(WORD_PATTERN.findall(text))


def utf8_size(text: str) -> int:
    return len(text.encode("utf-8"))


def issue_codes(issues: list[ValidationIssue]) -> set[str]:
    return {issue.code for issue in issues}


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML frontmatter: {path}")
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(f"Unterminated YAML frontmatter: {path}") from exc
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter must be a mapping: {path}")
    return data, body


def validate_context_budget(root: Path, legacy_names: set[str] | None = None) -> list[ValidationIssue]:
    root = Path(root)
    legacy_names = legacy_names or set()
    issues: list[ValidationIssue] = []
    total_description_words = 0
    total_description_bytes = 0
    total_frontmatter_bytes = 0

    for path in sorted((root / "skills").glob("*/SKILL.md")):
        try:
            frontmatter, _ = load_frontmatter(path)
        except ValueError as exc:
            issues.append(ValidationIssue("FRONTMATTER_INVALID", str(path), str(exc)))
            continue
        description = str(frontmatter.get("description", ""))
        words = count_words(description)
        size = utf8_size(description)
        total_description_words += words
        total_description_bytes += size
        total_frontmatter_bytes += utf8_size(yaml.safe_dump(frontmatter, allow_unicode=True))
        if words > 60:
            issues.append(ValidationIssue("DESCRIPTION_WORDS", str(path), f"{words} > 60"))
        if size > 640:
            issues.append(ValidationIssue("DESCRIPTION_BYTES", str(path), f"{size} > 640"))
        for legacy_name in legacy_names:
            if legacy_name.casefold() in description.casefold():
                issues.append(ValidationIssue("LEGACY_NAME_IN_DESCRIPTION", str(path), legacy_name))
        skill_words = count_words(path.read_text(encoding="utf-8"))
        skill_bytes = path.stat().st_size
        name = path.parent.name
        word_limit = 900 if name == "medrs" else 1200
        byte_limit = 12288 if name == "medrs" else 16384
        if skill_words > word_limit:
            issues.append(ValidationIssue("SKILL_WORDS", str(path), f"{skill_words} > {word_limit}"))
        if skill_bytes > byte_limit:
            issues.append(ValidationIssue("SKILL_BYTES", str(path), f"{skill_bytes} > {byte_limit}"))

    if total_description_words > 1200:
        issues.append(ValidationIssue("DESCRIPTION_AGGREGATE_WORDS", "skills", f"{total_description_words} > 1200"))
    if total_description_bytes > 12288:
        issues.append(ValidationIssue("DESCRIPTION_AGGREGATE_BYTES", "skills", f"{total_description_bytes} > 12288"))
    if total_frontmatter_bytes > 16384:
        issues.append(ValidationIssue("FRONTMATTER_AGGREGATE_BYTES", "skills", f"{total_frontmatter_bytes} > 16384"))

    inventory_path = root / "config/canonical-skills.yaml"
    if inventory_path.exists():
        inventory = yaml.safe_load(inventory_path.read_text(encoding="utf-8"))
        reserved = sum(int(item["description_target_words"]) for item in inventory["skills"])
        if reserved > int(inventory["description_limits"]["aggregate_words"]):
            issues.append(ValidationIssue("DESCRIPTION_RESERVED_WORDS", str(inventory_path), str(reserved)))
    return issues
