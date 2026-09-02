"""Traceable statistical-analysis orchestration for R and Stata."""

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable


VALID_BACKENDS = {"r", "stata"}


class AnalysisPolicyError(ValueError):
    """Raised when a requested analysis change violates the prespecified plan."""

    code = "RESEARCH_INTEGRITY_BLOCKED"

    def __init__(self, message: str, safe_alternative: str):
        super().__init__(message)
        self.safe_alternative = safe_alternative


@dataclass(frozen=True)
class BackendScript:
    backend: str
    extension: str
    text: str
    plan_hash: str
    input_hash: str
    assumption_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalysisRun:
    backend: str
    runtime_verified: bool
    runtime_executable: str | None
    runtime_version: str | None
    command: str
    code_hash: str
    input_hash: str | None
    output_paths: tuple[str, ...]
    output_hashes: dict[str, str]
    deviations: tuple[str, ...]
    status: str
    exit_code: int | None
    notes: str = ""

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["output_paths"] = list(self.output_paths)
        payload["deviations"] = list(self.deviations)
        return payload


def _hash_bytes(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _hash_file(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


def _validate_backend(backend: str) -> str:
    normalized = backend.casefold()
    if normalized not in VALID_BACKENDS:
        raise ValueError(f"Unsupported analysis backend: {backend}")
    return normalized


def assess_analysis_change(*, action: str, basis: str, prespecified: bool) -> dict:
    """Reject result-driven changes while allowing traceable prespecified actions."""
    normalized_action = action.casefold()
    normalized_basis = basis.casefold()
    significance_signals = ("p_value", "p-value", "significance", "statistical_significance")

    if normalized_action == "select_model" and (
        not prespecified or any(signal in normalized_basis for signal in significance_signals)
    ):
        raise AnalysisPolicyError(
            "Model selection for significance is prohibited; use the prespecified estimand, design, and assumptions.",
            "Retain the prespecified primary model, inventory all attempted specifications, and label justified extras as sensitivity or exploratory analyses.",
        )
    if normalized_action == "reduce_target_sample_to_observed_n":
        raise AnalysisPolicyError(
            "The target sample cannot be rewritten after recruitment; preserve planned and achieved sample sizes separately.",
            "Report under-recruitment as a deviation and discuss its effect on precision or power.",
        )
    if normalized_action == "delete_outliers" and not prespecified:
        raise AnalysisPolicyError(
            "outlier deletion needs a prespecified rule or documented data-error evidence, plus a sensitivity analysis.",
            "Keep the primary dataset and report prespecified or influence analyses with and without the observation.",
        )
    return {
        "decision": "ALLOW",
        "classification": "PRESPECIFIED" if prespecified else "EXPLORATORY",
        "action": action,
        "basis": basis,
    }


def create_analysis_run(
    *,
    backend: str,
    command: str,
    code: str,
    input_path: Path,
    output_paths: Iterable[Path] = (),
    runtime_executable: str | None = None,
    runtime_version: str | None = None,
    executed: bool = False,
    exit_code: int | None = None,
    deviations: Iterable[str] = (),
) -> AnalysisRun:
    """Create provenance from real files; this function never executes analysis code."""
    normalized_backend = _validate_backend(backend)
    input_path = Path(input_path)
    if not input_path.is_file():
        raise FileNotFoundError(input_path)

    if executed and (not runtime_executable or not runtime_version or exit_code is None):
        raise ValueError("Verified execution requires runtime evidence: executable, version, and exit code.")

    if executed:
        normalized_outputs = tuple(str(Path(path)) for path in output_paths)
        for path in normalized_outputs:
            if not Path(path).is_file():
                raise FileNotFoundError(path)
        output_hashes = {path: _hash_file(Path(path)) for path in normalized_outputs}
        status = "RUN_VERIFIED" if exit_code == 0 else "RUN_FAILED"
    else:
        normalized_outputs = ()
        output_hashes = {}
        status = "NOT_RUN"
        exit_code = None

    return AnalysisRun(
        backend=normalized_backend,
        runtime_verified=executed,
        runtime_executable=runtime_executable if executed else None,
        runtime_version=runtime_version if executed else None,
        command=command,
        code_hash=_hash_bytes(code.encode("utf-8")),
        input_hash=_hash_file(input_path),
        output_paths=normalized_outputs,
        output_hashes=output_hashes,
        deviations=tuple(deviations),
        status=status,
        exit_code=exit_code,
        notes="Analysis was not executed." if not executed else "Execution evidence recorded.",
    )


def interpret_supplied_output(*, backend: str, output_path: Path) -> AnalysisRun:
    """Register author-supplied output without laundering it into a local run claim."""
    normalized_backend = _validate_backend(backend)
    output_path = Path(output_path)
    if not output_path.is_file():
        raise FileNotFoundError(output_path)
    path_text = str(output_path)
    return AnalysisRun(
        backend=normalized_backend,
        runtime_verified=False,
        runtime_executable=None,
        runtime_version=None,
        command="",
        code_hash="",
        input_hash=None,
        output_paths=(path_text,),
        output_hashes={path_text: _hash_file(output_path)},
        deviations=(),
        status="USER_SUPPLIED_OUTPUT_UNVERIFIED",
        exit_code=None,
        notes="Interpret conditionally; execution and linkage to the source dataset are unverified.",
    )


def validate_run_artifacts(run: AnalysisRun) -> list[str]:
    issues: list[str] = []
    for path_text, expected_hash in run.output_hashes.items():
        path = Path(path_text)
        if not path.is_file():
            issues.append(f"OUTPUT_MISSING:{path}")
        elif _hash_file(path) != expected_hash:
            issues.append(f"OUTPUT_HASH_MISMATCH:{path}")
    return issues


def generate_backend_script(
    *,
    backend: str,
    plan_hash: str,
    input_hash: str,
    analysis_commands: Iterable[str],
    assumption_artifacts: Iterable[str],
) -> BackendScript:
    normalized_backend = _validate_backend(backend)
    artifacts = tuple(assumption_artifacts)
    if not plan_hash or not input_hash:
        raise ValueError("plan_hash and input_hash are required")
    if not artifacts:
        raise ValueError("At least one assumption-reporting artifact is required")

    marker = "#" if normalized_backend == "r" else "*"
    provenance = [
        f"{marker} GENERATED ANALYSIS TEMPLATE — NOT RUN",
        f"{marker} analysis_plan_sha256: {plan_hash}",
        f"{marker} input_sha256: {input_hash}",
        f"{marker} required_assumption_artifacts: {', '.join(artifacts)}",
    ]
    commands = list(analysis_commands)
    if normalized_backend == "r":
        text = "\n".join(provenance + commands + ["sessionInfo()", ""])
        extension = ".R"
    else:
        text = "\n".join(provenance + ["about"] + commands + [""])
        extension = ".do"
    return BackendScript(
        backend=normalized_backend,
        extension=extension,
        text=text,
        plan_hash=plan_hash,
        input_hash=input_hash,
        assumption_artifacts=artifacts,
    )
