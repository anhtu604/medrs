from pathlib import Path
import sys

from medical_research_skills_vn.intake import draft_passport_from_project, extract_project

FIXTURES = Path(__file__).parent / "fixtures/in-progress"
sys.path.insert(0, str(FIXTURES))
from build_docx_fixture import build  # noqa: E402


def test_docx_intake_builds_draft_not_confirmed_passport(tmp_path):
    docx_path = build(tmp_path / "thesis-partial.docx")
    passport = draft_passport_from_project(extract_project(docx_path), "legacy-001")
    assert passport["objectives"]["status"] == "DRAFT_INFERRED"
    assert passport["objectives"]["provenance"][0]["artifact"].endswith(".docx")
    assert passport["study_design"]["status"] == "UNRESOLVED"
    assert passport["title"]["status"] == "DRAFT_INFERRED"


def test_conflicting_objectives_become_author_question(tmp_path):
    docx_path = build(tmp_path / "thesis-partial.docx")
    passport = draft_passport_from_project(extract_project(docx_path), "legacy-001")
    assert "AUTHOR_APPROVAL_REQUIRED" in passport["unresolved_markers"]
    assert any(question["field"] == "objectives" for question in passport["intake_questions"])


def test_markdown_intake_preserves_line_provenance():
    path = FIXTURES / "thesis-partial.md"
    passport = draft_passport_from_project(extract_project(path), "legacy-md")
    assert passport["population"]["status"] == "DRAFT_INFERRED"
    assert "line" in passport["population"]["provenance"][0]


def test_intake_never_infers_ethics_approval_or_verified_results(tmp_path):
    docx_path = build(tmp_path / "thesis-partial.docx")
    passport = draft_passport_from_project(extract_project(docx_path), "legacy-001")
    assert passport["verified_results"] == []
    assert passport["ethics_approval"]["status"] == "UNRESOLVED"
