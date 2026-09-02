"""Deterministic state and safety checks for the medical writing gate."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


@dataclass(frozen=True)
class ClaimAudit:
    status: str
    findings: tuple[Finding, ...]


@dataclass(frozen=True)
class FormulaicAudit:
    findings: tuple[Finding, ...]
    ai_authorship: None = None
    detector_score: None = None


@dataclass(frozen=True)
class AuditState:
    document_hash: str
    section_hashes: dict[str, str]
    locale_profile_version: str
    source_ledger_version: str
    reference_versions: dict[str, str]


@dataclass(frozen=True)
class ReauditPlan:
    reuse: set[str]
    reaudit: set[str]
    run_global_consistency: bool


OBSERVATIONAL_DESIGNS = {"cross-sectional", "case-control", "cohort", "ecological"}
CAUSAL_PATTERN = re.compile(r"\b(cause[sd]?|caused by|prove[sd]?)\b", re.IGNORECASE)


def audit_claims(claims: list[dict]) -> ClaimAudit:
    findings: list[Finding] = []
    for claim in claims:
        if not claim.get("citation_verified", False):
            findings.append(Finding("SOURCE_UNVERIFIED", "Citation has not been verified."))
        if not claim.get("result_verified", False):
            findings.append(Finding("VERIFIED_RESULTS_REQUIRED", "Result provenance is missing."))
        design = str(claim.get("study_design", "")).casefold()
        if design in OBSERVATIONAL_DESIGNS and CAUSAL_PATTERN.search(str(claim.get("text", ""))):
            findings.append(
                Finding("CAUSAL_OVERREACH", "Causal wording exceeds the observational design.")
            )
    return ClaimAudit("PASS" if not findings else "REVISE", tuple(findings))


def audit_formulaic_patterns(text: str) -> FormulaicAudit:
    lowered = text.casefold()
    findings: list[Finding] = []
    if any(term in lowered for term in ("pivotal", "underscore", "ever-evolving landscape")):
        findings.append(
            Finding("GENERIC_SIGNIFICANCE", "Replace generic importance with the specific result and implication.")
        )
    if "not only" in lowered and "but also" in lowered:
        findings.append(
            Finding("NEGATIVE_PARALLELISM", "Check whether the paired construction adds meaning.")
        )
    return FormulaicAudit(tuple(findings))


def plan_reaudit(
    previous: AuditState,
    current: AuditState,
    source_dependent_sections: set[str],
) -> ReauditPlan:
    section_names = set(previous.section_hashes) | set(current.section_hashes)
    if (
        previous.locale_profile_version != current.locale_profile_version
        or previous.reference_versions != current.reference_versions
    ):
        reaudit = section_names
    else:
        reaudit = {
            name
            for name in section_names
            if previous.section_hashes.get(name) != current.section_hashes.get(name)
        }
        if previous.source_ledger_version != current.source_ledger_version:
            reaudit |= source_dependent_sections
    reuse = section_names - reaudit
    return ReauditPlan(
        reuse=reuse,
        reaudit=reaudit,
        run_global_consistency=(previous.document_hash != current.document_hash or bool(reaudit)),
    )
