"""Measure an author's writing habits from the author's own documents.

Run from the MedRS skill folder:
    python scripts/style_profile.py --author "Tên tác giả" --out author-style-profile.json bai1.docx bai2.docx
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median, quantiles

MIN_CONFIDENT_WORDS = 8000
MAX_EXCERPT_WORDS = 40
WORD = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
CONNECTORS = (
    "Nghiên cứu của chúng tôi",
    "Bên cạnh đó",
    "Trong khi đó",
    "Kết quả này",
    "Tuy nhiên",
    "Như vậy",
    "Do đó",
    "Vì vậy",
    "Ngoài ra",
    "Mặt khác",
    "Tương tự",
    "Điều này",
    "In addition",
    "In contrast",
    "However",
    "Therefore",
    "Moreover",
    "Similarly",
    "Notably",
    "Thus",
)
NUMERIC_CITATION = re.compile(r"\[\d+(?:\s*[,–-]\s*\d+)*\]")
AUTHOR_YEAR_CITATION = re.compile(r"\([^()]*\b(?:19|20)\d{2}[a-z]?\)")
P_VALUE = re.compile(r"\b[pP]\s*[<=>≤≥]\s*0[.,]\d+")
ABBREVIATION = re.compile(r"\(([A-ZĐ]{2,6})\)")


def count_words(text: str) -> int:
    return len(WORD.findall(text))


def read_text(path: Path) -> str:
    suffix = path.suffix.casefold()
    if suffix == ".docx":
        from docx import Document

        return "\n\n".join(p.text for p in Document(str(path)).paragraphs if p.text.strip())
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    raise ValueError(f"UNSUPPORTED_SOURCE:{path.name} (convert PDF to DOCX or TXT first)")


def _sentences(paragraph: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", paragraph.strip()) if count_words(s)]


def _distribution(values: list[int]) -> dict:
    if not values:
        return {"mean": 0.0, "median": 0.0, "p25": 0.0, "p75": 0.0}
    q = quantiles(values, n=4) if len(values) > 1 else [values[0], values[0], values[0]]
    return {"mean": round(mean(values), 1), "median": round(median(values), 1), "p25": round(q[0], 1), "p75": round(q[2], 1)}


def _dominant(first: int, second: int, first_label: str, second_label: str) -> str:
    if not first and not second:
        return "none"
    if first and second:
        return first_label if first >= 3 * second else second_label if second >= 3 * first else "mixed"
    return first_label if first else second_label


def measure(text: str) -> dict:
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    sentences = [s for p in paragraphs for s in _sentences(p)]
    words = count_words(text)
    per_thousand = (lambda n: round(n * 1000 / words, 2)) if words else (lambda n: 0.0)
    connectors = Counter()
    for sentence in sentences:
        for connector in CONNECTORS:
            if sentence.startswith(connector):
                connectors[connector] += 1
                break
    p_styles = Counter(re.sub(r"\d", "0", m.group(0)) for m in P_VALUE.finditer(text))
    numeric = NUMERIC_CITATION.findall(text)
    author_year = AUTHOR_YEAR_CITATION.findall(text)
    citations = [m for m in re.finditer(f"{NUMERIC_CITATION.pattern}|{AUTHOR_YEAR_CITATION.pattern}", text)]
    at_clause_end = sum(1 for m in citations if re.match(r"\s*[.;,]|\s*$", text[m.end() :]))
    openers = Counter(" ".join(WORD.findall(s)[:2]) for s in sentences)
    lowered = text.casefold()
    return {
        "words": words,
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "sentence_words": _distribution([count_words(s) for s in sentences]),
        "paragraph_words": _distribution([count_words(p) for p in paragraphs]),
        "connectors": dict(connectors),
        "top_openers": dict(openers.most_common(10)),
        "first_person_per_1000_words": per_thousand(lowered.count("chúng tôi") + len(re.findall(r"\bwe\b", lowered))),
        "passive_markers_per_1000_words": per_thousand(len(re.findall(r"\b(?:được|bị|was|were)\b", lowered))),
        "decimal_separator": _dominant(len(re.findall(r"\d,\d", text)), len(re.findall(r"\d\.\d", text)), "comma", "point"),
        "p_value_style": p_styles.most_common(1)[0][0] if p_styles else None,
        "percent_spacing": _dominant(len(re.findall(r"\d%", text)), len(re.findall(r"\d %", text)), "no-space", "space"),
        "citation_style": _dominant(len(numeric), len(author_year), "numeric", "author-year"),
        "citation_at_clause_end_ratio": round(at_clause_end / len(citations), 2) if citations else None,
        "abbreviations": dict(Counter(ABBREVIATION.findall(text)).most_common(10)),
    }


def build_profile(paths: list[Path], author: str) -> dict:
    texts = []
    sources = []
    for path in paths:
        text = read_text(Path(path))
        texts.append(text)
        sources.append(
            {
                "path": Path(path).name,
                "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                "words": count_words(text),
            }
        )
    combined = "\n\n".join(texts)
    measured = measure(combined)
    vietnamese = len(re.findall(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", combined.casefold()))
    return {
        "schema_version": "1.0.0",
        "author": author,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": sources,
        "total_words": measured["words"],
        "confidence": "NORMAL" if measured["words"] >= MIN_CONFIDENT_WORDS else "LOW_CONFIDENCE",
        "locale": "vi" if vietnamese > measured["words"] * 0.05 else "en",
        "measured": measured,
        "patterns": [],
    }


def validate_patterns(profile: dict) -> list[str]:
    return [
        f"PATTERN_EXCERPT_TOO_LONG:{index}"
        for index, pattern in enumerate(profile.get("patterns", []))
        if count_words(pattern.get("excerpt", "")) > MAX_EXCERPT_WORDS
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an author style profile from the author's own documents.")
    parser.add_argument("--author", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    profile = build_profile(args.files, args.author)
    args.out.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{args.out} — {profile['total_words']} words, {profile['confidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
