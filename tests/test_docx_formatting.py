from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from medical_research_skills_vn.docx_formatting import REFRESH_SAFE_STYLES, format_docx
from medical_research_skills_vn.docx_validation import validate_docx
from medical_research_skills_vn.structure_profiles import load_structure_profile


ROOT = Path(__file__).parents[1]
PROFILE_PATH = ROOT / "profiles/institution/hmu/word-format-master-2020-current-2026.yaml"
STYLE_CARRIER = ROOT / "skills/dinh-dang-tai-lieu/assets/hmu-word-styles.docx"


def _fixture(path: Path):
    document = Document()
    document.styles.add_style("CustomBody", WD_STYLE_TYPE.PARAGRAPH)
    document.add_heading("MỤC LỤC", level=1)
    document.add_paragraph("Mục lục cũ")
    document.add_heading("ĐẶT VẤN ĐỀ", level=1)
    body = document.add_paragraph("Nội dung thử nghiệm có chỉnh sửa.", style="CustomBody")
    insertion = OxmlElement("w:ins")
    insertion.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id", "7")
    body._p.append(insertion)
    document.add_heading("CHƯƠNG 1. TỔNG QUAN", level=1)
    document.add_paragraph("Tổng quan.")
    document.add_paragraph("Ý ngắn", style="List Bullet")
    document.add_paragraph(
        "Ý dài hơn để kiểm tra thụt lề và căn dòng tiếp theo của danh sách tự động.",
        style="List Bullet",
    )
    table = document.add_table(rows=3, cols=3)
    values = [
        ("STT", "Biến", "Định nghĩa và cách đo lường"),
        ("1", "Tuổi", "Tuổi tính theo năm hoàn thành tại thời điểm thu thập số liệu"),
        ("2", "Giới", "Nam hoặc nữ theo hồ sơ nghiên cứu"),
    ]
    for row, content in zip(table.rows, values):
        for cell, value in zip(row.cells, content):
            cell.text = value
    document.save(path)


def test_ooxml_formatter_never_overwrites_source(tmp_path):
    source = tmp_path / "source.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)
    result = format_docx(source, source, profile, author_approved=True)
    assert result["status"] == "SOURCE_OVERWRITE_FORBIDDEN"


def test_formats_and_validates_the_generated_docx_not_configuration(tmp_path):
    source = tmp_path / "source.docx"
    output = tmp_path / "formatted.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)

    result = format_docx(source, output, profile, author_approved=True)
    report = validate_docx(output, profile, rendered_artifacts=[])

    assert result["status"] == "FORMATTED_WITH_UNPERFORMED_CHECKS"
    assert output.exists()
    assert report["artifact_hash"] == result["output_hash"]
    assert report["mechanical_checks"]["normal_style"] == "PASS"
    assert report["mechanical_checks"]["direct_formatting"] == "PASS"
    assert report["mechanical_checks"]["margins"] == "PASS"
    assert report["mechanical_checks"]["toc_field"] == "PASS"
    assert report["mechanical_checks"]["page_number_field"] == "PASS"
    assert report["mechanical_checks"]["page_restart_at_introduction"] == "PASS"
    assert report["mechanical_checks"]["refresh_safe_styles"] == "PASS"
    assert report["mechanical_checks"]["adaptive_table_widths"] == "PASS"
    assert report["mechanical_checks"]["list_numbering"] == "PASS"
    assert report["rendered_checks"]["pagination"] == "AUTHOR_APPROVAL_REQUIRED"
    assert report["rendered_checks"]["visual_layout"] == "AUTHOR_APPROVAL_REQUIRED"


def test_preserves_tracked_change_xml_and_creates_new_file(tmp_path):
    source = tmp_path / "source.docx"
    output = tmp_path / "formatted.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)
    before = source.read_bytes()

    format_docx(source, output, profile, author_approved=True)
    with ZipFile(output) as archive:
        xml = archive.read("word/document.xml")
    assert b"<w:ins" in xml
    assert source.read_bytes() == before


def test_builds_refresh_safe_word_style_system(tmp_path):
    source = tmp_path / "source.docx"
    output = tmp_path / "formatted.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)

    format_docx(source, output, profile, author_approved=True)
    document = Document(output)

    for style_name in [
        "Normal",
        "Body Text",
        "Heading 1",
        "Heading 2",
        "Heading 3",
        "Heading 4",
        "TOC Heading",
        "TOC 1",
        "TOC 2",
        "TOC 3",
        "TOC 4",
        "Table of Figures",
        "Caption",
        "Bibliography",
        "List Paragraph",
        "MedRS Table Text",
    ]:
        assert style_name in document.styles
        style = document.styles[style_name]
        assert style.font.name == profile["body"]["font"]

    for style_name in ["Normal", "Body Text", "TOC 1", "Table of Figures", "Bibliography"]:
        assert document.styles[style_name].paragraph_format.line_spacing == profile["body"]["line_spacing"]
    for style_name in ["Body Text", "Heading 1", "Heading 2", "Heading 3", "Heading 4", "Caption", "List Paragraph", "MedRS Table Text"]:
        assert document.styles[style_name].quick_style is True
        assert document.styles[style_name].hidden is False

    with ZipFile(output) as archive:
        settings = archive.read("word/settings.xml")
    assert b"updateFields" in settings
    assert b'val="true"' in settings or b'val="1"' in settings


def test_uses_content_weighted_table_widths_and_deterministic_bullets(tmp_path):
    source = tmp_path / "source.docx"
    output = tmp_path / "formatted.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)

    format_docx(source, output, profile, author_approved=True)
    document = Document(output)

    grid = document.tables[0]._tbl.tblGrid
    widths = [int(item.get(qn("w:w"))) for item in grid.gridCol_lst]
    assert widths[0] < widths[1] < widths[2]
    assert widths[2] / widths[0] >= 2
    for row in document.tables[0].rows:
        for cell in row.cells:
            assert all(paragraph.style.name == "MedRS Table Text" for paragraph in cell.paragraphs)

    bullets = [p for p in document.paragraphs if p.text.startswith("Ý ")]
    assert len(bullets) == 2
    assert all(p.style.name == "List Paragraph" for p in bullets)
    num_ids = []
    for paragraph in bullets:
        num_pr = paragraph._p.pPr.numPr
        assert num_pr is not None
        assert num_pr.ilvl.val == 0
        num_ids.append(num_pr.numId.val)
        assert paragraph.paragraph_format.left_indent is None
        assert paragraph.paragraph_format.first_line_indent is None
    assert len(set(num_ids)) == 1

    with ZipFile(output) as archive:
        numbering = archive.read("word/numbering.xml")
    assert b'MedRSBullet' in numbering
    assert b'w:hanging="360"' in numbering


def test_formatting_requires_profile_and_author_approval(tmp_path):
    source = tmp_path / "source.docx"
    output = tmp_path / "formatted.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)
    assert format_docx(source, output, profile, author_approved=False)["status"] == "AUTHOR_APPROVAL_REQUIRED"
    stale = dict(profile, verification_status="STALE")
    assert format_docx(source, output, stale, author_approved=True)["status"] == "OFFICIAL_RULE_REQUIRED"


def test_hmu_style_carrier_contains_refresh_safe_styles():
    assert STYLE_CARRIER.is_file()
    document = Document(STYLE_CARRIER)
    assert all(name in document.styles for name in REFRESH_SAFE_STYLES)
    with ZipFile(STYLE_CARRIER) as archive:
        assert b"updateFields" in archive.read("word/settings.xml")


def test_plain_libreoffice_render_does_not_fake_field_refresh(tmp_path):
    source = tmp_path / "source.docx"
    output = tmp_path / "formatted.docx"
    pdf = tmp_path / "render.pdf"
    png = tmp_path / "page-1.png"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)
    format_docx(source, output, profile, author_approved=True)
    pdf.write_bytes(b"%PDF-1.4")
    png.write_bytes(b"png")

    report = validate_docx(output, profile, rendered_artifacts=[pdf, png], backend="libreoffice-convert")

    assert report["rendered_checks"]["visual_layout"] == "PASS"
    assert report["rendered_checks"]["pagination"] == "FIELD_UPDATE_UNVERIFIED"


def test_reformatting_is_idempotent_for_fields_and_medrs_numbering(tmp_path):
    source = tmp_path / "source.docx"
    first = tmp_path / "first.docx"
    second = tmp_path / "second.docx"
    _fixture(source)
    profile = load_structure_profile(PROFILE_PATH)

    format_docx(source, first, profile, author_approved=True)
    format_docx(first, second, profile, author_approved=True)
    with ZipFile(second) as archive:
        document_xml = archive.read("word/document.xml")
        numbering_xml = archive.read("word/numbering.xml")
        header_xml = b"".join(archive.read(name) for name in archive.namelist() if name.startswith("word/header"))

    assert document_xml.count(b"TOC ") == 1
    assert header_xml.count(b">PAGE<") == 1
    assert numbering_xml.count(b'MedRSBullet') == 1
