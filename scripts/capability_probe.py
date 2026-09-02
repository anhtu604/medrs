import json
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from medical_research_skills_vn.capabilities import probe_capabilities  # noqa: E402


if __name__ == "__main__":
    print(json.dumps(probe_capabilities(), ensure_ascii=False, indent=2))
