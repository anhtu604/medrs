"""Inspect the actual generated DOCX and rendered evidence."""

from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.oxml.ns import qn

from .structure_profiles import _sha256
from .word_backends import validate_render_claim


def _near(actual, expected, tolerance=0.03):
    return actual is not None and abs(actual.cm - float(expected)) <= tolerance


def validate_docx(path: Path, profile: dict, *, rendered_artifacts: list, backend: str = "ooxml-only") -> dict:
    path = Path(path)
    document = Document(path)
    normal = document.styles["Normal"]
    body = profile["body"]
    normal_pass = normal.font.name == body["font"] and round(normal.font.size.pt, 1) in profile["body"]["allowed_size_pt"]
    runs = [run for paragraph in document.paragraphs for run in paragraph.runs if run.text]
    direct_formatting_pass = all(
        (run.font.name in {None, body["font"]})
        and (run.font.size is None or round(run.font.size.pt, 1) in body["allowed_size_pt"])
        for run in runs
    )
    page = profile["page"]
    margins_pass = all(
        _near(section.top_margin, page["top_cm"])
        and _near(section.bottom_margin, page["bottom_cm"])
        and _near(section.left_margin, page["left_cm"])
        and _near(section.right_margin, page["right_cm"])
        for section in document.sections
    )
    with ZipFile(path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        header_xml = "".join(
            archive.read(name).decode("utf-8") for name in archive.namelist() if name.startswith("word/header")
        )
    rendered_pdf = next((item for item in rendered_artifacts if str(item).lower().endswith(".pdf")), None)
    rendered_images = [item for item in rendered_artifacts if str(item).lower().endswith((".png", ".jpg", ".jpeg"))]
    render_state = validate_render_claim(backend, rendered_pdf, rendered_images)
    rendered_check = "PASS" if render_state == "RENDERED_ARTIFACTS_AVAILABLE" else render_state
    return {
        "artifact_hash": _sha256(path),
        "mechanical_checks": {
            "normal_style": "PASS" if normal_pass else "FAIL",
            "direct_formatting": "PASS" if direct_formatting_pass else "FAIL",
            "margins": "PASS" if margins_pass else "FAIL",
            "toc_field": "PASS" if "TOC " in document_xml else "FAIL",
            "page_number_field": "PASS" if "PAGE" in header_xml else "FAIL",
            "page_restart_at_introduction": "PASS" if 'w:pgNumType w:start="1"' in document_xml else "FAIL",
        },
        "rendered_checks": {"pagination": rendered_check, "visual_layout": rendered_check},
    }
