# Second Reader sample vault

A starter Obsidian vault for the [Second Reader](https://github.com/kevinmil54/second-reader-obsidian-promote) literature-note workflow, set up the way I set up vaults for my own courses, with a four-week sample course, SR 101: Thinking With Machines, built on eight openly licensed readings about how people interact with large language models. All the PDFs are included.

Use it to try Second Reader before setting up your own course, or as a starting point for one.

## What's here

```
second-reader-sample-vault/        open this folder in Obsidian
  READ ME FIRST.md
  Home.md
  STUDENT SETUP GUIDE - SR 101.md
  How was GenAI used in the preparation of these materials.md
  Classes/
    Lesson flow schematic.md       the five planning phases the Instructor notes follow
    SR 101 example/
      SR 101 changes for next time.md   changes to make the next time the course is taught
      Winter 2027/                 one folder per offering of the course
        Syllabus - SR 101 Thinking With Machines - student copy.md
        SR 101 - Course home.md
        Meeting notes/             one note per class, pulling goals, questions and readings from the syllabus
        Planning/                  one folder per class with the instructor's planning note, for that day's materials
  Literature notes/                one note per reading, linked to the reader's own Zotero copy
  Authors/                         one note per lead author: short bio, links, and a photo linked from their own page
  Images/                          figures from the papers (one folder per reading), and from Zotero highlights
  Permanent notes/  Synthesis notes/  Projects/  Inbox/  Uploads/
  Tools/make_literature_notes.py   makes the literature and author notes from a Zotero RDF export,
                                   using the author details and figure lists in Tools/
  Templates/                       literature, permanent, synthesis, project, course offering, and student and instructor class meeting templates
  .obsidian/                       Second Reader, Dataview, Templater and Style Settings plugins,
                                   AnuPpuccin theme and settings; no personal data
  Second Reader Sample Readings (Zotero)/
    Second Reader Sample Readings (Zotero).rdf   Zotero collection file, pointing at files/
    files/                         the PDFs, all openly licensed, plus snapshots of some article pages
  SOURCES.md                       every reading with its license
```

## Getting started

1. Download a release (version 1.1: https://github.com/kevinmil54/second-reader-sample-vault/archive/refs/tags/v1.1.zip) or the latest version (green **Code** button → **Download ZIP**, or **Use this template** to make your own copy), and unzip it.
2. Import the Zotero collection in `Second Reader Sample Readings (Zotero)`, following its README.
3. Open the unzipped folder itself in Obsidian with **Open folder as vault**, trust the plugins, and follow `READ ME FIRST`.

You need Obsidian, Zotero 7 and the Better BibTeX plugin for Zotero. Second Reader, which is in Obsidian's community plugin directory, comes installed in the vault. It runs on desktop only.

## The sample course

| Week | Topic | Readings |
|---|---|---|
| 1 | Confidence, effort, and critical thinking | Lee et al. (2025); Gerlich (2025) |
| 2 | Learning when the machine has the answers | Zhai et al. (2024); Jose et al. (2025) |
| 3 | Ease, depth, and sameness | Stadler et al. (2024); Doshi & Hauser (2024) |
| 4 | Who makes the judgment calls | Buçinca et al. (2021); Sharma et al. (2025) |

Full references and licenses are in [SOURCES.md](SOURCES.md).

## Using it for your own course

Replace the syllabus, course home and meeting notes with your own. Then:

1. In Zotero, export your course collection with **Export Collection… → Zotero RDF**, checking **Export Files**.
2. Make the literature and author notes from it:

   ```
   python3 Tools/make_literature_notes.py --rdf "path/to/Your Course.rdf" --vault .
   ```

   Each note carries the reading's citation key from your Zotero, so after your students import the same RDF, **open pdf** and highlight sync find their own copy. Add author bios with `--authors authors.json` (format in the script's header).
3. For the syllabus, keep a master copy with your own Zotero links and run **Second Reader: Make class copy of syllabus**. The plugin README's "For instructors" section has the details.

## Licenses

The notes, syllabus, templates and CSS snippet are CC BY 4.0. The readings keep their own open licenses (see SOURCES.md). The bundled plugins and theme keep their own licenses: Second Reader, Style Settings and AnuPpuccin are GPL-3.0, Templater is AGPL-3.0, and Dataview is MIT. See [LICENSE.md](LICENSE.md).
