# coursenotes

Links a course syllabus (Markdown, in an Obsidian vault) to Zotero and to Obsidian literature notes. Zotero is the source of truth. Every command is a dry run unless you add `--write`; writes back up the syllabus first (`.coursenotes/backups`).

## Install
    pip install citeproc-py
    cd path/to/coursenotes && pip install -e .      # or: PYTHONPATH=path/to/coursenotes python3 -m coursenotes

## New course
1. `coursenotes init` in the course folder, then edit `coursenotes.toml` (vault, syllabus path, Zotero folder, collection).
2. Write the syllabus with `#### Week N (date): Title` headings and one numbered APA reading per line.
3. `coursenotes match` – report of readings that don't match a Zotero item, duplicates, and text that differs from Zotero.
4. `coursenotes hygiene` – Zotero records that will print bad references. Fix in Zotero.
5. `coursenotes verify` – compare against Crossref/DataCite (needs internet; set `mailto`).
6. `coursenotes all --write` – create missing literature notes, add "Zotero: open pdf · Literature note: [[...]]" lines, then check.
7. Optional: `scaffold --write` (week goal/question callouts + block IDs), `classes --write` (student class notes embedding those blocks).

Reports are written to `Tool reports/` beside the syllabus. `package` builds a zip for students and leaves no unzipped copy in the vault. Re-run any time; it only edits the "- Zotero:" sub-bullets, never your prose, and never overwrites a literature note you have edited.

## Commands
init, parse, match [--rematch], verify [--offline], hygiene, notes [--write] [--refresh], link [--write] [--rematch], scaffold, classes, check, all.

## Limits
- `verify` needs access to api.crossref.org / api.datacite.org; verified against live Crossref and DataCite for ED 336.
- Without a PDF attachment the link opens the Zotero item instead.
- Matching is by DOI, then fuzzy title/year/author; check the `match` report for anything not "locked" or "doi".
- Class-note and scaffold formats follow the ED 336 conventions; use `[classes] template` to change them.
- Tests: `python3 -m unittest discover -s tests`.
