"""Keep Zotero citations and cross-references alive while MedRS edits Word paragraphs.

The model edits text only. Every complex field is replaced by a token before the edit
(`⟦Z:n⟧` for Zotero, `⟦F:n⟧` for any other field) and restored byte for byte after it.
An audit compares complex fields and Zotero preferences before and after; any loss blocks delivery.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
import zipfile
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import count
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from lxml import etree

ZOTERO_PREFIXES = ("ADDIN ZOTERO_ITEM", "ADDIN ZOTERO_BIBL")
TOKEN = re.compile(r"⟦(?:Z|F):\d+⟧|⟦C:[0-9a-f]{32}⟧|⟦cite:[^⟧]+⟧")
FIELD_TOKEN = re.compile(r"⟦(?:Z|F):\d+⟧")
CITE_TOKEN = re.compile(r"⟦cite:([A-Za-z0-9]+(?:;[A-Za-z0-9]+)*)⟧")
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
FIELD_PARTS = ("word/document.xml", "word/footnotes.xml", "word/endnotes.xml")
PREFERENCE_PARTS = ("docProps/custom.xml", "word/settings.xml")
PREFERENCE_NAME = re.compile(r'name="(ZOTERO_PREF_\d+)"')
PARAGRAPH_CHILDREN = {qn("w:pPr"), qn("w:r"), qn("w:proofErr")}
TEXT_RUN_CHILDREN = {qn("w:rPr"), qn("w:t"), qn("w:tab"), qn("w:br"), qn("w:lastRenderedPageBreak")}
CSL_SCHEMA = "https://github.com/citation-style-language/schema/raw/master/csl-citation.json"


class ZoteroFieldError(ValueError):
    pass


@dataclass
class ParagraphFields:
    text: str = ""
    fields: dict[str, list] = field(default_factory=dict)
    base_rpr: object | None = None
    editable: bool = True
    reason: str | None = None
    mixed_formatting: bool = False


def _run_text(run) -> str:
    parts = []
    for child in run:
        if child.tag == qn("w:t"):
            parts.append(child.text or "")
        elif child.tag == qn("w:tab"):
            parts.append("\t")
        elif child.tag == qn("w:br"):
            parts.append("\n")
    return "".join(parts)


def tokenize_paragraph(p, counter, depth_in: int = 0) -> tuple[ParagraphFields, int]:
    pf = ParagraphFields()
    if depth_in:
        pf.editable, pf.reason = False, "INSIDE_MULTI_PARAGRAPH_FIELD"
    if any(child.tag not in PARAGRAPH_CHILDREN for child in p):
        pf.editable, pf.reason = False, pf.reason or "UNSUPPORTED_PARAGRAPH_CONTENT"
    depth = depth_in
    group: list = []
    instruction: list[str] = []
    collecting = False
    pieces: list[str] = []
    rprs: list[bytes] = []
    for run in p.iter(qn("w:r")):
        if run.getparent() is not p:
            continue
        # A run shared by adjacent fields cannot be assigned to either token
        # without splitting its original XML. Refuse the edit instead of losing one.
        if sum(child.tag == qn("w:fldChar") for child in run) > 1:
            pf.editable, pf.reason = False, pf.reason or "MULTIPLE_FIELD_BOUNDARIES_IN_RUN"
        started_here = False
        for child in run:
            if child.tag == qn("w:fldChar"):
                kind = child.get(qn("w:fldCharType"))
                if kind == "begin":
                    depth += 1
                    if depth == 1:
                        group, instruction, collecting, started_here = [], [], True, True
                elif kind == "separate" and depth == 1:
                    collecting = False
                elif kind == "end":
                    depth = max(depth - 1, 0)
            elif child.tag == qn("w:instrText") and collecting and depth == 1:
                instruction.append(child.text or "")
        in_field = bool(group) or started_here or depth > 0
        if in_field:
            if started_here and run.find(qn("w:t")) is not None:
                pf.editable, pf.reason = False, pf.reason or "MIXED_FIELD_RUN"
            group.append(deepcopy(run))
            if depth == 0:
                is_zotero = "".join(instruction).strip().startswith(ZOTERO_PREFIXES)
                token = f"⟦{'Z' if is_zotero else 'F'}:{next(counter)}⟧"
                pf.fields[token] = group
                pieces.append(token)
                group = []
            continue
        if any(child.tag not in TEXT_RUN_CHILDREN for child in run):
            pf.editable, pf.reason = False, pf.reason or "UNSUPPORTED_RUN_CONTENT"
        rpr = run.find(qn("w:rPr"))
        if pf.base_rpr is None and rpr is not None:
            pf.base_rpr = deepcopy(rpr)
        rprs.append(etree.tostring(rpr) if rpr is not None else b"")
        pieces.append(_run_text(run))
    if group:
        pf.editable, pf.reason = False, pf.reason or "FIELD_SPANS_PARAGRAPHS"
    pf.mixed_formatting = len(set(rprs)) > 1
    pf.text = "".join(pieces)
    return pf, depth


def _text_run(text: str, base_rpr) -> object:
    run = OxmlElement("w:r")
    if base_rpr is not None:
        run.append(deepcopy(base_rpr))
    for part in re.split(r"(\t|\n)", text):
        if part == "\t":
            run.append(OxmlElement("w:tab"))
        elif part == "\n":
            run.append(OxmlElement("w:br"))
        elif part:
            node = OxmlElement("w:t")
            node.set(qn("xml:space"), "preserve")
            node.text = part
            run.append(node)
    return run


def detokenize_paragraph(p, new_text: str, pf: ParagraphFields, citations: dict[str, list] | None = None) -> None:
    citations = citations or {}
    found = FIELD_TOKEN.findall(new_text)
    for token, seen in Counter(found).items():
        if token not in pf.fields:
            raise ZoteroFieldError(f"FIELD_TOKEN_UNKNOWN:{token}")
        if seen > 1:
            raise ZoteroFieldError(f"FIELD_TOKEN_DUPLICATED:{token}")
    missing = sorted(set(pf.fields) - set(found))
    if missing:
        raise ZoteroFieldError(f"FIELD_TOKEN_MISSING:{','.join(missing)}")
    for child in list(p):
        if child.tag != qn("w:pPr"):
            p.remove(child)
    position = 0
    for match in TOKEN.finditer(new_text):
        if match.start() > position:
            p.append(_text_run(new_text[position : match.start()], pf.base_rpr))
        runs = pf.fields.get(match.group(0)) or citations.get(match.group(0))
        if runs is None:
            raise ZoteroFieldError(f"CITATION_NOT_RESOLVED:{match.group(0)}")
        for run in runs:
            p.append(deepcopy(run))
        position = match.end()
    if position < len(new_text):
        p.append(_text_run(new_text[position:], pf.base_rpr))


def _paragraphs(document) -> list:
    return list(document.element.body.iter(qn("w:p")))


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export_paragraphs(path: Path) -> dict:
    document = Document(str(path))
    counter = count(1)
    depth = 0
    rows = []
    for index, p in enumerate(_paragraphs(document)):
        pf, depth = tokenize_paragraph(p, counter, depth)
        if pf.text.strip() or pf.fields:
            rows.append(
                {
                    "index": index,
                    "text": pf.text,
                    "editable": pf.editable,
                    "reason": pf.reason,
                    "mixed_formatting": pf.mixed_formatting,
                }
            )
    return {"source_sha256": _sha256(path), "paragraphs": rows}


def _expand_citations(text: str, resolver) -> tuple[str, dict[str, list], list[str]]:
    citations: dict[str, list] = {}
    unresolved: list[str] = []

    def replace(match):
        keys = match.group(1).split(";")
        if resolver is None:
            unresolved.extend(keys)
            return f"[CẦN TRÍCH DẪN: {'; '.join(keys)}]"
        items, missing = resolver(keys)
        if missing:
            unresolved.extend(missing)
            return f"[CẦN TRÍCH DẪN: {'; '.join(keys)}]"
        occurrence_id = uuid.uuid4().hex
        marker = f"⟦C:{occurrence_id}⟧"
        citations[marker] = build_citation_field(items, occurrence_id)
        return marker

    return CITE_TOKEN.sub(replace, text), citations, unresolved


def apply_edits(
    path: Path, edits: dict[int, str], out_path: Path, *, expected_sha256: str | None = None, resolver=None
) -> dict:
    path, out_path = Path(path), Path(out_path)
    if expected_sha256 and _sha256(path) != expected_sha256:
        raise ZoteroFieldError("SOURCE_CHANGED_SINCE_EXPORT")
    if path.resolve() == out_path.resolve():
        raise ZoteroFieldError("SOURCE_OVERWRITE_FORBIDDEN")
    document = Document(str(path))
    counter = count(1)
    depth = 0
    unresolved: list[str] = []
    for index, p in enumerate(_paragraphs(document)):
        pf, depth = tokenize_paragraph(p, counter, depth)
        if index not in edits or edits[index] == pf.text:
            continue
        if not pf.editable:
            raise ZoteroFieldError(f"PARAGRAPH_NOT_EDITABLE:{index}:{pf.reason}")
        new_text, citations, missing = _expand_citations(edits[index], resolver)
        unresolved.extend(missing)
        detokenize_paragraph(p, new_text, pf, citations)
    document.save(str(out_path))
    report = audit(path, out_path)
    report["unresolved_citations"] = sorted(set(unresolved))
    if report["status"] == "BLOCKED":
        out_path.unlink()
    return report


def _field_instructions(root, *, zotero_only: bool = True) -> list[str]:
    found = []
    depth = 0
    buffer: list[str] = []
    collecting = False
    for element in root.iter(f"{{{W_NS}}}fldChar", f"{{{W_NS}}}instrText"):
        if element.tag == f"{{{W_NS}}}fldChar":
            kind = element.get(f"{{{W_NS}}}fldCharType")
            if kind == "begin":
                depth += 1
                if depth == 1:
                    buffer, collecting = [], True
            elif kind == "separate" and depth == 1:
                collecting = False
            elif kind == "end":
                if depth == 1:
                    instruction = "".join(buffer).strip()
                    if instruction and (not zotero_only or instruction.startswith(ZOTERO_PREFIXES)):
                        found.append(instruction)
                depth = max(depth - 1, 0)
        elif collecting and depth == 1:
            buffer.append(element.text or "")
    return found


def _field_inventory(path: Path, *, zotero_only: bool) -> Counter:
    counts: Counter = Counter()
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        for part in FIELD_PARTS:
            if part in names:
                counts.update(_field_instructions(etree.fromstring(archive.read(part)), zotero_only=zotero_only))
    return counts


def zotero_inventory(path: Path) -> Counter:
    return _field_inventory(path, zotero_only=True)


def zotero_preferences(path: Path) -> set[str]:
    found: set[str] = set()
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        for part in PREFERENCE_PARTS:
            if part in names:
                found.update(PREFERENCE_NAME.findall(archive.read(part).decode("utf-8", errors="replace")))
    return found


def audit(before: Path, after: Path) -> dict:
    fields_before, fields_after = zotero_inventory(before), zotero_inventory(after)
    missing = _field_inventory(before, zotero_only=False) - _field_inventory(after, zotero_only=False)
    preferences_missing = sorted(zotero_preferences(before) - zotero_preferences(after))
    return {
        "status": "BLOCKED" if missing or preferences_missing else "PASS",
        "fields_before": sum(fields_before.values()),
        "fields_after": sum(fields_after.values()),
        "missing": [instruction[:160] for instruction in missing.elements()],
        "added_count": sum((fields_after - fields_before).values()),
        "preferences_missing": preferences_missing,
    }


def _fld_run(kind: str):
    run = OxmlElement("w:r")
    node = OxmlElement("w:fldChar")
    node.set(qn("w:fldCharType"), kind)
    run.append(node)
    return run


def _label(item) -> str:
    authors = item.csl.get("author") or []
    first_author = authors[0] if authors and isinstance(authors[0], dict) else {}
    name = first_author.get("literal") or first_author.get("family") or first_author.get("given") or item.key
    issued = item.csl.get("issued") or {}
    date_parts = issued.get("date-parts") or []
    year = date_parts[0][0] if date_parts and date_parts[0] else None
    return f"{name}, {year}" if year else name


def build_citation_field(items, citation_id: str) -> list:
    """Build a live ZOTERO_ITEM field; `items` need `.key`, `.item_id`, `.uri` and `.csl`."""
    display = "(" + "; ".join(_label(item) for item in items) + ")"
    payload = {
        "citationID": citation_id,
        "properties": {"formattedCitation": display, "plainCitation": display, "noteIndex": 0},
        "citationItems": [{"id": item.item_id, "uris": [item.uri], "itemData": item.csl} for item in items],
        "schema": CSL_SCHEMA,
    }
    instruction = OxmlElement("w:r")
    text = OxmlElement("w:instrText")
    text.set(qn("xml:space"), "preserve")
    text.text = " ADDIN ZOTERO_ITEM CSL_CITATION " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + " "
    instruction.append(text)
    return [_fld_run("begin"), instruction, _fld_run("separate"), _text_run(display, None), _fld_run("end")]
