"""Read-only OOXML structural checks and identity fingerprints; stdlib only."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
from collections import Counter
from xml.etree import ElementTree as ET
from zipfile import ZipFile, BadZipFile


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/package/2006/relationships"


def _q(name):
    return f"{{{W}}}{name}"


def _digest(records):
    values = sorted(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records)
    return hashlib.sha256(json.dumps(values, ensure_ascii=False).encode("utf-8")).hexdigest()


def audit_docx_integrity(path: Path) -> dict:
    issues = []
    def issue(code, part, detail=""):
        issues.append({"code": code, "part": part, "detail": detail})
    protected = {"fields": [], "relationships": [], "footnotes": [], "endnotes": [], "comments": [], "bookmarks": []}
    roots = {}
    try:
        with ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                issue("DUPLICATE_PACKAGE_PART", "package")
            if "word/document.xml" not in names:
                issue("MAIN_DOCUMENT_MISSING", "package")
            for name in names:
                if name.startswith("/") or ".." in PurePosixPath(name).parts:
                    issue("UNSAFE_PACKAGE_PATH", name)
                if not name.endswith((".xml", ".rels")):
                    continue
                info = archive.getinfo(name)
                if info.file_size > 32 * 1024 * 1024:
                    issue("XML_PART_TOO_LARGE", name)
                    continue
                raw = archive.read(name)
                if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
                    issue("UNSAFE_XML_DECLARATION", name)
                    continue
                try:
                    roots[name] = ET.fromstring(raw)
                except ET.ParseError:
                    issue("MALFORMED_XML", name)
    except (OSError, BadZipFile):
        issue("UNREADABLE_PACKAGE", "package")
        names = []
    targets = {}
    for kind, part, element in (("footnotes", "word/footnotes.xml", "footnote"),
                                ("endnotes", "word/endnotes.xml", "endnote"),
                                ("comments", "word/comments.xml", "comment")):
        root = roots.get(part)
        records = root.findall(_q(element)) if root is not None else []
        ids = [node.get(_q("id")) for node in records]
        targets[kind] = set(ids)
        if len(ids) != len(set(ids)):
            issue("DUPLICATE_OBJECT_ID", part)
        for node in records:
            protected[kind].append({"id": node.get(_q("id")), "xml": ET.tostring(node, encoding="unicode")})
    for part, root in roots.items():
        if part.endswith(".rels"):
            owner_dir = "" if part == "_rels/.rels" else str(PurePosixPath(part).parent.parent)
            for node in root.findall(f"{{{R}}}Relationship"):
                target = node.get("Target", "")
                mode = node.get("TargetMode", "Internal")
                protected["relationships"].append({"part": part, "id": node.get("Id"), "type": node.get("Type"), "target": target, "mode": mode})
                if mode == "External":
                    continue
                from urllib.parse import unquote
                decoded = unquote(target.split("#", 1)[0])
                resolved = posixpath.normpath(posixpath.join(owner_dir, decoded)) if not decoded.startswith("/") else decoded.lstrip("/")
                if resolved not in names:
                    issue("MISSING_RELATIONSHIP_TARGET", part, node.get("Id", ""))
        if not part.startswith("word/") or not part.endswith(".xml"):
            continue
        stack = []
        comment_marks = {"commentRangeStart": [], "commentRangeEnd": [], "commentReference": []}
        bookmarks = {"bookmarkStart": [], "bookmarkEnd": []}
        for node in root.iter():
            if node.tag == _q("fldChar"):
                kind = node.get(_q("fldCharType"))
                if kind == "begin":
                    stack.append({"instruction": "", "separated": False})
                elif kind == "separate":
                    if not stack or stack[-1]["separated"]:
                        issue("FIELD_UNBALANCED", part)
                    else:
                        stack[-1]["separated"] = True
                elif kind == "end":
                    if not stack:
                        issue("FIELD_UNBALANCED", part)
                    else:
                        protected["fields"].append({"part": part, "instruction": stack.pop()["instruction"].strip()})
            elif node.tag == _q("instrText"):
                if stack and not stack[-1]["separated"]:
                    stack[-1]["instruction"] += node.text or ""
                elif not stack:
                    issue("FIELD_INSTRUCTION_ORPHAN", part)
            elif node.tag == _q("fldSimple"):
                protected["fields"].append({"part": part, "instruction": (node.get(_q("instr")) or "").strip()})
            for kind, reference, code in (("footnotes", "footnoteReference", "MISSING_FOOTNOTE_TARGET"),
                                          ("endnotes", "endnoteReference", "MISSING_ENDNOTE_TARGET")):
                if node.tag == _q(reference) and node.get(_q("id")) not in targets[kind]:
                    issue(code, part, node.get(_q("id"), ""))
            for tag in comment_marks:
                if node.tag == _q(tag):
                    identifier = node.get(_q("id"))
                    comment_marks[tag].append(identifier)
                    protected["comments"].append({"part": part, "kind": tag, "id": identifier})
                    if identifier not in targets["comments"]:
                        issue("MISSING_COMMENT_TARGET", part, identifier or "")
            for tag in bookmarks:
                if node.tag == _q(tag):
                    bookmarks[tag].append(node.get(_q("id")))
                    protected["bookmarks"].append({"part": part, "kind": tag, "id": node.get(_q("id")), "name": node.get(_q("name"))})
        if stack:
            issue("FIELD_UNBALANCED", part)
        if sorted(comment_marks["commentRangeStart"]) != sorted(comment_marks["commentRangeEnd"]):
            issue("COMMENT_ANCHOR_UNBALANCED", part)
        if sorted(bookmarks["bookmarkStart"]) != sorted(bookmarks["bookmarkEnd"]):
            issue("BOOKMARK_UNBALANCED", part)
    return {"status": "FAIL" if issues else "PASS", "issues": issues,
            "protected_fingerprints": {kind: _digest(records) for kind, records in protected.items()},
            "protected_items": {kind: [_digest([record]) for record in records] for kind, records in protected.items()},
            "unperformed_checks": ["visual-layout", "field-refresh", "semantic-anchor-review"]}


def compare_docx_integrity(source: Path, output: Path) -> dict:
    before, after = audit_docx_integrity(source), audit_docx_integrity(output)
    lost = [kind for kind, items in before["protected_items"].items()
            if Counter(items) - Counter(after["protected_items"].get(kind, []))]
    return {"status": "FAIL" if lost or before["status"] != "PASS" or after["status"] != "PASS" else "PASS",
            "lost_protected_kinds": lost, "source": before, "output": after}
