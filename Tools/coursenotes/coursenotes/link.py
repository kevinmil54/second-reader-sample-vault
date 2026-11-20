"""Insert or refresh the per-reading link lines in the syllabus, editing the live file in place.

Rules, so that re-running never destroys hand edits:
  * only the sub-bullet that starts with "- Zotero:" is managed; any other sub-bullet is left alone;
  * a literature-note link that already points to an existing note is kept as is;
  * a reading with no Zotero match is never touched (except a web/video link line when it has a URL
    and a note exists for that URL).
"""
from __future__ import annotations

import difflib
import os
import re
import shutil
import time
from typing import List, Optional

NOTE_LINK_RE = re.compile(r"Literature note:\s*\[\[([^\]]+)\]\]")
TRAIL_COMMENTS_RE = re.compile(r"((?:\s*%%.*?%%)+)\s*$")


def _zseg(item, lib, existing_seg: Optional[str]):
    """The 'Zotero: [...](...)' segment. Keep a valid existing one; upgrade item links to PDF links."""
    if existing_seg:
        m = re.search(r"zotero://open-pdf/library/items/(\w+)", existing_seg)
        if m and lib.att_parent.get(m.group(1)) == item.key:
            return existing_seg
        m = re.search(r"zotero://select/library/items/(\w+)", existing_seg)
        if m and m.group(1) == item.key and not item.pdf_key:
            return existing_seg
    if item.pdf_key:
        return "Zotero: [open pdf](zotero://open-pdf/library/items/%s)" % item.pdf_key
    if item.key:
        return "Zotero: [open item](zotero://select/library/items/%s)" % item.key
    return "Zotero: [open item](zotero://select/items/@%s)" % item.citekey


def plan_links(syll, matches, lib, index, note_names: dict):
    """note_names: reading.id -> note basename (without .md) that exists or will exist."""
    lines = syll.lines
    edits = []  # (kind, line_no, old, new)
    for m in matches:
        r = m.reading
        subs = lines[r.sub_start:r.sub_end] if r.sub_start >= 0 else []
        if m.item is not None and not m.item.deleted:
            note = note_names.get(r.id, "")
            if r.z_line >= 0:
                old = lines[r.z_line]
                body = re.sub(r"^\s*[-*]\s+", "", old)
                indent = re.match(r"^(\s*)", old).group(1)
                tc = TRAIL_COMMENTS_RE.search(body)
                comments = tc.group(1) if tc else ""
                if tc:
                    body = body[: tc.start()]
                parts = [p.strip() for p in body.split(" · ")]
                zold = next((p for p in parts if p.startswith("Zotero:")), None)
                nm = NOTE_LINK_RE.search(body)
                keep_note = None
                if nm and index.resolve_name(nm.group(1)):
                    keep_note = nm.group(1)
                tgt = keep_note or note
                segs = [_zseg(m.item, lib, zold)]
                if tgt:
                    segs.append("Literature note: [[%s]]" % tgt)
                new = "%s- %s%s" % (indent, " · ".join(segs), comments)
                if new != old:
                    edits.append(("replace", r.z_line, old, new))
            else:
                has_zotero = any("zotero://" in s for s in subs)
                if has_zotero:
                    continue
                other_note = any("Literature note:" in s for s in subs)
                segs = [_zseg(m.item, lib, None)]
                if note and not other_note:
                    segs.append("Literature note: [[%s]]" % note)
                pos = r.sub_end if r.sub_end >= 0 else r.line_no + 1
                edits.append(("insert", pos, "", "   - " + " · ".join(segs)))
        elif m.item is None and r.url and note_names.get(r.id) and not any("Literature note:" in s for s in subs):
            note = note_names[r.id]
            label = "Video: [watch]" if re.search(r"\[(?:video|lecture)", r.raw, re.I) or "youtube" in r.url else "Web: [read]"
            pos = r.sub_end if r.sub_end >= 0 else r.line_no + 1
            edits.append(("insert", pos, "", "   - %s(%s) · Literature note: [[%s]]" % (label, r.url, note)))
    return edits


def apply_edits(lines: List[str], edits) -> List[str]:
    out = list(lines)
    for kind, pos, old, new in sorted(edits, key=lambda e: (e[1], e[0] == "insert"), reverse=True):
        if kind == "replace":
            out[pos] = new
        else:
            out.insert(pos, new)
    return out


def unified(old: List[str], new: List[str], name: str) -> str:
    return "\n".join(difflib.unified_diff(old, new, name, name + " (after)", lineterm="", n=0))


def backup(path: str, state_dir: str) -> str:
    d = os.path.join(state_dir, "backups")
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, "%s.%s" % (os.path.basename(path), time.strftime("%Y%m%d-%H%M%S")))
    shutil.copy2(path, dst)
    return dst


# ---------------------------------------------------------------------------
# scaffold: goal/question callouts and block ids that class notes can embed
# ---------------------------------------------------------------------------
GOAL_BLOCK = ["", "> [!goal] Themes or goals", "> ", "", "^{b}-goal", "",
              "> [!question] Questions to think about before class", "> - ", "", "^{b}-questions", ""]


def plan_scaffold(syll) -> List[tuple]:
    lines = syll.lines
    edits = []
    for w in syll.weeks:
        b = "w%02d" % w.num
        section = "\n".join(lines[w.start:w.end])
        if "^%s-goal" % b not in section and "^%s-questions" % b not in section:
            edits.append(("insert", w.start + 1, "", "\n".join(x.replace("{b}", b) for x in GOAL_BLOCK)))
        if "^%s-readings" % b not in section:
            if w.readings:
                pos = max(r.sub_end if r.sub_end >= 0 else r.line_no + 1 for r in w.readings)
            else:
                rl = [i for i in range(w.start, w.end) if lines[i].startswith("*Readings:*")]
                pos = (rl[0] + 1) if rl else w.start + 1
            edits.append(("insert", pos, "", "\n^%s-readings" % b))
    return edits
