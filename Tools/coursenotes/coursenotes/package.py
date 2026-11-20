"""Build student packages.

Zotero item keys differ between libraries, so zotero:// links cannot work for a student who imported an
export. The syllabus in the packages therefore (1) replaces each Zotero link with a DOI/URL link,
(2) points the literature-note links at a separate folder of instructor notes with path-qualified wikilinks,
so no student file is ever overwritten.

Two zips are written next to the syllabus:
  * "Student update <date>.zip"   syllabus + instructor notes + templates, to drop into an existing vault;
  * "Student starter vault <date>.zip"   a complete, ready-to-open vault (folders, templates, syllabus,
    course home, empty meeting notes, instructor notes).
Everything is built in a temp dir and only the zips are kept: an unzipped copy inside a vault duplicates note
names, and Obsidian then rewrites [[links]] to point at the copies.
"""
from __future__ import annotations

import os
import re
import time
import zipfile

from .link import NOTE_LINK_RE

ZLINK_RE = re.compile(r"Zotero:\s*\[[^\]]*\]\(zotero://[^)]*\)")
OPEN_IN_ZOTERO_RE = re.compile(r"\*\*Zotero:\*\*\s*\[Open in Zotero\]\([^)]*\)\s*·\s*")
FM_ZOTERO_RE = re.compile(r"^zotero:.*$", re.M)


def article_url(match):
    it, r = match.item, match.reading
    if it is not None and it.doi:
        return "https://doi.org/" + it.doi
    if it is not None and it.fields.get("url", "").startswith("http"):
        return it.fields["url"]
    if r.doi:
        return "https://doi.org/" + r.doi
    return r.url if r.url and r.url.startswith("http") else ""


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def safe_name(name, taken=(), maxlen=70):
    """File name that is valid on Windows and short enough to keep full paths under 260 characters.
    Removes ? * " < > |, turns : into ' -', and trims long names at a word boundary."""
    base = name[:-3] if name.endswith(".md") else name
    base = re.sub(r'[?*"<>|]', "", base)
    base = re.sub(r"\s*:\s*", " - ", base)
    base = re.sub(r"[\\/]", "-", base)
    base = re.sub(r"\s+", " ", base).strip()
    if len(base) > maxlen:
        base = base[:maxlen].rsplit(" ", 1)[0]
    base = base.rstrip(" .-")
    out, n = base, 2
    while out in taken:
        out = "%s %d" % (base, n)
        n += 1
    return out


def student_content(cfg, syll, matches, index, folder):
    """Returns (syllabus_text, {note filename: text}, missing reading ids)."""
    by_id = {m.reading.id: m for m in matches}
    lines = list(syll.lines)
    notes, missing = {}, []
    renamed = {}
    for r in syll.readings:
        if r.sub_start < 0:
            continue
        for j in range(r.sub_start, r.sub_end):
            line = lines[j]
            m = by_id.get(r.id)
            if ZLINK_RE.search(line):
                url = article_url(m) if m else ""
                line = ZLINK_RE.sub(("Article: [link](%s)" % url) if url else "Article: see the Zotero collection", line)
            nm = NOTE_LINK_RE.search(line)
            if nm:
                name = nm.group(1).split("|")[0].split("/")[-1]
                cands = index.resolve_name(name)
                src = cands[0] if cands else None
                if src and os.path.exists(src):
                    txt = OPEN_IN_ZOTERO_RE.sub("", _read(src))
                    txt = FM_ZOTERO_RE.sub("zotero: ", txt, count=1)
                    orig = os.path.basename(src)
                    if orig not in renamed:
                        renamed[orig] = safe_name(orig, taken=set(renamed.values())) + ".md"
                    notes[renamed[orig]] = txt
                    line = NOTE_LINK_RE.sub("Literature note: [[%s/%s|%s]]" % (folder, renamed[orig][:-3], name), line)
                else:
                    missing.append(r.id)
            lines[j] = line
    return "\n".join(lines), notes, missing


def _write_zip(path, root, files, dirs=()):
    """files: {relative path: text or bytes}; dirs: relative directory names to include (even if empty)."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for d in dirs:
            z.writestr(os.path.join(root, d) + "/", "")
        for rel, data in files.items():
            z.writestr(os.path.join(root, rel), data)


OBSIDIAN_APP = {"alwaysUpdateLinks": False, "attachmentFolderPath": "Attachments", "showInlineTitle": True,
                "propertiesInDocument": "visible", "livePreview": True, "defaultViewMode": "source"}
OBSIDIAN_CORE = ["file-explorer", "global-search", "switcher", "graph", "backlink", "outgoing-link", "tag-pane",
                 "properties", "page-preview", "templates", "note-composer", "command-palette", "bookmarks",
                 "outline", "word-count", "file-recovery"]
PLUGIN_FILES = ("main.js", "manifest.json", "styles.css")


def obsidian_config(cfg):
    """Files for the starter vault's .obsidian folder: settings, core plugins, and the community plugins named in
    [package] plugins (default dataview and second-reader-promote), copied from the instructor vault with the
    plugin's data.json (settings) copied only for plugins listed in [package] plugin_settings."""
    import json
    out, missing = {}, []
    plugins = cfg.get("package", "plugins", ["dataview", "second-reader-promote"]) or []
    with_data = cfg.get("package", "plugin_settings", ["second-reader-promote"]) or []
    src = os.path.join(cfg.vault_root, ".obsidian")
    out[".obsidian/app.json"] = json.dumps(OBSIDIAN_APP, indent=2)
    out[".obsidian/core-plugins.json"] = json.dumps(OBSIDIAN_CORE, indent=2)
    out[".obsidian/templates.json"] = json.dumps({"folder": "Templates", "date": "YYYY-MM-DD", "time": "hh:mm A"}, indent=2)
    found = []
    for pid in plugins:
        d = os.path.join(src, "plugins", pid)
        if not os.path.isdir(d):
            missing.append("plugin:" + pid)
            continue
        found.append(pid)
        for fn in PLUGIN_FILES:
            fp = os.path.join(d, fn)
            if os.path.exists(fp):
                out[".obsidian/plugins/%s/%s" % (pid, fn)] = _read(fp)
        if pid in with_data and os.path.exists(os.path.join(d, "data.json")):
            out[".obsidian/plugins/%s/data.json" % pid] = _read(os.path.join(d, "data.json"))
    out[".obsidian/community-plugins.json"] = json.dumps(found, indent=2)
    return out, missing


def course_label(cfg):
    """Short course label for file and folder names: [package] label, else the first 'DEPT 123' in the course name."""
    lab = cfg.get("package", "label", "")
    if lab:
        return lab
    m = re.match(r"\s*([A-Za-z]+\s*\d+)", cfg.get("course", "name", "") or "")
    return m.group(1) if m else "Course"


def build(cfg, syll, matches, index, stamp=None):
    stamp = stamp or time.strftime("%Y-%m-%d")
    label = course_label(cfg)
    folder = "%s notes (%s)" % (label, stamp)
    syl_name = os.path.basename(cfg.syllabus)
    syl_text, notes, missing = student_content(cfg, syll, matches, index, folder)

    # templates named in [package] templates (paths relative to the vault root)
    templates = {}
    for t in cfg.get("package", "templates", []) or []:
        p = cfg._abs(t, cfg.vault_root)
        if os.path.exists(p):
            templates[os.path.basename(p)] = _read(p)
        else:
            missing.append("template:" + t)
    course_folder = cfg.get("package", "course_folder", "") or cfg.get("course", "name", "Course")
    guide_path = cfg._abs(cfg.get("package", "guide", ""), cfg.vault_root) if cfg.get("package", "guide", "") else ""

    # --- update zip
    upd = {"READ ME FIRST.md": UPDATE_README.format(syllabus=syl_name, folder=folder, stamp=stamp, label=label),
           syl_name: syl_text}
    for fn, txt in notes.items():
        upd["%s/%s" % (folder, fn)] = txt
    for fn, txt in templates.items():
        upd["Templates/%s" % fn] = txt
    upd_zip = os.path.join(cfg.course_dir, "Student update %s.zip" % stamp)
    _write_zip(upd_zip, "Student update %s" % stamp, upd)

    # --- starter vault zip
    base = "%s starter vault" % label
    cdir = "Classes/%s" % course_folder
    st = {"READ ME FIRST.md": STARTER_README.format(cdir=cdir, stamp=stamp, label=label),
          "%s/%s" % (cdir, syl_name): syl_text}
    home = cfg.get("course", "home", "")
    if home:
        hp = os.path.join(cfg.course_dir, home + ".md")
        if os.path.exists(hp):
            st["%s/%s" % (cdir, os.path.basename(hp))] = _read(hp)
    mdir = cfg.classes_dir
    if os.path.isdir(mdir):
        for fn in sorted(os.listdir(mdir)):
            if fn.endswith(".md"):
                st["%s/Meeting notes/%s" % (cdir, fn)] = _read(os.path.join(mdir, fn))
    for fn, txt in notes.items():
        st["Literature notes/%s/%s" % (folder, fn)] = txt
    for fn, txt in templates.items():
        st["Templates/%s" % fn] = txt
    if guide_path and os.path.exists(guide_path):
        st["STUDENT SETUP GUIDE - %s.md" % label] = _read(guide_path)
    oc, om = obsidian_config(cfg)
    st.update(oc)
    missing.extend(om)
    star_zip = os.path.join(cfg.course_dir, "Student starter vault %s.zip" % stamp)
    _write_zip(star_zip, base, st, dirs=["Permanent notes", "Synthesis notes", "Projects", "Attachments"])
    return {"update": upd_zip, "starter": star_zip, "notes": len(notes), "templates": sorted(templates), "missing": missing}


UPDATE_README = """# {label} update ({stamp})

This update changes only what you drop in. Nothing of yours is replaced except the syllabus, and you keep your copy of that.

## Obsidian (4 steps)
1. In your {label} folder, rename your current syllabus by adding " (old)" to its name.
2. Copy `{syllabus}` from this update into the same folder.
3. Copy the folder `{folder}` into your vault, anywhere. Your own literature notes are not touched.
4. Copy the files in the `Templates` folder into your vault's `Templates` folder. If a file with the same name is already there, keep your copy unless the guide tells you to replace it.

The syllabus now links to the notes in the instructor folder. If you wrote your own note on a reading, it stays where it is; open both side by side if you want to compare.

## Zotero
Open Zotero, choose File > Import, and import the new collection file from Canvas. If you see duplicates afterwards, use "Duplicate Items" in the left panel and merge. The Zotero links in the old syllabus are replaced by links to each article's page (DOI), so they work without matching Zotero items.
"""

STARTER_README = """# {label} starter vault ({stamp})

This folder is a ready-made Obsidian vault for the course.

1. Unzip it somewhere on your computer (not inside another vault).
2. Open Obsidian, choose "Open folder as vault", and select the unzipped folder.
3. Obsidian will ask whether you trust the author of this vault. Choose "Trust author and enable plugins". If it does not ask, go to Settings > Community plugins and choose "Turn on community plugins".
4. Install Zotero with the Better BibTeX add-on (Part 1 of `STUDENT SETUP GUIDE - {label}.md`). The folders, templates, plugins and the import format are already set up in this vault.
5. Import the course Zotero file from Canvas (Part 4a of the guide).
6. Start at `{cdir}`: the syllabus, the course home note, and one meeting note per class.
"""
