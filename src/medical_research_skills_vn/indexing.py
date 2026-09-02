"""Portable skill-index generation and reference reachability checks."""

from pathlib import Path

from .budgets import ValidationIssue, load_frontmatter


def build_index(root: Path) -> dict:
    root = Path(root)
    entries = []
    for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
        frontmatter, _ = load_frontmatter(skill_path)
        metadata = frontmatter.get("metadata", {})
        references = [
            path.relative_to(root).as_posix()
            for path in sorted((skill_path.parent / "references").glob("**/*"))
            if path.is_file()
        ]
        entries.append(
            {
                "name": frontmatter["name"],
                "purpose": frontmatter["description"],
                "role": metadata.get("role", "leaf"),
                "locale": metadata.get("locale", ["vi", "en"]),
                "document_types": metadata.get("document_types", []),
                "skill_path": skill_path.relative_to(root).as_posix(),
                "reference_files": references,
            }
        )
    return {"schema_version": "1.0.0", "skills": entries}


def validate_reference_callers(root: Path) -> list[ValidationIssue]:
    root = Path(root)
    issues = []
    for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
        body = skill_path.read_text(encoding="utf-8")
        references = skill_path.parent / "references"
        for reference in sorted(references.glob("**/*")) if references.exists() else []:
            if reference.is_file() and reference.name not in body:
                issues.append(
                    ValidationIssue(
                        "REFERENCE_ORPHAN",
                        str(reference),
                        f"{skill_path.name} does not explicitly name this reference",
                    )
                )
    return issues
