"""Resolve Zotero item keys read-only against the author's zotero.sqlite."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

CSL_TYPES = {
    "journalArticle": "article-journal",
    "book": "book",
    "bookSection": "chapter",
    "thesis": "thesis",
    "report": "report",
    "conferencePaper": "paper-conference",
    "webpage": "webpage",
}

# Only roles with a direct CSL name are emitted. In particular, Zotero's
# contributor role must not be silently promoted to author.
CSL_CREATOR_ROLES = {"author", "editor", "translator"}


@dataclass(frozen=True)
class ZoteroItem:
    key: str
    item_id: int
    uri: str
    csl: dict


def open_library(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(Path(db_path).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)


def _account(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM settings WHERE setting = 'account' AND key = ?", (key,)).fetchone()
    return str(row[0]) if row and row[0] not in (None, "") else None


def _uri_prefix(conn: sqlite3.Connection, library_id: int) -> str | None:
    kind = conn.execute("SELECT type FROM libraries WHERE libraryID = ?", (library_id,)).fetchone()
    if kind is None:
        return None
    if kind[0] == "group":
        group = conn.execute('SELECT groupID FROM "groups" WHERE libraryID = ?', (library_id,)).fetchone()
        if group is None:
            return None
        return f"http://zotero.org/groups/{group[0]}"
    if kind[0] != "user":
        return None
    user_id = _account(conn, "userID")
    if user_id:
        return f"http://zotero.org/users/{user_id}"
    local_key = _account(conn, "localUserKey")
    if local_key is None:
        return None
    return f"http://zotero.org/users/local/{local_key}"


def _field(conn: sqlite3.Connection, item_id: int, name: str) -> str | None:
    row = conn.execute(
        """SELECT v.value FROM itemData d
           JOIN fields f ON f.fieldID = d.fieldID
           JOIN itemDataValues v ON v.valueID = d.valueID
           WHERE d.itemID = ? AND f.fieldName = ?""",
        (item_id, name),
    ).fetchone()
    return str(row[0]) if row else None


def _creators(conn: sqlite3.Connection, item_id: int) -> dict[str, list[dict]]:
    rows = conn.execute(
        """SELECT ct.creatorType, c.lastName, c.firstName FROM itemCreators ic
           JOIN creators c ON c.creatorID = ic.creatorID
           JOIN creatorTypes ct ON ct.creatorTypeID = ic.creatorTypeID
           WHERE ic.itemID = ? ORDER BY ic.orderIndex""",
        (item_id,),
    ).fetchall()
    creators: dict[str, list[dict]] = {}
    for role, last, first in rows:
        if role not in CSL_CREATOR_ROLES or not last:
            continue
        creators.setdefault(role, []).append({"family": last, "given": first} if first else {"literal": last})
    return creators


def resolve_items(db_path: Path, keys: list[str]) -> tuple[list[ZoteroItem], list[str]]:
    conn = open_library(db_path)
    found: list[ZoteroItem] = []
    missing: list[str] = []
    try:
        for key in keys:
            rows = conn.execute(
                """SELECT i.itemID, i.libraryID, t.typeName FROM items i
                   JOIN itemTypes t ON t.itemTypeID = i.itemTypeID
                   WHERE i.key = ? AND i.itemID NOT IN (SELECT itemID FROM deletedItems)""",
                (key,),
            ).fetchall()
            if len(rows) != 1:
                missing.append(key)
                continue
            item_id, library_id, type_name = rows[0]
            uri_prefix = _uri_prefix(conn, library_id)
            if uri_prefix is None:
                missing.append(key)
                continue
            csl: dict = {"id": item_id, "type": CSL_TYPES.get(type_name, "article")}
            title = _field(conn, item_id, "title")
            journal = _field(conn, item_id, "publicationTitle")
            date = _field(conn, item_id, "date")
            creators = _creators(conn, item_id)
            if title:
                csl["title"] = title
            if journal:
                csl["container-title"] = journal
            csl.update(creators)
            if date and date[:4].isdigit():
                csl["issued"] = {"date-parts": [[int(date[:4])]]}
            found.append(ZoteroItem(key=key, item_id=item_id, uri=f"{uri_prefix}/items/{key}", csl=csl))
    finally:
        conn.close()
    return found, missing
