"""Build the redistributable HMU style carrier used by DOCX-capable hosts."""

import sys
from pathlib import Path

import yaml
from docx import Document
from docx.shared import Cm

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.docx_formatting import _configure_style_system, _enable_field_refresh  # noqa: E402


def main() -> int:
    profile_path = ROOT / "profiles/institution/hmu/word-format-master-2020-current-2026.yaml"
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    document = Document()
    _configure_style_system(document, profile)
    _enable_field_refresh(document)
    page = profile["page"]
    for section in document.sections:
        section.top_margin = Cm(page["top_cm"])
        section.bottom_margin = Cm(page["bottom_cm"])
        section.left_margin = Cm(page["left_cm"])
        section.right_margin = Cm(page["right_cm"])
    destination = ROOT / "skills/dinh-dang-tai-lieu/assets/hmu-word-styles.docx"
    destination.parent.mkdir(parents=True, exist_ok=True)
    document.save(destination)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
