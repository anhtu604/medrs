"""Coverage-manifest validation for externally governed instruments."""

from pathlib import Path

import yaml

from .budgets import ValidationIssue


REQUIRED_METADATA = {"instrument", "version", "source_url", "license", "last_verified", "caller"}


def load_coverage_manifest(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def validate_coverage_manifest(manifest: dict) -> list[str]:
    issues: list[str] = []
    missing_metadata = sorted(REQUIRED_METADATA - set(manifest))
    issues.extend(f"METADATA_MISSING:{field}" for field in missing_metadata)
    for field in REQUIRED_METADATA:
        if field in manifest and not str(manifest[field]).strip():
            issues.append(f"METADATA_EMPTY:{field}")
    expected = list(manifest.get("expected_ids", []))
    implemented = list(manifest.get("implemented_ids", []))
    if expected != implemented or len(expected) != len(set(expected)):
        issues.append("COVERAGE_MISMATCH")
    items = {str(item.get("id")): item for item in manifest.get("items", [])}
    if set(items) != set(expected):
        issues.append("ITEM_SET_MISMATCH")
    for identifier in expected:
        item = items.get(identifier, {})
        if not item.get("operational_prompt") or not item.get("source_locator"):
            issues.append(f"ITEM_CONTENT_MISSING:{identifier}")
    if manifest.get("caller") and not Path(manifest["caller"]).is_file():
        issues.append("CALLER_MISSING")
    return issues


def validate_coverage_manifests(root: Path) -> list[ValidationIssue]:
    issues = []
    for path in sorted((Path(root) / "coverage").glob("*.yaml")):
        for message in validate_coverage_manifest(load_coverage_manifest(path)):
            issues.append(ValidationIssue("COVERAGE_MANIFEST_INVALID", str(path), message))
    return issues
