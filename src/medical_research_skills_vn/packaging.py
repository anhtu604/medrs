"""Reproducible secondary ZIP packaging."""

from pathlib import Path
import zipfile


ROOT_FILES = {
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "ATTRIBUTION.md",
    "CHANGELOG.md",
    "requirements.txt",
    "pyproject.toml",
}
ROOT_DIRS = {
    ".claude-plugin",
    "config",
    "docs",
    "profiles",
    "schemas",
    "scripts",
    "skills",
    "sources",
    "src",
}


def _included(relative: Path) -> bool:
    if relative.as_posix() in ROOT_FILES:
        return True
    if not relative.parts or relative.parts[0] not in ROOT_DIRS:
        return False
    text = relative.as_posix()
    if "__pycache__" in relative.parts or text.endswith((".pyc", ".pyo")):
        return False
    if text.startswith("sources/hmu/snapshots/"):
        return False
    return True


def build_package(root: Path, destination: Path) -> Path:
    root = Path(root)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    files = [path for path in root.rglob("*") if path.is_file() and _included(path.relative_to(root))]
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return destination
