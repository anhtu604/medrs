"""Inspect manuscript surfaces and keyed results, without claiming visual/semantic review."""

import json
import re
from math import isclose, isfinite
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
RESULT_ID_FIELDS = ("variable", "indicator", "denominator", "group", "time_pair", "test", "adjustment")


def inspect_docx(path, banned_terms=()):
    findings, surfaces = [], []
    with ZipFile(path) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise ValueError("CORRUPT_DOCX:" + corrupt)
        if "word/document.xml" not in archive.namelist():
            raise ValueError("NOT_A_DOCX")
        for name in archive.namelist():
            if not name.startswith("word/") or not name.endswith(".xml"):
                continue
            if name.startswith("word/comments"):
                continue  # Review instructions are not manuscript prose.
            root = ET.fromstring(archive.read(name))
            # Per paragraph joins catch fragments split into different runs.
            for index, paragraph in enumerate(root.findall(".//w:p", NS)):
                text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
                if text:
                    surfaces.append({"part": name, "paragraph": index, "text": text})
            for index, node in enumerate(root.findall(".//a:t", NS)):
                if node.text:
                    surfaces.append({"part": name, "drawing_label": index, "text": node.text})
        members = set(archive.namelist())
        embedded = sorted(name for name in members if name.startswith("word/embeddings/"))
    generic = (r"\bTask\s*\d", r"\bvòng\s+\d", r"theo chỉ đạo tác giả",
               r"chờ nghiệm thu", r"hồ sơ vòng", r"3\.NEW")
    for surface in surfaces:
        text = surface["text"]
        for pattern in generic:
            if re.search(pattern, text, re.IGNORECASE):
                findings.append({**surface, "code": "WORKFLOW_LANGUAGE", "pattern": pattern})
        for term in banned_terms:
            if term.casefold() in text.casefold():
                findings.append({**surface, "code": "PROJECT_TERM", "term": term})
    return {"package_integrity": "PASS", "findings": findings,
            "surfaces_checked": len(surfaces), "embedded_objects_to_review": embedded,
            "unperformed": ["embedded-workbook-values", "raster-chart-labels", "visual-layout", "field-refresh"]}


def compare_result_claim(claim, result, *, tolerance=1e-8):
    """Reject a numerically equal p from a different pair/indicator/test."""
    errors = []
    for field in RESULT_ID_FIELDS:
        if field not in claim or field not in result:
            errors.append("IDENTITY_MISSING:" + field)
        elif claim[field] != result[field]:
            errors.append("IDENTITY_MISMATCH:" + field)
    valid_number = lambda value: type(value) in (int, float) and isfinite(value)
    for field in ("value", "p", "ci_low", "ci_high"):
        if field not in claim:
            continue
        if not valid_number(claim[field]):
            errors.append("NUMERIC_INVALID:" + field)
        elif field not in result or not valid_number(result[field]):
            errors.append("SOURCE_NUMERIC_INVALID:" + field)
        elif not isclose(claim[field], result[field], abs_tol=tolerance, rel_tol=0):
            errors.append("VALUE_MISMATCH:" + field)
    if "p" in claim and valid_number(claim["p"]) and not 0 <= claim["p"] <= 1:
        errors.append("P_OUT_OF_RANGE")
    if "ci_low" in claim and "ci_high" in claim and valid_number(claim["ci_low"]) and valid_number(claim["ci_high"]):
        low, high = claim["ci_low"], claim["ci_high"]
        if low > high:
            errors.append("CI_REVERSED")
        # Bounds belong to the actual estimand, not a similarly named outcome.
        bounds = result.get("estimand_bounds")
        if bounds and (low < bounds[0] or high > bounds[1]):
            errors.append("CI_OUT_OF_DOMAIN")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


if __name__ == "__main__":
    import argparse
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--banned-term", action="append", default=[])
    args = parser.parse_args()
    report = inspect_docx(args.docx, args.banned_term)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if report["findings"] else 0)
