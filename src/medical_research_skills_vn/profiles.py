"""Validation for machine-readable target and locale profiles."""

from datetime import date
from pathlib import Path

import yaml

from .budgets import ValidationIssue
from .freshness import verification_status


REQUIRED_SOURCE_FIELDS = {
    "source_url",
    "source_version",
    "source_license",
    "source_cutoff",
    "last_verified",
    "expires_after_days",
    "verification_status",
}


def validate_profiles(root: Path, as_of: date) -> list[ValidationIssue]:
    issues = []
    for path in sorted((Path(root) / "profiles").glob("**/*.yaml")):
        profile = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        missing = REQUIRED_SOURCE_FIELDS - set(profile)
        if missing:
            issues.append(
                ValidationIssue(
                    "PROFILE_SOURCE_METADATA_MISSING",
                    str(path),
                    ", ".join(sorted(missing)),
                )
            )
            continue
        computed = verification_status(profile, as_of)
        if computed != profile["verification_status"]:
            issues.append(
                ValidationIssue(
                    "PROFILE_FRESHNESS_MISMATCH",
                    str(path),
                    f"declared {profile['verification_status']}, computed {computed}",
                )
            )
    return issues
