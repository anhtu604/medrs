import json
import shutil
import subprocess
from pathlib import Path

from medical_research_skills_vn.installer import validate_install_source


ROOT = Path(__file__).parents[1]
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")


def _run(script, *args):
    return subprocess.run(
        [POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / script), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_source_validator_requires_exactly_twenty_four_indexed_skills(tmp_path):
    assert validate_install_source(ROOT)["status"] == "VALID"
    broken = tmp_path / "broken"
    (broken / "skills/only-one").mkdir(parents=True)
    (broken / "skills/only-one/SKILL.md").write_text("---\nname: only-one\ndescription: x\n---\n", encoding="utf-8")
    assert validate_install_source(broken)["status"] == "INVALID"


def test_local_installer_supports_all_targets_and_paths_with_spaces(tmp_path):
    user_root = tmp_path / "User Profile With Spaces"
    result = _run(
        "install.ps1",
        "-SourceRoot", ROOT,
        "-UserRoot", user_root,
        "-Targets", "codex,claude,generic",
        "-Quiet",
        "-VersionRef", "test-ref",
    )
    assert result.returncode == 0, result.stderr + result.stdout
    for host in (".codex", ".claude", ".agents"):
        host_root = user_root / host
        assert len(list((host_root / "skills").glob("*/SKILL.md"))) == 24
        support = host_root / "medical-research-skills-vn"
        assert (support / "coverage/rob2-parallel-2019.yaml").is_file()
        assert (support / "profiles/institution/hmu/word-format-master-2020-current-2026.yaml").is_file()
        manifest = json.loads((host_root / "medical-research-skills-vn.install.json").read_text(encoding="utf-8-sig"))
        assert manifest["version_ref"] == "test-ref"
        assert len(manifest["skills"]) == 24


def test_failed_source_validation_does_not_replace_existing_install(tmp_path):
    user_root = tmp_path / "user"
    first = _run("install.ps1", "-SourceRoot", ROOT, "-UserRoot", user_root, "-Targets", "codex", "-Quiet")
    assert first.returncode == 0
    marker = user_root / ".codex/skills/co-van/user-marker.txt"
    marker.write_text("preserve", encoding="utf-8")
    broken = tmp_path / "broken"
    broken.mkdir()
    failed = _run("install.ps1", "-SourceRoot", broken, "-UserRoot", user_root, "-Targets", "codex", "-Quiet")
    assert failed.returncode != 0
    assert marker.read_text(encoding="utf-8") == "preserve"


def test_uninstaller_removes_only_manifest_owned_paths(tmp_path):
    user_root = tmp_path / "user"
    assert _run("install.ps1", "-SourceRoot", ROOT, "-UserRoot", user_root, "-Targets", "codex", "-Quiet").returncode == 0
    unrelated = user_root / ".codex/skills/my-own-skill/SKILL.md"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("mine", encoding="utf-8")
    removed = _run("uninstall.ps1", "-UserRoot", user_root, "-Targets", "codex", "-Quiet")
    assert removed.returncode == 0, removed.stderr + removed.stdout
    assert unrelated.is_file()
    assert not (user_root / ".codex/skills/co-van").exists()


def test_doctor_detects_complete_and_tampered_install(tmp_path):
    user_root = tmp_path / "user"
    assert _run("install.ps1", "-SourceRoot", ROOT, "-UserRoot", user_root, "-Targets", "codex", "-Quiet").returncode == 0
    healthy = _run("doctor.ps1", "-UserRoot", user_root, "-Targets", "codex", "-Quiet")
    assert healthy.returncode == 0, healthy.stderr + healthy.stdout
    (user_root / ".codex/skills/co-van/SKILL.md").unlink()
    broken = _run("doctor.ps1", "-UserRoot", user_root, "-Targets", "codex", "-Quiet")
    assert broken.returncode != 0


def test_web_bootstrap_is_repo_parameterized_and_supports_checksum_pin():
    text = (ROOT / "install/web.ps1").read_text(encoding="utf-8")
    assert "anhtu604/medrs" in text
    assert "MEDICAL_RESEARCH_SKILLS_REPO" in text
    assert "ArchiveSha256" in text
    assert "-UserRoot $UserRoot" in text
    assert "Get-FileHash" in text
    assert "finally" in text
