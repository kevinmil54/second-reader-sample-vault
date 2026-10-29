# Second Reader sample vault

A starter Obsidian vault for the [Second Reader](https://github.com/kevinmil54/second-reader-obsidian-promote) literature-note workflow, with a six-week sample course, SR 101: Thinking With Machines, built on eleven open-access readings about how people interact with large language models.

Use it to try Second Reader before setting up your own course, or as a starting point for one.

## What's here

```
Sample Vault/                 open this folder in Obsidian
  Start here.md
  Classes/SR 101 - Thinking With Machines/Sample term/
    Syllabus - student copy.md
    Meeting notes/            one note per class meeting
  Literature notes/           empty; Second Reader's import fills it
  Permanent notes/
  Synthesis notes/
  Project notes/
  Templates/                  literature, permanent, synthesis, project and meeting-note templates
  Attachments/
  Uploads/
  .obsidian/                  Second Reader plugin included, no personal settings
Readings for Zotero/
  SR 101 readings.ris         references for Zotero, pointing at files/
  files/                      PDFs whose licenses allow redistribution
  fetch_readings.py           downloads the others to your own computer
SOURCES.md                    every reading with its license
```

## Getting started

1. Download this repository (green **Code** button → **Download ZIP**, or **Use this template** to make your own copy) and unzip it.
2. Fetch the readings and import them into Zotero, following `Readings for Zotero/README.md`.
3. Open `Sample Vault` in Obsidian with **Open folder as vault**, trust the plugins, and read `Start here`.

You need Obsidian, Zotero 7 and the Better BibTeX plugin for Zotero. Second Reader runs on desktop only. The full setup guide is [STUDENT-SETUP-GUIDE.md](https://github.com/kevinmil54/second-reader-obsidian-promote/blob/main/STUDENT-SETUP-GUIDE.md) in the plugin repository.

## The sample course

| Week | Topic | Readings |
|---|---|---|
| 1 | What people use AI assistants for | Tamkin et al. (2024), Clio; Steyvers et al. (2025) |
| 2 | Confidence, effort, and critical thinking | Lee et al. (2025); Gerlich (2025) |
| 3 | Learning when the machine has the answers | Bastani et al. (2025); Zhai et al. (2024) |
| 4 | Writing, memory, and metacognition | Kosmyna et al. (2025); Fan et al. (2025) |
| 5 | Sameness and companionship | Doshi & Hauser (2023); Fang et al. (2025) |
| 6 | Who makes the judgment calls | Herdağdelen et al. (2026) |

Full references and licenses are in [SOURCES.md](SOURCES.md).

## Using it for your own course

Replace the syllabus and meeting notes with your own. For your students, keep a master syllabus with your own Zotero links, run **Second Reader: Make class copy of syllabus**, and give them the student copy along with a Zotero RDF export of your readings. The plugin README's "For instructors" section has the details.

## Licenses

The notes, syllabus and templates are CC BY 4.0. The readings keep their own licenses (see SOURCES.md). The bundled Second Reader plugin is GPL-3.0. See [LICENSE.md](LICENSE.md).
