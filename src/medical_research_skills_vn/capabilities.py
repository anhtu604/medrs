"""Evidence-based host capability detection."""

from importlib.util import find_spec
import platform
import shutil


def _first(locate, names):
    for name in names:
        path = locate(name)
        if path:
            return path
    return None


def probe_capabilities(platform_name=None, locate=shutil.which, module_available=None):
    platform_name = platform_name or platform.system()
    module_available = module_available or (lambda name: find_spec(name) is not None)
    r_path = _first(locate, ("Rscript", "R"))
    stata_path = _first(locate, ("stata-mp", "stata-se", "stata", "StataMP-64", "StataSE-64"))
    soffice_path = _first(locate, ("soffice", "libreoffice"))
    windows = platform_name.casefold() == "windows"
    return {
        "execution_surface": platform_name,
        "python_docx": {"available": bool(module_available("docx")), "evidence": "python module: docx"},
        "r": {"available": bool(r_path), "executable": r_path},
        "stata": {"available": bool(stata_path), "executable": stata_path},
        "word_com": {
            "available": bool(windows and module_available("win32com")),
            "evidence": "Windows + python module: win32com",
        },
        "libreoffice_uno": {
            "available": bool(soffice_path and module_available("uno")),
            "executable": soffice_path,
            "evidence": "soffice/libreoffice executable + python module: uno",
        },
    }
