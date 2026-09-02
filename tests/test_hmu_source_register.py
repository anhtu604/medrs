import hashlib
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
REGISTER = ROOT / "sources/hmu/source-register.yaml"


def test_hmu_register_separates_acquisition_from_slice_four_encoding():
    register = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))

    assert register["acquisition_due"] == "2026-09-30"
    assert register["encoding_status"] == "DEFERRED_TO_SLICE_4"
    assert register["encoding_acceptance_gate"] == "slice-4"
    assert register["sources"]


def test_hmu_sources_have_public_provenance_without_redistributed_snapshots():
    register = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))

    for source in register["sources"]:
        snapshot = ROOT / source["snapshot_path"]
        assert source["source_url"].startswith("https://sdh.hmu.edu.vn/")
        assert len(source["sha256"]) == 64
        assert source["redistribution"] == "PROHIBITED_OR_UNKNOWN"
        if snapshot.exists():
            digest = hashlib.sha256(snapshot.read_bytes()).hexdigest().upper()
            assert digest == source["sha256"]


def test_hmu_register_records_the_current_official_presentation_source():
    register = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))

    assert register["presentation_rule_status"] == "AUTHORITATIVE_ACCESS_CONFIRMED"
    assert register["status"] == "AUTHORITATIVE_PRESENTATION_SOURCE_ACQUIRED"
    presentation_sources = [
        source for source in register["sources"]
        if source["scope"] == "thesis-presentation-format"
    ]
    assert len(presentation_sources) == 1

    source = presentation_sources[0]
    assert source["official_page"] == (
        "https://sdh.hmu.edu.vn/news/"
        "tID12202_quy-trinh-va-bieu-mau-dung-cho-bao-ve-luan-van-"
        "sau-dai-hoc-cap-nhat-nam-2026.html"
    )
    assert source["source_url"] == (
        "https://sdh.hmu.edu.vn/images/"
        "9_%20Yeu%20cau%20luan%20van_2020%281%29.docx"
    )
    assert source["verification_status"] == "CURRENT"
    assert not (ROOT / "sources/hmu/BLOCKED.md").exists()
