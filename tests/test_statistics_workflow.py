from pathlib import Path

import pytest
from jsonschema import validate
import json

from medical_research_skills_vn.statistics import (
    AnalysisPolicyError,
    assess_analysis_change,
    create_analysis_run,
    generate_backend_script,
    interpret_supplied_output,
    validate_run_artifacts,
)


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "statistics"


def test_significance_driven_model_selection_is_refused():
    with pytest.raises(AnalysisPolicyError, match="significance") as caught:
        assess_analysis_change(
            action="select_model",
            basis="smallest_p_value_after_twelve_models",
            prespecified=False,
        )
    assert caught.value.code == "RESEARCH_INTEGRITY_BLOCKED"
    assert caught.value.safe_alternative


def test_post_hoc_target_sample_reduction_is_refused():
    with pytest.raises(AnalysisPolicyError, match="target sample"):
        assess_analysis_change(
            action="reduce_target_sample_to_observed_n",
            basis="recruitment_finished",
            prespecified=False,
        )


def test_outlier_deletion_requires_prespecified_rule_or_error_evidence():
    with pytest.raises(AnalysisPolicyError, match="outlier"):
        assess_analysis_change(
            action="delete_outliers",
            basis="results_look_better",
            prespecified=False,
        )


def test_missing_runtime_produces_code_but_never_an_execution_claim(tmp_path):
    data = tmp_path / "analysis.csv"
    data.write_bytes((FIXTURES / "descriptive.csv").read_bytes())
    run = create_analysis_run(
        backend="r",
        command="Rscript analysis.R",
        code="summary(read.csv('analysis.csv'))",
        input_path=data,
        runtime_executable=None,
    )

    assert run.status == "NOT_RUN"
    assert run.runtime_verified is False
    assert run.output_paths == ()
    assert run.code_hash
    assert run.input_hash


def test_supplied_real_output_is_traceable_but_not_claimed_as_locally_executed():
    output = FIXTURES / "r_regression_output.txt"
    run = interpret_supplied_output(backend="r", output_path=output)

    assert run.status == "USER_SUPPLIED_OUTPUT_UNVERIFIED"
    assert run.runtime_verified is False
    assert run.output_hashes[str(output)]
    assert "interpret conditionally" in run.notes.lower()


@pytest.mark.parametrize(
    ("backend", "extension", "required_text"),
    [
        ("r", ".R", "sessionInfo()"),
        ("stata", ".do", "about"),
    ],
)
def test_backend_scripts_embed_provenance_and_assumption_outputs(
    backend, extension, required_text
):
    script = generate_backend_script(
        backend=backend,
        plan_hash="plan-sha256",
        input_hash="input-sha256",
        analysis_commands=["MODEL_COMMAND"],
        assumption_artifacts=["model_diagnostics.txt", "missing_data_summary.csv"],
    )

    assert script.extension == extension
    assert "plan-sha256" in script.text
    assert "input-sha256" in script.text
    assert required_text in script.text
    assert "model_diagnostics.txt" in script.text
    assert "missing_data_summary.csv" in script.text


def test_output_hash_mismatch_is_detected_after_a_verified_run(tmp_path):
    data = tmp_path / "analysis.csv"
    data.write_bytes((FIXTURES / "descriptive.csv").read_bytes())
    output = tmp_path / "table.csv"
    output.write_text("term,estimate\nexposure,1.2\n", encoding="utf-8")
    run = create_analysis_run(
        backend="stata",
        command="stata-mp -b do analysis.do",
        code="regress outcome exposure",
        input_path=data,
        output_paths=[output],
        runtime_executable="C:/Program Files/Stata/StataMP-64.exe",
        runtime_version="Stata 18",
        executed=True,
        exit_code=0,
    )
    output.write_text("term,estimate\nexposure,9.9\n", encoding="utf-8")

    issues = validate_run_artifacts(run)

    assert issues == [f"OUTPUT_HASH_MISMATCH:{output}"]


def test_verified_execution_requires_runtime_version_and_success_exit(tmp_path):
    data = tmp_path / "analysis.csv"
    data.write_bytes((FIXTURES / "descriptive.csv").read_bytes())

    with pytest.raises(ValueError, match="runtime evidence"):
        create_analysis_run(
            backend="r",
            command="Rscript analysis.R",
            code="summary(read.csv('analysis.csv'))",
            input_path=data,
            runtime_executable="Rscript",
            runtime_version=None,
            executed=True,
            exit_code=0,
        )


def test_analysis_run_serialization_matches_schema(tmp_path):
    data = tmp_path / "analysis.csv"
    data.write_bytes((FIXTURES / "descriptive.csv").read_bytes())
    run = create_analysis_run(
        backend="r",
        command="Rscript analysis.R",
        code="summary(read.csv('analysis.csv'))",
        input_path=data,
    )
    schema = json.loads((ROOT / "schemas" / "analysis-run.schema.json").read_text(encoding="utf-8"))

    validate(instance=run.to_dict(), schema=schema)
