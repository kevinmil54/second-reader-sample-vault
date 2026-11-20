"""Match syllabus readings to Zotero items (DOI first, then author/year/title)."""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from typing import List, Optional

from .zotero import Item, Library, norm, norm_doi, norm_title


@dataclass
class Match:
    reading: object
    item: Optional[Item] = None
    status: str = "none"  # locked | doi | fuzzy | none | locked-missing
    score: float = 0.0
    notes: List[str] = field(default_factory=list)
    alternatives: List[tuple] = field(default_factory=list)  # (item, score)


def title_sim(a: str, b: str) -> float:
    na, nb = norm_title(a), norm_title(b)
    if not na or not nb:
        return 0.0
    short, long_ = (na, nb) if len(na) <= len(nb) else (nb, na)
    if len(short) >= 15 and short in long_:
        return 0.95
    return difflib.SequenceMatcher(None, na, nb).ratio()


def _pref(it: Item, collections: List[str]):
    in_coll = bool(collections) and any(c in it.collections for c in collections)
    return (in_coll, bool(it.pdf_key), bool(it.doi), len(it.collections))


def _year_score(ry: str, iy: str) -> float:
    if not ry or not iy:
        return 0.5
    d = abs(int(ry) - int(iy))
    return 1.0 if d == 0 else (0.5 if d == 1 else 0.0)


def match_reading(r, lib: Library, collections: List[str], use_locks: bool = True) -> Match:
    m = Match(reading=r)
    if use_locks and (r.locked_key or r.locked_att):
        it = lib.resolve_key(r.locked_key or r.locked_att)
        if it is None:
            m.status = "locked-missing"
            m.notes.append("the key in the syllabus is not in Zotero (item deleted or moved?)")
            return m
        m.item, m.status, m.score = it, "locked", 1.0
        if it.deleted:
            m.notes.append("this Zotero item is in the trash")
        return m
    if r.doi:
        cands = [c for c in lib.by_doi.get(norm_doi(r.doi), []) if not c.deleted]
        if cands:
            cands.sort(key=lambda c: _pref(c, collections), reverse=True)
            m.item, m.status, m.score = cands[0], "doi", 1.0
            m.alternatives = [(c, 1.0) for c in cands[1:]]
            if r.title and title_sim(r.title, cands[0].title) < 0.4:
                m.notes.append("DOI matches but the titles differ: check the DOI")
            return m
    # fuzzy
    fam = norm(r.author)
    cands = list(lib.by_family.get(fam, []))
    if not cands and r.author:
        cands = list(lib.by_family.get(norm(r.author.split()[0]), []))
    if not cands and r.title:
        counts: dict = {}
        for tok in set(norm_title(r.title).split()):
            for it in lib.token_index.get(tok, []):
                counts[it.key or id(it)] = counts.get(it.key or id(it), 0) + 1
        pool = {(it.key or id(it)): it for tok in set(norm_title(r.title).split()) for it in lib.token_index.get(tok, [])}
        cands = [pool[k] for k, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:30]]
    scored = []
    for it in cands:
        if it.deleted:
            continue
        ts = title_sim(r.title, it.title) if r.title else 0.0
        a = 1.0 if (fam and fam in [norm(x) for x in it.authors]) or not it.authors else 0.0
        s = 0.7 * ts + 0.15 * _year_score(r.year, it.year) + 0.15 * a
        scored.append((s, ts, it))
    scored.sort(key=lambda t: (round(t[0], 2), _pref(t[2], collections)), reverse=True)
    if scored and scored[0][0] >= 0.78 and scored[0][1] >= 0.6:
        s, _, it = scored[0]
        m.item, m.status, m.score = it, "fuzzy", round(s, 2)
        m.alternatives = [(x[2], round(x[0], 2)) for x in scored[1:4] if x[0] >= s - 0.1]
        return m
    m.alternatives = [(x[2], round(x[0], 2)) for x in scored[:3]]
    return m


def match_all(readings, lib: Library, collections: List[str], use_locks: bool = True) -> List[Match]:
    return [match_reading(r, lib, collections, use_locks) for r in readings]


def _pages(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").replace("–", "-").replace("—", "-"))


def discrepancies(r, it: Item) -> List[str]:
    """Differences between the citation typed in the syllabus and the Zotero record."""
    out = []
    if r.year and it.year and r.year != it.year:
        out.append("year: syllabus %s, Zotero %s" % (r.year, it.year))
    if r.volume and it.field("volume") and r.volume != it.field("volume"):
        out.append("volume: syllabus %s, Zotero %s" % (r.volume, it.field("volume")))
    if r.issue and it.field("issue") and r.issue != it.field("issue"):
        out.append("issue: syllabus %s, Zotero %s" % (r.issue, it.field("issue")))
    if r.pages and it.field("pages") and _pages(r.pages) != _pages(it.field("pages")):
        out.append("pages: syllabus %s, Zotero %s" % (r.pages, it.field("pages")))
    if r.doi and it.doi and norm_doi(r.doi) != it.doi:
        out.append("DOI: syllabus %s, Zotero %s" % (r.doi, it.doi))
    if r.title and it.title and title_sim(r.title, it.title) < 0.6:
        out.append("title: syllabus “%s”, Zotero “%s”" % (r.title[:60], it.title[:60]))
    return out
