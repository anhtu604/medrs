"""Decision support and interpretation ceilings, not statistical execution."""
from math import isfinite


def interpretation_ceiling(plan: dict, run: dict) -> dict:
    qualifications, unresolved = [], []
    prespecified = plan.get("prespecified") is True
    if not prespecified:
        qualifications.append("EXPLORATORY")
    multiple = run.get("multiple_tests")
    handled = run.get("multiplicity_addressed") is True
    if multiple is None:
        unresolved.append("MULTIPLICITY_UNKNOWN")
    elif multiple is True and not handled:
        qualifications.append("MULTIPLICITY_UNADDRESSED")
    execution_verified = run.get("status") == "RUN_VERIFIED"
    if not execution_verified:
        unresolved.append("EXECUTION_UNVERIFIED")
    if run.get("model") == "cox" and run.get("ph_pass") is False:
        qualifications.append("NONPROPORTIONAL_HAZARDS")
    if run.get("model") == "cox" and run.get("ph_pass") is None:
        unresolved.append("PH_UNCHECKED")
    causal = (plan.get("design") == "randomized-trial" and plan.get("randomization_verified") is True
              and run.get("causal_assumptions_met") is True and execution_verified)
    return {"causal_allowed": causal, "confirmatory_allowed": prespecified and (multiple is False or (multiple is True and handled)),
            "qualifications": qualifications, "unresolved": unresolved}


def select_basic_test(problem: dict) -> dict:
    if problem.get("clustered") is True:
        return {"status": "SPECIALIST_REVIEW_REQUIRED", "test": None}
    paired, kind = problem.get("paired"), problem.get("outcome_type")
    if paired is None:
        return {"status": "DESIGN_REQUIRED", "test": None}
    if kind == "continuous" and paired:
        if problem.get("mean_difference_estimand") is True and problem.get("difference_mean_inference_supported") is True:
            return {"status": "CANDIDATE", "test": "paired-t"}
        return {"status": "ASSUMPTIONS_REQUIRED", "test": None}
    if kind == "continuous" and paired is False:
        if problem.get("mean_inference_supported") is True:
            return {"status": "CANDIDATE", "test": "pooled-t" if problem.get("equal_variance_supported") is True else "welch-t"}
        return {"status": "ASSUMPTIONS_REQUIRED", "test": None}
    if kind == "categorical" and paired:
        return {"status": "SPECIALIST_REVIEW_REQUIRED", "test": "paired-categorical-review"}
    if kind == "categorical" and problem.get("counts_verified") is True:
        if problem.get("sparse") is True:
            return {"status": "CANDIDATE", "test": "fisher-exact"}
        if problem.get("chi_square_assumptions_supported") is True:
            return {"status": "CANDIDATE", "test": "chi-square"}
    return {"status": "ASSUMPTIONS_REQUIRED", "test": None}


def validate_extraction(record: dict) -> list[str]:
    issues = []
    for field in ("source_locator", "outcome", "group", "time", "adjustment"):
        if record.get(field) in (None, ""):
            issues.append(f"IDENTITY_REQUIRED:{field}")
    if record.get("secondary_only") is True:
        issues.append("PRIMARY_SOURCE_REQUIRED")
    available = record.get("outcome_available_n")
    if not isinstance(available, int) or isinstance(available, bool) or available < 1:
        issues.append("OUTCOME_N_REQUIRED")
    elif record.get("reported_n") != available:
        issues.append("OUTCOME_DENOMINATOR_MISMATCH")
    if not record.get("measure") or not record.get("reported_measure"):
        issues.append("EFFECT_MEASURE_REQUIRED")
    elif record.get("measure") != record.get("reported_measure"):
        issues.append("EFFECT_MEASURE_MISMATCH")
    return issues


def threshold_policy(request: dict) -> dict:
    if request.get("requested") is not True:
        return {"mode": "CONTINUOUS", "classification": "PRESPECIFIED", "all_attempts_required": True}
    source = bool(request.get("source_url")) and request.get("source_kind") in {"consensus", "reference-range", "single-study"}
    approved = source and request.get("protocol_approved") is True and request.get("outcome_seen") is False
    return {"mode": "THRESHOLD", "classification": "PRESPECIFIED" if approved else "EXPLORATORY",
            "all_attempts_required": True, "source_required": not source,
            "applicability_review_required": True}


def format_p(value: float, digits: int = 3) -> str:
    if not isinstance(value, (float, int)) or isinstance(value, bool) or not isfinite(value) or not 0 <= value <= 1:
        raise ValueError("INVALID_P_VALUE")
    if not isinstance(digits, int) or not 1 <= digits <= 10:
        raise ValueError("INVALID_P_PRECISION")
    threshold = 10 ** -digits
    return f"<{threshold:.{digits}f}" if value < threshold else f"{value:.{digits}f}"
