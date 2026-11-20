---
type: map
created: 2026-04-23
updated: 2026-10-15
name: lesson-planning-workflow
description: "Multi-phase lesson planning workflow for university courses. Use when the user asks to plan a class session, generate an agenda, create slides, or analyze a class transcript against a lesson plan. This skill covers the full cycle: reading analysis → lesson plan → student agenda → slides → post-class analysis. The user may invoke any single phase or the full sequence. Incorporates principles from Japanese lesson study (jugyō kenkyū) adapted for university teaching, including hatsumon (key question), anticipated student thinking, and matome (consolidation). Written for seminar courses and adaptable to others. Phase 3 (student agenda) produces a markdown source file plus a one-page WeasyPrint PDF in the three-column time | title | details format, rendered with Skills/agenda_md_to_pdf.py. The phases are run inside the vault: one Planning folder per class, an instructor note with phase checkboxes, and a student note (see the vault workflow section)."
---

# Multi-Phase Lesson Planning Workflow

The course this planning is for, its meeting time and its length come from the syllabus, which is attached or is in the vault under `Classes/<course>/<offering>/`. The sample vault's course is SR 101: Thinking With Machines (`Classes/SR 101 example/Winter 2027/`). The skill was written for 170-minute weekly seminars; scale segment times to your own class length.

## Overview

This skill implements a multi-phase workflow for planning, delivering, and reflecting on university class sessions. Each phase produces a specific artifact. The phases are designed to be used sequentially but can be invoked independently.

The workflow incorporates selected principles from Japanese lesson study (jugyō kenkyū), adapted for university teaching:

- **Hatsumon (発問)**: Identifying the key question that drives student thinking for the session
- **Kyōzai kenkyū (教材研究)**: Deep analysis of readings as teaching materials — not just what they say, but how students will read them
- **Anticipated student thinking**: Specific predictions about how students will respond — what they'll say, what they won't say, and what would indicate deep vs. surface engagement
- **Kikan-shido (机間指導)**: Purposeful observation during student work to inform subsequent teaching moves
- **Neriage (練り上げ)**: Orchestrating comparison and synthesis of student ideas through structured discussion
- **Matome (まとめ)**: Planned consolidation at the end of the session — the closing question is a fixed element, not an afterthought
- **Research question**: The instructor's own inquiry about teaching, connecting content expertise to pedagogical questions

These principles are embedded in the workflow without requiring Japanese terminology in the outputs (unless the instructor requests it).

---

## Example: a discussion-only seminar

Some seminars have discussion conventions that should be followed consistently across all phases. These are the ones from one of the author's seminars; replace them with your own course's conventions, or delete this section:

- **No pair work or small-group breakouts.** Discussion is whole-class throughout.
- **No in-class writing prompts.** Students think and respond verbally; there are no written reflection exercises during class.
- **No weekly quizzes in the plan.** Any quiz system described in the syllabus does not appear in lesson plans or agendas.
- **Cold-call openings.** The instructor opens segments by calling on students directly rather than waiting for volunteers. Lesson plans should specify cold-call language.
- **Discussion is driven by student questions.** Students submit reaction papers and questions before class (via Canvas); these shape the session. The lesson plan should incorporate specific student questions as discussion anchors, not just as background.
- **Scope-challenging is a goal, not just content delivery.** For each major body of research, the lesson plan should plan explicitly for students to evaluate the scope and limits of the findings — not just receive them. Strong findings should be complicated; incomplete paradigms should be named as such.

## Vault workflow

This is how the phases are run inside an Obsidian vault set up for Second Reader. Use it as the default and adapt it to your course.

### Where things live

Course folder: `Classes/<course>/<offering>/` (in the sample vault, `Classes/SR 101 example/Winter 2027/`)

- `Planning/Class NN - YYYY-MM-DD/` is one folder per class. Everything made for the class goes in it, including the slides. Do not put the .qmd or the rendered slides in Talks.
  - `Class NN - YYYY-MM-DD - Instructor.md` is the working note (made from `Templates/Class Meeting - Instructor Template.md`).
  - `edNNN_weekN_agenda.md` and `EDNNN_WeekN_Agenda.pdf` (Phase 3).
  - `edNNN-weekNN-<topic>.qmd` and the rendered `.html` (Phase 4).
  - `Class NN - Handout - <name>.md` for each handout.
  - `Class NN - Lesson plan (print).md`, the printable plan.
  - `_extensions/grantmcdermott/clean/` and `mathjax-config.js`, copied from an earlier deck (see Phase 4).
- `Meeting notes/Class NN - YYYY-MM-DD - Student.md` is the student note.
- `Student notes/` holds literature notes that students wrote.
- The Course Offering template makes every class's folder, each holding its instructor note. If a class has none, create the folder when you start the class and move its note into it. Wikilinks resolve by file name, so moving files does not break them.

### Phase numbering in the instructor note

The instructor note uses these headings. They line up with the phases below as follows.

| Instructor note heading | This skill |
|---|---|
| Phase 1: Read and analyze | Phase 1 (1a to 1h) |
| Phase 2: Lesson plan | Phase 2 and 2b |
| Phase 3: Agenda (Document A) | Phase 3 |
| Phase 4: Slides (Document B) | Phase 4, plus handouts and the printable plan |
| Phase 5: Student note (Document C) | Fill in the student note (see Phase 3) |
| After class | Post-class analysis (Phase 5 below) |

Tick each checkbox as the step is done. Add `[completion:: YYYY-MM-DD]` where the template has it. Link the files made, using a wikilink for notes and PDFs and a code-formatted path for the .qmd and .html.

### Working rules

1. Say which phases are being done and what the output is before starting. Set up a task list. The last task is checking: facts against their sources, page numbers, arithmetic, and a look at the rendered output.
2. Before editing an existing instructor or student note, copy it to a backup outside the vault. Edit it in place, not as a new file.
3. When the instructor adds material in the middle of a task (a figure, a story, a study), add it everywhere it belongs in one pass: the instructor note resources, the slides with footnotes, the speaker notes, and the printable plan. Then report what was added and what is still unverified.
4. Fix errors in the plan when you find them and say so. Class 06 had a wrong figure in the plan note (54 to 34 min/day) that was corrected from the Surgeon General graphic itself (60 to 20 min/day for time with friends). Check a number against the source graphic or table, not against an earlier note.
5. Do not state a reference as verified unless a source was opened. Crossref and OpenAlex rate limit (HTTP 429). When that happens, verify the DOI from the publisher or PubMed page. Anything still unconfirmed stays off the slide footnote and goes in the notes block as `[unverified, check before class]`.
6. Close each phase with a short list of open items for the instructor (unverified references, things that need a local render, timing risks, "Shared with students" still unchecked).

---

## Phase 1: Reading Analysis and Session Framing

### When to use

When the instructor provides readings, syllabus context, and/or prior session information and asks to begin planning a new session. This is the foundation — do this before generating a lesson plan.

### Inputs the instructor may provide

- Assigned readings (PDFs, articles, or summaries)
- Syllabus or course schedule (for situating the session)
- Prior session's lesson plan, transcript, or summary
- Notes about what the instructor wants to emphasize
- Student reaction papers (if available — see section 1g)

### What to produce

A single markdown document with these sections:

#### 1a. Session context

- Where this session sits in the course arc: what came before (concepts students have encountered), what comes after (where this session needs to lead)
- The conceptual move this session needs to accomplish — what should students think differently about afterward?
- Any unfinished threads from the prior session that need to be picked up

#### 1b. Reading analysis (kyōzai kenkyū)

For each assigned reading:

- **The author's argument in one sentence** — the instructor's reading, not a generic summary
- **2–3 passages students are likely to have noticed or reacted to** — what grabbed them, what resonated, what provoked. Include page numbers or section references. These are candidates for pull quotes on slides.
- **1–2 passages students probably skimmed but that are analytically important** — the dry table, the methodological caveat, the qualifying paragraph that changes the argument. These may need to be surfaced in class. Also candidates for pull quotes, but for a different reason.
- **What students are likely to misread or flatten** — where will their prior assumptions collide with the reading? Where will they read selectively?
- **Connections students won't make without help** — across readings, between readings and prior course content, between readings and their own experience
- **The intellectual difficulty of this reading** — where will students struggle not because the text is poorly written, but because the idea genuinely challenges their current mental models? What makes this content *inherently* difficult, not just dense?

#### 1c. Candidate pull quotes

For each reading, identify 3–5 passages (keep them short — a sentence or two) that could go on slides to anchor discussion. For each, note whether it's:
- A passage students likely noticed (use to validate and then deepen)
- A passage students likely missed (use to surface and complicate)
- A passage that crystallizes the reading's argument (use to anchor)

Record the page number for each passage, and once per reading record the full APA reference and a verified DOI or stable URL. Phase 4 uses these for slide footnotes.

#### 1c-2. Check the literature notes against the readings

Instructors and students work from the Zotero literature notes, so check them against the articles before using their numbers or page citations in class.

- Zotero highlights carry PDF page numbers. Journal pages are the start page plus the page-marker index in the markdown extraction (`{n}------` markers). Ainsworth's highlights on PDF pages 1, 3, and 4, for example, are journal pages 932, 934, and 935.
- Check each statistic in a literature note against the article. Class 06 found a note giving 59% secure for Hazan & Shaver Study 1 where the article gives 56%.
- Record each discrepancy in the instructor note under the readings, and use the article's number on slides.
- When a passage is used on a slide or in the plan, give the journal page. Re-check the page when a passage sits near a page break (the Hazan & Shaver self-selection passage was left flagged between pp. 517 and 518).

#### 1d. Hatsumon — the driving question

Propose 1–2 candidate hatsumon for the session. A good hatsumon:
- Creates productive tension rather than having an obvious answer
- Connects the readings to something students care about or have experienced
- Is specific enough to generate concrete responses, not just abstract discussion
- Could produce genuine disagreement among thoughtful students

Note: the hatsumon may or may not be the opening question. Sometimes the opening question *leads into* the hatsumon; sometimes it *is* the hatsumon.

#### 1e. Research question

Propose a research question for the session — something the instructor wants to learn about teaching this material. This is not a learning objective; it's a professional inquiry. Examples:
- "How do students move from personal anecdote to analytical framework when discussing [topic]?"
- "Does starting with the case study or the theoretical reading produce better discussion of [concept]?"
- "At what point in the session do students start connecting this week's material to prior weeks?"

#### 1f. Opening question

Propose an opening question that everyone can discuss — it should be low-stakes, personally accessible, and connected (directly or by analogy) to the session's intellectual territory. This may be the hatsumon itself or a warm-up that leads into it.

In a seminar, the opening question is typically put to the whole class via cold-call. Consider whether the best opening puts students in the experiential position of the research subjects (i.e., having them *do* or *notice* something before they discuss the findings about it).

#### 1g. Student reaction paper analysis

When student reaction papers or Canvas discussion posts are provided as inputs, analyze them in this section before the lesson plan is written. This section has two purposes: (1) identifying student questions worth incorporating into the lesson plan, and (2) sharpening the anticipated-thinking predictions in Phase 2.

For each submitted paper:
- **What is this student genuinely puzzling over?** Distinguish authentic intellectual difficulty from questions that sound good but don't reflect actual confusion.
- **What have they understood well?** Note framings, syntheses, or connections that are worth drawing on in class.
- **What have they misread, flattened, or stopped short of?** These are the points where discussion can push further.
- **Which of their questions are worth using in class, and where?** For each usable question, note where in the session it fits and why it's productive.

Then across all papers:
- **What patterns emerge?** Where do multiple students converge on the same reading (accurate or not)?

- **What important territory is no one asking about?** Gaps in student questions are as informative as the questions themselves — they reveal what hasn't registered yet.

- **How does this change the anticipated-thinking predictions?** The reaction papers are the most direct evidence available about what students actually think going into class. Update predictions accordingly.

State how many submissions were read against enrollment (Class 06: seven of about 15), and treat the patterns as partial. In the plan, name the students whose questions are used, with the page each question points to.

Students also write permanent-note candidates from the readings. Collect them into a one-page handout, `Class NN - Handout - Permanent note candidates.md`:

- Include the instructor's own permanent-note candidates from the instructor's literature notes for the week's readings, mixed in with the students' and not marked as the instructor's. Those notes are in the top-level `Literature notes/` folder. If a note there is a blank template while the syllabus link opens a filled-in one, a second copy with the same name exists somewhere in the vault (for example, an unzipped student package); bare `[[Title]]` links resolve to whichever copy Obsidian indexes first. Find the duplicate, move the content to `Literature notes/`, and get the duplicate out of the vault rather than working from it.
- No names on any candidate.
- Format: the title line (`# Class NN handout: Permanent note candidates`), the course and date line, then the candidates grouped by article under a bold author-year heading (`**Hebb (1946)**`), in syllabus order. Nothing else: no introduction, no instructions, no closing questions.
- Give every title in full. A promoted candidate's link (`[[short name|full title]]`) is truncated before the `|`, so take the text after it. If the full title runs to a paragraph, end it at the first complete sentence. No title ends with an ellipsis.
- Fix duplicated text left by repeated promotion (for example, a title repeated with `(2)`, `(3)` suffixes) and obvious typos, without changing the wording otherwise.

- #### 1h. Answers to predictable questions

  I want to be able to include some analysis of predictable questions:

  - "What's changed since then?"
  - Look at the information on the readings and see what you can find about how things (lives of children, environment, etc.) have changed since they were published (or since the research was done). "

  #### 

### Formatting

Output as a markdown file. Use headers (####) for subsections. Keep the whole document to something like 4–7 pages.

---

## Phase 2: Lesson Plan (Preliminary)

### When to use

After Phase 1 is complete (or when the instructor provides equivalent information). This produces the preliminary lesson plan *before* student reaction papers are available. If reaction papers are already available, proceed directly to Phase 2b.

### What to produce

A markdown document with these sections:

#### Header

- Session title
- Course, date, duration
- Hatsumon (the driving question)
- Research question

#### Timed segments

Each segment includes:
- **Segment number and title** with time allocation
- **Purpose** — what intellectual work this segment accomplishes in 1–2 sentences
- **Teacher moves** — the key question/prompt that launches the segment, specific language for cold-calls and transitions
- **Anticipated student thinking** — 3–5 specific, concrete predictions:
  - What students will likely say (with examples of actual language they might use)
  - What prior knowledge they'll draw on
  - What they'll miss or overlook
  - What response would indicate surface vs. deep engagement
- **Neriage moves** — how you'll orchestrate comparison of student responses: which positions to sequence, what contrasts to draw out, how to build toward synthesis
- **Scope challenge** (for segments presenting empirical research): What are the limits or boundary conditions of this body of work? How will you prompt students to evaluate scope rather than just receive findings?
- **Connection to next segment** — the transition or bridge

#### Segment structure conventions

- **Opening** (10–20 min in a long seminar): Low-stakes cold-call. 🟢 Protected. Consider whether the opening can put students in the experiential position of the research before they discuss it.
- **Middle segments** (variable): The intellectual core. Mix of instructor framing, cold-call discussion, pull quotes, video or case analysis, scope challenge. Tag each 🟢 🟡 or 🔴.
- **Matome / Closing reflection** (15–20 min in a long seminar): **Always the final segment. Always 🟢 Protected.**

  The closing has two components:

  1. **Brief synthesis (2–4 min)** — the instructor crystallizes the conceptual move of the session: not a summary of topics covered, but a statement of what intellectual territory was traversed and what the key distinction or reframing was.

  2. **Cold-call reflection** — the instructor poses the closing question and calls on 5–6 students:
     > *What did you learn today that is new to you, important for you, and/or worth remembering?*

  In the plan, specify:
  - What you hope students will say (tied to the hatsumon and session goals)
  - What would indicate surface vs. deep engagement
  - What would indicate the session didn't accomplish its purpose
  - The forward bridge to next week

#### Pacing tags

Mark each segment as one of:
- 🟢 **Protected** — happens no matter what
- 🟡 **Compressible** — can be shortened; note what to cut first
- 🔴 **Expandable** — can absorb extra time; note when to move on regardless

#### Hard time check

Note a specific time (roughly the 2/3 mark of the session) where the instructor should assess paging. Include a decision rule: "If you haven't started [segment X] by [time], compress/skip [segment Y]."

#### Session map

A table of segments with start times and durations.

#### Contingency notes

For each segment likely to stall or run over: a specific recovery move. These should be concrete (an alternative question, a redirect, a deliberate deferral to next week) rather than generic.

#### Instructor resources

Brief list of concepts, frameworks, examples, or outside material (historical anecdotes, cultural examples, analogies from other fields) the instructor may deploy during discussion. This is a memory aid, not a script. Include specific language where useful.

### Formatting

Markdown file, 4–6 pages for a long seminar (longer sessions warrant more detail). Use `###` for segment titles.

---

## Phase 2b: Revised Lesson Plan (After Student Reaction Papers)

### When to use

After student reaction papers have been collected (Canvas submissions, the evening before class) and analyzed in Phase 1g. This phase updates the preliminary plan with specific student questions and revised anticipated thinking.

### Additional inputs

- Student reaction papers (analyzed in Phase 1g)
- Instructor's priorities among student questions

### What to produce

A complete revised lesson plan incorporating:

#### Incorporated student questions

For 2–4 student questions selected from the reaction papers:
- Where in the session each question will be addressed
- How it connects to the readings or hatsumon
- Specific language for how you'll introduce the question in class (e.g., "Sunhyo raised a question that the readings don't directly address...")
- What makes it a productive question to discuss (why it opens territory rather than closing it)

#### Revised anticipated thinking

Update the anticipated-thinking sections for segments where student questions change the prediction. The reaction papers are direct evidence — use them. Note explicitly where a paper confirmed a prediction and where it revealed something unexpected.

#### What the papers reveal about gaps

Based on the reaction papers: what important material is no one asking about? These gaps often reveal what needs to be explicitly surfaced in class rather than assumed.

#### Everything else from Phase 2

Carry forward all sections. Mark changes from the preliminary plan where helpful.

### Formatting

Markdown file. No need to use strikethrough unless the instructor requests it — a clean revised document is more useful than a tracked-changes document.

Break (updated Nov 4, 2026): every lesson plan has a 10-minute break near the middle of the class, placed at a natural seam between segments and shown as its own row in the session map and in the agenda (and in the student note's agenda and the printable plan). Take the time from the later segments and say what was cut. Do not make a break slide in the slides. Also don't include metacognitive slides like "The Hinge" - don't call out the structure of the class. For the Matome, don't tell me to cold-call students - I ask as many to respond as are willing to.

---

## Phase 3: Student Agenda

### When to use

After the lesson plan is finalized (Phase 2 or 2b). Produces two files: a **markdown source file** for review and editing, and a **PDF** rendered from it with `Skills/agenda_md_to_pdf.py` (WeasyPrint, three-column layout, Chinese character support via Noto Sans CJK SC).

Always produce both. The markdown is for editing; the PDF is what gets distributed to students.

### What to produce

#### Step 1: Draft the markdown source

Write a markdown file with four sections in order:

**Header block:**
```
# [Course Number] — [Course Name]
## [Week N, Session N] · [Day, Month D, Year] · [Start–End time] · [Room]
### [Week Theme]
```

**Reading block** (if readings assigned for this session):
```
> **Reading for today:** [Author(s)] ([year]). [Title]. *[Journal/Book]*, [vol/pages].
> [Second reading on its own line, same format.]
```

**Agenda body** — parsed by `Skills/agenda_md_to_pdf.py`. One segment per blank-line-separated block:

```
9:00–9:10 · [Short title]
- bullet detail line
*Italic discussion question*
Plain note line

9:10–9:40 · [Next segment title]
- bullet
*Question*
```

Detail line types:
- `- text` → rendered as a bulleted line
- `*text*` → rendered in italics (use for discussion questions)
- Plain text → rendered as a normal note line

Section dividers (optional gray header rows in the PDF): `## SECTION LABEL`

**Footer block:**
```
---
closing: What did you learn today that is new to you, important for you, and/or worth remembering?
lookahead: [Label, e.g. "Looking ahead — Week 14"]
note: [One bridging sentence connecting today to next week's question.]
- [Author(s)] ([year]) — [Short title]
- [Author(s)] ([year]) — [Short title]
```

**What not to include:** instructor notes, pacing tags (🟢🟡🔴), the hatsumon label, the research question, anticipated student responses, or any facilitation cues.

Filename convention: `ed[NNN]_week[N]_agenda.md` — e.g., `sr101_week2_agenda.md`. No day in the name: the classes now meet once a week (changed Nov 4, 2026).

#### Step 2: Render to PDF

Run `Skills/agenda_md_to_pdf.py` on the markdown file:

```
python Skills/agenda_md_to_pdf.py edNNN_weekN_agenda.md EDNNN_WeekN_Agenda.pdf
```

It needs WeasyPrint (`pip install weasyprint --break-system-packages`). It reads the markdown format described above and produces the three-column layout (time | title | details) in Michigan blue, with the reading block above the table and the closing reflection and lookahead below. Check that the PDF is one page. If it spills onto a second page, tighten the details text before changing the CSS. The older `class-agenda-pdf` skill and its `agenda_pdf.py` are no longer used.

The same agenda goes into the student note, in an `## Agenda` section placed before `## Your notes`, followed by a `## Links` section for slides, handouts, and the PDF. Do not include facilitation cues in either place.

Save both files in the class's Planning folder and link them from the Phase 3 checkbox in the instructor note.

---

## Phase 4: Slide Deck

### When to use

After the lesson plan is finalized. Creates a Quarto-based reveal.js slide deck.

### What to produce

A `.qmd` (Quarto markdown) file that compiles to HTML slides and PDF using the `clean-revealjs` theme (Grant McDermott). The deck follows the conventions of the talk-planning skill (`Skills/talk-planning-skill-2026-09.md`). Its reference model is the talk deck `why-students-use-genai.qmd`, and Class 07 (October 14, 2026) was the first lesson deck built this way. The deck should:

- Match the lesson plan's segment structure, with one `#` section break per major segment
- Give every content slide a title
- Carry the skeleton on the slides and the teaching in the speaker notes
- Include pull quotes identified in Phase 1c, and figures from the readings where they exist
- Include the opening question and closing reflection as dedicated slides

### Slide conventions

**Slides carry the skeleton; notes carry the class.** Times, cold-call language, student questions behind a slide, neriage moves, scope challenges, transitions, and the instructor's own anecdotes all go in `::: {.notes}`. A slide with two lines and a long notes block is working as designed.

**Every content slide has a title.** Use a short descriptive title, even on quote slides ("What's wrong with anthropomorphism?", "Four identical pairs of stockings"). Untitled `## {.center}` is reserved for the closing slide.

**Section breaks.** Each major segment (usually one per reading or pair of readings) opens with a standalone section slide. It has no slide text; its notes block carries the segment's time, aim, and pacing tag.

```markdown
# Telling more than we can know {.center}

::: {.notes}
1:50–2:30. Aim: ... Hard time check at 2:45.
:::
```

Level-1 headings make vertical stacks in reveal.js. Arrow keys still move through every slide in order, so this needs no extra setting.

**Standard content slide.** A title, one or two lean lines, and an italic prompt in a `.question` span when the slide puts a question to the class.

```markdown
## A student's question {.center}

How much experience with someone do you need before you can read their emotions reliably?

[Does the chatbot you use have a baseline?]{.question}

::: {.notes}
...
:::
```

**Pull quote slide.** Title, blockquote, attribution with the footnote, and optionally a `.question` line. Add `.long-quote` to the slide classes for quotes longer than about 35 words; it shrinks the blockquote to 0.75em.

```markdown
## What's wrong with anthropomorphism? {.center .long-quote}

> "[Quotation.]"

::: {.attribution}
— Author (Year, p. N)^[APA reference. <https://doi.org/...>]
:::

[How would you tell a discovered similarity from an invented one?]{.question}
```

**Text and figure.** When a reading has a figure, table, or image worth showing, use two columns: the claim or excerpt on the left and the figure on the right. Put the footnote marker after the claim on the left, or on a `.source-line` below the columns when the left side is a dialogue or quotation.

```markdown
## People tell AI what they won't tell a person {.center}

:::: {.columns}

::: {.column width="50%"}
Guilty feelings went deeper with AI; sad feelings didn't^[APA reference. <https://doi.org/...>]
:::

::: {.column width="50%"}
![](images/kim2022_guilt_sad.jpeg)
:::

::::
```

Figures come from the paper-figure attachments the literature notes embed (`Attachments/<citekey>/<citekey> figNN.jpeg`). Copy them into an `images/` folder in the class's Planning folder with names that say what they show. Look at each image before using it; the caption in the literature note can be wrong (Class 07: the Kim et al. note labeled the guilt/sadness bar chart as the Replika instructions figure). Read any numbers for the notes off the figure itself. Add `{height="420"}` for tall images.

**Student question slides.** Title with the student's first name ("Sam's question", "Maria's example", "Li's note"), the question or claim as plain text, and a `.question` follow-up if there is one. No quotation marks unless the wording is verbatim; say in the notes when it is paraphrased.

**Statistics as rhetoric.** When a number is the point, put it in a `.big-num` (or `.big-num-muted`) div as the visual center of the slide, with a one-line label and a footnote.

**Chinese text.** Use a `.kaiti` span or div (ZCOOL KaiTi, loaded with a `<link>` tag) as in the talk skill, with pinyin and a one-line gloss, and the source in a footnote.

**Lookahead slide.** Titled "Next week: [topic]", with the driving question and a `.question` line. The readings go in the notes.

**Closing reflection slide.** Always the final slide, in the talk-deck format:

```markdown
## {.center}

*What did you learn today that is new to you, important for you, and/or worth remembering?*
```

Do not add a contact line ("Let me know at...") to the closing slide. The instructor asks the question in class.

**Do not** add a break slide, an agenda slide, or any slide that names the structure of the class. Don't put an HTML comment between the YAML header and the first slide; Quarto turns it into a blank second slide (Class 07).

### Citation footnotes (standard feature)

Any slide that draws on a specific source gets a footnote at the bottom of the slide with the full APA reference and a working link, so students can click through from a quote, finding, figure, or clip to the original. Build these in as the deck is written, not as a later pass.

#### Which slides get one

Footnote: pull quotes, findings and statistics, figures or tables taken or adapted from a paper, framework slides based on a specific author's model, and media slides (video, image, transcript excerpt).

Skip: the title slide, section breaks, the opening question, discussion prompts, student question slides, the lookahead slide, and the closing reflection. A discussion prompt that paraphrases a specific reading can take a footnote, but it's optional. Full-bleed `background-image` slides have no room; put the credit in the notes block instead.

#### Syntax

Use Pandoc inline footnotes (`^[...]`). Quarto collects them into an aside at the bottom of the slide and numbers them from 1 on each slide.

Pull quote slide:

```markdown
## [Short slide title] {.center}

> "[Short quotation from the reading.]"

::: {.attribution}
— Author (Year, p. N)^[Author, A. A., & Author, B. B. (Year). *Title of book*. Publisher. <https://search.worldcat.org/title/[OCLC number]>]
:::

::: {.notes}
...
:::
```

Finding slide:

```markdown
## Number names and early counting {.center}

U.S. and Chinese preschoolers counted equally well to 10. The gap opened in the teens.^[Miller, K. F., Smith, C. M., Zhu, J., & Zhang, H. (1995). Preschool origins of cross-national differences in mathematical competence: The role of number-naming systems. *Psychological Science, 6*(1), 56–60. <https://doi.org/10.1111/j.1467-9280.1995.tb00305.x>]
```

The first example is a format template. The second is a real, verified reference.

Rules:

- Put the marker at the end of the attribution line on pull-quote slides, or directly after the claim on other slides. Never inside the blockquote or the slide heading.
- The slide shows the short form (Author, Year, page for quotes). The footnote holds the full reference. Don't repeat the full reference on the slide itself.
- Footnote content is an APA 7 reference followed by the link. With more than three authors, first author et al. is fine to keep it to one or two lines.
- Write links as autolinks (`<https://...>`) so the URL is visible in the PDF version. Use `[label](url)` only when the URL is too long to be readable.
- One footnote per source, and no more than two or three per slide. A slide that needs more is probably two slides.
- For a reading used on several slides, repeat the footnote on each slide. Numbering restarts per slide, so there is no cross-slide referencing.

#### Which link to use

In order of preference:

1. DOI, written as `https://doi.org/...`
2. The publisher's or journal's stable article page
3. An open-access copy (PubMed Central, ERIC, PsyArXiv, arXiv, SSRN, OSF, an institutional repository)
4. For books: the publisher's page or the WorldCat record
5. For reports, news articles, and web pages: the original URL

#### Verification

Look up every DOI and URL (Crossref, the publisher's site, or a web search) before it goes on a slide. Never construct a DOI from memory. If the reference is confirmed but no link can be verified, give the reference without a link and put `[unverified link — check before class]` in that slide's notes block. If the reference itself can't be confirmed, leave the footnote off the slide and flag it in the notes. Unverified material never appears on the slide itself.

#### Layout

The styles in the YAML header below handle two things. They keep footnotes small and grey. And they fix a problem with `{.center}` slides: Quarto pins footnotes to the bottom of the slide's content box, which on a centered slide lands on top of the content. The `section.center > aside` rule moves the footnote just below the content instead. Keep both rules in every deck.

Don't set `reference-location: document`, which moves every footnote to the end of the deck. The same footnotes pass through to the `clean-typst` PDF as native Typst footnotes with working links.

### Quarto YAML header

Use this header for class decks. Replace the title and subtitle (for the sample course, `SR 101 · Thinking With Machines · Week N`), and put your own name, ORCID, email and affiliation in `author`. Set `date` to the class date.

```yaml
---
title: "[Session Title]"
subtitle: "[Course number · Course title · Week N]"
author:
- name: Your Name
  orcid: 0000-0000-0000-0000
  email: you@example.edu
  affiliations: Your University

date: YYYY-MM-DD

format:
  clean-revealjs:
    slide-number: true
    preview-links: auto
    self-contained: true
    show-notes: false
    include-in-header:
      text: |
        <style>
        .reveal, .reveal * { font-family: system-ui, -apple-system, "Segoe UI", Arial, sans-serif !important; }
        .reveal *:not(strong):not(b):not(th) { font-weight: 400 !important; }
        .reveal strong, .reveal b, .reveal th { font-weight: 600 !important; }
        .reveal .slides { color: #222; }
        .reveal .attribution p { font-size: 0.75em; color: #666; margin-top: 1em; }
        .reveal .question { font-style: italic; margin-top: 1em; }
        .reveal .big-num { font-size: 3.5em; font-weight: 300; line-height: 1.1; }
        .reveal .big-num-muted { font-size: 3.5em; font-weight: 300; line-height: 1.1; color: #aaa; }
        .reveal .long-quote blockquote { font-size: 0.75em; }
        .reveal .source-line { font-size: 0.5em; color: #666; }
        .reveal .source-line a { color: #666; text-decoration: underline; word-break: break-all; }
        .reveal .slide aside .aside-footnotes { font-size: 0.5em; color: #666; }
        .reveal .slide aside .aside-footnotes a { color: #666; text-decoration: underline; word-break: break-all; }
        .reveal .slides section.center > aside { position: relative; left: auto; right: auto; bottom: auto; width: 100%; margin-top: 2.5em; }
        </style>
  clean-typst:
    font-size: 20pt
    color-accent: "009F8C"
---
```

Add classes the deck needs (for example `.eliza` for a monospace transcript, or `.kaiti` with its `<link>` tag for Chinese) to the same style block. Keep the three footnote rules in every deck.

Put custom CSS in `include-in-header` as shown, not in a `css: |` block. Quarto treats `css:` as a file path, so inline CSS placed there is silently ignored. Load web fonts with a `<link>` tag, not `@import`.

### Technical notes
- `#` for section breaks, `##` for slides
- `:::: {.columns}` with two `::: {.column width="50%"}` blocks for text and figure
- `[text]{.question}` for an italic prompt under the slide text
- Use `:::` for incremental reveals or fragments only if needed
- Keep backgrounds simple and readable

### Building and rendering the deck (lessons from Classes 06 and 07)

- File location: the Class NN Planning folder, not Talks. Name it `<course>-weekNN-<topic>.qmd` (for example `sr101-week02-learning.qmd`).
- Extension: Quarto looks for `_extensions/grantmcdermott/clean` next to the .qmd and fails from a new subfolder ("Unable to read the extension 'clean'"). Copy `_extensions/` and `mathjax-config.js` from the previous class folder into the new one.
- YAML: use the subtitle `Course number · Course title · Week N`. Keep the footnote CSS from the header above. Add `.question` (italic, margin-top 1em), `.big-num` (2.6em, weight 300), and `.zh` (2.6em, line-height 1.2) rules to `include-in-header` if the deck uses them.
- Chinese text: put it in a `::: {.zh}` block so it renders large. A story with a Chinese term gets the characters, the pinyin, and a one-line gloss, with the source in a footnote (Class 06: the zhīyīn story of Bo Ya and Zhong Ziqi, cited to Wang, 2024).
- Figures: use the published graphic when the instructor names one (Class 06: the Surgeon General's advisory figure on time with friends). Read the numbers off the graphic, put two footnotes on the slide (the advisory and the underlying study), and check the speaker notes against the graphic.
- Studies the instructor cites from memory (Class 06: Roff's Minnesota clinic cohort; Cowen et al., 1973, on friendship versus relations with parents or authorities as a predictor): give each its own slide with a footnote, using a verified secondary source (Parker & Asher, 1987) when the primary cannot be confirmed. State sample sizes and the comparison only as far as a source supports them. Put the rest in the notes as `[unverified, check before class]`.
- Render with `quarto render <file>.qmd`. Use the system UI font at normal weight (the first rules in the `include-in-header` style block in the YAML header above). The clean theme sets most text to `font-weight: lighter`, which with Helvetica Neue renders as a thin, hard-to-read face, so the override forces weight 400. The instructor does not need Roboto, so a cloud render is fine. Do not flag the font or ask about re-rendering for fonts.
- Images: copy figures into `images/` in the class folder (see "Text and figure" above) so the .qmd renders from that folder.
- Check the render: slide count, a title on every content slide, figures visible and legible, footnotes on the slides that need them, the closing slide last, and no break slide, blank slide, or slide that names the structure of the class. Section breaks make vertical stacks, so step through with the next-slide command (not by horizontal index) when taking screenshots.
- Look up every footnote DOI or URL when the slide is written, not afterward.

### Board plan (bansho)

Every class gets a board plan, and it is one of the ways the class is structured. The instructor works it on paper under the classroom document camera, filling it in left to right over the session without erasing, so that at the closing the whole lesson is visible at once.

Make two files in the Planning folder:

- `Class NN - Board (fill in).pdf` (with its `.html` source): the sheet used in class. Letter landscape, rendered with WeasyPrint, sized for the document camera. It carries the structure and the prompts (title, date, today's question in the red box, panel labels, the italic questions for each segment, table headers and row labels, the student-question list) and leaves every answer empty for the class to fill in. Use a CSS table layout (`display:table` / `table-cell`) for the panels, not flexbox; WeasyPrint overlaps flex children. Class 07 (October 15, 2026) is the model.
- `Class NN - Board plan.pdf` (optional): the instructor's filled-in version showing what is expected in each space, 11×17 landscape. Same four panels, left to right:
  1. Date, title, today's question (めあて, in a red box), and a dashed slot for what students noticed first.
  2. The readings: the key finding of each, the short pull quote with page, and a return arrow when a later segment sends the class back to panel 1.
  3. Comparing ideas (比べる): the main comparison table, with the student questions that belong to each column written beside it.
  4. The closing material: the second comparison or the transfer question, and the summary box (まとめ, red double border) with "We can now say" and "We still can't answer" left empty.
  Use red for the question and key turns, blue for structure or design, and yellow for the person or the script. Dashed boxes mark space left for students' words. Put the segment time on each panel label. Name the students whose questions go on the board.
- The blank template is `Skills/bansho-templates/Board plan - blank template.pdf` (letter landscape, labeled panels) and `Board plan - blank template (no labels).pdf`. Point the instructor to these rather than making new ones.

In the lesson plan, name the board panel each segment fills (a column in the session map and a note on each segment heading), and say what gets written where.

Link the board plan from the Phase 4 checkbox in the instructor note. The slides' fill-in tables (contenteditable HTML tables) can mirror the board, but the paper board is the record; don't add slides that describe it.

### Printable lesson plan

When the instructor wants something to bring to class, make `Class NN - Lesson plan (print).md` in the Planning folder. It is the Phase 2/2b plan only: the header line (course, date, time, room, readings, hard time check), the learning aim, and the numbered segments with times, cold-call language, italic questions, student questions with the page they point to, neriage and scope-challenge cues, and the closing. Leave out the reading analysis, the resource notes, and the verification flags. Use the same segment numbers and times as the agenda, including the 10-minute break.

### Student group discussion and handout

Create at least one optional student small group discussion and if appropriate a separate 1-page markdown document I can pass out to the students for their discussion. This is distinct from the agenda.

### Formatting

Quarto markdown (.qmd) file that compiles to HTML and PDF.

---

## Phase 5: Post-Class Analysis

### When to use

After the session has been taught and a transcript is available (from auto-captioning or recording). Produces three documents.

### Inputs

- The lesson plan (Phase 2 or 2b)
- A transcript of the class session
- Student responses to the closing reflection question (if available separately)

### Output

Three documents: **Document A** (instructor analysis), **Document B** (student summary), **Document C** (future lesson plan).

---

### Document A: Instructor Analysis

#### 5a. Plan vs. reality

For each planned segment, briefly note:
- **Did it happen?** (yes / compressed / skipped / expanded / replaced by something else)
- **Timing**: Roughly how long did it actually take vs. planned?
- **What happened that wasn't planned?** Productive digressions, student-driven detours, unplanned instructor examples or outside material that worked

#### 5b. Anticipated thinking vs. actual thinking

This is the most valuable section for improving future planning. For each major discussion segment:

**Create a simple table:**

| Segment | What we predicted | What actually happened | Interpretation |
|---------|------------------|----------------------|----------------|
| [name] | Students will probably focus on X because Y | Students said: [specific examples] | Why was this different? What does it reveal? |

**Then synthesize:**
- **Confirmed predictions** — where the plan accurately anticipated student thinking. What allowed this?
- **Mismatches revealing deeper engagement** — students went further or differently than expected. What prompted it?
- **Mismatches revealing gaps** — students didn't go where expected, struggled with something anticipated to be easy, or stayed at the surface. What does this reveal about their current framework?
- **What didn't come up** — ideas or connections that were planned but didn't emerge. Was the prompt insufficient? The timing wrong? The concept genuinely difficult?

**The meta-question:** What does this evidence teach you about how *these* students think about *this* content?

#### 5c. Student engagement and participation

Based on available evidence in the transcript:
- **Who talked?** Rough distribution — was it a few students or many? Did the same students dominate?
- **Quality of engagement**: Substantive (making arguments, connecting to readings, building on each other) or surface-level (repeating the reading, agreeing with the instructor, anecdote without analysis)?
- **Moments of genuine engagement**: 2–3 moments where students seemed most engaged — follow-up questions, disagreement, unexpected connections. What prompted these?
- **Moments of low engagement**: Segments where students went quiet or the instructor was carrying the session alone. What was happening?

#### 5d. The closing reflection as evidence

What did students say in response to the closing question?

- Did their responses indicate the session accomplished its conceptual purpose?
- Did they engage with the hatsumon's territory?
- Did they focus on surface features or the intellectual work?
- What's the gap between what the plan hoped they would say and what they actually said?

#### 5e. Research question — what did you learn about teaching?

Return to the research question from the lesson plan. Based on transcript evidence:
- **What did you learn?** Be specific.
- **What would you try differently?**
- **What new questions does this raise?**

This is not about whether the lesson "worked" — it's about what you learned as a teacher-researcher from this iteration.

#### 5f. Instructor feedback

- **What worked well** — specific moments, moves, or choices, with transcript evidence
- **What could be refined** — specific and actionable, not vague. "Consider moving segment X before segment Y because students needed X's framework to engage with Y's question."
- **Pacing** — did protected segments get their time? Was the matome compressed?

#### 5g. Carry-forward items

2–3 specific items for the next session:
- An unfinished thread to pick up
- A concept that didn't land and needs a different approach
- A student question or contribution worth revisiting
- A revised prediction about student thinking

#### 5h. Running record of anecdotes

Every Phase 5 pass, scan the transcript for personal stories and anecdotes the instructor told (first-person narratives — family, students, fieldwork, colleagues — not just illustrative hypotheticals), and update a persistent running-record file for the course, e.g. `[course]-anecdote-record.md`. This file lives alongside the lesson plans and persists across the whole course, not just one session.

**Columns:**
- **Story** — a short, memorable name for it
- **Description** — one sentence, enough to recognize it without re-reading the transcript
- **First told (on file)** — the earliest session this record has evidence for; note "unknown" honestly if the record doesn't go back far enough to say
- **Used for** — what point it illustrated in that session
- **Told before?** — yes / no / unclear, with the evidence: an explicit self-reference in the transcript ("I may have mentioned this," "I think I said this already") is strong evidence; recurrence across transcripts on file is also strong evidence; anything else is a guess and should be labeled as such
- **Better fit elsewhere?** — yes / no, with a specific alternate session named if yes, and the reasoning in one line

**Process:**
1. If a record file for this course doesn't exist yet, ask the instructor for it before assuming it doesn't exist — it may be filed elsewhere.
2. Extract candidate stories from the current transcript. Distinguish the instructor's own first-person anecdotes from students' stories (a small seminar transcript will have both) and from hypothetical illustrations ("let's say you're a parent...") that use first-person phrasing but aren't autobiographical.
3. Cross-check each candidate against the existing record. Add new ones; for repeats, update "told before" with the new session and evidence.
4. Flag anything that seems like a better fit for a different week's topic than the one it was told in, based on the course's actual topic list, not a guess at what topics might exist.
5. Note explicitly, in the file or in your reply, any story you're not fully confident is a repeat or an autobiographical anecdote, rather than silently guessing.

This is a genuinely cumulative record — its value compounds over a semester and across repeated offerings of the course, so treat completeness and honesty about uncertainty as more important than a clean-looking table on the first pass.

---

### Document B: Student Summary

A markdown document summarizing the session for students — study aid and record for those absent or reviewing.

#### What to include

- **The session's big question** — the hatsumon, stated plainly
- **What we did** — a narrative summary of each major segment in first-person plural ("We examined...", "We discussed..."). Include the substance of key ideas and what the class actually worked through.
- **Key concepts** — short list with brief definitions
- **Connections to readings** — how discussion connected to, extended, or complicated the assigned readings
- **Looking ahead** — the bridging question and next week's readings

#### What NOT to include

- Instructor self-assessment or pedagogical reasoning
- Specific student names or attributable quotes (unless the instructor approves)
- Planning artifacts or anticipated-thinking analysis
- Evaluation of whether the session "worked"

#### Tone and format

- Written as by a knowledgeable observer, not as a transcript
- Conversational but substantive — a student should learn something from reading it
- Markdown, 2–3 pages, `###` for section headings

---

### Document C: Future Lesson Plan

A revised lesson plan based on what actually happened. If productive ad-libs or unplanned moves worked well, incorporate them. Include a brief section describing what changed and why. This is the starting point for teaching this topic in a future semester. Give a concise summary of what's changed between the original and revised lesson plan.

---

### Formatting for all three documents

- Markdown file
- 4–6 pages — useful but not burdensome, but the lesson plan can be longer if needed.
- Direct and specific. The instructor values accuracy over flattery.

---

## General Principles Across All Phases

### Preserve the instructor's voice

The instructor is an experienced teacher and researcher with deep content knowledge. The workflow makes implicit reasoning explicit — it does not substitute generic pedagogy for the instructor's judgment. When source notes contain specific framings, anecdotes, or analytical moves, preserve them.

### Be genuinely specific

The most common failure mode is vagueness. "Students will discuss the reading" is useless. "Students are likely to focus on the vivid case in section 3 and overlook the methodological caveat in section 5, because the case is emotionally engaging and the methodology is abstract" is useful. Every prediction should be concrete enough to be falsifiable.

### Calibrate detail to the instructor's needs

The instructor has taught many of these topics before. Content they know cold needs a trigger, not a paragraph. Transitions, time management, and anticipated student thinking are where the plan adds value. Err toward less content description and more pedagogical scaffolding.

### The closing question is non-negotiable

Every session ends with:

> *What did you learn today that is new to you, important for you, and/or worth remembering?*

This appears on the final slide, in the agenda, and in the lesson plan. The post-class analysis treats student responses as primary assessment data.

### Bring in outside intellectual resources when they enrich the discussion

The instructor draws freely on cultural examples, historical anecdotes, non-English-language concepts, and material from outside the assigned readings when they sharpen the analytical point. When planning a session, identify any such resources that could serve this function — a chengyu, a historical case, a metaphor from another field, a quotation that predates the academic literature. Note these in the instructor resources section of the lesson plan with enough context to deploy them fluently.

### Scope-challenging is part of the lesson plan, not a bonus

For sessions built around empirical research, the lesson plan should include an explicit plan for helping students evaluate the scope and limits of the findings — not just understand them. Strong findings should be complicated; incomplete paradigms should be named as such. This is especially important in ED 724, where students are doctoral researchers who need to be able to critically evaluate research, not just receive it.

### Anticipated thinking accretes across phases

- Phase 1b: How students are likely to read the assigned texts
- Phase 1g: What the reaction papers reveal about their actual thinking going in
- Phase 2: Specific predicted responses for each discussion prompt
- Phase 2b: Predictions revised in light of reaction papers
- Phase 5b: Compare all predictions to what happened

This cumulative approach keeps the anticipation work lightweight at each step but builds a useful record over time.

---

## Output Format Summary

| Phase | Output | Format | Length |
|-------|--------|--------|--------|
| 1 | Reading analysis & session framing (includes 1g if papers available) | Markdown (.md) | 4–6 pages |
| 2 | Preliminary lesson plan | Markdown (.md) | 4–6 pages |
| 2b | Revised lesson plan (after reaction papers) | Markdown (.md) | 4–6 pages |
| 3 | Student agenda (source + rendered) | Markdown (.md) + PDF via `Skills/agenda_md_to_pdf.py` (WeasyPrint) | 1 page |
| 4 | Slide deck, with citation footnotes on source-based slides | Quarto (.qmd) → HTML + PDF | Variable |
| 4 (opt) | Session handout (group discussion, permanent-note candidates) | Markdown (.md) | 1 page |
| 4 | Board (bansho) fill-in sheet for the document camera | HTML → PDF (WeasyPrint), letter landscape | 1 page |
| 4 (opt) | Board plan, filled in | HTML → PDF (WeasyPrint), 11×17 landscape | 1 page |
| 4 (opt) | Printable lesson plan | Markdown (.md) | 2–4 pages |
| Student note | Agenda and links added to the student note | Markdown (.md) | In the note |
| 5a | Instructor analysis | Markdown (.md) | 4–6 pages |
| 5b | Student summary | Markdown (.md) | 2–3 pages |
| 5c | Future lesson plan | Markdown (.md) | 3–4 pages |
| 5h | Running record of anecdotes (cumulative, updated each pass) | Markdown (.md) | Grows over the semester |
