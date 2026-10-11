"""Portable version protection and evidence-bound final acceptance; stdlib only."""

import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(path):
    path = Path(path).resolve()
    before = path.stat()
    digest = sha256(path)
    after = path.stat()
    if (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size):
        raise RuntimeError("SOURCE_CHANGED_DURING_SNAPSHOT")
    return {"path": str(path), "sha256": digest, "mtime_ns": after.st_mtime_ns}


def assert_unchanged(record):
    current = snapshot(record["path"])
    if current != record:
        raise RuntimeError("SOURCE_CHANGED")


@contextmanager
def output_lease(output, owner):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    lock = output.with_name(output.name + ".medrs-lock")
    with lock.open("x", encoding="utf-8") as stream:
        json.dump({"owner": owner, "pid": os.getpid(), "output": str(output)}, stream)
    try:
        yield
    finally:
        lock.unlink()


def commit_new_artifact(staged, output, source_snapshot, *, owner="medrs"):
    """Publish only to a vacant destination after verifying the author's source."""
    staged, output = Path(staged).resolve(), Path(output).resolve()
    source = Path(source_snapshot["path"]).resolve()
    if output == source or staged == source or output == staged:
        raise ValueError("SOURCE_OVERWRITE_FORBIDDEN")
    if output.exists():
        raise FileExistsError("OUTPUT_ALREADY_EXISTS")
    with output_lease(output, owner):
        assert_unchanged(source_snapshot)
        # Hard-link creation is atomic and cannot replace an existing destination.
        # Copy to a same-directory temporary first to support another-volume staging.
        descriptor, temporary_name = tempfile.mkstemp(prefix=".medrs-", dir=output.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as dest, staged.open("rb") as src:
                for chunk in iter(lambda: src.read(1048576), b""):
                    dest.write(chunk)
                dest.flush()
                os.fsync(dest.fileno())
            assert_unchanged(source_snapshot)
            os.link(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
    return snapshot(output)


def effective_decisions(records):
    """Latest chronological confirmed decision wins for the same scoped key."""
    active = {}
    for record in records:
        if record.get("status") == "CONFIRMED":
            active[(record.get("scope", "project"), record["key"])] = record
    return list(active.values())


def final_acceptance(artifact, tasks, evidence, *, source_preserved, propagation_complete,
                     docx=True, author_acceptance="PENDING"):
    """Evidence files are reviewed externally, then checked for hash/round drift here."""
    final_hash = sha256(artifact)
    required = {"content", "clear-prose", "scope-preservation"}
    if docx:
        required |= {"docx-integrity", "field-refresh", "presentation", "visual-inspection"}
    problems = []
    if not tasks:
        problems.append("TASK_LIST_EMPTY")
    for task in tasks:
        if task.get("status") != "DONE":
            problems.append("TASK_INCOMPLETE:" + str(task.get("id", "?")))
    if not source_preserved:
        problems.append("SOURCE_NOT_PRESERVED")
    if not propagation_complete:
        problems.append("PROPAGATION_INCOMPLETE")
    by_kind = {}
    for item in evidence:
        problems.extend(status_receipt_issues(item, "artifact-check"))
        by_kind.setdefault(item.get("kind"), []).append(item)
    for kind in sorted(required):
        items = by_kind.get(kind, [])
        if not items:
            problems.append("EVIDENCE_MISSING:" + kind)
            continue
        for item in items:
            if item.get("artifact_sha256") != final_hash:
                problems.append("EVIDENCE_STALE:" + kind)
            if item.get("status") != "PASS":
                problems.append("CHECK_NOT_PASSED:" + kind)
            if not item.get("reviewer"):
                problems.append("REVIEWER_MISSING:" + kind)
            path = Path(item.get("path") or "")
            if not path.is_file() or sha256(path) != item.get("sha256"):
                problems.append("EVIDENCE_FILE_INVALID:" + kind)
    if any(problem.startswith("EVIDENCE_STALE") for problem in problems):
        status = "RE_REVIEW_REQUIRED"
    elif any(problem.startswith(("CHECK_NOT_PASSED", "TASK_INCOMPLETE", "SOURCE_NOT", "PROPAGATION")) for problem in problems):
        status = "NEEDS_REVISION"
    elif problems:
        status = "VERIFICATION_INCOMPLETE"
    else:
        status = "ACCEPTED_INTERNAL"
    return {"status": status, "artifact": str(Path(artifact).resolve()),
            "artifact_sha256": final_hash, "problems": problems,
            "author_acceptance": author_acceptance}


def receipt_is_current(receipt):
    path = Path(receipt["artifact"])
    return path.is_file() and sha256(path) == receipt["artifact_sha256"]


def status_receipt_issues(receipt, context):
    """Context/evidence presence validation; never substitutes for external review."""
    registry_path = Path(__file__).resolve().parents[3] / "schemas/status-codes.json"
    if not registry_path.is_file():
        registry_path = Path(__file__).resolve().parents[3] / "medical-research-skills-vn/schemas/status-codes.json"
    try:
        codes = json.loads(registry_path.read_text(encoding="utf-8"))["codes"]
    except (OSError, ValueError, KeyError):
        return ["STATUS_REGISTRY_UNAVAILABLE"]
    status = receipt.get("status")
    definition = codes.get(status)
    if definition is None:
        return ["STATUS_UNKNOWN:" + str(status)]
    issues = []
    if context not in definition["contexts"]:
        issues.append("STATUS_CONTEXT_INVALID:" + status)
    for field in definition.get("required_evidence", []):
        if not receipt.get(field):
            issues.append("STATUS_EVIDENCE_MISSING:" + field)
    return issues
