"""Read a Zotero library: item keys, PDF attachments and collections from a copy of zotero.sqlite,
and citation data from a CSL JSON export (Better BibTeX auto-export or Zotero's Export Library)."""
from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import tempfile
import unicodedata
from typing import Dict, List, Optional


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", strip_accents(s).lower())


def norm_title(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", strip_accents(s).lower())).strip()


def norm_doi(d: str) -> str:
    d = (d or "").strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d)
    d = re.sub(r"\.pdf$", "", d)
    return d


class Item:
    def __init__(self, key, itype, fields, creators, deleted=False, collections=None, attachments=None):
        self.key = key
        self.itype = itype
        self.fields: Dict[str, str] = fields
        self.creators = creators  # list of (last, first, fieldMode, creatorType)
        self.deleted = deleted
        self.collections: List[str] = collections or []
        self.attachments = attachments or []  # list of (key, contentType)
        self.csl: Optional[dict] = None
        self.citekey: str = fields.get("citationKey", "")

    @property
    def title(self) -> str:
        return self.fields.get("title", "") or (self.csl or {}).get("title", "")

    @property
    def year(self) -> str:
        m = re.search(r"(\d{4})", self.fields.get("date", ""))
        if m:
            return m.group(1)
        dp = ((self.csl or {}).get("issued") or {}).get("date-parts")
        return str(dp[0][0]) if dp and dp[0] and dp[0][0] else ""

    @property
    def doi(self) -> str:
        return norm_doi(self.fields.get("DOI") or (self.csl or {}).get("DOI", ""))

    @property
    def pdf_key(self) -> str:
        for k, ct in self.attachments:
            if ct == "application/pdf":
                return k
        return ""

    @property
    def authors(self) -> List[str]:
        out = [c for c in self.creators if len(c) < 4 or c[3] in ("author", "")]
        return [(c[0] if c[2] == 1 else c[0]) for c in out] or [
            a.get("family") or a.get("literal", "") for a in (self.csl or {}).get("author", [])
        ]

    @property
    def author_names(self) -> str:
        out = []
        for c in self.creators:
            if len(c) >= 4 and c[3] not in ("author", ""):
                continue
            out.append(c[0] if c[2] == 1 else (c[1] + " " + c[0]).strip())
        if not out:
            for a in (self.csl or {}).get("author", []):
                out.append(a.get("literal") or (a.get("given", "") + " " + a.get("family", "")).strip())
        return ", ".join(out)

    def field(self, name: str) -> str:
        return self.fields.get(name, "")


_TYPE = {
    "journalArticle": "article-journal", "book": "book", "bookSection": "chapter",
    "conferencePaper": "paper-conference", "report": "report", "preprint": "article",
    "webpage": "webpage", "thesis": "thesis", "newspaperArticle": "article-newspaper",
    "magazineArticle": "article-magazine", "videoRecording": "motion_picture",
}


def csl_from_item(it: Item) -> dict:
    f = it.fields
    e = {"id": it.citekey or it.key, "type": _TYPE.get(it.itype, "document"), "title": f.get("title", "")}
    cont = f.get("publicationTitle") or f.get("bookTitle") or f.get("proceedingsTitle") or f.get("websiteTitle")
    if cont:
        e["container-title"] = cont
    for src, dst in (("volume", "volume"), ("issue", "issue"), ("pages", "page"), ("DOI", "DOI"),
                     ("url", "URL"), ("publisher", "publisher"), ("edition", "edition")):
        if f.get(src):
            e[dst] = f[src]
    m = re.search(r"(\d{4})(?:-(\d{2}))?", f.get("date", ""))
    if m:
        e["issued"] = {"date-parts": [[int(x) for x in m.groups() if x and x != "00"]]}
    au = []
    for c in it.creators:
        if len(c) >= 4 and c[3] != "author":
            continue
        au.append({"literal": c[0]} if c[2] == 1 else {"family": c[0], "given": c[1]})
    if au:
        e["author"] = au
    return e


class Library:
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self.att_parent: Dict[str, str] = {}
        self.csl: List[dict] = []
        self.has_sqlite = False
        self.by_doi: Dict[str, List[Item]] = {}
        self.by_family: Dict[str, List[Item]] = {}
        self.token_index: Dict[str, List[Item]] = {}

    # ------------------------------------------------------------------
    @classmethod
    def load(cls, sqlite_path: str = "", csl_path: str = "", bbt_path: str = "") -> "Library":
        lib = cls()
        if csl_path and os.path.exists(csl_path):
            with open(csl_path, encoding="utf-8") as fh:
                data = json.load(fh)
            lib.csl = data["items"] if isinstance(data, dict) and "items" in data else data
        if sqlite_path and os.path.exists(sqlite_path):
            lib._load_sqlite(sqlite_path, bbt_path)
            lib.has_sqlite = True
        lib._attach_csl()
        lib._build_indexes()
        return lib

    def _load_sqlite(self, path: str, bbt_path: str = ""):
        tmp = tempfile.mkdtemp(prefix="coursenotes-")
        dst = os.path.join(tmp, "z.sqlite")
        shutil.copy2(path, dst)
        if os.path.exists(path + "-journal"):  # a hot journal rolls back in the copy only
            shutil.copy2(path + "-journal", dst + "-journal")
        con = sqlite3.connect(dst)
        try:
            lib_row = con.execute("SELECT libraryID FROM libraries WHERE type='user'").fetchone()
            lib_id = lib_row[0] if lib_row else 1
            rows = con.execute(
                "SELECT i.itemID, i.key, t.typeName FROM items i JOIN itemTypes t USING(itemTypeID) "
                "WHERE i.libraryID=? AND t.typeName NOT IN ('attachment','note','annotation')", (lib_id,)
            ).fetchall()
            ids = {r[0]: r for r in rows}
            fields: Dict[int, dict] = {}
            for iid, fname, val in con.execute(
                "SELECT d.itemID, f.fieldName, v.value FROM itemData d JOIN fields f USING(fieldID) "
                "JOIN itemDataValues v USING(valueID)"
            ):
                if iid in ids:
                    fields.setdefault(iid, {})[fname] = val
            creators: Dict[int, list] = {}
            for iid, last, first, mode, ctype in con.execute(
                "SELECT ic.itemID, c.lastName, c.firstName, c.fieldMode, ct.creatorType FROM itemCreators ic "
                "JOIN creators c USING(creatorID) JOIN creatorTypes ct USING(creatorTypeID) "
                "ORDER BY ic.itemID, ic.orderIndex"
            ):
                if iid in ids:
                    creators.setdefault(iid, []).append((last or "", first or "", mode or 0, ctype))
            deleted = set(r[0] for r in con.execute("SELECT itemID FROM deletedItems"))
            colls: Dict[int, list] = {}
            for iid, name in con.execute(
                "SELECT ci.itemID, c.collectionName FROM collectionItems ci JOIN collections c USING(collectionID)"
            ):
                if iid in ids:
                    colls.setdefault(iid, []).append(name)
            atts: Dict[int, list] = {}
            for parent, akey, ctype, aid in con.execute(
                "SELECT a.parentItemID, i.key, a.contentType, i.itemID FROM itemAttachments a "
                "JOIN items i ON i.itemID=a.itemID WHERE a.parentItemID IS NOT NULL"
            ):
                if aid in deleted or parent not in ids:
                    continue
                atts.setdefault(parent, []).append((akey, ctype or ""))
            for iid, (_, key, typ) in ids.items():
                it = Item(key, typ, fields.get(iid, {}), creators.get(iid, []), iid in deleted,
                          colls.get(iid, []), atts.get(iid, []))
                self.items[key] = it
                for akey, _ in it.attachments:
                    self.att_parent[akey] = key
        finally:
            con.close()
            shutil.rmtree(tmp, ignore_errors=True)
        self.bbt: Dict[str, str] = {}
        if bbt_path and os.path.exists(bbt_path):
            tmp = tempfile.mkdtemp(prefix="coursenotes-")
            dst = os.path.join(tmp, "bbt.sqlite")
            shutil.copy2(bbt_path, dst)
            try:
                c2 = sqlite3.connect(dst)
                self.bbt = dict(c2.execute("SELECT itemKey, citationKey FROM citationkey").fetchall())
                c2.close()
            except sqlite3.Error:
                pass
            shutil.rmtree(tmp, ignore_errors=True)

    def _attach_csl(self):
        by_id = {e["id"]: e for e in self.csl}
        by_doi: Dict[str, list] = {}
        by_title: Dict[tuple, list] = {}
        for e in self.csl:
            d = norm_doi(e.get("DOI", ""))
            if d:
                by_doi.setdefault(d, []).append(e)
            dp = (e.get("issued") or {}).get("date-parts") or [[""]]
            by_title.setdefault((norm_title(e.get("title", "")), str(dp[0][0]) if dp[0] else ""), []).append(e)
        if not self.items:  # CSL only: build pseudo-items so everything downstream still works
            for e in self.csl:
                it = Item("", e.get("type", ""), {"title": e.get("title", ""), "DOI": e.get("DOI", ""),
                                                  "citationKey": e["id"]}, [])
                it.csl = e
                it.creators = [((a.get("literal") or a.get("family", "")), a.get("given", ""),
                                1 if a.get("literal") else 0, "author") for a in e.get("author", [])]
                self.items["csl:" + e["id"]] = it
            return
        bbt = getattr(self, "bbt", {})
        for it in self.items.values():
            ck = it.fields.get("citationKey") or bbt.get(it.key, "")
            e = by_id.get(ck) if ck else None
            if e is None and it.doi and by_doi.get(it.doi):
                e = by_doi[it.doi][0]
            if e is None:
                cands = by_title.get((norm_title(it.title), it.year))
                if cands:
                    e = cands[0]
            if e is not None:
                it.csl = e
                if not it.citekey:
                    it.citekey = e["id"]
            else:
                it.csl = csl_from_item(it)

    def _build_indexes(self):
        for it in self.items.values():
            if it.doi:
                self.by_doi.setdefault(it.doi, []).append(it)
            for a in it.authors:
                self.by_family.setdefault(norm(a), []).append(it)
            for tok in set(norm_title(it.title).split()):
                if len(tok) >= 4:
                    self.token_index.setdefault(tok, []).append(it)

    # ------------------------------------------------------------------
    def resolve_key(self, key: str) -> Optional[Item]:
        if key in self.items:
            return self.items[key]
        parent = self.att_parent.get(key)
        return self.items.get(parent) if parent else None
