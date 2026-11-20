---
title: Instructor guide
tags: [teaching]
---

This is the instructor version of the Second Reader sample vault. It has everything in the student version (the sample course SR 101, eight openly licensed readings, literature notes, author notes and templates) plus what an instructor uses to plan and run the course:

- the master syllabus, with Zotero links, and the student copy Second Reader makes from it
- a planning note for each class (`Planning/Class NN …/Class NN … - Instructor.md`) and the five-phase planning workflow ([[Lesson flow schematic]])
- templates for setting up a course offering and its class meetings
- the Claude skills I use for lesson planning, agendas, board plans, term reports and course setup ([[Skills/README|Skills]])
- `Tools/coursenotes`, a Python tool that links a syllabus to Zotero and makes literature and class notes
- a [[Projects home]] page, with the project and project-letter templates

The student version is on the repository's `main` branch. Give that one to students.

## 1. Set up

1. Unzip the vault somewhere that is not inside another vault, open Obsidian, choose **Open folder as vault**, and select the unzipped folder.
2. Choose **Trust author and enable plugins**. Second Reader, Dataview, Templater and Style Settings are installed and update from Obsidian's community plugin directory.
3. In Settings > Second Reader, click the download button next to **PDF utility**.
4. Install Zotero 7 and the Better BibTeX add-on, then import `Second Reader Sample Readings (Zotero)` (its README has the steps). Part 3 of [[STUDENT SETUP GUIDE - SR 101]] covers Zotero in more detail.

## 2. How the course is laid out

```
Classes/
  Lesson flow schematic.md
  SR 101 example/                      one folder per course
    SR 101 changes for next time.md    notes for the next offering
    Winter 2027/                       one folder per offering
      Syllabus - SR 101 Thinking With Machines.md               master, with your Zotero links
      Syllabus - SR 101 Thinking With Machines - student copy.md made by Second Reader; give this to students
      SR 101 - Course home.md
      Meeting notes/                   one student-facing note per class
      Planning/Class NN - date/        everything you make for that class
```

Each class meeting has two notes. The student note (in `Meeting notes`) shows that week's goal, questions and readings, pulled from the syllabus by block links, and has room for students' own notes. The instructor note (in `Planning`) has the same material plus the planning phases as checklists, the files made for the class, and what to change next time.

## 3. The syllabus

Keep one master syllabus with your own Zotero links. In the sample, each reading line looks like this:

```
- Zotero: [open pdf](zotero://select/items/@lee2025) · Literature note: [[Title of the reading]]
```

`zotero://select/items/@citekey` opens the item in your own Zotero (Better BibTeX resolves the citation key). Those links only work on your computer, so students get a copy:

1. Open the master syllabus.
2. Run **Second Reader: Make class copy of syllabus** from the command palette.
3. Second Reader writes `… - student copy.md` next to it. Each Zotero link becomes an **open pdf** link that opens the student's own copy of the reading through their literature note, and each week gets a **Package my Week N literature notes for upload** link.

Edit only the master, and make the copy again after each change. Students put the student copy in their own vault. Links to literature notes in it are colored by each student's progress: no note yet, note made, highlights synced, or written in.

**Go to the next class session in this syllabus** (give it a hotkey) jumps to the week that meets next.

## 4. The readings and literature notes

For your own course:

1. In Zotero, right-click the course collection, choose **Export Collection…**, pick **Zotero RDF**, check **Export Files**, and leave notes and annotations unchecked. Zip the result for students.
2. Make the literature and author notes from that export, either with `Tools/make_literature_notes.py` (see README.md) or with `Tools/coursenotes` and the [[course-setup-coursenotes-SKILL|course setup skill]].
3. To send students new or revised notes during the term, give them a folder with a `Literature notes` folder in it. They run **Second Reader: Bring in course update**, which adds new notes and replaces only notes they haven't started.

## 5. Planning a class

The planning workflow has five phases: read and analyze the readings, write the lesson plan (and revise it after students' reaction papers), make the student agenda, make the slides and handouts, then fill in the student note. After class, compare what happened with what you predicted.

To do this with Claude, give it the [[lesson-planning-SKILL|lesson-planning skill]] and point it at the class's instructor note, for example: "Do Phase 1 and Phase 2 for SR 101 Class 02." The skill writes into the class's Planning folder and ticks the phase checkboxes in the instructor note. [[class-agenda-SKILL]] and `Skills/agenda_md_to_pdf.py` make the one-page agenda; [[japanese-lesson-plan-SKILL]] adds anticipated student responses and a board plan.

To set up a new offering, run Templater's **Create new note from template** with `Course Offering Template`. It asks for the course, first class date, number of meetings and days between them, then makes the folders, the course home and a "changes for next time" note. Make each class's notes with the Class Meeting templates.

## 6. Collecting work

Students hand in a week's literature notes with the **Package my Week N** link in their copy of the syllabus. It zips the notes they've made for that week, with their name in the file name, and shows the zip so they can upload it.

## 7. Projects

[[Projects home]] lists your projects and the time you've spent on each. Its **➕ New project** link (or the command **Second Reader: New project**) asks for a category and a name and makes a folder with a project note and a project letter. The letter is a dated log written to your second reader. Click **▶️ Start** when you sit down to write and **🛑 Stop** when you finish; Stop shows the session's length and the project's total. Every session is saved in `Projects/project-time-log.csv`.

The categories are set in Settings > Second Reader > Projects, one per line. Add `| folder | template` to a line to give a category its own folder or template.

## 8. Permanent and synthesis notes

Checking a box under **Permanent note candidates** in a literature note makes a permanent note and turns the line into a link. If you type more after a promoted link and check the box again, the new text goes into that note instead of making a second one. When four permanent notes share a topic, Second Reader makes a synthesis note for it and keeps a list of the permanent notes you haven't used there yet.

## More

- Plugin documentation: https://github.com/kevinmil54/second-reader-obsidian-promote (README and TUTORIAL)
- What students read first: [[READ ME FIRST]] in the student version, and [[STUDENT SETUP GUIDE - SR 101]]
