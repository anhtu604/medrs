import json
import builtins
import sys
from pathlib import Path
from zipfile import ZipFile

from jsonschema import validate

from style_profile import build_profile, main, measure, read_text, validate_patterns


ROOT = Path(__file__).parents[1]
SAMPLE = (
    "Nghiên cứu của chúng tôi gồm 120 bệnh nhân được theo dõi trong 12 tháng. "
    "Tuy nhiên, tỷ lệ đáp ứng là 45,2% (p < 0,05). "
    "Như vậy, kết quả này tương đồng với nghiên cứu trước [1].\n\n"
    "Tăng huyết áp (THA) là yếu tố nguy cơ chính. "
    "Bên cạnh đó, chúng tôi ghi nhận tỷ lệ biến chứng 12,5% [2, 3]."
)


def test_measure_captures_the_authors_habits():
    measured = measure(SAMPLE)
    assert measured["sentences"] == 5
    assert measured["paragraphs"] == 2
    assert measured["decimal_separator"] == "comma"
    assert measured["p_value_style"] == "p < 0,00"
    assert measured["percent_spacing"] == "no-space"
    assert measured["citation_style"] == "numeric"
    assert measured["connectors"] == {"Tuy nhiên": 1, "Như vậy": 1, "Bên cạnh đó": 1, "Nghiên cứu của chúng tôi": 1}
    assert measured["first_person_per_1000_words"] > 0
    assert measured["abbreviations"] == {"THA": 1}


def test_profile_is_low_confidence_below_the_word_threshold_and_matches_schema(tmp_path):
    source = tmp_path / "bai-bao.txt"
    source.write_text(SAMPLE, encoding="utf-8")
    profile = build_profile([source], author="Tác giả mẫu")
    schema = json.loads((ROOT / "schemas/author-style-profile.schema.json").read_text(encoding="utf-8"))
    validate(profile, schema)
    assert profile["confidence"] == "LOW_CONFIDENCE"
    assert profile["sources"][0]["words"] == profile["total_words"]
    assert profile["patterns"] == []


def test_pattern_excerpts_are_capped_at_forty_words():
    profile = {"patterns": [{"move": "limitation", "excerpt": " ".join(["từ"] * 41), "source": "a.docx"}]}
    assert validate_patterns(profile) == ["PATTERN_EXCERPT_TOO_LONG:0"]


def test_docx_reads_runs_tabs_and_breaks_without_python_docx(tmp_path, monkeypatch):
    source = tmp_path / "author.docx"
    xml = (
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body><w:p><w:r><w:t>Alpha </w:t></w:r><w:r><w:t>beta</w:t>'
        '<w:tab/><w:t>gamma</w:t><w:br/><w:t>delta</w:t></w:r></w:p>'
        '<w:p><w:r><w:t>Second paragraph</w:t></w:r></w:p></w:body></w:document>'
    )
    with ZipFile(source, "w") as archive:
        archive.writestr("word/document.xml", xml)

    original_import = builtins.__import__

    def reject_docx(name, *args, **kwargs):
        if name == "docx" or name.startswith("docx."):
            raise ModuleNotFoundError("No module named 'docx'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_docx)
    assert read_text(source) == "Alpha beta\tgamma\ndelta\n\nSecond paragraph"


def test_pattern_sources_and_excerpts_are_verified_against_author_text(tmp_path):
    source = tmp_path / "author.txt"
    source.write_text(SAMPLE, encoding="utf-8")
    profile = build_profile([source], author="Tác giả mẫu")
    pattern = {"move": "limitation", "excerpt": "Tuy nhiên, tỷ lệ đáp ứng là 45,2%", "source": source.name}
    profile["patterns"] = [pattern]
    assert validate_patterns(profile, [source]) == []

    pattern["excerpt"] = "Tuy nhiên, tỷ lệ đáp ứng là 99,9%"
    assert validate_patterns(profile, [source]) == ["PATTERN_EXCERPT_NOT_FOUND:0"]

    pattern["source"] = "fabricated.txt"
    assert validate_patterns(profile, [source]) == ["PATTERN_SOURCE_UNKNOWN:0"]


def test_pattern_cannot_be_used_when_source_unavailable_or_changed(tmp_path):
    source = tmp_path / "author.txt"
    source.write_text(SAMPLE, encoding="utf-8")
    profile = build_profile([source], author="Tác giả mẫu")
    profile["patterns"] = [{"move": "strength", "excerpt": "Nghiên cứu của chúng tôi", "source": source.name}]
    assert validate_patterns(profile, []) == ["PATTERN_SOURCE_UNAVAILABLE:0"]
    source.write_text(SAMPLE + " changed", encoding="utf-8")
    assert validate_patterns(profile, [source]) == ["PATTERN_SOURCE_HASH_MISMATCH:0"]


def test_cli_refuses_unverified_patterns(tmp_path, monkeypatch, capsys):
    source = tmp_path / "author.txt"
    source.write_text(SAMPLE, encoding="utf-8")
    profile = build_profile([source], author="Tác giả mẫu")
    profile["patterns"] = [{"move": "limitation", "excerpt": "invented excerpt", "source": source.name}]
    profile_path = tmp_path / "author-style-profile.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["style_profile.py", "--check-profile", str(profile_path), str(source)])
    assert main() == 1
    assert "PATTERN_EXCERPT_NOT_FOUND:0" in capsys.readouterr().err

    profile["patterns"][0]["excerpt"] = "Nghiên cứu của chúng tôi"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
    assert main() == 0
