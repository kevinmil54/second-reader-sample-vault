"""Consistency checks on the syllabus, its links and the notes."""
from __future__ import annotations

import os
import re
from typing import List, Tuple

WIKI_RE = re.compile(r"(!?)\[\[([^\]]+)\]\]")


def check_syllabus(cfg, syll, matches, lib, index) -> List[Tuple[str, str, str]]:
    probs = []
    lines = syll.lines
    for i, line in enumerate(lines, 1):
        for emb, target in WIKI_RE.findall(line):
            name = target.split("|")[0].split("#")[0].strip()
            if not name:
                continue
            paths = index.resolve_name(name)
            if not paths:
                probs.append(("error", "line %d" % i, "link target not found: [[%s]]" % name))
            elif len(paths) > 1:
                probs.append(("warn", "line %d" % i, "ambiguous link [[%s]]: %d files share that name" % (name, len(paths))))
    for m in matches:
        r = m.reading
        subs = lines[r.sub_start:r.sub_end] if r.sub_start >= 0 else []
        joined = "\n".join(subs)
        label = "%s %s" % (r.id, (r.author + " " + r.year).strip())
        if "Literature note:" not in joined:
            probs.append(("warn", label, "no literature note link"))
        if m.item is None and "zotero://" not in joined:
            probs.append(("info", label, "no Zotero item"))
        for key in re.findall(r"zotero://(?:select|open-pdf)/library/items/(\w+)", joined):
            if lib.has_sqlite and lib.resolve_key(key) is None:
                probs.append(("error", label, "Zotero key %s is not in the library" % key))
        if m.item is not None and m.item.deleted:
            probs.append(("error", label, "linked Zotero item is in the trash"))
        if m.item is not None:
            note = None
            nm = re.search(r"Literature note:\s*\[\[([^\]|]+)", joined)
            if nm:
                ps = index.resolve_name(nm.group(1))
                note = ps[0] if len(ps) == 1 else None
            if note:
                head = open(note, encoding="utf-8").read(3000)
                kk = re.search(r"^zotero:\s*\"?zotero://select/(?:library/)?items/(@?[\w\-]+)", head, re.M)
                if kk and kk.group(1) not in (m.item.key, "@" + m.item.citekey):
                    probs.append(("info", label, "note is attached to a different Zotero item (%s) than the link (%s): a duplicate item?" % (kk.group(1), m.item.key)))
        if m.status == "locked-missing":
            probs.append(("error", label, "Zotero key in the syllabus is not in the library"))
    for w in syll.weeks:
        b = "w%02d" % w.num
        sec = "\n".join(lines[w.start:w.end])
        for suffix in ("goal", "questions", "readings"):
            if "^%s-%s" % (b, suffix) not in sec:
                probs.append(("info", "Week %d" % w.num, "no block id ^%s-%s (run `scaffold` if class notes embed it)" % (b, suffix)))
    return probs
