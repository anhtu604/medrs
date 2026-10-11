"""Repository adapter to the portable, single-source MedRS router."""
import sys
from pathlib import Path

_scripts = Path(__file__).parents[2] / "skills/medrs/scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))
from router import RoutingDecision, RoutingRequest, route_plan, route_request  # noqa: E402,F401
