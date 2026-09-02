"""Deterministic ethics artifacts and source-register validation."""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from .freshness import verification_status


@dataclass(frozen=True)
class SourceIssue:
    code: str
    source_id: str
    message: str


@dataclass
class SourceValidationReport:
    issues: list[SourceIssue] = field(default_factory=list)
    banners: list[str] = field(default_factory=list)

    def has(self, code: str) -> bool:
        return any(issue.code == code for issue in self.issues)


def load_source_register(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def validate_source_registers(root: Path, as_of: date) -> list[SourceIssue]:
    issues = []
    for path in sorted(Path(root).glob("skills/*/references/source-register.yaml")):
        register = load_source_register(path)
        if not register.get("sources"):
            issues.append(SourceIssue("SOURCE_REGISTER_EMPTY", str(path), "At least one source is required"))
            continue
        issues.extend(validate_sources(register, as_of).issues)
    return issues


def validate_sources(register: dict, as_of: date) -> SourceValidationReport:
    report = SourceValidationReport()
    for source in register.get("sources", []):
        source_id = source.get("id", "<missing-id>")
        if source.get("source_type") != "PRIMARY":
            report.issues.append(SourceIssue("SOURCE_NOT_PRIMARY", source_id, "Primary source required"))

        status = verification_status(source, as_of)
        if status != source.get("verification_status"):
            report.issues.append(
                SourceIssue("SOURCE_STATUS_MISMATCH", source_id, f"Declared status differs from {status}")
            )
        if status == "STALE":
            report.issues.append(SourceIssue("SOURCE_STALE", source_id, "Reverify before applying current rules"))
            report.banners.append(f"SOURCE_STALE: {source_id}")
        elif status == "UNVERIFIED":
            report.issues.append(SourceIssue("SOURCE_UNVERIFIED", source_id, "Verification evidence missing"))
            report.banners.append(f"SOURCE_UNVERIFIED: {source_id}")

        coverage = source.get("coverage", {})
        expected = coverage.get("expected_identifiers", [])
        implemented = coverage.get("implemented_identifiers", [])
        if not expected or not implemented:
            report.issues.append(SourceIssue("SOURCE_COVERAGE_EMPTY", source_id, "Coverage identifiers required"))
        expected_count = coverage.get("expected_count")
        implemented_count = coverage.get("implemented_count")
        if (
            expected_count != len(expected)
            or implemented_count != len(implemented)
            or expected_count != implemented_count
        ):
            report.issues.append(
                SourceIssue(
                    "SOURCE_COVERAGE_COUNT_MISMATCH",
                    source_id,
                    "Declared counts must equal the exact identifier lists",
                )
            )
        if expected and implemented and expected != implemented:
            report.issues.append(
                SourceIssue("SOURCE_COVERAGE_MISMATCH", source_id, "Expected and implemented identifiers differ")
            )
    return report


def build_ethics_artifact(
    *,
    jurisdiction: str,
    study_stage: str,
    data_class: str,
    destination: str,
    approval_number: str | None,
    consent_state: str,
    registration_state: str,
) -> dict:
    unresolved = []
    if not approval_number:
        unresolved.append("OFFICIAL_RULE_REQUIRED")
    if consent_state == "UNRESOLVED":
        unresolved.append("AUTHOR_APPROVAL_REQUIRED")
    return {
        "jurisdiction": jurisdiction,
        "study_stage": study_stage,
        "data_class": data_class,
        "destination": destination,
        "authorization_basis": "UNRESOLVED",
        "consent_state": consent_state,
        "registration_state": registration_state,
        "approval_number": approval_number,
        "unresolved_approvals": sorted(set(unresolved)),
        "invented_values": [],
    }
