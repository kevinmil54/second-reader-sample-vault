---
name: student-materials-second-reader
description: Prepare and post what students need to take reading notes in Obsidian with the Second Reader plugin — the readings file for Zotero, the student copy of the syllabus, the templates and the Canvas announcement — and keep syllabus links working when the syllabus changes. Use after course setup, whenever the syllabus or readings change, or when meeting notes show syllabus embeds as "not created yet".
type: skill
created: 2026-10-04
source course: ED 359 Fall 2026
---

# Student materials for Second Reader

## What this does

Students import the course readings into their own Zotero, put a student copy of the syllabus in their Obsidian vault, and make literature notes with the Second Reader plugin. In the student copy, each reading's "open pdf" opens the student's own PDF, and its "Literature note" link is colored by progress (dimmed = no note yet, yellow = highlights synced, green = written in). This skill covers making those files, checking them and posting them.

It follows the `course-setup-coursenotes` skill, which builds the syllabus links, literature notes and meeting notes.

## What students get

| File | Made by | Students do |
|---|---|---|
| `<Collection>-<date>.zip` (readings) | Zotero export, then zipped | Unzip, then Zotero → File → Import…, pick the `.rdf`, choose "Copy files to the Zotero storage folder" |
| `<Syllabus name>.md` (student copy) | Second Reader: "Make class copy of syllabus" | Put it anywhere in their vault, replacing any older copy |
| `Second Reader templates.zip` | The four templates (literature and permanent from the plugin repo; synthesis and project from the vault's `Templates/`) | Only for first-time setup |
| `<Course> starter vault <date>.zip` | Built by Claude (see below) | New students open the unzipped folder as their vault |
| `<Course> update <date>.zip` | Built by Claude (see below) | Students already set up: replace the syllabus, add meeting notes they lack |
| Announcement text | Claude drafts, the instructor edits | — |

Setup guide (first time): https://github.com/kevinmil54/second-reader-obsidian-promote/blob/main/STUDENT-SETUP-GUIDE.md
Update instructions (already set up): https://github.com/kevinmil54/second-reader-obsidian-promote/blob/main/UPDATING.md

Make a folder outside the vault for each posting, e.g. `~/Desktop/<Course> - files for students (<date>)/`, and put the files there plus an `Instructor checklist.md`.

## Students' vault structure

Five top-level folders, with these exact names (the plugin's defaults, the import format and the templates assume them):

| Folder | Holds | Template |
|---|---|---|
| `Templates` | the four templates | — |
| `Literature notes` | one note per reading, made by Second Reader's Zotero import, named by title | `Literature Note Template - Zotero Import.md` |
| `Permanent notes` | one idea per note, created by checking a candidate box | `Permanent Note Template.md` |
| `Synthesis notes` | permanent notes on one topic gathered, plus what the student now thinks | `Synthesis Note Template.md` (Dataview list) |
| `Project notes` | the argument-and-evidence framework for a paper or talk | `Project Template (student).md` (Dataview table) |

The flow is Literature note → Permanent notes → Synthesis note, with Project notes drawing on permanent notes. A permanent note's Connections section links to the Synthesis and Project notes that use it. Synthesis and Project templates need the Dataview plugin. The course's own material goes in `Classes/<Course> <Term>/` (syllabus, course home, `Meeting notes/`).

There are no Structure, Evergreen, Attachments or `Projects` folders. Older guides and starter vaults (before Oct 4, 2026) named some of those; correct them if they turn up.

## Rule 1: give the syllabus one name for the whole term

Name the master syllabus without a date, e.g. `Syllabus - ED 359 Growing Up in School - F26`, and keep the date in its `syllabus-version:` frontmatter line.

Why: meeting notes, the course home and planning notes link to and embed the syllabus by file name. A dated name (`… 10-03`, then `… 10-04`) breaks every one of those links on each revision; the embeds then show "not created yet", and clicking one creates an empty note of the old name in `Inbox/`. If a rename is needed, do it inside Obsidian so it updates the links, then update `syllabus =` in `coursenotes.toml` by hand (Obsidian doesn't edit non-note files).

The student copy is posted under the **same name** as the master, so links in student meeting notes resolve and each new posting replaces the old one.

## Rule 2: Zotero titles are the note names

Second Reader names literature notes by the reading's title (`Literature notes/{{title}}.md`), and the syllabus finds a student's note by that title. So before exporting:
- remove trailing periods from Zotero titles;
- fix any title typos in Zotero, not only in the syllabus.

The import replaces `:` `"` `<` `>` `|` with " - " and `*` `?` with a space; the class-copy command applies the same rules, so links still match. Students whose notes are named by citekey get an offer from the plugin to rename them by title.

## Workflow

1. **Finish the master syllabus** (readings, framework links, `syllabus-version`). Run `coursenotes check` if the readings changed.
2. **Make the student copy.** Open the master syllabus in Obsidian, Cmd+P, "Second Reader: Make class copy of syllabus". It writes `<name> - student copy.md` next to the master and reports how many Zotero links it rewrote (should equal the number of readings with PDFs) and how many literature-note links it repointed. Move it to the posting folder and rename it to the master's exact name (drop " - student copy"). Rename outside the vault, since the master already has that name inside it. Don't edit the copy; edit the master and run the command again.
3. **Export the readings.** In Zotero, right-click the course collection → Export Collection… → Zotero RDF, check "Export Files", leave notes off. Save it **outside the vault** (an export inside the vault shows its PDFs in Obsidian and can create duplicate note names). Zip the folder. Students' imported collection is named after the file, so use a readable name like `<Collection>-<date>`.
4. **Check** (below), then **write the Instructor checklist and announcement**.
5. **Post to Canvas.** Upload the files to Canvas Files (a 50 MB readings zip may be too large for an announcement attachment). Post the announcement with links to the files. For later revisions, upload with the same file name and choose **Replace**, so existing links keep working.
6. **Clean up.** Delete or move the Zotero export folder; delete any empty syllabus notes in `Inbox/` created by clicking broken links.

## Starter vault and update package

**Starter vault** (new students): the five folders above (empty except `Templates`, which has the four templates), `Classes/<Course> <Term>/` with the student copy of the syllabus, the course home and the student meeting notes, and a `READ ME FIRST.md`. **Never include instructor literature notes**: they have the same names as the notes students will make, so the syllabus links would find the instructor's notes instead of theirs (wrong progress colors, "open pdf" failing). Include a preconfigured `.obsidian` folder so students skip section 4 of the guide (except 4h). When they open the folder as a vault and click "Trust author and enable plugins", everything is set up:
- `community-plugins.json`: `obsidian42-brat`, `second-reader-promote`, `dataview`, `obsidian-style-settings` (nothing else; the instructor's personal and AI plugins stay out)
- `plugins/<id>/`: `main.js`, `manifest.json` and `styles.css` copied from the instructor's vault (Second Reader from the repo build)
- Second Reader `data.json`: import format named "Literature Note", output `Literature notes/{{title}}.md`, template `Templates/Literature Note Template - Zotero Import.md`, APA, open notes after import; promote to `Permanent notes` with `Templates/Permanent Note Template.md`
- BRAT `data.json`: only `kevinmil54/second-reader-obsidian-promote`, unfrozen, so it updates at startup; no token
- Style Settings `data.json`: only the `anuppuccin-theme-settings@@` keys from the instructor's
- `themes/AnuPpuccin/`, `appearance.json` (AnuPpuccin, light, accent `#8b6df0`, snippet `sr-candidate-tag-color`), `snippets/sr-candidate-tag-color.css`, `templates.json` (folder `Templates`)
- No `workspace.json` and no paid or personal-use-only snippets (Nick Milo's Pro callouts, TfTHacker's Cornell CSS)

Check it by loading the plugin with that `data.json` in the Node harness: the "Literature Note" command should exist.

**Look kit** (students already set up): `How to make Obsidian look like the class setup.md`, `AnuPpuccin settings.json` (the same Style Settings keys, pasted into Style Settings → Import), and `sr-candidate-tag-color.css`.

**Update package** (students already set up): `READ ME FIRST.md`, the student syllabus, the meeting notes (add only ones they don't have — never replace a note they've written in), and the templates. The readings zip is separate and shared by both groups. For small Zotero corrections (a title fix), tell existing students to edit the item in their own Zotero rather than re-import — re-importing creates duplicates and deleting the old collection loses their highlights.

Build both in the scratchpad, zip with `zip -rX` (no `.DS_Store`), and never unzip them inside the vault. The older `coursenotes package` zips don't follow these rules, so don't post them.

## Checks Claude runs before posting

- **Student syllabus:** number of `obsidian://second-reader?open-pdf=` links equals the readings with PDFs; every literature-note link matches the name a student's import will give that note (computed from the note's `title:` frontmatter); no `zotero://` links left.
- **Readings export:** every syllabus reading present; every attachment's file present; no Zotero notes; PDFs byte-identical to the originals in `~/Zotero/storage` (so the instructor's highlights are not shared). Extra non-syllabus items, web snapshots and full-text files are harmless but worth listing.
- **Links to the syllabus:** in the course folder, nothing still links to an old syllabus name, and every embedded section (`#^wNN-goal`, `#^wNN-questions`, `#^wNN-readings`, headings) exists in the current syllabus.
- **Starter vault zip** (if posting one): its syllabus is the student copy under the master's name, and its meeting notes link to that name. Rebuild it with `coursenotes package` after any rename.

When editing course notes in bulk, back them up to the scratchpad first and confirm by diff that only the intended text changed. Keep searches inside the course folder; don't grep the whole vault.

## Announcement outline

- One line on who it's for (students taking notes in Obsidian instead of reaction papers).
- What's new, if the plugin changed (link to the update report in the repo).
- Files and what each is for.
- First-time setup → setup guide link; already set up → update instructions link.
- Then: import the readings (skip if already imported this term); put the syllabus in the vault, replacing the old one; click Update template / Rename if Obsidian asks.
- Where to get help (troubleshooting section of the guide, office hours).

## Later in the term

- **Syllabus edited:** run the class-copy command again, rename, replace the Canvas file, short announcement.
- **New readings:** export only the new items into a new readings file; students import it the same way. Re-importing the whole collection creates duplicates in students' Zotero.
- **Plugin updated:** students update through BRAT (see UPDATING.md); the plugin offers template and note-name fixes on startup.
