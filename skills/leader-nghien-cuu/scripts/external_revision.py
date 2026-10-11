"""Consent-bound local handoff and returned-file intake. Never sends data."""

import difflib
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from revision_guard import sha256
from project_workspace import record_event

_word_scripts = Path(__file__).parents[3] / "skills/dinh-dang-tai-lieu/scripts"
if str(_word_scripts) not in sys.path:
    sys.path.insert(0, str(_word_scripts))
from docx_integrity import audit_docx_integrity, compare_docx_integrity


def transfer_permitted(authorization: dict) -> bool:
    return (authorization.get("confirmed") is True
            and isinstance(authorization.get("destination"), str) and bool(authorization["destination"].strip())
            and isinstance(authorization.get("data_class"), str) and bool(authorization["data_class"].strip())
            and isinstance(authorization.get("fields"), list) and bool(authorization["fields"])
            and all(isinstance(field, str) and bool(field.strip()) for field in authorization["fields"])
            and isinstance(authorization.get("scope"), str) and bool(authorization["scope"].strip()))


def prepare_handoff(source: Path, tasks: list[dict], authorization: dict) -> dict:
    source = Path(source).resolve()
    permitted = transfer_permitted(authorization)
    ids = [task["id"] for task in tasks]
    if any(not isinstance(identifier, str) or not identifier for identifier in ids) or len(ids) != len(set(ids)):
        raise ValueError("UNIQUE_TASK_IDS_REQUIRED")
    report = {"schema_version": "1.0.0", "status": "READY_FOR_AUTHORIZED_HANDOFF" if permitted else "AUTHOR_APPROVAL_REQUIRED",
              "source": str(source), "source_sha256": sha256(source), "task_ids": ids,
              "tasks": tasks, "authorization": authorization, "transfer_permitted": permitted, "sent": False,
              "prompt": ""}
    if source.suffix.casefold() == ".docx":
        report["integrity"] = audit_docx_integrity(source)
        if report["integrity"]["status"] != "PASS":
            report.update(status="SOURCE_INTEGRITY_FAILED", transfer_permitted=False)
    if report["transfer_permitted"]:
        report["prompt"] = ("Revise only the selected author's scope: " + authorization["scope"]
                            + ". Keep numerical results, study design, live fields, footnotes, bookmarks and comment IDs intact. "
                            "Return a new file plus a task-by-task change record. Unresolved facts remain qualified. "
                            "Do not label the returned file accepted; the originating leader will inspect it.")
    return report


def _text(path):
    path = Path(path)
    if path.suffix.casefold() != ".docx":
        return path.read_text(encoding="utf-8")
    paragraphs = []
    w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if name.startswith("word/") and name.endswith(".xml") and not name.startswith("word/comments"):
                root = ET.fromstring(archive.read(name))
                for paragraph in root.iter(w + "p"):
                    paragraphs.append("".join(node.text or "" for node in paragraph.iter(w + "t")))
    return "\n".join(paragraphs)


def inspect_returned_revision(source: Path, returned: Path, handoff: dict) -> dict:
    source, returned = Path(source), Path(returned)
    source_hash, returned_hash = sha256(source), sha256(returned)
    report = {"status": "REVIEW_REQUIRED", "source_sha256": source_hash, "returned_sha256": returned_hash,
              "task_ids": handoff.get("task_ids", []), "acceptance_invalidated": returned_hash != source_hash,
              "protected_changes": [], "numeric_change": False, "diff": [],
              "unperformed_checks": ["scope-and-content", "design-consistency", "numeric-claim-identity", "field-refresh", "visual-layout"]}
    if source_hash != handoff.get("source_sha256"):
        report.update(status="SOURCE_CHANGED", acceptance_invalidated=True)
        return report
    if source.suffix.casefold() == ".docx" and returned.suffix.casefold() == ".docx":
        audit = compare_docx_integrity(source, returned)
        report["integrity"] = audit
        report["protected_changes"] = audit["lost_protected_kinds"]
        if audit["status"] != "PASS":
            report.update(status="PROTECTED_CONTENT_CHANGED", acceptance_invalidated=True)
            return report
    elif source.suffix.casefold() != returned.suffix.casefold():
        report.update(status="FORMAT_CHANGED_REVIEW_REQUIRED", acceptance_invalidated=True)
        return report
    before, after = _text(source), _text(returned)
    report["diff"] = list(difflib.unified_diff(before.splitlines(), after.splitlines(), fromfile="last-delivered", tofile="returned", lineterm=""))
    numbers = re.compile(r"(?<!\w)[+-]?\d+(?:[.,]\d+)?%?")
    report["numeric_change"] = numbers.findall(before) != numbers.findall(after)
    if returned_hash == source_hash:
        report["status"] = "NO_CHANGES"
    return report


def record_revision_intake(root: Path, date: str, report: dict) -> Path:
    return record_event(root, date, {"action": "RETURNED_REVISION", "status": report["status"],
                                   "summary": "Returned file inspected; semantic and presentation review remain explicit",
                                   "sha256": report["returned_sha256"],
                                   "changes": "Prior acceptance invalidated" if report["acceptance_invalidated"] else "No byte changes"})
