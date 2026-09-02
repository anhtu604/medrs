from pathlib import Path
import sys
from datetime import date

import yaml

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.budgets import validate_context_budget  # noqa: E402
from medical_research_skills_vn.coverage import validate_coverage_manifests  # noqa: E402
from medical_research_skills_vn.ethics import validate_source_registers  # noqa: E402
from medical_research_skills_vn.indexing import build_index, validate_reference_callers  # noqa: E402
from medical_research_skills_vn.inventory import validate_inventory  # noqa: E402
from medical_research_skills_vn.profiles import validate_profiles  # noqa: E402
from medical_research_skills_vn.structure import validate_shared_preflight  # noqa: E402


def main() -> int:
    mapping = ROOT / "skills/co-van/references/legacy-skill-map.yaml"
    legacy_names: set[str] = set()
    if mapping.exists():
        legacy_names = set((yaml.safe_load(mapping.read_text(encoding="utf-8")) or {}).get("legacy", {}))
    structural_issues = (
        validate_context_budget(ROOT, legacy_names)
        + validate_inventory(ROOT)
        + validate_shared_preflight(ROOT)
        + validate_reference_callers(ROOT)
        + validate_profiles(ROOT, date.today())
        + validate_coverage_manifests(ROOT)
    )
    index_path = ROOT / "skills/index.json"
    if not index_path.exists():
        from medical_research_skills_vn.budgets import ValidationIssue

        structural_issues.append(ValidationIssue("SKILL_INDEX_MISSING", str(index_path), "run build_index.py"))
    else:
        import json

        if json.loads(index_path.read_text(encoding="utf-8")) != build_index(ROOT):
            from medical_research_skills_vn.budgets import ValidationIssue

            structural_issues.append(ValidationIssue("SKILL_INDEX_DRIFT", str(index_path), "run build_index.py"))
    source_issues = validate_source_registers(ROOT, date.today())
    for issue in structural_issues:
        print(f"{issue.code}: {issue.path}: {issue.message}")
    for issue in source_issues:
        print(f"{issue.code}: {issue.source_id}: {issue.message}")
    if structural_issues or source_issues:
        return 1
    print("Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
