"""Explicit synthetic provenance for mechanical Word unit tests, never official acceptance."""
from hashlib import sha256
from pathlib import Path

from medical_research_skills_vn.structure_profiles import load_structure_profile


def load_test_profile(path):
    profile = load_structure_profile(path)
    source = Path(__file__).parent / "fixtures/profiles/synthetic-layout-source.txt"
    profile.update({
        "profile_id": "synthetic-mechanics-only", "source_path": str(source.resolve()),
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "source_version": "synthetic fixture", "last_verified": "2026-10-11",
        "semantic_rules": [{"id": "fixture", "source_locator": "TEXT:Synthetic rules", "summary": "Unit-test fixture only"}],
    })
    return profile
