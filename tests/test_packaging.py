import zipfile
from pathlib import Path

from medical_research_skills_vn.packaging import build_cowork_package, build_package


ROOT = Path(__file__).parents[1]


def test_package_contains_only_active_skill_roots_and_no_v1(tmp_path):
    package = build_package(ROOT, tmp_path / "plugin.zip")
    with zipfile.ZipFile(package) as bundle:
        names = set(bundle.namelist())

    skill_roots = {name.split("/")[1] for name in names if name.startswith("skills/") and name.count("/") >= 2}
    skill_roots.discard("index.json")
    present = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    assert skill_roots == present
    assert not any(name.startswith("archive/") for name in names)
    assert not any("sources/hmu/snapshots/" in name for name in names)


def test_package_is_byte_reproducible(tmp_path):
    import hashlib
    first = build_package(ROOT, tmp_path / "first.zip")
    second = build_package(ROOT, tmp_path / "second.zip")

    assert hashlib.sha256(first.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest()


def test_cowork_package_is_minimal_complete_and_reproducible(tmp_path):
    import hashlib
    first = build_cowork_package(ROOT, tmp_path / "medrs-first.zip")
    second = build_cowork_package(ROOT, tmp_path / "medrs-second.zip")
    with zipfile.ZipFile(first) as bundle:
        names = set(bundle.namelist())

    assert ".claude-plugin/plugin.json" in names
    assert ".claude-plugin/marketplace.json" in names
    assert "skills/index.json" in names
    assert len({name.split("/")[1] for name in names if name.startswith("skills/") and name.endswith("/SKILL.md")}) == 24
    assert any(name.startswith("coverage/") for name in names)
    assert any(name.startswith("profiles/") for name in names)
    assert any(name.startswith("schemas/") for name in names)
    assert not any(name.startswith(("tests/", "src/", "scripts/", "archive/", "sources/")) for name in names)
    assert hashlib.sha256(first.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest()
