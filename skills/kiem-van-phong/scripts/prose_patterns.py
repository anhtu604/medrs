"""Suggest rewrites for descriptive paragraph openings and misread p-values/CIs.

Findings are revision suggestions, never gate failures. Patterns favour precision
over recall: a missed sentence is cheaper than a false alarm on sound prose.
"""

import argparse
import json
from pathlib import Path
import re
import sys

# ponytail: fixed regex lists; extend per locale when a real miss is reported.
_NUM = r"\d+(?:[.,]\d+)?\s*%"
PATTERNS = {
    "en": {
        "OPENING_DESCRIPTIVE": [
            r"(?:table|figure|fig\.)\s+\d+[a-z]?(?:\.\d+)*\s+(?:shows|presents|displays|summari[sz]es|describes|illustrates|lists|reports)\b"],
        "OPENING_STUDY_LIST": [
            r"(?:several|many|previous|other|numerous|various)\s+(?:previous\s+)?(?:studies|authors|investigators|reports)\s+(?:have\s+)?(?:reported|found|shown|demonstrated|observed)\b",
            r"(?:our|these)\s+(?:findings|results)\s+(?:are|were)\s+(?:consistent|in line|in agreement)\s+with\s+(?:previous|other|earlier)\s+(?:studies|reports|findings)\s*(?:\[[^\]]*\]\s*)?[.;]"],
        "PVALUE_MISREAD": [
            _NUM + r"\s+(?:probability|chance|likelihood)\s+(?:that\s+)?(?:the\s+|this\s+|these\s+)?(?:results?|findings?|differences?|associations?|effects?)\s+(?:is|are|was|were)\s+(?:due to|caused by|explained by)\s+chance",
            _NUM + r"\s+(?:probability|chance|likelihood)\s+(?:that\s+)?(?:the\s+|this\s+)?(?:intervention|treatment|drug|therapy)\s+(?:is|was)\s+(?:effective|efficacious|beneficial)"],
        "CI_MISREAD": [
            r"95\s*%\s+(?:probability|chance|likelihood)\s+(?:that\s+)?the\s+true\s+(?:value|effect|mean|parameter)"],
    },
    "vi": {
        "OPENING_DESCRIPTIVE": [
            r"(?:bảng|biểu đồ|hình)\s+\d+(?:\.\d+)*\s+(?:trình bày|mô tả|thể hiện|tóm tắt|liệt kê)\b"],
        "OPENING_STUDY_LIST": [
            r"(?:nhiều|một số|các|những)\s+(?:nghiên cứu|tác giả)\s+(?:trước đây\s+|trước\s+|khác\s+)?(?:đã\s+)?(?:báo cáo|ghi nhận|cho thấy|chỉ ra|công bố)\b",
            r"(?:kết quả|nghiên cứu)\s+(?:của chúng tôi\s+)?(?:tương đồng|phù hợp|tương tự)\s+với\s+(?:các\s+|những\s+)?(?:nghiên cứu|tác giả)\s+(?:khác|trước(?:\s+đây)?)\s*(?:\[[^\]]*\]\s*)?[.;]"],
        "PVALUE_MISREAD": [
            _NUM + r"\s+(?:khả năng|xác suất)\s+(?:là\s+)?(?:kết quả|khác biệt|mối liên quan)\s+(?:này\s+)?(?:là\s+)?do\s+(?:yếu tố\s+)?ngẫu nhiên",
            _NUM + r"\s+(?:khả năng|xác suất)\s+(?:là\s+)?(?:can thiệp|điều trị|thuốc|liệu pháp)\s+(?:này\s+)?(?:có\s+)?hiệu quả"],
        "CI_MISREAD": [
            r"95\s*%\s+(?:xác suất|khả năng)\s+(?:là\s+)?(?:giá trị|tác động|trung bình|tham số)\s+thật"],
    },
}
OPENING = {"OPENING_DESCRIPTIVE", "OPENING_STUDY_LIST"}
# A table verb followed by an actual finding ("shows that…", "…cao hơn…") is finding-led, not descriptive.
_FINDING = {
    "en": re.compile(r"^\s*that\b|\b(?:higher|lower|greater|smaller|more|fewer|less|increased|decreased|"
                     r"associated with|longer|shorter)\b", re.IGNORECASE),
    "vi": re.compile(r"(?:cao hơn|thấp hơn|nhiều hơn|ít hơn|lớn hơn|nhỏ hơn|dài hơn|ngắn hơn|tăng|giảm|"
                     r"liên quan với|có liên quan)", re.IGNORECASE),
}


def _first_sentence_rest(text, end):
    rest = text[end:]
    stop = re.search(r"[.!?](?:\s|$)", rest)
    return rest[:stop.start()] if stop else rest
SUGGESTIONS = {
    "vi": {
        "OPENING_DESCRIPTIVE": "Mở đoạn bằng phát hiện chính rồi dẫn bảng/hình trong ngoặc; giữ đúng mức chắc chắn của dữ liệu.",
        "OPENING_STUDY_LIST": "Mở đoạn bằng cách giải thích hoặc ý nghĩa của phát hiện, rồi mới dẫn và so sánh các nghiên cứu.",
        "PVALUE_MISREAD": "p không phải xác suất kết quả do ngẫu nhiên hay xác suất can thiệp hiệu quả; nêu độ lớn tác động và KTC.",
        "CI_MISREAD": "KTC là vùng giá trị còn tương thích với dữ liệu, không phải xác suất giá trị thật nằm trong khoảng.",
    },
    "en": {
        "OPENING_DESCRIPTIVE": "Open with the main finding and cite the table/figure in parentheses; keep the certainty the data allow.",
        "OPENING_STUDY_LIST": "Open with the interpretation or meaning of the finding, then bring in and compare the studies.",
        "PVALUE_MISREAD": "A p-value is not the probability that the result is due to chance or that the intervention works; report effect size and CI.",
        "CI_MISREAD": "A CI is the range of values compatible with the data, not a probability that the true value lies inside it.",
    },
}
_COMPILED = {locale: {name: [re.compile(p, re.IGNORECASE) for p in items] for name, items in groups.items()}
             for locale, groups in PATTERNS.items()}


def scan_prose(paragraphs: list[str], locale: str) -> list[dict]:
    if locale not in _COMPILED:
        raise ValueError("UNKNOWN_LOCALE")
    findings = []
    for index, paragraph in enumerate(paragraphs):
        text = paragraph.strip()
        for name, regexes in _COMPILED[locale].items():
            for regex in regexes:
                match = regex.match(text) if name in OPENING else regex.search(text)
                if match and name == "OPENING_DESCRIPTIVE" and _FINDING[locale].search(_first_sentence_rest(text, match.end())):
                    match = None
                if match:
                    excerpt = text[:120] if name in OPENING else match.group(0)
                    findings.append({"pattern": name, "paragraph": index, "excerpt": excerpt,
                                     "suggestion": SUGGESTIONS[locale][name]})
                    break
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", choices=sorted(PATTERNS), required=True)
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    paragraphs = [part for part in re.split(r"\n\s*\n", args.path.read_text(encoding="utf-8")) if part.strip()]
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(scan_prose(paragraphs, args.locale), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
