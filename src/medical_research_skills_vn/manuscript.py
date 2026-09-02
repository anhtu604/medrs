"""Document-level assembly state for medical manuscripts."""

from hashlib import sha256


def assemble_manuscript(*, sections: list[dict], substantive_revision: bool) -> dict:
    names = [section["section"] for section in sections]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate manuscript section")
    text = "\n\n".join(section.get("draft", "") for section in sections)
    blockers = sorted(
        {
            marker
            for section in sections
            for marker in section.get("markers", [])
        }
        | {
            f"PREFLIGHT_{section['section']}"
            for section in sections
            if section.get("preflight", {}).get("status") not in {None, "PASS"}
        }
        | {
            f"SECTION_NOT_SUBMISSION_READY:{section['section']}"
            for section in sections
            if section.get("submission_verdict") not in {None, "READY_FOR_DOCUMENT_GATE"}
        }
        | {
            f"SECTION_LIFECYCLE_NOT_FINAL:{section['section']}"
            for section in sections
            if section.get("lifecycle_state") not in {None, "FINAL_VERIFIED"}
        }
    )
    return {
        "sections": names,
        "document_hash": sha256(text.encode("utf-8")).hexdigest(),
        "full_gate_invocations": 2 if substantive_revision else 1,
        "full_gate_scope": "assembled-document",
        "gate_skill": "kiem-van-phong",
        "status": "BLOCKED" if blockers else "PENDING_FULL_GATE",
        "blockers": blockers,
    }
