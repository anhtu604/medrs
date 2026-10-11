"""Packaged execution and honest status/evidence contracts."""
from pathlib import Path
import json
import subprocess
import sys
import zipfile
from medical_research_skills_vn.packaging import build_cowork_package, build_package
from revision_guard import final_acceptance, sha256

ROOT = Path(__file__).parents[1]


def test_cowork_contains_portable_runtime_and_user_readme(tmp_path):
    archive = build_cowork_package(ROOT, tmp_path / "cowork.zip")
    with zipfile.ZipFile(archive) as bundle:
        assert "skills/dinh-dang-tai-lieu/scripts/docx_integrity.py" in bundle.namelist()
        assert "skills/leader-nghien-cuu/scripts/project_workspace.py" in bundle.namelist()
        assert bundle.read("README.md") == (ROOT / "docs/cowork-README.md").read_bytes()
        assert "docs/source-gaps.md" in bundle.namelist()
        assert "schemas/status-codes.json" in bundle.namelist()


def test_repository_package_contains_reporting_coverage(tmp_path):
    archive = build_package(ROOT, tmp_path / "repository.zip")
    with zipfile.ZipFile(archive) as bundle:
        assert "coverage/cross-2021.yaml" in bundle.namelist()


def test_no_private_source_snapshots_ship_in_either_package(tmp_path):
    root = tmp_path / "fixture"
    private = root / "sources/journals/snapshots/private.html"
    private.parent.mkdir(parents=True)
    private.write_text("synthetic private original", encoding="utf-8")
    for build in (build_package, build_cowork_package):
        with zipfile.ZipFile(build(root, tmp_path / (build.__name__ + ".zip"))) as bundle:
            assert "sources/journals/snapshots/private.html" not in bundle.namelist()


def test_extracted_zip_access_and_registry_run_without_repository(tmp_path):
    extracted = tmp_path / "sandbox"
    with zipfile.ZipFile(build_cowork_package(ROOT, tmp_path / "cowork.zip")) as bundle:
        bundle.extractall(extracted)
    assert not (extracted / "src").exists()
    assert not (extracted / "scripts").exists()
    code = """
import runpy, json
p = runpy.run_path('skills/tim-y-van/scripts/access_policy.py')
g = runpy.run_path('skills/leader-nghien-cuu/scripts/revision_guard.py')
print(json.dumps({
 'access': p['access_state']([{'http_status':403,'hits':None}]),
 'unknown': g['status_receipt_issues']({'status':'FAKE_PASS'}, 'artifact-check'),
 'notrun': g['status_receipt_issues']({'status':'NOT_RUN'}, 'runtime'),
 'unperformed': g['status_receipt_issues']({'status':'UNPERFORMED'}, 'artifact-check')
}))
"""
    result = subprocess.run([sys.executable, "-I", "-c", code], cwd=extracted,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data == {"access": "INACCESSIBLE", "unknown": ["STATUS_UNKNOWN:FAKE_PASS"],
                    "notrun": [], "unperformed": []}


def test_status_registry_rejects_pass_without_evidence_and_wrong_context():
    from revision_guard import status_receipt_issues
    assert "STATUS_CONTEXT_INVALID:ACCEPTED_INTERNAL" in status_receipt_issues(
        {"status": "ACCEPTED_INTERNAL"}, "runtime")
    assert "STATUS_EVIDENCE_MISSING:artifact_sha256" in status_receipt_issues(
        {"status": "PASS"}, "artifact-check")


def test_absent_word_checks_and_later_edit_cannot_be_accepted(tmp_path):
    artifact = tmp_path / "final.docx"
    artifact.write_bytes(b"Synthetic fixture")
    report = tmp_path / "evidence.md"
    report.write_text("Synthetic fixture receipt", encoding="utf-8")
    evidence = [{"kind": kind, "artifact_sha256": sha256(artifact), "status": "PASS",
                 "reviewer": "synthetic", "path": str(report), "sha256": sha256(report)}
                for kind in ("content", "clear-prose", "scope-preservation")]
    kwargs = {"source_preserved": True, "propagation_complete": True}
    result = final_acceptance(artifact, [{"id": "T1", "status": "DONE"}], evidence, **kwargs)
    assert result["status"] == "VERIFICATION_INCOMPLETE"
    assert "EVIDENCE_MISSING:field-refresh" in result["problems"]
    artifact.write_bytes(b"Author edits after check")
    assert final_acceptance(artifact, [{"id": "T1", "status": "DONE"}], evidence,
                            **kwargs)["status"] == "RE_REVIEW_REQUIRED"


def test_uno_helper_refuses_source_overwrite_before_runtime_probe(tmp_path):
    import runpy
    helper = runpy.run_path(str(ROOT / "skills/dinh-dang-tai-lieu/scripts/refresh_uno.py"))
    source = tmp_path / "source.docx"
    source.write_bytes(b"Synthetic only")
    assert helper["refresh_document"](source, source, tmp_path / "out.pdf")["status"] == "SOURCE_OVERWRITE_FORBIDDEN"
    assert source.read_bytes() == b"Synthetic only"


def test_uno_unavailable_does_not_create_or_certify_output(tmp_path):
    import runpy
    helper = runpy.run_path(str(ROOT / "skills/dinh-dang-tai-lieu/scripts/refresh_uno.py"))
    source, output, pdf = (tmp_path / p for p in ("source.docx", "new.docx", "new.pdf"))
    source.write_bytes(b"Synthetic only")
    result = helper["refresh_document"](source, output, pdf, uno_loader=lambda: None)
    assert result["status"] == "HOST_CAPABILITY_UNAVAILABLE"
    assert not output.exists()
    assert not pdf.exists()


def test_uno_receipt_survives_ascii_console_with_vietnamese():
    import io
    import runpy
    from contextlib import redirect_stdout
    helper = runpy.run_path(str(ROOT / "skills/dinh-dang-tai-lieu/scripts/refresh_uno.py"))
    data = {"status": "REFRESHED_REVIEW_REQUIRED", "index_text": ["ĐẶT VẤN ĐỀ"]}
    stream = io.BytesIO()
    text = io.TextIOWrapper(stream, encoding="ascii")
    with redirect_stdout(text):
        helper["emit_receipt"](data)
    text.flush()
    assert json.loads(stream.getvalue().decode("ascii")) == data
