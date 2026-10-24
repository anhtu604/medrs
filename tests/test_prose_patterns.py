import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
CLI = ROOT / "skills/kiem-van-phong/scripts/prose_patterns.py"


def patterns(paragraph, locale):
    from prose_patterns import scan_prose

    return [finding["pattern"] for finding in scan_prose([paragraph], locale)]


@pytest.mark.parametrize("paragraph, locale", [
    ("Table 2 presents the results of logistic regression analysis.", "en"),
    ("Figure 3 shows the differences between two groups.", "en"),
    ("Bảng 3.2 trình bày đặc điểm chung của đối tượng nghiên cứu.", "vi"),
    ("Biểu đồ 3.1 mô tả phân bố tuổi.", "vi"),
])
def test_flags_descriptive_openings(paragraph, locale):
    assert patterns(paragraph, locale) == ["OPENING_DESCRIPTIVE"]


@pytest.mark.parametrize("paragraph, locale", [
    ("Several studies have reported different prevalence rates of gestational diabetes.", "en"),
    ("Our findings are consistent with previous studies.", "en"),
    ("Nhiều nghiên cứu đã báo cáo tỷ lệ khác nhau.", "vi"),
    ("Kết quả của chúng tôi tương đồng với các nghiên cứu trước.", "vi"),
])
def test_flags_study_list_openings(paragraph, locale):
    assert patterns(paragraph, locale) == ["OPENING_STUDY_LIST"]


@pytest.mark.parametrize("paragraph, locale, expected", [
    ("There is only a 2% probability that the result is due to chance.", "en", "PVALUE_MISREAD"),
    ("There is a 98% chance that the intervention is effective.", "en", "PVALUE_MISREAD"),
    ("There is a 95% probability that the true value lies within the interval.", "en", "CI_MISREAD"),
    ("Chỉ có 2% khả năng kết quả này là do ngẫu nhiên.", "vi", "PVALUE_MISREAD"),
    ("Có 98% khả năng can thiệp có hiệu quả.", "vi", "PVALUE_MISREAD"),
    ("Có 95% xác suất giá trị thật nằm trong khoảng này.", "vi", "CI_MISREAD"),
])
def test_flags_p_and_ci_misreadings(paragraph, locale, expected):
    assert patterns(paragraph, locale) == [expected]


@pytest.mark.parametrize("paragraph, locale", [
    ("Higher maternal BMI was associated with an increased risk of gestational diabetes (Table 3).", "en"),
    ("Mortality was lower in the intervention group. Table 2 shows the full model.", "en"),
    ("Bảng 3.2 cho thấy tỷ lệ nam cao hơn nữ.", "vi"),
    ("Khác biệt về tiêu chuẩn chẩn đoán có thể giải thích một phần sự chênh lệch tỷ lệ giữa các nghiên cứu.", "vi"),
])
def test_scanner_leaves_finding_led_and_mid_paragraph_sentences(paragraph, locale):
    assert patterns(paragraph, locale) == []


def test_findings_carry_location_and_suggestion():
    from prose_patterns import scan_prose

    finding = scan_prose(["Nội dung đầu.", "Bảng 3.2 trình bày đặc điểm chung."], "vi")[0]
    assert finding["paragraph"] == 1
    assert finding["excerpt"].startswith("Bảng 3.2 trình bày")
    assert finding["suggestion"]


def test_cli_outputs_json(tmp_path):
    text = tmp_path / "chuong3.md"
    text.write_text("Tỷ lệ nam cao hơn nữ (Bảng 3.1).\n\nBảng 3.2 trình bày đặc điểm lâm sàng.\n", encoding="utf-8")
    result = subprocess.run([sys.executable, str(CLI), "--locale", "vi", str(text)],
                            capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    findings = json.loads(result.stdout)
    assert [(item["pattern"], item["paragraph"]) for item in findings] == [("OPENING_DESCRIPTIVE", 1)]
