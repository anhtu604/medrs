from medical_research_skills_vn.word_backends import select_word_backend, validate_render_claim


def test_backend_selection_respects_execution_surface():
    capabilities = {
        "word_com": {"available": False},
        "libreoffice_uno": {"available": False},
        "python_docx": {"available": True},
    }
    assert select_word_backend(capabilities)["backend"] == "ooxml-only"
    assert select_word_backend(capabilities, requested="word-com")["status"] == "HOST_CAPABILITY_UNAVAILABLE"


def test_rendered_pass_requires_real_pdf_and_images(tmp_path):
    assert validate_render_claim("ooxml-only", None, []) == "AUTHOR_APPROVAL_REQUIRED"
    pdf = tmp_path / "render.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    assert validate_render_claim("libreoffice-uno", pdf, []) == "RENDER_EVIDENCE_INCOMPLETE"
    image = tmp_path / "page-1.png"
    image.write_bytes(b"png")
    assert validate_render_claim("libreoffice-uno", pdf, [image]) == "RENDERED_ARTIFACTS_AVAILABLE"
