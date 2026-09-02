"""Host-aware Word backend selection and render-claim validation."""

from pathlib import Path


def select_word_backend(capabilities: dict, requested: str = "auto") -> dict:
    mapping = {
        "word-com": "word_com",
        "libreoffice-uno": "libreoffice_uno",
        "ooxml-only": "python_docx",
    }
    if requested != "auto":
        key = mapping.get(requested)
        if not key or not capabilities.get(key, {}).get("available"):
            return {"status": "HOST_CAPABILITY_UNAVAILABLE", "backend": requested}
        return {"status": "AVAILABLE", "backend": requested}
    for backend, key in mapping.items():
        if capabilities.get(key, {}).get("available"):
            return {"status": "AVAILABLE", "backend": backend}
    return {"status": "HOST_CAPABILITY_UNAVAILABLE", "backend": None}


def validate_render_claim(backend: str, pdf_path, image_paths: list) -> str:
    if backend == "ooxml-only":
        return "AUTHOR_APPROVAL_REQUIRED"
    pdf = Path(pdf_path) if pdf_path else None
    images = [Path(path) for path in image_paths]
    if not pdf or not pdf.is_file() or not images or not all(path.is_file() for path in images):
        return "RENDER_EVIDENCE_INCOMPLETE"
    return "RENDERED_ARTIFACTS_AVAILABLE"
