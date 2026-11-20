---
title: Skills
tags: [skills]
---

These are the Claude skills I use to plan and run classes and to work on projects in this vault. Each one is a set of instructions that tells Claude how to do one job the way I do it. They were written for my own courses and adapted here for the sample course, SR 101. Expect to edit them for yours: class length, discussion conventions, course numbers and your name in the slide header.

## The skills

| Skill | What it does |
|---|---|
| [[lesson-planning-SKILL]] | The whole planning cycle for one class: reading analysis and the key question (hatsumon), the lesson plan, the plan revised after students' reaction papers, the student agenda, the slide deck, and post-class analysis of a transcript. It works inside this vault, with one Planning folder per class and the instructor note from `Templates/Class Meeting - Instructor Template.md`. |
| [[class-agenda-SKILL]] | A one- or two-page student agenda for a class. `agenda_md_to_pdf.py` turns the markdown agenda into a PDF. |
| [[japanese-lesson-plan-SKILL]] | Turns a lesson plan into lesson-study format: anticipated student responses, teacher moves beside them, and a board plan. The blank board-plan sheets are in `bansho-templates/`. |
| [[term-feedback-workflow-skill]] | A report on a whole term's teaching from transcripts of classes early and late in the term. |
| [[course-setup-coursenotes-SKILL]] | Sets up a course's readings from the syllabus: checks citations, makes literature notes and class notes, and builds update packages for students. Most of the work is done by the Python tool in `Tools/coursenotes`. |
| [[student-materials-second-reader-SKILL]] | Prepares what students need: the readings file for Zotero, the student copy of the syllabus, the templates, and an announcement. |
| [[new-project-SKILL]] | Starts a project: a folder in `Projects`, a project note and a project letter. Second Reader's **New project** command does the same thing without Claude. |
| [[place-notes-in-project-outline-SKILL]] | Puts links to permanent notes under the points of a project note's outline. |
| `literature-note.skill` | Fills in a literature note from an article, with page numbers for quotes. It was written for an earlier version of the literature-note template. |

## Using a skill with Claude

A skill is a markdown file with a short description at the top that says when to use it. You can give one to Claude in either of two ways:

- Attach the file to a conversation, or add it to a Claude project's files, and ask for the job it describes ("Plan Class 02 using the lesson-planning skill").
- Install it as a skill in Claude, so Claude uses it whenever a request matches its description. A skill installed this way is a folder holding a file named `SKILL.md`. `literature-note.skill` is already packaged that way.

The skills read and write files in this vault, so they work best when Claude can reach the vault folder on your computer.

## Programs the skills use

- `agenda_md_to_pdf.py` needs Python 3 and WeasyPrint (`pip install weasyprint`).
- Slides from the lesson-planning skill are Quarto files that use the clean-revealjs theme.
- `Tools/coursenotes` is installed with `pip install -e Tools/coursenotes` from the vault folder. Its README has the commands.
