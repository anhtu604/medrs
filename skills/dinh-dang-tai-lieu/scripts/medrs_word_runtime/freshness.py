"""Source freshness calculations."""

from datetime import date


def verification_status(record: dict, as_of: date) -> str:
    raw = record.get("last_verified")
    if not raw:
        return "UNVERIFIED"
    try:
        verified = date.fromisoformat(raw)
        ttl = record["expires_after_days"]
        if isinstance(ttl, bool) or not isinstance(ttl, int) or ttl <= 0:
            return "UNVERIFIED"
        expires_after_days = ttl
    except (KeyError, TypeError, ValueError):
        return "UNVERIFIED"
    if verified > as_of:
        return "UNVERIFIED"
    return "CURRENT" if (as_of - verified).days <= expires_after_days else "STALE"
