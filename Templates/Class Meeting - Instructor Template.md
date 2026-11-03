<%*
const course = await tp.system.prompt("Course", "SR 101: Thinking With Machines (sample course)");
const offering = await tp.system.prompt("Offering", "Winter 2027");
const num = String(await tp.system.prompt("Meeting number (e.g. 3)", "")).padStart(2, "0");
const date = await tp.system.prompt("Date (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD"));
const topic = await tp.system.prompt("Topic", "");
const base = `Class ${num} - ${date}`;
// File the note as <offering>/Planning/<base>/<base> - Instructor
let dir = tp.file.folder(true);
if (dir === "/") dir = "";
dir = dir.replace(/(^|\/)Meeting notes$/, "");
const at = dir.search(/(^|\/)Planning(\/|$)/);
let planning;
if (at >= 0) planning = dir.slice(0, dir.indexOf("Planning", at) + "Planning".length);
else planning = dir ? `${dir}/Planning` : "Planning";
const target = `${planning}/${base}`;
if (!app.vault.getAbstractFileByPath(target)) await app.vault.createFolder(target);
await tp.file.move(`${target}/${base} - Instructor`);
-%>
---
type: class-meeting-instructor
course: "<% course %>"
offering: <% offering %>
meeting: <% Number(num) %>
date: <% date %>
topic: "<% topic %>"
status: planning
student-note: "[[<% base %> - Student]]"
topics: []
tags: [teaching, class-meeting]
---

# <% base %>: <% topic %> (instructor)

Student note: [[<% base %> - Student]] · Syllabus: [[Syllabus - SR 101 Thinking With Machines - student copy|Syllabus]] · Workflow: [[Lesson flow schematic]]

## Syllabus text for this class
![[Syllabus - SR 101 Thinking With Machines - student copy#^w<% num %>-goal]]
![[Syllabus - SR 101 Thinking With Machines - student copy#^w<% num %>-questions]]

## Phase 1: Read and analyze
- [ ] Readings pulled; Zotero highlights imported to literature notes
**Readings and literature notes**
- 

**Key claims / quotes (with page numbers)**
- 

**Hatsumon (questions that open the reading up)**
- 

**Predicted student reactions** (confusions, objections, what will resonate)
- 

## Phase 2: Lesson plan
- [ ] Draft plan reviewed
**Learning aim for today (one sentence)**


**Segments** (numbered, with times; discussion questions in italics)
1. (0:00) Opening question: 
2. 
3. (last 10 min) *What did you learn today...*

**Link to previous meeting / student feedback to use**
- 

## Phase 3: Student agenda
- [ ] Agenda made · file: 

## Phase 4: Slides
- [ ] Slides made · file: 
- [ ] Speaker notes done

## Student note
- [ ] Student note filled in: readings, agenda, links, discussion prompts
- [ ] Shared with students

## Phase 5: Post-class analysis
- [ ] Transcript or class notes gathered
- [ ] Document A: Instructor analysis · file: 
- [ ] Document B: Student summary · file: 
- [ ] Document C: Future lesson plan · file: 

**What happened vs. predicted**
- 

**What worked / didn't**
- 

**Student feedback / learning summaries**
- 

**Change for next time / carry into next meeting** (also add it to the course's "changes for next time" note)
- 

**Ideas worth keeping** (promote to permanent notes): 
