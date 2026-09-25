import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
for extra in (ROOT / "src", ROOT / "skills/kiem-van-phong/scripts", ROOT / "skills/quan-ly-trich-dan/scripts"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

