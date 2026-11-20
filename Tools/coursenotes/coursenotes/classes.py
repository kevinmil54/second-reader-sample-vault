"""Create student-facing class notes (one per meeting) that embed the syllabus blocks. Existing notes are never touched."""
from __future__ import annotations

import os
import re
from typing import List

from .notes import safe_filename, yaml_q
from .templates import STUDENT_CLASS_NOTE, fill

MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def parse_date(date_text: str, year: str) -> str:
    m = re.match(r"\s*([A-Za-z]+)\.?\s+(\d{1,2})", date_text or "")
    if not m or not year or m.group(1)[:3].lower() not in MONTHS:
        return ""
    return "%s-%02d-%02d" % (year, MONTHS[m.group(1)[:3].lower()], int(m.group(2)))


def plan_classes(syll, cfg, template: str = "") -> List[dict]:
    year = str(cfg.get("course", "year", "") or (syll.front_matter.get("first-class", "") or "")[:4])
    course = cfg.get("course", "name", "") or syll.front_matter.get("course", "")
    offering = cfg.get("course", "offering", "") or os.path.basename(cfg.course_dir)
    fmt = cfg.get("classes", "name_format", "Class {nn} - {date} - Student")
    syllabus_name = os.path.splitext(os.path.basename(cfg.syllabus))[0]
    home = cfg.get("course", "home", "")
    names = []
    for w in syll.weeks:
        date = parse_date(w.date_text, year)
        names.append((w, date, fmt.format(nn="%02d" % w.num, week=w.num, date=date, title=w.title)))
    out = []
    for i, (w, date, name) in enumerate(names):
        if not date:
            out.append({"week": w.num, "action": "skip", "detail": "cannot read a date from “%s” (set [course] year)" % w.date_text})
            continue
        prev_ = "[[%s]]" % names[i - 1][2] if i > 0 else ""
        next_ = "[[%s]]" % names[i + 1][2] if i + 1 < len(names) else ""
        extra = ""
        if home:
            extra += " · [[%s|Course home]]" % home
        extra += " · [[%s|Syllabus]]" % syllabus_name
        text = fill(template or STUDENT_CLASS_NOTE, {
            "course": course, "offering": offering, "meeting": w.num, "nn": "%02d" % w.num, "date": date,
            "topic": w.title, "topic_yaml": yaml_q(w.title), "prev": prev_, "next": next_,
            "extra_links": extra, "syllabus": syllabus_name, "block": "w%02d" % w.num,
        })
        path = os.path.join(cfg.classes_dir, safe_filename(name))
        out.append({"week": w.num, "action": "exists" if os.path.exists(path) else "create", "path": path, "text": text})
    return out


def apply_classes(plan) -> int:
    n = 0
    for p in plan:
        if p["action"] == "create":
            os.makedirs(os.path.dirname(p["path"]), exist_ok=True)
            with open(p["path"], "w", encoding="utf-8") as fh:
                fh.write(p["text"])
            n += 1
    return n
