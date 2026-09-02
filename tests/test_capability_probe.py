import json
import subprocess
import sys
from pathlib import Path

from medical_research_skills_vn.capabilities import probe_capabilities


ROOT = Path(__file__).parents[1]


def test_probe_never_advertises_an_unlocated_backend():
    result = probe_capabilities(
        platform_name="Windows",
        locate=lambda _name: None,
        module_available=lambda _name: False,
    )

    assert result["r"]["available"] is False
    assert result["stata"]["available"] is False
    assert result["libreoffice_uno"]["available"] is False
    assert result["word_com"]["available"] is False


def test_word_com_requires_windows_and_its_python_bridge():
    locate = lambda name: "C:/Program Files/R/Rscript.exe" if name == "Rscript" else None
    modules = lambda name: name in {"win32com", "docx"}

    windows = probe_capabilities("Windows", locate, modules)
    linux = probe_capabilities("Linux", locate, modules)

    assert windows["word_com"]["available"] is True
    assert linux["word_com"]["available"] is False
    assert windows["r"]["available"] is True


def test_capability_probe_cli_emits_machine_readable_json():
    completed = subprocess.run(
        [sys.executable, "scripts/capability_probe.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert "execution_surface" in json.loads(completed.stdout)
