"""Deterministic contracts for section-level medical writing."""

from hashlib import sha256
import json
import re


class WritingContractError(ValueError):
    pass


OBSERVATIONAL_DESIGNS = {"cross-sectional", "case-control", "cohort", "ecological"}
REQUIRED_INPUTS = {
    "passport_hash",
    "target_profile",
    "locale_profile",
    "outline_approved",
    "source_ledger_version",
    "word_budget",
}


def _require_inputs(inputs: dict) -> None:
    missing = sorted(REQUIRED_INPUTS - set(inputs))
    if missing:
        raise WritingContractError(f"WRITING_INPUT_REQUIRED:{','.join(missing)}")
    if not inputs["outline_approved"]:
        raise WritingContractError("AUTHOR_APPROVAL_REQUIRED:section-outline")


def _claim_evidence_rows(claims: list[dict]) -> list[dict]:
    return [
        {
            "claim": claim.get("text", ""),
            "evidence_id": claim.get("evidence_id"),
            "result_verified": bool(claim.get("result_verified", False)),
            "source_verified": bool(claim.get("source_verified", False)),
            "artifact_id": claim.get("artifact_id"),
            "locator": claim.get("locator"),
            "full_text_locator": claim.get("full_text_locator"),
            "analysis_artifact_id": claim.get("analysis_artifact_id"),
        }
        for claim in claims
    ]


def _is_observational(design: str) -> bool:
    normalized = design.casefold()
    signals = OBSERVATIONAL_DESIGNS | {
        "observational",
        "retrospective",
        "prospective cohort",
        "đoàn hệ",
        "bệnh chứng",
        "cắt ngang",
        "quan sát",
    }
    return any(signal in normalized for signal in signals)


def _causal_text(text: str) -> bool:
    return bool(re.search(r"\b(cause[sd]?|effect|caused by)\b|gây ra|dẫn đến|tác động", text, re.I))


def build_section_artifact(*, section: str, inputs: dict, claims: list[dict]) -> dict:
    _require_inputs(inputs)
    section = section.casefold()
    markers: list[str] = []

    if section == "results":
        supplied_unverified = []
        for claim in claims:
            if claim.get("result_verified", False):
                continue
            if claim.get("output_status") == "USER_SUPPLIED_OUTPUT_UNVERIFIED":
                if not claim.get("artifact_id") or not claim.get("locator"):
                    raise WritingContractError("RESULT_ARTIFACT_LOCATOR_REQUIRED")
                supplied_unverified.append(claim)
            else:
                raise WritingContractError("VERIFIED_RESULTS_REQUIRED")
        if supplied_unverified:
            markers.append("AUTHOR_SUPPLIED_OUTPUT_UNVERIFIED")
        if any(
            claim.get("result_verified", False)
            and (not claim.get("artifact_id") or not claim.get("locator"))
            for claim in claims
        ):
            raise WritingContractError("RESULT_ARTIFACT_LOCATOR_REQUIRED")
        interpretive_flags = {"causal", "mechanism", "recommendation", "value_judgment"}
        if any(
            claim.get("kind") == "interpretation"
            or any(claim.get(flag, False) for flag in interpretive_flags)
            for claim in claims
        ):
            raise WritingContractError("RESULTS_INTERPRETATION_NOT_ALLOWED")
    elif section == "literature-review":
        if claims and any(not claim.get("theme") for claim in claims):
            raise WritingContractError("THEMATIC_SYNTHESIS_REQUIRED")
    elif section == "discussion":
        if not inputs.get("discussion_blueprint_approved", False):
            raise WritingContractError("AUTHOR_APPROVAL_REQUIRED:discussion-blueprint")
        if any(claim.get("copied_from_comparator", False) for claim in claims):
            raise WritingContractError("PHRASE_COPY_NOT_ALLOWED")
        if not inputs.get("study_design") or not inputs.get("inferential_ceiling"):
            raise WritingContractError("DISCUSSION_PREFLIGHT_REQUIRED")
        if _is_observational(inputs.get("study_design", "")) and any(
            claim.get("causal", False) or _causal_text(claim.get("text", "")) for claim in claims
        ):
            raise WritingContractError("CAUSAL_OVERREACH")
        citation_records = inputs.get("citation_verification_records", {})
        for claim in claims:
            if not claim.get("source_verified", False):
                markers.append("SOURCE_NEEDED")
            elif not all(
                claim.get(field)
                for field in (
                    "evidence_id",
                    "source_locator",
                    "access_level",
                    "support_verified",
                    "verification_record_id",
                )
            ):
                raise WritingContractError("CITATION_SUPPORT_RECORD_REQUIRED")
            elif not all(
                citation_records.get(claim["verification_record_id"], {}).get(field)
                for field in ("verified", "artifact_hash")
            ):
                raise WritingContractError("CITATION_VERIFICATION_ARTIFACT_REQUIRED")
        audits = inputs.get("discussion_audits", {})
        if claims and any(
            not isinstance(audits.get(name), dict)
            or audits[name].get("status") != "PASS"
            or not audits[name].get("artifact_id")
            or not audits[name].get("artifact_hash")
            for name in ("similarity", "causal_language", "citation")
        ):
            raise WritingContractError("DISCUSSION_AUDIT_REQUIRED")
    elif section == "conclusion":
        if any(not claim.get("present_in_results", False) for claim in claims):
            raise WritingContractError("NEW_FINDING_NOT_ALLOWED")
        if not inputs.get("study_design") or not inputs.get("inferential_ceiling"):
            raise WritingContractError("CONCLUSION_PREFLIGHT_REQUIRED")
        if _is_observational(inputs.get("study_design", "")) and any(
            claim.get("causal", False) or _causal_text(claim.get("text", "")) for claim in claims
        ):
            raise WritingContractError("CAUSAL_OVERREACH")
        required_basis = {"design", "certainty", "benefit_harm", "feasibility", "scope"}
        if any(
            claim.get("recommendation")
            and not all(
                isinstance(claim.get("recommendation_basis", {}).get(item), dict)
                and claim["recommendation_basis"][item].get("status") == "VERIFIED"
                and claim["recommendation_basis"][item].get("locator")
                for item in required_basis
            )
            for claim in claims
        ):
            raise WritingContractError("OVERCLAIM_BLOCKED")
    elif section == "abstract":
        lifecycle_state = inputs.get("abstract_state", "FINAL_VERIFIED")
        if lifecycle_state not in {"SKELETON", "DRAFT_FROM_INCOMPLETE_MANUSCRIPT", "SYNCED_DRAFT", "FINAL_VERIFIED"}:
            raise WritingContractError("ABSTRACT_STATE_INVALID")
        if lifecycle_state in {"SYNCED_DRAFT", "FINAL_VERIFIED"} and not inputs.get("full_text_ready", False):
            raise WritingContractError("FULL_TEXT_REQUIRED:final-abstract")
        if lifecycle_state in {"SYNCED_DRAFT", "FINAL_VERIFIED"}:
            if not all(
                inputs.get(field)
                for field in (
                    "manuscript_hash",
                    "manuscript_snapshot",
                    "manuscript_version",
                    "generation_timestamp",
                    "required_consistency_fields",
                )
            ):
                raise WritingContractError("MANUSCRIPT_SNAPSHOT_REQUIRED")
            if stable_snapshot_hash(inputs["manuscript_snapshot"]) != inputs["manuscript_hash"]:
                raise WritingContractError("MANUSCRIPT_SNAPSHOT_HASH_MISMATCH")
            required_fields = set(inputs["required_consistency_fields"])
            if not required_fields <= set(inputs.get("abstract_facts", {})) or not required_fields <= set(
                inputs.get("full_text_facts", {})
            ):
                raise WritingContractError("ABSTRACT_CONSISTENCY_COVERAGE_REQUIRED")
            conflicts = validate_abstract_consistency(
                abstract_facts=inputs.get("abstract_facts", {}),
                full_text_facts=inputs.get("full_text_facts", {}),
            )
            if conflicts:
                raise WritingContractError(f"BLOCKED_CONFLICT:{','.join(conflicts)}")
            if any(
                (claim.get("numeric") or re.search(r"\d", claim.get("text", "")))
                and (not claim.get("full_text_locator") or not claim.get("analysis_artifact_id"))
                for claim in claims
            ):
                raise WritingContractError("NUMERIC_PROVENANCE_REQUIRED")
        priority_pattern = re.compile(r"\b(first|novel|unprecedented|only)\b|đầu tiên|mới đầu tiên|duy nhất", re.I)
        novelty_unverified = any(
            (claim.get("novelty_claim") or priority_pattern.search(claim.get("text", "")))
            and not claim.get("novelty_verified")
            for claim in claims
        )
        if novelty_unverified:
            if lifecycle_state == "FINAL_VERIFIED":
                raise WritingContractError("NOVELTY_VERIFICATION_REQUIRED")
            markers.append("NOVELTY_VERIFICATION_REQUIRED")
    elif section == "introduction":
        if any(not claim.get("source_verified", False) for claim in claims):
            markers.append("SOURCE_NEEDED")

    draft = "\n\n".join(claim.get("text", "") for claim in claims if claim.get("text"))
    section_hash = sha256(draft.encode("utf-8")).hexdigest()
    artifact = {
        "section": section,
        "draft": draft,
        "claim_evidence": _claim_evidence_rows(claims),
        "markers": sorted(set(markers)),
        "dependencies": [inputs["passport_hash"], inputs["source_ledger_version"]],
        "author_approval_requests": ["SCIENTIFIC_INTERPRETATION_APPROVAL"],
        "locale_profile": inputs["locale_profile"],
        "target_profile": inputs["target_profile"],
        "word_budget": inputs["word_budget"],
        "section_hash": section_hash,
        "preflight": {
            "status": "REVISE" if markers else "PASS",
            "contract": "shared-writing-preflight",
            "markers": sorted(set(markers)),
        },
        "full_gate": {"status": "PENDING", "skill": "kiem-van-phong"},
    }
    if section == "abstract":
        artifact["lifecycle_state"] = lifecycle_state
        artifact["manuscript_hash"] = inputs.get("manuscript_hash")
        artifact["manuscript_version"] = inputs.get("manuscript_version")
        artifact["generation_timestamp"] = inputs.get("generation_timestamp")
        artifact["submission_verdict"] = (
            "READY_FOR_DOCUMENT_GATE"
            if lifecycle_state == "FINAL_VERIFIED" and not markers
            else "BLOCKED_INCOMPLETE_MANUSCRIPT"
            if lifecycle_state in {"SKELETON", "DRAFT_FROM_INCOMPLETE_MANUSCRIPT"}
            else "BLOCKED"
        )
    return artifact


def build_discussion_blueprint(
    *, comparators: list[dict], paper_selection_approved: bool, blueprint_approved: bool
) -> dict:
    if not paper_selection_approved or not blueprint_approved:
        raise WritingContractError("AUTHOR_APPROVAL_REQUIRED:discussion-workflow")
    permitted = {"author-supplied-full-text", "publisher-open-access", "repository-full-text", "pmc"}
    if not comparators or any(item.get("access") not in permitted for item in comparators):
        raise WritingContractError("FULL_TEXT_REQUIRED:discussion-reverse-engineering")
    return {
        "comparators": [
            {"doi": item.get("doi"), "access": item["access"], "stored_content": "functional-summary-only"}
            for item in comparators
        ],
        "moves": ["finding", "meaning", "comparison", "explanation", "limitation", "implication"],
        "copying_policy": "RHETORICAL_MOVES_ONLY_NO_PHRASE_COPY",
        "approved": True,
    }


def validate_abstract_consistency(*, abstract_facts: dict, full_text_facts: dict) -> list[str]:
    keys = sorted(set(abstract_facts) | set(full_text_facts))
    return [
        f"ABSTRACT_FULL_TEXT_MISMATCH:{key}"
        for key in keys
        if abstract_facts.get(key) != full_text_facts.get(key)
    ]


def stable_snapshot_hash(payload: dict) -> str:
    return sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
