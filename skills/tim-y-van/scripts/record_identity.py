"""Conservative portable record normalization, retaining source disagreements."""
from copy import deepcopy
from datetime import date
import re
import unicodedata


def normalize_doi(value):
    if not value:
        return None
    value = str(value).strip().casefold()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    value = re.sub(r"^doi:\s*", "", value).strip()
    return value or None


def record_key(record):
    doi = normalize_doi(record.get("doi"))
    if doi:
        return "doi:" + doi
    if record.get("pmid"):
        return "pmid:" + str(record["pmid"]).strip()
    title = unicodedata.normalize("NFC", str(record.get("title") or "")).casefold()
    title = re.sub(r"\W+", " ", title).strip()
    if not title:
        return None
    return f"title-year:{title}:{record.get('year', '')}"


def _date(check):
    try:
        return date.fromisoformat(check["checked_at"])
    except (KeyError, TypeError, ValueError):
        return date.min


def deduplicate_records(records):
    merged = {}
    for ordinal, original in enumerate(records):
        record = deepcopy(original)
        if record.get("doi"):
            record["doi"] = normalize_doi(record["doi"])
        key = record_key(record) or ("unresolved", ordinal)
        routes = list(record.pop("discovery_routes", []))
        route = record.pop("discovered_by", None)
        if route:
            routes.append(route)
        checks = list(record.pop("publication_status_history", []))
        check = record.pop("publication_status_check", None)
        if check:
            checks.append(check)
        if key not in merged:
            merged[key] = record | {"discovery_routes": []}
        target = merged[key]
        for route in routes:
            if route not in target["discovery_routes"]:
                target["discovery_routes"].append(route)
        for field, value in record.items():
            if not target.get(field) and value:
                target[field] = value
        if checks:
            history = target.setdefault("publication_status_history", [])
            for check in checks:
                if check not in history:
                    history.append(check)
            dated = [c for c in history if _date(c) != date.min and c.get("source")]
            if not dated:
                target["publication_status_check"] = {
                    "status": "unresolved", "source": "deduplication", "checked_at": ""}
            else:
                latest_date = max(_date(c) for c in dated)
                latest = [c for c in dated if _date(c) == latest_date]
                target["publication_status_check"] = deepcopy(latest[-1])
                if len({c.get("status") for c in latest}) != 1:
                    target["publication_status_check"]["status"] = "unresolved"
                    target["publication_status_conflict"] = True
    return list(merged.values())
