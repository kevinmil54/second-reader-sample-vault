from __future__ import annotations

import argparse
import os
import sys
from collections import Counter

from . import __version__
from .check import check_syllabus
from .classes import apply_classes, plan_classes
from .config import load_config
from .hygiene import check_item, duplicates
from .link import apply_edits, backup, plan_links, plan_scaffold, unified
from .match import discrepancies, match_all
from .notes import VaultIndex, apply_notes, plan_notes
from .parse import parse_syllabus
from .report import table, write_report
from .zotero import Library

EXAMPLE_CONFIG = '''# coursenotes configuration. Paths may be absolute or "~/..."; relative paths are explained below.
[vault]
root = "~/Obsidian-KFM"                      # your Obsidian vault

[course]
name = "ED 336/536 & Psych 401-026"          # written into literature notes ("course:") and class notes
offering = "2026-Fall"                       # shown in class notes; defaults to the syllabus folder name
year = "2026"                                # used with week dates such as "(Sept 9)"
syllabus = "Classes/My course/2026-Fall/Syllabus.md"   # relative to the vault root
literature_dir = "Literature notes"          # relative to the vault root; new literature notes go here
classes_dir = "Meeting notes"                # relative to the folder that holds the syllabus
# home = "ED 336 Fall 2026 - Course home"    # optional: name of a course-home note to link from class notes

[zotero]
data_dir = "~/Zotero"                        # folder with zotero.sqlite
csl_json = "My Library.json"                 # CSL JSON export (Better BibTeX auto-export works); relative to data_dir
csl_style = "styles/apa.csl"                 # relative to data_dir
sqlite = "zotero.sqlite"                     # read from a temporary copy, never modified
# bbt_sqlite = "better-bibtex.migrated"      # optional, for Better BibTeX citation keys
collections = ["My course collection"]       # optional: prefer items from these Zotero collections when a paper has duplicates

[syllabus]
# Regex for a week heading: group 1 = week number, group 2 = date text, group 3 = title.
# The default matches "#### Week 5 (Sept 30): Title".
# week_heading = '^#{2,6}\\s*Week\\s+(\\d+)\\s*(?:\\(([^)]*)\\))?\\s*[:\\-–—]?\\s*(.*?)\\s*$'

[notes]
# template = "Templates/My literature template.md"   # uses {{title}} {{authors}} {{year}} {{citekey}} {{zotero_uri}} {{reference}} ...

[classes]
# name_format = "Class {nn} - {date} - Student"
# template = "Templates/My class template.md"

[verify]
# mailto = "you@example.edu"   # optional: Crossref asks for a contact address in the request header
'''


class Ctx:
    def __init__(self, cfg, rematch=False):
        self.cfg = cfg
        with open(cfg.syllabus, encoding="utf-8") as fh:
            self.text = fh.read()
        self.syll = parse_syllabus(self.text, cfg.get("syllabus", "week_heading"))
        self.lib = Library.load(cfg.zpath("sqlite", "zotero.sqlite"), cfg.zpath("csl_json", "My Library.json"),
                                cfg.zpath("bbt_sqlite", ""))
        if not self.lib.items:
            raise SystemExit("No Zotero data found. Check [zotero] data_dir, csl_json and sqlite in the config.")
        self.matches = match_all(self.syll.readings, self.lib, cfg.collections, use_locks=not rematch)
        self._index = None
        self._renderer = None

    @property
    def index(self):
        if self._index is None:
            self._index = VaultIndex(self.cfg.vault_root)
        return self._index

    def reindex(self):
        self._index = None

    @property
    def renderer(self):
        if self._renderer is None:
            from .render import Renderer
            self._renderer = Renderer(self.cfg.zpath("csl_style", "styles/apa.csl"))
        return self._renderer

    def template(self, section):
        p = self.cfg.get(section, "template", "")
        if not p:
            return ""
        with open(self.cfg._abs(p, self.cfg.vault_root), encoding="utf-8") as fh:
            return fh.read()


def short(r) -> str:
    return ("%s %s: %s" % (r.author, r.year, r.title))[:80]


# ---------------------------------------------------------------------------
def cmd_parse(args):
    cfg = load_config(args.config)
    ctx = Ctx(cfg)
    rows = [[w.num, w.date_text, w.title, len(w.readings), w.assignments[:60]] for w in ctx.syll.weeks]
    body = "# Syllabus structure\n\n" + table(["Week", "Date", "Title", "Readings", "Assignments"], rows)
    body += "\n## Readings as parsed\n\n" + table(
        ["ID", "Author", "Year", "Title", "DOI", "Vol(issue)", "Pages"],
        [[r.id, r.author, r.year, r.title[:70], r.doi, "%s(%s)" % (r.volume, r.issue) if r.volume else "", r.pages or r.article]
         for r in ctx.syll.readings])
    print("%d weeks, %d readings. Report: %s" % (len(ctx.syll.weeks), len(ctx.syll.readings), write_report(cfg, "parse", body)))


def cmd_match(args):
    cfg = load_config(args.config)
    ctx = Ctx(cfg, rematch=args.rematch)
    c = Counter(m.status for m in ctx.matches)
    rows, decide, diffs = [], [], []
    for m in ctx.matches:
        r = m.reading
        it = m.item
        extra = list(m.notes)
        if m.alternatives:
            extra.append("also: " + ", ".join("%s “%s” (%.2f)" % (a.key or a.citekey, a.title[:35], s) for a, s in m.alternatives[:3]))
        rows.append([r.id, short(r), ("%s %s" % (it.key, it.title[:50])) if it else "", m.status, "; ".join(extra)])
        if m.status in ("none", "locked-missing"):
            decide.append([r.id, short(r), m.status, "; ".join(extra) or "no candidate"])
        elif m.alternatives and m.status != "locked":
            decide.append([r.id, short(r), "duplicate items", "; ".join(extra)])
        if it:
            for d in discrepancies(r, it):
                diffs.append([r.id, short(r), d])
    body = "# Match: syllabus readings to Zotero\n\n" + ", ".join("%s: %d" % kv for kv in sorted(c.items())) + "\n\n"
    body += "## Needs a decision\n\n" + table(["ID", "Reading", "Problem", "Detail"], decide)
    body += "\n## Syllabus text differs from the Zotero record\n\n" + table(["ID", "Reading", "Difference"], diffs)
    body += "\n## All readings\n\n" + table(["ID", "Reading", "Zotero item", "How", "Notes"], rows)
    print(", ".join("%s: %d" % kv for kv in sorted(c.items())), "| decisions needed:", len(decide), "| differences:", len(diffs))
    print("Report:", write_report(cfg, "match", body))


def cmd_verify(args):
    from .verify import Fetcher, verify_all
    cfg = load_config(args.config)
    ctx = Ctx(cfg)
    f = Fetcher(os.path.join(cfg.state_dir, "cache"), cfg.get("verify", "mailto", ""), offline=args.offline)
    rows = verify_all(ctx.matches, f)
    c = Counter(r[1] for r in rows)
    body = "# Verify citations against Crossref / DataCite\n\n" + ", ".join("%s: %d" % kv for kv in sorted(c.items())) + "\n\n"
    if f.failures:
        body += "**%d lookups failed.** Last error: `%s`\n\n" % (f.failures, f.last_error)
    by = {m.reading.id: m.reading for m in ctx.matches}
    body += table(["ID", "Reading", "Result", "Detail", "DOI"], [[i, short(by[i]), s, d, doi] for i, s, d, doi in rows])
    print(", ".join("%s: %d" % kv for kv in sorted(c.items())), "| lookup failures:", f.failures, ("| last error: " + f.last_error) if f.failures else "")
    print("Report:", write_report(cfg, "verify", body))


def cmd_hygiene(args):
    cfg = load_config(args.config)
    ctx = Ctx(cfg)
    seen, rows = set(), []
    items = []
    for m in ctx.matches:
        if m.item is not None and id(m.item) not in seen:
            seen.add(id(m.item))
            items.append((m.reading, m.item))
    order = {"error": 0, "warn": 1, "info": 2}
    for r, it in items:
        for lvl, msg in check_item(it):
            if lvl == "info" and not args.all:
                continue
            rows.append([order[lvl], "%s %s" % (r.author, r.year), "%s %s" % (it.key, it.title[:40]), lvl, msg])
    rows.sort(key=lambda x: x[0])
    dups = duplicates(ctx.lib, [it for _, it in items])
    body = "# Zotero record problems for the readings in this syllabus\n\n"
    body += table(["Reading", "Zotero item", "Level", "Problem"], [r[1:] for r in rows])
    body += "\n## Duplicate Zotero items\n\n" + table(["Item", "Also"], [["%s %s" % (a.key, a.title[:50]), "%s (%s)" % (b.key, ", ".join(b.collections) or "no collection")] for a, b in dups])
    print("%d problems on %d items, %d duplicates. Report: %s" % (len(rows), len(items), len(dups), write_report(cfg, "zotero hygiene", body)))


def _note_names(plan):
    names = {}
    for p in plan:
        if p.get("path") and p["action"] in ("exists", "create", "refresh", "skip-edited", "same-as"):
            names[p["reading"].id] = os.path.basename(p["path"])[:-3]
    return names


def cmd_notes(args, ctx=None):
    cfg = load_config(args.config)
    ctx = ctx or Ctx(cfg)
    plan = plan_notes(ctx.matches, ctx.index, ctx.renderer, cfg, ctx.template("notes"), "", refresh=args.refresh)
    c = Counter(p["action"] for p in plan)
    rows = [[p["reading"].id, short(p["reading"]), p["action"], os.path.basename(p.get("path", "") or ""), p.get("detail", "")] for p in plan]
    body = "# Literature notes\n\n" + ", ".join("%s: %d" % kv for kv in sorted(c.items())) + "\n\n" + table(["ID", "Reading", "Action", "Note", "Detail"], rows)
    path = write_report(cfg, "notes", body)
    if args.write:
        n = apply_notes(plan, cfg)
        ctx.reindex()
        print("wrote %d notes" % n, "|", ", ".join("%s: %d" % kv for kv in sorted(c.items())))
    else:
        print("dry run (add --write to create notes) |", ", ".join("%s: %d" % kv for kv in sorted(c.items())))
    print("Report:", path)
    return plan


def cmd_link(args, ctx=None, notes_plan=None):
    cfg = load_config(args.config)
    ctx = ctx or Ctx(cfg, rematch=args.rematch)
    if notes_plan is None:
        notes_plan = plan_notes(ctx.matches, ctx.index, ctx.renderer, cfg, ctx.template("notes"))
    names = _note_names(notes_plan)
    edits = plan_links(ctx.syll, ctx.matches, ctx.lib, ctx.index, names)
    new_lines = apply_edits(ctx.syll.lines, edits)
    diff = unified(ctx.syll.lines, new_lines, os.path.basename(cfg.syllabus))
    body = "# Syllabus link changes\n\n%d change(s).\n\n```diff\n%s\n```\n" % (len(edits), diff)
    path = write_report(cfg, "link", body)
    if edits and args.write:
        b = backup(cfg.syllabus, cfg.state_dir)
        with open(cfg.syllabus, "w", encoding="utf-8") as fh:
            fh.write("\n".join(new_lines))
        print("updated %d line(s); backup: %s" % (len(edits), b))
    else:
        print("%d change(s) %s" % (len(edits), "(dry run; add --write to apply)" if edits else "needed"))
    print("Report:", path)
    return edits


def cmd_scaffold(args):
    cfg = load_config(args.config)
    ctx = Ctx(cfg)
    edits = plan_scaffold(ctx.syll)
    new_lines = apply_edits(ctx.syll.lines, edits)
    body = "# Scaffold weeks\n\n%d insertion(s).\n\n```diff\n%s\n```\n" % (len(edits), unified(ctx.syll.lines, new_lines, os.path.basename(cfg.syllabus)))
    path = write_report(cfg, "scaffold", body)
    if edits and args.write:
        b = backup(cfg.syllabus, cfg.state_dir)
        with open(cfg.syllabus, "w", encoding="utf-8") as fh:
            fh.write("\n".join(new_lines))
        print("inserted %d block(s); backup: %s" % (len(edits), b))
    else:
        print("%d insertion(s) %s" % (len(edits), "(dry run; add --write to apply)" if edits else "needed"))
    print("Report:", path)


def cmd_classes(args):
    cfg = load_config(args.config)
    ctx = Ctx(cfg)
    plan = plan_classes(ctx.syll, cfg, ctx.template("classes"))
    c = Counter(p["action"] for p in plan)
    body = "# Class notes\n\n" + ", ".join("%s: %d" % kv for kv in sorted(c.items())) + "\n\n" + table(
        ["Week", "Action", "File / detail"], [[p["week"], p["action"], os.path.basename(p.get("path", "")) or p.get("detail", "")] for p in plan])
    path = write_report(cfg, "classes", body)
    if args.write:
        print("created %d class notes" % apply_classes(plan), "|", ", ".join("%s: %d" % kv for kv in sorted(c.items())))
    else:
        print("dry run (add --write to create) |", ", ".join("%s: %d" % kv for kv in sorted(c.items())))
    print("Report:", path)


def cmd_check(args, ctx=None):
    cfg = load_config(args.config)
    ctx = ctx or Ctx(cfg)
    probs = check_syllabus(cfg, ctx.syll, ctx.matches, ctx.lib, ctx.index)
    order = {"error": 0, "warn": 1, "info": 2}
    probs.sort(key=lambda p: order[p[0]])
    c = Counter(p[0] for p in probs)
    body = "# Checks\n\n" + (", ".join("%s: %d" % kv for kv in sorted(c.items())) or "no problems") + "\n\n" + table(["Level", "Where", "Problem"], probs)
    print(", ".join("%s: %d" % kv for kv in sorted(c.items())) or "no problems", "| Report:", write_report(cfg, "check", body))
    return probs


def cmd_package(args):
    from .package import build
    cfg = load_config(args.config)
    ctx = Ctx(cfg)
    r = build(cfg, ctx.syll, ctx.matches, ctx.index)
    print("built %s" % r["update"])
    print("built %s" % r["starter"])
    print("%d instructor notes; templates: %s%s" % (r["notes"], ", ".join(r["templates"]) or "none",
          ("; MISSING: " + ", ".join(r["missing"])) if r["missing"] else ""))


def cmd_all(args):
    cfg = load_config(args.config)
    ctx = Ctx(cfg, rematch=args.rematch)
    print("== notes")
    plan = cmd_notes(args, ctx)
    print("== link")
    cmd_link(args, ctx, plan if not args.write else None)
    ctx.reindex()
    print("== check")
    ctx2 = Ctx(cfg)
    cmd_check(args, ctx2)


def cmd_init(args):
    path = os.path.join(args.dir, "coursenotes.toml")
    if os.path.exists(path):
        raise SystemExit("%s already exists" % path)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(EXAMPLE_CONFIG)
    print("wrote", path, "(edit the paths, then run: coursenotes match)")


def main(argv=None):
    p = argparse.ArgumentParser(prog="coursenotes", description="Link a syllabus to Zotero and Obsidian literature notes.")
    p.add_argument("--version", action="version", version="coursenotes " + __version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_, write=False, rematch=False, extra=None):
        sp = sub.add_parser(name, help=help_)
        sp.add_argument("-c", "--config", default="coursenotes.toml", help="config file (default: ./coursenotes.toml)")
        if write:
            sp.add_argument("--write", action="store_true", help="apply the changes (default is a dry run)")
        if rematch:
            sp.add_argument("--rematch", action="store_true", help="ignore the Zotero links already in the syllabus and match from scratch")
        if extra:
            extra(sp)
        sp.set_defaults(func=fn)
        return sp

    i = sub.add_parser("init", help="write a starter coursenotes.toml")
    i.add_argument("dir", nargs="?", default=".")
    i.set_defaults(func=cmd_init)
    add("parse", cmd_parse, "show how the syllabus is read")
    add("match", cmd_match, "match readings to Zotero items; report differences and duplicates", rematch=True)
    add("verify", cmd_verify, "check citations against Crossref/DataCite (needs internet)",
        extra=lambda s: s.add_argument("--offline", action="store_true", help="use cached lookups only"))
    add("hygiene", cmd_hygiene, "list Zotero records that will print a bad reference",
        extra=lambda s: s.add_argument("--all", action="store_true", help="include informational items"))
    add("notes", cmd_notes, "create missing literature notes", write=True,
        extra=lambda s: s.add_argument("--refresh", action="store_true", help="also regenerate notes that are still as generated"))
    add("link", cmd_link, "insert/refresh the Zotero and literature-note link lines in the syllabus", write=True, rematch=True)
    add("scaffold", cmd_scaffold, "add goal/question callouts and block ids to each week of the syllabus", write=True)
    add("classes", cmd_classes, "create missing student class notes that embed the syllabus blocks", write=True)
    add("check", cmd_check, "check links and notes")
    add("package", cmd_package, "build student zips (update + starter vault) with DOI links instead of Zotero links")
    add("all", cmd_all, "notes + link + check", write=True, rematch=True,
        extra=lambda s: s.add_argument("--refresh", action="store_true", help=argparse.SUPPRESS))
    args = p.parse_args(argv)
    if not hasattr(args, "refresh"):
        args.refresh = False
    if not hasattr(args, "rematch"):
        args.rematch = False
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
