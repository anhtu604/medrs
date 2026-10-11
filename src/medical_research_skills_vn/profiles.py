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


def official_profile_readiness(profile: dict, as_of: date) -> str:
    """Adapt existing target profiles to the portable source/scope policy."""
    import sys
    sys.path.insert(0, str(Path(__file__).parents[2] / "skills/bo-cuc-tai-lieu/scripts"))
    from profile_policy import profile_readiness, adapt_source_profile
    return profile_readiness(adapt_source_profile(profile), as_of.isoformat())


def validate_profiles(root: Path, as_of: date) -> list[ValidationIssue]:
    issues = []
    profile_root = Path(root) / "profiles"
    for path in sorted(profile_root.glob("**/*.yaml")):
        if path.relative_to(profile_root).parts[0] == "document-type":
            continue
        profile = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if "source_kind" in profile:
            readiness = official_profile_readiness(profile, as_of)
            if readiness != "READY":
                issues.append(ValidationIssue("PROFILE_OFFICIAL_READINESS", str(path), readiness))
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
