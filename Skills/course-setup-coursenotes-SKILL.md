---
name: course-setup-coursenotes
description: Set up a course's readings in Zotero and Obsidian from a syllabus, verify citations, create literature notes and class notes, and build student update packages. Use at the start of each course or when the syllabus changes. Most work is done by the Python tool coursenotes, not by Claude.
type: skill
created: 2026-10-03
source course: ED 336/536 Fall 2026
---

# Course setup with coursenotes

## What this does

Every reading on a syllabus ends up linked to a Zotero item and an Obsidian literature note. Zotero is the source of truth for reference data. The syllabus, notes and student packages are generated or checked from it by a Python tool, so Claude is only needed for the parts that need judgment.

## Division of labor

Python (`Tools/coursenotes`) does:
- parsing the syllabus and matching each reading to a Zotero item (DOI first, then title, year and author)
- flagging Zotero records that will print bad references (`hygiene`)
- comparing citations with Crossref and DataCite (`verify`)
- creating missing literature notes and adding the link lines to the syllabus (`notes`, `link`, `all`)
- adding week goal and question callouts with block IDs (`scaffold`)
- creating student meeting notes that embed those blocks (`classes`)
- checking that every link and note resolves (`check`)
- building the student update zip and starter vault zip (`package`)

Claude or the instructor does:
- choosing readings and writing the syllabus text
- deciding which of several Zotero duplicates to keep (compare the PDFs, then delete the others)
- fixing Zotero records the reports flag (Zotero's Run JavaScript can do bulk edits)
- filling in literature note content (the `literature-note` skill)
- reading the reports and deciding what a mismatch means

## Where things live

| Item | Location |
|---|---|
| Tool | `Tools/coursenotes/` (top level of the vault) |
| Course folder | `Classes/<Course>/<Term>/` (syllabus, course home, `Meeting notes/`, `Planning/`, `Tool reports/`, `coursenotes.toml`) |
| Literature notes | `Literature notes/` |
| Templates | `Templates/` |
| Zotero data | `~/Zotero` |
| Backups | `.coursenotes/backups` beside the syllabus |

## Install (once)

```
pip3 install citeproc-py
pip3 install -e <your vault>/Tools/coursenotes
```

If `coursenotes` is not found as a command, run it from the course folder as:

```
cd "<course folder>"
PYTHONPATH=<your vault>/Tools/coursenotes python3 -m coursenotes <command>
```

If the editable install still points at an old location (after folder renames), reinstall it with the `pip3 install -e` line above.

## Workflow for a new course

1. Create `Classes/<Course>/<Term>/` and write the syllabus. Use `#### Week N (date): Title` headings and one numbered APA reading per line.
2. Put every reading in a Zotero collection, with the PDF attached. The collection should contain exactly the syllabus readings.
3. In the course folder run `coursenotes init`, then edit `coursenotes.toml`: vault root, syllabus path, Zotero data folder, collection name, `classes_dir = "Meeting notes"`, and the `[package]` section.
4. `coursenotes match` and read the report. Fix readings that do not match a Zotero item, duplicates, and text that differs from Zotero. Fix the Zotero record when Zotero is wrong and the syllabus when the syllabus is wrong, then run `match` again until there are no differences.
5. `coursenotes hygiene`. Fix the flagged records in Zotero.
6. `coursenotes verify`. It needs internet. On macOS it falls back to curl if Python's SSL certificates fail. Treat each mismatch as a question to check against the article, because Crossref is sometimes wrong (a preprint year or an author list, for example).
7. `coursenotes all --write` creates missing literature notes, writes the link lines, and runs `check`.
8. Optional: `coursenotes scaffold --write` and `coursenotes classes --write`.
9. `coursenotes check`. Expect only items that legitimately have no Zotero item (books, videos).
10. Fill in literature note content (the `literature-note` skill, one article at a time).

Every command is a dry run until `--write` is added. A write backs up the syllabus first.

## Zotero conventions that keep the matching clean

- DOI field holds the bare DOI (`10.xxxx/...`), not `https://doi.org/...`. A Zotero Run JavaScript script can strip the prefix across the library. Run it with a `DRY` flag first and read the output.
- A reading that is a preprint should be a Preprint item type.
- Page fields should match the PDF. Check preprints against the PDF itself.
- One Zotero item per reading. Delete older duplicates, and compare the attachments before deleting.
- Authors are checked against the article, not only Crossref. Zotero can be right when Crossref differs.
- A single-letter surname is the only thing `hygiene` treats as an error, since short real surnames (Li, Su) are common.

## Rules the tool follows

- It edits only the `- Zotero:` sub-bullets in the syllabus. The prose is not touched.
- It never overwrites a literature note that has been edited.
- Obsidian links resolve by note name, so two notes with the same name anywhere in the vault are a hazard. With "Automatically update internal links" on, Obsidian may rewrite syllabus links to the wrong copy and rename the syllabus. This happened on 2026-10-03 when an unzipped student package sat inside the vault. The fix was to delete the copies, restore the links and rename the syllabus. `package` therefore writes zips only and leaves no unzipped folder in the vault. Do not unzip student packages inside the vault.
- `Tool reports/` holds generated reports and can be deleted at any time.

## Student packages

`coursenotes package` writes two zips into the course folder:
- `Student update <date>.zip` for students who already have an earlier setup: a README, the student syllabus, the instructor literature notes in their own folder, and the templates. The instructor notes go in a separate dated folder so they never replace notes students wrote themselves.
- `Student starter vault <date>.zip` for students who are starting fresh: empty working folders, the course folder, the instructor literature notes, the templates and the setup guide.

The student syllabus replaces `zotero://` links with DOI or URL links, since Zotero item links work only in the library that holds those item keys. Items with no URL say "see the Zotero collection". Instructor literature notes have the `zotero:` frontmatter blanked and the "Open in Zotero" link removed.

The student guide (`Student setup guide/STUDENT SETUP GUIDE - ED 336.md`) covers installing Zotero and Obsidian, the folders and plugins, the templates, and how to make literature, permanent, synthesis and project notes. It was written for ED 336 and mentions that course by name, so copy it and change the course-specific parts for another course. It has not been tested on a fresh install.

## Zotero updates for students

Importing a new RDF into a library that already holds the earlier import creates duplicates, because Zotero does not de-duplicate on import. The guide gives two options:
1. In Zotero, right-click the old collection, choose "Delete Collection and Items...", then import the new RDF. This is simplest for students who did not add their own annotations.
2. Rename the old collection, import the new RDF, then use Duplicate Items to merge in bulk (the older item is kept as master, so annotations survive).

A shared group library avoids duplicates but counts against the owner's storage, and the free allowance is 300 MB.

## Size of the readings export

Export the course collection only (right-click the collection, Export Collection, Zotero RDF, "Export Files"). For ED 336 the 49 syllabus items came to about 106 MB across 305 files. A 5 GB export means the scope was wrong (whole library or an older large collection). Large items are saved web snapshots (`.html`) and duplicate PDFs. Delete duplicate attachments and unneeded snapshots before exporting. Posting PDFs to students also raises a copyright question to settle before using Canvas.

## Report checklist for each new course

Read these before telling students the setup is final.
- `match`: zero differences, no unmatched readings
- `hygiene`: no flagged records
- `verify`: every mismatch resolved or understood
- `link`: zero changes on a second run
- `check`: only expected items without Zotero records
- Zotero collection equals the syllabus readings (count and titles)
- `python3 -m unittest discover -s tests` passes in `Tools/coursenotes`
- Student zips unpacked in a scratch folder outside the vault and opened in a clean Obsidian vault

## Known gaps

- The Dataview queries in the synthesis and project templates are untested in a real vault.
- The student guide and starter vault have not been run on a clean machine.
- `verify` depends on Crossref and DataCite being reachable. Items without a DOI are not verified.
- Class-note and scaffold formats follow ED 336 conventions. The `[classes] template` setting changes the class-note format.
- The tool README still lists an older folder name in places. The commands above are current.

## Using this skill in a Claude session

Give Claude the course folder path and ask it to run the workflow above with the Python tool, report the output of each step, and stop before any `--write` until the dry-run report has been read. Claude should not rewrite syllabus text, literature notes or Zotero data by hand where a tool command exists.
