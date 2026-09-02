"""Source freshness calculations."""

from datetime import date


def verification_status(record: dict, as_of: date) -> str:
    raw = record.get("last_verified")
    if not raw:
        return "UNVERIFIED"
    verified = date.fromisoformat(raw)
    expires_after_days = int(record["expires_after_days"])
    return "CURRENT" if (as_of - verified).days <= expires_after_days else "STALE"
