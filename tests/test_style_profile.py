import json
from pathlib import Path

from jsonschema import validate

from style_profile import build_profile, measure, validate_patterns


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
