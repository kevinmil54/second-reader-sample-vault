"""Find Zotero records that will produce a bad reference line."""
from __future__ import annotations

import re
from typing import List, Tuple

from .zotero import Item, Library, norm, norm_title


def _title_case_ratio(t: str) -> float:
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", t) if len(w) >= 4]
    return sum(1 for w in words if w[0].isupper()) / len(words) if words else 0.0


def check_item(it: Item) -> List[Tuple[str, str]]:
    out = []
    t, f = it.itype, it.fields
    if not f.get("date"):
        out.append(("error", "no date: the reference will say (n.d.)"))
    if t == "journalArticle":
        if not f.get("publicationTitle"):
            out.append(("error", "no journal name"))
        if not f.get("volume"):
            out.append(("warn", "no volume"))
        if not f.get("pages") and not f.get("articleNumber"):
            out.append(("warn", "no pages or article number"))
    if t in ("book", "report") and not (f.get("publisher") or f.get("institution")):
        out.append(("warn", "no publisher"))
    if t == "conferencePaper" and not (f.get("proceedingsTitle") or f.get("conferenceName")):
        out.append(("warn", "no proceedings title"))
    doi = f.get("DOI", "")
    if doi and (doi.lower().startswith("http") or doi.lower().endswith(".pdf")):
        out.append(("error", "DOI field is not a bare DOI (%s): the reference prints it wrongly" % doi[-40:]))
    if re.match(r"^\S+( et al\.)? \(\d{4}\)\s", it.title):
        out.append(("error", "title starts with author and year: “%s”" % it.title[:50]))
    if t != "webpage" and not any((c[3] if len(c) > 3 else "author") == "author" for c in it.creators):
        out.append(("warn", "no author"))
    persons = [c for c in it.creators if c[2] == 0]
    orgs = [c for c in it.creators if c[2] == 1]
    if persons and orgs:
        out.append(("warn", "an organization is listed as an author next to people (%s): usually belongs in Publisher" % orgs[0][0][:40]))
    for c in persons:
        if len(c[0].strip(". ")) <= 1 and c[1]:
            out.append(("warn", "very short family name “%s, %s”: first and last may be swapped" % (c[0], c[1])))
        if "(" in c[1] or c[1].endswith("."):
            if "(" in c[1]:
                out.append(("warn", "given name has parentheses: “%s”" % c[1]))
    for name, val in f.items():
        if re.search(r"\b\d{4}-\d{5}-\d{3}\b", val or ""):
            out.append(("warn", "database accession number in field %s will print in the reference" % name))
    if it.title and len(it.title.split()) > 4 and _title_case_ratio(it.title) > 0.6:
        out.append(("info", "title is in Title Case; APA prints it as stored (sentence case expected)"))
    if not it.pdf_key:
        out.append(("info", "no PDF attached"))
    return out


def duplicates(lib: Library, items) -> List[Tuple[Item, Item]]:
    out = []
    for it in items:
        for other in lib.items.values():
            if other is it or other.deleted:
                continue
            same = (it.doi and it.doi == other.doi) or (
                norm_title(it.title) == norm_title(other.title) and it.year == other.year and it.title)
            if same:
                out.append((it, other))
    return out
