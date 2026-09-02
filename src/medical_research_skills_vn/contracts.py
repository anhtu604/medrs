"""Machine-readable ownership boundaries between canonical skills."""

from pathlib import Path

import yaml


def load_contract(root, skill_name):
    path = Path(root) / "skills" / skill_name / "references/contract.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def planning_decision(contract, requested_action):
    if requested_action in set(contract.get("forbidden_actions", [])):
        return "REFUSE_AND_EXPLAIN"
    normalized = requested_action.removeprefix("define_")
    if normalized in set(contract.get("owns", [])):
        return "ALLOW"
    return "HANDOFF_REQUIRED"
