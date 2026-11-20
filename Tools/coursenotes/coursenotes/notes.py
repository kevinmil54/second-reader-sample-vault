"""Create literature notes (never overwrites a note you may have edited)."""
from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Dict, List, Optional

from .templates import LITERATURE_NOTE, WEB_NOTE, fill

SKIP_DIRS = {".obsidian", ".coursenotes", ".trash", ".git", "Templates", ".smart-env", "_to_delete", "Tool reports"}
SKIP_PREFIXES = ("Student update",)
KEY_RE = re.compile(r"^zotero:\s*\"?zotero://select/(?:library/)?items/(@?[\w\-]+)", re.M)
URL_RE = re.compile(r"^url:\s*\"?(\S+?)\"?\s*$", re.M)


def sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def safe_filename(title: str) -> str:
    t = title.replace(":", " -").replace("/", "-").replace("\\", "-")
    t = re.sub(r'["<>|*?]', "", t)
    t = re.sub(r"\s+", " ", t).strip().rstrip(".")
    return t[:180] + ".md"


class VaultIndex:
    """Which Markdown files in the vault are literature notes for which Zotero key / URL."""

    def __init__(self, root: str):
        self.root = root
        self.by_key: Dict[str, List[str]] = {}
        self.by_url: Dict[str, List[str]] = {}
        self.by_name: Dict[str, List[str]] = {}
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(SKIP_PREFIXES)]
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                p = os.path.join(dp, fn)
                self.by_name.setdefault(fn[:-3].strip().lower(), []).append(p)
                try:
                    with open(p, encoding="utf-8") as fh:
                        head = fh.read(4000)
                except (OSError, UnicodeDecodeError):
                    continue
                m = KEY_RE.search(head)
                if m:
                    self.by_key.setdefault(m.group(1), []).append(p)
                u = URL_RE.search(head)
                if u and head.startswith("---"):
                    self.by_url.setdefault(u.group(1).rstrip("/"), []).append(p)

    @staticmethod
    def _best(paths: List[str], prefer_dir: str = "") -> Optional[str]:
        if not paths:
            return None
        def rank(p):
            b = os.path.basename(p)
            return (prefer_dir and os.path.dirname(p) == prefer_dir, not b.endswith("-old.md"), not b.startswith(" "), os.path.getsize(p))
        return max(paths, key=rank)

    def note_for_item(self, item, prefer_dir: str = "") -> Optional[str]:
        for k in (item.key, "@" + item.citekey if item.citekey else None):
            if k and k in self.by_key:
                return self._best(self.by_key[k], prefer_dir)
        return None

    def note_for_url(self, url: str, prefer_dir: str = "") -> Optional[str]:
        return self._best(self.by_url.get((url or "").rstrip("/"), []), prefer_dir)

    def resolve_name(self, name: str) -> List[str]:
        """Paths a [[wikilink]] with this name could point to."""
        n = name.split("|")[0].split("#")[0].strip().lower()
        if "/" in n:
            n = n.rsplit("/", 1)[1]
        return self.by_name.get(n, [])


def zotero_uri(item) -> str:
    return "zotero://select/library/items/%s" % item.key if item.key else "zotero://select/items/@%s" % item.citekey


def yaml_q(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def build_zotero_note(item, reference: str, course: str, template: str = "") -> str:
    vals = {
        "title": item.title, "title_yaml": yaml_q(item.title), "authors": item.author_names, "year": item.year,
        "citekey": item.citekey or item.key, "zotero_uri": zotero_uri(item), "reference": reference,
        "course_yaml": '"%s"' % yaml_q(course) if course else "", "doi": item.doi,
    }
    return fill(template or LITERATURE_NOTE, vals)


def source_type_of(reading) -> str:
    raw = reading.raw.lower()
    if "[video" in raw or "[lecture" in raw or "youtube" in raw:
        return "video"
    return "web page"


def build_web_note(reading, course: str, template: str = "") -> str:
    vals = {
        "title": reading.title or reading.text[:80], "title_yaml": yaml_q(reading.title or reading.text[:80]),
        "authors": reading.author, "year": reading.year, "source_type": source_type_of(reading),
        "url": reading.url, "reference": reading.text, "course_yaml": '"%s"' % yaml_q(course) if course else "",
    }
    return fill(template or WEB_NOTE, vals)


def load_state(state_dir: str) -> dict:
    p = os.path.join(state_dir, "state.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    return {"notes": {}}


def save_state(state_dir: str, state: dict):
    os.makedirs(state_dir, exist_ok=True)
    with open(os.path.join(state_dir, "state.json"), "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1, ensure_ascii=False)


def plan_notes(matches, index: VaultIndex, renderer, cfg, template_zotero="", template_web="", refresh=False):
    """Return a list of dicts: {reading, action, path, text, detail}. Nothing is written here."""
    course = cfg.get("course", "name", "")
    lit_dir = cfg.literature_dir
    state = load_state(cfg.state_dir)
    seen = {}
    plan = []
    for m in matches:
        r = m.reading
        if m.item is not None and not m.item.deleted:
            it = m.item
            ident = it.key or it.citekey
            if ident in seen:
                plan.append({"reading": r, "action": "same-as", "path": seen[ident], "detail": ""})
                continue
            existing = index.note_for_item(it, lit_dir)
            ref = renderer.apa(it.csl)
            text = build_zotero_note(it, ref, course, template_zotero)
            fn = safe_filename(it.title)
        elif r.url and m.status in ("none",):
            existing = index.note_for_url(r.url, lit_dir)
            text = build_web_note(r, course, template_web)
            fn = safe_filename(r.title or r.text[:80])
            ident = r.url
            if ident in seen:
                plan.append({"reading": r, "action": "same-as", "path": seen[ident], "detail": ""})
                continue
        else:
            plan.append({"reading": r, "action": "no-source", "path": "", "detail": "no Zotero item and no URL"})
            continue
        if existing:
            seen[ident] = existing
            rel = os.path.basename(existing)
            recorded = state["notes"].get(rel)
            cur = open(existing, encoding="utf-8").read()
            if refresh and recorded and sha(cur) == recorded and cur != text:
                plan.append({"reading": r, "action": "refresh", "path": existing, "text": text, "detail": ""})
            elif refresh and recorded and sha(cur) != recorded:
                plan.append({"reading": r, "action": "skip-edited", "path": existing, "detail": "edited since it was generated"})
            else:
                dup = [p for p in index.by_key.get(it.key, []) if p != existing] if m.item is not None else []
                plan.append({"reading": r, "action": "exists", "path": existing,
                             "detail": ("also: " + ", ".join(os.path.basename(p) for p in dup)) if dup else ""})
            continue
        path = os.path.join(lit_dir, fn)
        if os.path.exists(path):
            plan.append({"reading": r, "action": "name-collision", "path": path, "detail": "a different note already has this file name"})
            continue
        seen[ident] = path
        plan.append({"reading": r, "action": "create", "path": path, "text": text, "detail": ""})
    return plan


def apply_notes(plan, cfg):
    state = load_state(cfg.state_dir)
    n = 0
    for p in plan:
        if p["action"] in ("create", "refresh"):
            os.makedirs(os.path.dirname(p["path"]), exist_ok=True)
            with open(p["path"], "w", encoding="utf-8") as fh:
                fh.write(p["text"])
            state["notes"][os.path.basename(p["path"])] = sha(p["text"])
            n += 1
    if n:
        save_state(cfg.state_dir, state)
    return n
