import medical_research_skills_vn


def test_claim_audit_marks_unverified_citation_and_cross_sectional_causality():
    claims = [
        {
            "text": "Night-shift work causes hypertension [Nguyen et al., 2024].",
            "study_design": "cross-sectional",
            "citation_verified": False,
            "result_verified": True,
        }
    ]

    result = medical_research_skills_vn.style_gate.audit_claims(claims)

    assert result.status == "REVISE"
    assert {finding.code for finding in result.findings} == {
        "CAUSAL_OVERREACH",
        "SOURCE_UNVERIFIED",
    }


def test_formulaic_patterns_are_quality_flags_not_ai_authorship_scores():
    text = (
        "These pivotal findings not only underscore the importance of screening, "
        "but also highlight the complex and ever-evolving landscape of health."
    )

    result = medical_research_skills_vn.style_gate.audit_formulaic_patterns(text)

    assert {finding.code for finding in result.findings} >= {
        "GENERIC_SIGNIFICANCE",
        "NEGATIVE_PARALLELISM",
    }
    assert result.ai_authorship is None
    assert result.detector_score is None


def test_audit_state_reuses_unchanged_sections_and_invalidates_source_dependents():
    previous = medical_research_skills_vn.style_gate.AuditState(
        document_hash="doc-v1",
        section_hashes={"methods": "m1", "discussion": "d1"},
        locale_profile_version="vi-1",
        source_ledger_version="sources-1",
        reference_versions={"composition-vi": "1"},
    )
    current = medical_research_skills_vn.style_gate.AuditState(
        document_hash="doc-v2",
        section_hashes={"methods": "m1", "discussion": "d2"},
        locale_profile_version="vi-1",
        source_ledger_version="sources-2",
        reference_versions={"composition-vi": "1"},
    )

    decision = medical_research_skills_vn.style_gate.plan_reaudit(
        previous,
        current,
        source_dependent_sections={"discussion"},
    )

    assert decision.reuse == {"methods"}
    assert decision.reaudit == {"discussion"}
    assert decision.run_global_consistency is True
