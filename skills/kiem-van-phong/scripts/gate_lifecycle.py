"""Select audit scope; this function does not perform or certify an audit."""


def required_gate_scope(mode: str, changed_sections: list[str]) -> dict:
    if mode == "assembled":
        return {"full": ["document"], "local": [], "consistency": True}
    if mode not in {"revision", "standalone"}:
        raise ValueError("Unknown writing mode")
    if not changed_sections or any(not isinstance(s, str) or not s.strip() for s in changed_sections):
        raise ValueError("Explicit section scope required")
    sections = sorted(set(changed_sections))
    if mode == "revision":
        return {"full": [], "local": sections, "consistency": True}
    return {"full": sections, "local": [], "consistency": False}
