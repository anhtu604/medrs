"""Shared MedRS refresh lease; does not lock or modify Zotero itself."""
from contextlib import contextmanager
import hashlib
from pathlib import Path
import sys

_leader = Path(__file__).parents[3] / "skills/leader-nghien-cuu/scripts"
if str(_leader) not in sys.path:
    sys.path.insert(0, str(_leader))
from revision_guard import output_lease


@contextmanager
def citation_session(lock_root: Path, library_identity: str, owner: str):
    if not library_identity or not owner:
        raise ValueError("LIBRARY_AND_OWNER_REQUIRED")
    key = hashlib.sha256(library_identity.encode("utf-8")).hexdigest()
    with output_lease(Path(lock_root).resolve() / f".medrs-zotero-{key}", owner):
        yield
