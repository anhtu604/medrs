import json
from pathlib import Path

import pytest

from revision_guard import snapshot, sha256, output_lease


def workspace_module():
    import project_workspace
    return project_workspace


def accepted(path):
    return {"status": "ACCEPTED_INTERNAL", "sha256": sha256(path)}


def prepare(tmp_path):
    api = workspace_module()
    root = tmp_path / "project"
    api.initialize_project(root, "synthetic", "2026-10-11")
    source = tmp_path / "author.txt"
    source.write_text("original", encoding="utf-8")
    staged = tmp_path / "manuscript.txt"
    staged.write_text("accepted draft", encoding="utf-8")
    return api, root, source, staged


def test_initialize_preserves_author_readme_and_daily_notes(tmp_path):
    api = workspace_module()
    root = tmp_path / "project"
    api.initialize_project(root, "fixture", "2026-10-11")
    note = root / "README.md"
    note.write_text(note.read_text(encoding="utf-8") + "\nAuthor note\n", encoding="utf-8")
    daily = root / "history/2026-10-11/README.md"
    daily.write_text(daily.read_text(encoding="utf-8") + "\nDaily author note\n", encoding="utf-8")
    api.initialize_project(root, "fixture", "2026-10-11")
    assert "Author note" in note.read_text(encoding="utf-8")
    assert "Daily author note" in daily.read_text(encoding="utf-8")
    assert (root / "final").is_dir()
    with pytest.raises(ValueError, match="PROJECT_ID_CONFLICT"):
        api.initialize_project(root, "different", "2026-10-11")


@pytest.mark.parametrize("value", ["../escape", "2026-1-1", "2026-02-30", "2026-10-11/other"])
def test_invalid_date_creates_nothing(tmp_path, value):
    api = workspace_module()
    root = tmp_path / "project"
    with pytest.raises(ValueError):
        api.initialize_project(root, "fixture", value)
    assert not root.exists()


def test_paths_cannot_escape_project(tmp_path):
    api, root, _, _ = prepare(tmp_path)
    for path in ("../outside", str(tmp_path / "outside"), "."):
        with pytest.raises(ValueError):
            api.project_path(root, path)


def test_events_append_and_explain_changes_without_losing_previous_day(tmp_path):
    api, root, _, _ = prepare(tmp_path)
    first = api.record_event(root, "2026-10-11", {"action": "REVISED", "summary": "Corrected heading styles", "changes": "Replaced direct formatting"})
    api.record_event(root, "2026-10-11", {"action": "TESTED", "summary": "Checked fields", "status": "PASS"})
    api.record_event(root, "2026-10-12", {"action": "REVISED", "summary": "Updated table widths", "changes": "Narrowed numeric column vs previous day"})
    records = [json.loads(line) for line in first.read_text(encoding="utf-8").splitlines()]
    assert [item["action"] for item in records] == ["REVISED", "TESTED"]
    assert "Corrected heading styles" in (root / "history/2026-10-11/README.md").read_text(encoding="utf-8")
    assert "Narrowed numeric column" in (root / "history/2026-10-12/README.md").read_text(encoding="utf-8")
    assert "Updated table widths" in (root / "README.md").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="EVENT_FIELD"):
        api.record_event(root, "2026-10-11", {"action": "WRITE", "participant_rows": [{"name": "private"}]})


def test_promotion_keeps_both_versions_and_original_source(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    before = snapshot(source)
    first = api.promote_final(root, staged, before, "2026-10-11", acceptance=accepted(staged))
    staged.write_text("second accepted draft", encoding="utf-8")
    second = api.promote_final(root, staged, before, "2026-10-11", acceptance=accepted(staged))
    assert (root / "final/manuscript.txt").read_text(encoding="utf-8") == "second accepted draft"
    assert snapshot(source) == before
    assert first["round"] != second["round"]
    assert (Path(second["round"]) / "previous/manuscript.txt").read_text(encoding="utf-8") == "accepted draft"
    assert (Path(first["round"]) / "staged/manuscript.txt").read_text(encoding="utf-8") == "accepted draft"
    state = json.loads((root / ".medrs-project.json").read_text(encoding="utf-8"))
    assert state["final"]["manuscript.txt"]["sha256"] == sha256(root / "final/manuscript.txt")


def test_promotion_rejects_missing_or_stale_acceptance(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    for evidence in (None, {"status": "PENDING", "sha256": sha256(staged)}, {"status": "ACCEPTED_INTERNAL", "sha256": "old"}):
        with pytest.raises(ValueError, match="ACCEPTANCE_REQUIRED"):
            api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=evidence)
    assert not (root / "final/manuscript.txt").exists()


def test_changed_source_blocks_promotion(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    before = snapshot(source)
    source.write_text("author edited", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_CHANGED"):
        api.promote_final(root, staged, before, "2026-10-11", acceptance=accepted(staged))
    assert not (root / "final/manuscript.txt").exists()
    assert source.read_text(encoding="utf-8") == "author edited"


def test_unmanaged_final_collision_is_not_overwritten(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    target = root / "final/manuscript.txt"
    target.write_text("author final", encoding="utf-8")
    with pytest.raises(RuntimeError, match="FINAL_CHANGED_OR_UNMANAGED"):
        api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    assert target.read_text(encoding="utf-8") == "author final"


def test_author_modified_managed_final_is_not_overwritten(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    target = root / "final/manuscript.txt"
    target.write_text("new author edit", encoding="utf-8")
    with pytest.raises(RuntimeError, match="FINAL_CHANGED_OR_UNMANAGED"):
        api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    assert target.read_text(encoding="utf-8") == "new author edit"


def test_failed_replace_preserves_recovery_files(tmp_path, monkeypatch):
    api, root, source, staged = prepare(tmp_path)
    api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    staged.write_text("new accepted", encoding="utf-8")
    real_replace = api.os.replace
    def failed_replace(src, dst):
        if Path(dst) == root / "final/manuscript.txt":
            raise OSError("file held open")
        return real_replace(src, dst)
    monkeypatch.setattr(api.os, "replace", failed_replace)
    with pytest.raises(OSError, match="file held open"):
        api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    assert (root / "final/manuscript.txt").read_text(encoding="utf-8") == "accepted draft"
    recoveries = list((root / "history/2026-10-11").glob("round-*/staged/manuscript.txt"))
    assert any(path.read_text(encoding="utf-8") == "new accepted" for path in recoveries)
    statuses = [json.loads(p.read_text(encoding="utf-8"))["status"] for p in (root / "history/2026-10-11").glob("round-*/promotion.json")]
    assert "PROMOTION_INCOMPLETE" in statuses


def test_project_lock_blocks_concurrent_promotion(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    with output_lease(root / ".medrs-project.json", "other"):
        with pytest.raises(FileExistsError):
            api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    assert not (root / "final/manuscript.txt").exists()


def test_accepts_existing_leader_receipt_shape(tmp_path):
    api, root, source, staged = prepare(tmp_path)
    receipt = {"status": "ACCEPTED_INTERNAL", "artifact_sha256": sha256(staged)}
    result = api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=receipt)
    assert result["status"] == "PROMOTED"


def test_source_change_during_staging_leaves_final_and_recovery_intact(tmp_path, monkeypatch):
    api, root, source, staged = prepare(tmp_path)
    api.promote_final(root, staged, snapshot(source), "2026-10-11", acceptance=accepted(staged))
    before = snapshot(source)
    real_copy = api.shutil.copyfile
    def copy_then_author_edit(src, dst):
        result = real_copy(src, dst)
        if Path(dst).suffix == ".pending":
            source.write_text("concurrent author edit", encoding="utf-8")
        return result
    monkeypatch.setattr(api.shutil, "copyfile", copy_then_author_edit)
    staged.write_text("new candidate", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_CHANGED"):
        api.promote_final(root, staged, before, "2026-10-11", acceptance=accepted(staged))
    assert (root / "final/manuscript.txt").read_text(encoding="utf-8") == "accepted draft"
    assert source.read_text(encoding="utf-8") == "concurrent author edit"
    assert any(path.read_text(encoding="utf-8") == "new candidate" for path in (root / "history/2026-10-11").glob("round-*/staged/manuscript.txt"))
