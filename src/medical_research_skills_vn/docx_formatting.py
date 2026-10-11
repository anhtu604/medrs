"""Thin repository adapter; canonical implementation ships inside the Word skill."""
import importlib
from pathlib import Path
import sys

_scripts = Path(__file__).parents[2] / "skills/dinh-dang-tai-lieu/scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))
sys.modules[__name__] = importlib.import_module("medrs_word_runtime.docx_formatting")
