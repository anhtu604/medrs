from copy import deepcopy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/ho-so-nghien-cuu/scripts"))


def api():
    import data_provenance
    return data_provenance


def confirmed():
    return {"confirmed": True, "data_updated_to_real": True, "author": "author", "timestamp": "2026-10-11"}


def test_author_confirmation_not_independent_verification():
    report = api().transition_data_state({"state": "SIMULATED", "digest": "a"}, {"digest": "b", "replacement_received": True}, confirmed())
    assert report["state"] == "AUTHOR_DECLARED_REAL"
    assert report["author_recheck_required"] is True
    assert report["remove_current_simulation_labels"] is True
    assert report["history_preserved"] is True


@pytest.mark.parametrize("decision,replacement", [({}, {"digest": "b", "replacement_received": True}), (confirmed(), {"digest": "b", "replacement_received": False})])
def test_no_transition_without_confirmation_and_replacement(decision, replacement):
    report = api().transition_data_state({"state": "SIMULATED", "digest": "a"}, replacement, decision)
    assert report["state"] == "SIMULATED"
    assert report["remove_current_simulation_labels"] is False


def test_explicit_still_simulated_preserves_current_label():
    report = api().transition_data_state({"state": "SIMULATED", "digest": "a"}, {"digest": "b", "replacement_received": True}, {**confirmed(), "still_simulated": True})
    assert report["state"] == "SIMULATED"
    assert report["remove_current_simulation_labels"] is False


def test_identical_values_require_resolution_not_accusation():
    report = api().transition_data_state({"state": "SIMULATED", "digest": "same"}, {"digest": "same", "replacement_received": True}, confirmed())
    assert report["state"] == "UNRESOLVED"
    assert report["remove_current_simulation_labels"] is False
    assert "SAME_VALUES_REQUIRE_REVIEW" in report["qualifications"]
    assert report["author_declaration"] == "REAL_UPDATED"


def test_partial_replacement_does_not_relabel_whole_dataset():
    report = api().transition_data_state({"state": "SIMULATED", "digest": "a"}, {"digest": "b", "replacement_received": True, "partial": True}, confirmed())
    assert report["state"] == "UNRESOLVED"
    assert report["remove_current_simulation_labels"] is False


def test_verified_receipt_is_bound_to_replacement_digest():
    replacement = {"digest": "b", "replacement_received": True, "verification": {"status": "PASS", "digest": "old", "reviewer": "independent"}}
    assert api().transition_data_state({"state": "SIMULATED", "digest": "a"}, replacement, confirmed())["state"] == "AUTHOR_DECLARED_REAL"
    replacement["verification"]["digest"] = "b"
    assert api().transition_data_state({"state": "SIMULATED", "digest": "a"}, replacement, confirmed())["state"] == "VERIFIED_REAL"


def test_previous_state_is_immutable_and_lineage_retained():
    previous = {"state": "SIMULATED", "digest": "a", "history": [{"state": "SIMULATED"}]}
    old = deepcopy(previous)
    result = api().transition_data_state(previous, {"digest": "b", "replacement_received": True}, confirmed())
    assert previous == old
    assert result["history"][-1]["previous_digest"] == "a"


def test_reordering_keeps_fingerprint_duplicate_rows_do_not():
    rows = [{"age": 20, "group": "A"}, {"age": 30, "group": "B"}]
    key = b"private-local-key-32-bytes-minimum"
    first = api().fingerprint_records(rows, ["age", "group"], key)
    second = api().fingerprint_records(list(reversed(rows)), ["group", "age"], key)
    assert first == second
    assert first != api().fingerprint_records(rows + [rows[0]], ["age", "group"], key)
    assert first != api().fingerprint_records(rows, ["age", "group"], b"another-private-local-key-32bytes")


@pytest.mark.parametrize("rows,columns,key", [([], ["age"], b"x" * 32), ([{"age": 20}], ["missing"], b"x" * 32), ([{"age": float('nan')}], ["age"], b"x" * 32), ([{"age": 20}], ["age"], b"short")])
def test_bad_fingerprint_inputs_not_silently_normalized(rows, columns, key):
    with pytest.raises(ValueError):
        api().fingerprint_records(rows, columns, key)
