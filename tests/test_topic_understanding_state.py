import json
from pathlib import Path

import pytest
from jsonschema import validate


ROOT = Path(__file__).parents[1]
DAY = "2026-10-23"
SCHEMA = json.loads((ROOT / "schemas/project-state.schema.json").read_text(encoding="utf-8"))


def api():
    import project_workspace
    return project_workspace


def state_of(root):
    return json.loads((root / ".medrs-project.json").read_text(encoding="utf-8"))


def readme(root):
    return (root / "README.md").read_text(encoding="utf-8")


def write_v1_project(root):
    root.mkdir(parents=True)
    (root / "README.md").write_text("# Đề tài ROP\n\nGhi chú tác giả.\n", encoding="utf-8")
    (root / ".medrs-project.json").write_text(json.dumps({
        "schema_version": "1.0.0", "project_id": "rop", "status": "IN_PROGRESS",
        "final": {}, "last_event": None}), encoding="utf-8")


def advance(ws, root, part):
    for value in ("EXPLAINED", "CHECKED_BACK", "DONE"):
        ws.set_understanding(root, DAY, part=part, part_state=value)


def test_new_readme_has_eleven_context_sections_then_progress_block(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY)
    text = readme(root)
    headings = ws.CONTEXT_SECTIONS["vi"]
    assert len(headings) == 11
    positions = [text.index(f"\n## {heading}\n") for heading in headings]
    assert positions == sorted(positions)
    assert positions[-1] < text.index(ws.BEGIN)
    after = text[text.index("\n## Hiểu đề tài\n"):]
    block = after[after.index(ws.UNDERSTANDING_BEGIN):after.index(ws.UNDERSTANDING_END)]
    assert after.index(ws.UNDERSTANDING_BEGIN) < after.index("\n## Kiến thức nền\n")
    assert "NOT_STARTED" in block


def test_english_locale_uses_english_headings(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY, locale="en")
    text = readme(root)
    assert "\n## Topic understanding\n" in text
    assert "## Hiểu đề tài" not in text


def test_existing_readme_gets_missing_sections_without_rewrite(tmp_path):
    ws = api()
    root = tmp_path / "rop"
    write_v1_project(root)
    original = (root / "README.md").read_bytes()
    ws.initialize_project(root, "rop", DAY)
    assert (root / "README.md").read_bytes().startswith(original)
    text = readme(root)
    for heading in ws.CONTEXT_SECTIONS["vi"]:
        assert text.count(f"\n## {heading}\n") == 1
    ws.initialize_project(root, "rop", DAY)
    again = readme(root)
    for heading in ws.CONTEXT_SECTIONS["vi"]:
        assert again.count(f"\n## {heading}\n") == 1


def test_ambiguous_understanding_markers_refuse(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY)
    note = root / "README.md"
    duplicated = note.read_text(encoding="utf-8") + f"\n{ws.UNDERSTANDING_BEGIN}\nx\n{ws.UNDERSTANDING_END}\n"
    note.write_text(duplicated, encoding="utf-8")
    before_state = (root / ".medrs-project.json").read_bytes()
    with pytest.raises(ValueError, match="README_MARKERS_AMBIGUOUS"):
        ws.set_understanding(root, DAY, status="IN_PROGRESS")
    assert note.read_text(encoding="utf-8") == duplicated
    assert (root / ".medrs-project.json").read_bytes() == before_state


def test_v1_state_reads_as_not_started_and_upgrades(tmp_path):
    ws = api()
    root = tmp_path / "rop"
    write_v1_project(root)
    validate(state_of(root), SCHEMA)
    current = ws.read_understanding(root)
    assert current["workspace"] is True
    assert current["status"] == "NOT_STARTED"
    assert set(current["parts"].values()) == {"NOT_STARTED"}
    ws.initialize_project(root, "rop", DAY)
    ws.set_understanding(root, DAY, part="background", part_state="EXPLAINED")
    upgraded = state_of(root)
    assert upgraded["schema_version"] == "1.1.0"
    validate(upgraded, SCHEMA)


def test_read_understanding_without_workspace(tmp_path):
    current = api().read_understanding(tmp_path)
    assert current["workspace"] is False
    assert current["status"] == "NOT_STARTED"


def test_part_cannot_be_done_without_check_back(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY)
    result = ws.set_understanding(root, DAY, part="background", part_state="EXPLAINED")
    assert result["status"] == "IN_PROGRESS"
    with pytest.raises(ValueError, match="CHECK_BACK_REQUIRED"):
        ws.set_understanding(root, DAY, part="background", part_state="DONE")
    ws.set_understanding(root, DAY, part="background", part_state="CHECKED_BACK")
    result = ws.set_understanding(root, DAY, part="background", part_state="DONE")
    assert result["parts"]["background"] == "DONE"
    with pytest.raises(ValueError, match="UNKNOWN_PART"):
        ws.set_understanding(root, DAY, part="ethics", part_state="EXPLAINED")
    with pytest.raises(ValueError, match="UNKNOWN_PART_STATE"):
        ws.set_understanding(root, DAY, part="question", part_state="FINISHED")


def test_confirm_requires_all_parts_done(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY)
    for part in ("background", "question", "methods"):
        advance(ws, root, part)
    with pytest.raises(ValueError, match="PARTS_NOT_DONE"):
        ws.set_understanding(root, DAY, status="CONFIRMED", confirmation="Tôi đã hiểu rõ")
    assert ws.read_understanding(root)["status"] == "IN_PROGRESS"


def test_confirm_requires_author_words(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY)
    for part in ws.PARTS:
        advance(ws, root, part)
    with pytest.raises(ValueError, match="AUTHOR_CONFIRMATION_REQUIRED"):
        ws.set_understanding(root, DAY, status="CONFIRMED", confirmation="  ")
    result = ws.set_understanding(root, DAY, status="CONFIRMED", confirmation="Tôi đã hiểu rõ")
    assert result["status"] == "CONFIRMED"
    assert result["confirmed_on"] == DAY
    text = readme(root)
    block = text[text.index(ws.UNDERSTANDING_BEGIN):text.index(ws.UNDERSTANDING_END)]
    assert "CONFIRMED" in block and "Tôi đã hiểu rõ" in block
    events = (root / f"history/{DAY}/events.jsonl").read_text(encoding="utf-8")
    assert "UNDERSTANDING_CONFIRMED" in events
    assert "Tôi đã hiểu rõ" not in events
    validate(state_of(root), SCHEMA)


def test_defer_is_recorded(tmp_path):
    ws = api()
    root = tmp_path / "p"
    ws.initialize_project(root, "p", DAY)
    ws.set_understanding(root, DAY, part="background", part_state="EXPLAINED")
    result = ws.set_understanding(root, DAY, status="DEFERRED_BY_AUTHOR", open_items=2)
    assert result["status"] == "DEFERRED_BY_AUTHOR"
    assert result["parts"]["background"] == "EXPLAINED"
    assert result["open_items"] == 2
    with pytest.raises(ValueError, match="UNKNOWN_UNDERSTANDING_STATE"):
        ws.set_understanding(root, DAY, status="DONE")
