"""Recoverable local project lifecycle. No network; no participant data logging."""

from datetime import date as calendar_date
import json
import os
from pathlib import Path
import shutil
import uuid

from revision_guard import assert_unchanged, output_lease, sha256


STATE_FILE = ".medrs-project.json"
BEGIN = "<!-- medrs:progress:start -->"
END = "<!-- medrs:progress:end -->"
EVENT_FIELDS = {"action", "summary", "changes", "status", "task_id", "artifact", "sha256", "round"}


def _date(value):
    if not isinstance(value, str) or calendar_date.fromisoformat(value).isoformat() != value:
        raise ValueError("ISO_DATE_REQUIRED")
    return value


def project_path(root: Path, relative: str) -> Path:
    root = Path(root).resolve()
    candidate = (root / relative).resolve()
    if candidate == root or root not in candidate.parents:
        raise ValueError("PATH_OUTSIDE_PROJECT")
    return candidate


def _read_state(root):
    return json.loads(project_path(root, STATE_FILE).read_text(encoding="utf-8"))


def _atomic_json(path, value):
    path = Path(path)
    temporary = path.with_name(f".{path.name}-{uuid.uuid4().hex}.tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def _update_note(path, content):
    """Replace only the managed block; keep all author text outside it."""
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    block = f"{BEGIN}\n{content.rstrip()}\n{END}"
    if existing.count(BEGIN) != existing.count(END) or existing.count(BEGIN) > 1:
        raise ValueError("README_MARKERS_AMBIGUOUS")
    if BEGIN in existing:
        left, tail = existing.split(BEGIN, 1)
        _, right = tail.split(END, 1)
        text = left + block + right
    else:
        text = existing.rstrip() + ("\n\n" if existing else "") + block + "\n"
    temporary = path.with_name(f".{path.name}-{uuid.uuid4().hex}.tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def _ensure_day(root, date):
    daily = project_path(root, f"history/{_date(date)}")
    daily.mkdir(parents=True, exist_ok=True)
    (daily / "logs").mkdir(exist_ok=True)
    note = daily / "README.md"
    if not note.exists():
        with note.open("x", encoding="utf-8") as stream:
            stream.write(f"# {date}\n\nWork and changes versus the previous day are recorded below.\n")
    return daily


def _refresh_notes(root, state, date):
    daily = _ensure_day(root, date)
    journal = daily / "events.jsonl"
    entries = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines()] if journal.exists() else []
    lines = [f"- {item['action']}: {item.get('summary', '')}" + (f" — changes: {item['changes']}" if item.get("changes") else "") for item in entries]
    _update_note(daily / "README.md", "## Activity\n\n" + ("\n".join(lines) or "No work recorded yet."))
    current = "\n".join(f"- {name}: {record['sha256']}" for name, record in state["final"].items()) or "No accepted final artifacts yet."
    latest = state.get("last_event") or {}
    content = (f"# Project {state['project_id']}\n\n"
               f"Status: {state['status']}\n\n"
               f"Latest activity ({date}): {latest.get('summary', 'Project initialized')}\n\n"
               f"## Current accepted files\n\n{current}\n\n"
               "## Storage\n\nfinal/: accepted current files.\n"
               "history/YYYY-MM-DD/: archived rounds, daily notes, events and logs.\n"
               "Keep all history and logs; never store participant identifiers in progress notes.\n")
    _update_note(project_path(root, "README.md"), content)


def initialize_project(root: Path, project_id: str, date: str) -> dict:
    _date(date)
    if not isinstance(project_id, str) or not project_id.strip() or any(char in project_id for char in "\r\n"):
        raise ValueError("PROJECT_ID_REQUIRED")
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    state_path = project_path(root, STATE_FILE)
    with output_lease(state_path, "project-init"):
        if state_path.exists():
            state = _read_state(root)
            if state["project_id"] != project_id:
                raise ValueError("PROJECT_ID_CONFLICT")
        else:
            state = {"schema_version": "1.0.0", "project_id": project_id, "status": "IN_PROGRESS", "final": {}, "last_event": None}
            _atomic_json(state_path, state)
        project_path(root, "final").mkdir(exist_ok=True)
        _ensure_day(root, date)
        _refresh_notes(root, state, date)
    return state


def _append_event(root, date, event):
    if set(event) - EVENT_FIELDS:
        raise ValueError("EVENT_FIELD_NOT_ALLOWED")
    if not isinstance(event.get("action"), str) or not event["action"].strip():
        raise ValueError("EVENT_ACTION_REQUIRED")
    if any(not isinstance(value, str) for value in event.values()):
        raise ValueError("EVENT_VALUES_MUST_BE_REDACTED_STRINGS")
    journal = _ensure_day(root, date) / "events.jsonl"
    record = {**event, "date": date, "event_id": uuid.uuid4().hex}
    with journal.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return journal, record


def record_event(root: Path, date: str, event: dict) -> Path:
    _date(date)
    root = Path(root).resolve()
    with output_lease(project_path(root, STATE_FILE), "project-event"):
        state = _read_state(root)
        journal, record = _append_event(root, date, event)
        state["last_event"] = record
        _atomic_json(project_path(root, STATE_FILE), state)
        _refresh_notes(root, state, date)
    return journal


def promote_final(root: Path, staged: Path, source_snapshot: dict, date: str, *, acceptance: dict | None = None) -> dict:
    """Promote one accepted artifact; recoverable archives precede any replacement.

    Acceptance is a caller-supplied evidence-bound receipt, not semantic proof
    supplied by this mechanical utility. Author acceptance remains separate.
    """
    _date(date)
    root, staged = Path(root).resolve(), Path(staged).resolve()
    digest = sha256(staged)
    if not acceptance or acceptance.get("status") != "ACCEPTED_INTERNAL" or acceptance.get("artifact_sha256", acceptance.get("sha256")) != digest:
        raise ValueError("ACCEPTANCE_REQUIRED")
    target = project_path(root, f"final/{staged.name}")
    source = Path(source_snapshot["path"]).resolve()
    if staged == target or staged == source or source == target:
        raise ValueError("SOURCE_OVERWRITE_FORBIDDEN")
    with output_lease(project_path(root, STATE_FILE), "project-promote"):
        state = _read_state(root)
        assert_unchanged(source_snapshot)
        existing = state["final"].get(staged.name)
        if target.exists() and (not existing or existing["sha256"] != sha256(target)):
            raise RuntimeError("FINAL_CHANGED_OR_UNMANAGED")
        if existing and not target.exists():
            raise RuntimeError("FINAL_CHANGED_OR_UNMANAGED")
        daily = _ensure_day(root, date)
        round_path = daily / f"round-{uuid.uuid4().hex}"
        round_path.mkdir()
        (round_path / "staged").mkdir()
        archived = round_path / "staged" / staged.name
        shutil.copyfile(staged, archived)
        if sha256(archived) != digest:
            raise RuntimeError("STAGED_CHANGED")
        if target.exists():
            (round_path / "previous").mkdir()
            shutil.copyfile(target, round_path / "previous" / target.name)
        receipt = {"status": "PROMOTION_PENDING", "sha256": digest, "artifact": staged.name,
                   "source_sha256": source_snapshot["sha256"], "round": str(round_path), "date": date}
        _atomic_json(round_path / "promotion.json", receipt)
        temporary = project_path(root, f"final/.medrs-{uuid.uuid4().hex}.pending")
        try:
            shutil.copyfile(archived, temporary)
            assert_unchanged(source_snapshot)
            if target.exists() and (not existing or sha256(target) != existing["sha256"]):
                raise RuntimeError("FINAL_CHANGED_OR_UNMANAGED")
            os.replace(temporary, target)
            state["final"][target.name] = {"sha256": digest, "date": date, "round": str(round_path)}
            _, event = _append_event(root, date, {"action": "PROMOTED", "summary": f"Accepted artifact: {target.name}",
                                               "artifact": target.name, "sha256": digest, "round": str(round_path),
                                               "changes": "Previous accepted version archived before replacement"})
            state["last_event"] = event
            _atomic_json(project_path(root, STATE_FILE), state)
            _refresh_notes(root, state, date)
            receipt["status"] = "PROMOTED"
            _atomic_json(round_path / "promotion.json", receipt)
        except Exception:
            receipt["status"] = "PROMOTION_INCOMPLETE"
            _atomic_json(round_path / "promotion.json", receipt)
            raise
    return receipt
