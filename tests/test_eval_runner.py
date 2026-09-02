import subprocess
import sys
from pathlib import Path

from medical_research_skills_vn.evaluation import run_scenario


ROOT = Path(__file__).parents[1]
SCENARIO = ROOT / "tests/cases/end-to-end/protocol-new-project.yaml"


def test_protocol_exemplar_preserves_explicit_provenance_and_planned_tense():
    result = run_scenario(SCENARIO, ROOT)

    assert result.errors == []
    assert result.artifacts["passport"]["research_question"]["status"] == "CONFIRMED"
    assert result.artifacts["passport"]["verified_results"] == []
    assert result.artifacts["ethics"]["approval_number"] is None
    assert result.artifacts["methods"]["claims_procedure_completed"] is False
    assert all(
        claim["execution_status"] == "PLANNED"
        for claim in result.artifacts["methods"]["procedure_claims"]
    )


def test_offline_cli_runs_checked_in_scenarios():
    completed = subprocess.run(
        [sys.executable, "tests/eval_runner.py", "--offline"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert "protocol-new-project: PASS" in completed.stdout


def test_unsupported_live_adapter_fails_clearly():
    completed = subprocess.run(
        [sys.executable, "tests/eval_runner.py", "--host", "chatgpt"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "adapter not implemented" in completed.stderr.lower()
