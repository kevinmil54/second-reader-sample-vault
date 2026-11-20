"""Parse a markdown syllabus into weeks and numbered readings."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s)\]>]+")
COMMENT_RE = re.compile(r"%%.*?%%")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
READ_RE = re.compile(r"^(\d+)\.\s*(\S.*)$")
SUB_RE = re.compile(r"^\s+[-*]\s+")
Z_LINE_RE = re.compile(r"^\s+[-*]\s+Zotero:")
MARK_RE = re.compile(r"%%\s*cn\s+z:(\w+)\s*%%")
SELECT_RE = re.compile(r"zotero://select/library/items/(\w+)")
OPENPDF_RE = re.compile(r"zotero://open-pdf/library/items/(\w+)")


@dataclass
class Reading:
    id: str
    week: int
    index: int
    line_no: int  # 0-based index into lines
    raw: str
    text: str = ""
    url: str = ""
    doi: str = ""
    year: str = ""
    author: str = ""
    title: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    article: str = ""
    sub_start: int = -1  # indented bullet lines under the reading: [sub_start, sub_end)
    sub_end: int = -1
    z_line: int = -1  # index of the "- Zotero: ..." line this tool manages, if any
    locked_key: str = ""
    locked_att: str = ""


@dataclass
class Week:
    num: int
    date_text: str
    title: str
    heading: str
    start: int
    end: int = -1
    assignments: str = ""
    readings: List[Reading] = field(default_factory=list)


@dataclass
class Syllabus:
    lines: List[str]
    weeks: List[Week]
    readings: List[Reading]
    front_matter: dict


def plain(raw: str) -> str:
    t = COMMENT_RE.sub("", raw)
    t = MD_LINK_RE.sub(lambda m: m.group(1), t)
    t = re.sub(r"[*`]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def describe(raw: str) -> dict:
    """Pull year, author, title, DOI, volume/issue/pages out of one APA-style line."""
    out = {"url": "", "doi": "", "year": "", "author": "", "title": "", "volume": "", "issue": "", "pages": "", "article": ""}
    body = COMMENT_RE.sub("", raw)
    m = DOI_RE.search(body)
    if m:
        out["doi"] = m.group(0).rstrip(".,;:").lower()
    urls = re.findall(r"https?://[^\s)\]>]+", body)
    non_doi = [u for u in urls if "doi.org/" not in u]
    if non_doi:
        out["url"] = non_doi[0].rstrip(".,;")
    t = re.sub(r"^\s*\d+\.\s*", "", plain(raw))
    ym = re.search(r"\((\d{4})[a-z]?(?:,[^)]*)?\)", t)
    if ym:
        out["year"] = ym.group(1)
    am = re.match(r"\s*([^,(]+?)\s*(?:,|\()", t)
    if am:
        out["author"] = am.group(1).strip().rstrip(".")
    tm = re.search(r"\((?:\d{4}[a-z]?[^)]*|n\.d\.)\)\.?\s*(.*)$", t)
    if tm:
        rest = tm.group(1)
        if rest.startswith("["):
            out["title"] = re.sub(r"^\[(?:Review of(?: the book)?\s*)?(.*?)(?:,\s*by\s[^\]]*)?\]\s*\.?.*$", r"\1", rest)
        else:
            sm = re.match(r"(.+?[.?!])(?:\s|$)", rest)
            out["title"] = (sm.group(1) if sm else rest).rstrip(".").strip()
    vm = re.search(r"\*[^*\n]*?,\s*(\d+)\*(?:\((\d+)\))?", raw)
    if vm:
        out["volume"] = vm.group(1)
        out["issue"] = vm.group(2) or ""
    after = raw[vm.end():] if vm else raw
    pm = re.search(r"(?:,|pp\.)\s*(\d+\s*[–-]\s*\d+)", after)
    if pm:
        out["pages"] = re.sub(r"\s+", "", pm.group(1))
    am2 = re.search(r"Article\s+(\w+)", raw)
    if am2:
        out["article"] = am2.group(1)
    return out


def _front_matter(lines: List[str]):
    fm: dict = {}
    if lines and lines[0].strip() == "---":
        for k in range(1, len(lines)):
            if lines[k].strip() == "---":
                for ln in lines[1:k]:
                    m = re.match(r"^([\w-]+):\s*(.*)$", ln)
                    if m:
                        fm[m.group(1)] = m.group(2).strip().strip('"')
                return fm, k + 1
    return fm, 0


def parse_syllabus(text: str, week_heading: str) -> Syllabus:
    lines = text.split("\n")
    fm, start = _front_matter(lines)
    wre = re.compile(week_heading)
    weeks: List[Week] = []
    readings: List[Reading] = []
    cur = None
    seen = {}
    for i in range(start, len(lines)):
        line = lines[i]
        if re.match(r"^#{1,6}\s", line):
            if cur is not None:
                cur.end = i
            m = wre.match(line)
            if m:
                cur = Week(int(m.group(1)), (m.group(2) or "").strip(), (m.group(3) or "").strip(), line.strip(), i)
                weeks.append(cur)
            else:
                cur = None
            continue
        if cur is None:
            continue
        if line.startswith("*Assignments:*"):
            cur.assignments = line[len("*Assignments:*"):].strip()
            continue
        rm = READ_RE.match(line)
        if not rm:
            continue
        idx = int(rm.group(1))
        rid = "W%d-%d" % (cur.num, idx)
        seen[rid] = seen.get(rid, 0) + 1
        if seen[rid] > 1:
            rid += chr(ord("a") + seen[rid] - 2)
        r = Reading(id=rid, week=cur.num, index=idx, line_no=i, raw=line)
        d = describe(line)
        r.text = plain(line)
        for k, v in d.items():
            setattr(r, k, v)
        j = i + 1
        while j < len(lines) and SUB_RE.match(lines[j]):
            if r.z_line < 0 and Z_LINE_RE.match(lines[j]):
                r.z_line = j
            j += 1
        if j > i + 1:
            r.sub_start, r.sub_end = i + 1, j
        blob = "\n".join([line] + lines[i + 1 : j])
        mk = MARK_RE.search(blob)
        sel = SELECT_RE.search(blob)
        opn = OPENPDF_RE.search(blob)
        r.locked_key = mk.group(1) if mk else (sel.group(1) if sel else "")
        r.locked_att = opn.group(1) if (opn and not r.locked_key) else ""
        readings.append(r)
        cur.readings.append(r)
    if cur is not None and cur.end < 0:
        cur.end = len(lines)
    return Syllabus(lines=lines, weeks=weeks, readings=readings, front_matter=fm)
