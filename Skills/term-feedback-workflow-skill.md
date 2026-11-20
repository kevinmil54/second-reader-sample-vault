---
type: map
created: 2026-04-22
name: term-feedback-workflow
description: "Generates a term-level instructor feedback report for a university course, based on a sample of transcripts from the beginning and end of the term. Use when the instructor provides a set of session transcripts spanning the arc of a term and asks for cross-term analysis, pattern identification, or summative pedagogical feedback. This skill is the term-level analogue of Phase 5 (post-class analysis) in the lesson-planning-workflow skill. It produces a single Instructor Term Report (Document T) in markdown."
---

# Term Feedback Workflow

This skill generates a **Term Instructor Report** — a summative, evidence-based feedback document covering the arc of a complete course term. It is the term-level analogue of Phase 5 (post-class analysis) in the lesson-planning-workflow skill.

Unlike a single-session post-class analysis, this report does not focus on moment-to-moment moves. It focuses on **patterns**: what persisted across the term, what developed, what is structurally missing, and what the instructor should carry forward into the next iteration.

---

## Inputs Required

The instructor provides:

1. **Course identification** — course name, number, term, instructor
2. **Syllabus or course schedule** — for situating sessions in the course arc and identifying intended sequence and conceptual goals
3. **Session transcripts** — auto-generated captions or similar. The workflow is designed for:
   - 6–10 sessions from the **beginning** of the term (first ~4 weeks), *excluding* the first session (orientation/syllabus day)
   - 6–10 sessions from the **end** of the term (last ~4 weeks), *excluding* the final session if it is primarily presentations or wrap-up with no substantive discussion
4. **Optional: lesson plans** — if available from earlier planning workflow phases, these inform what was intended vs. what happened

The instructor may also note any known contextual factors (small vs. large class, unusual disruptions, first vs. repeat offering).

---

## What This Skill Does NOT Do

- It does not reconstruct the content of every session. It identifies patterns across sessions.
- It does not evaluate whether the course "went well" in a generic sense. It identifies specific, evidence-grounded observations about pedagogy.
- It does not treat garbled or incomplete transcript passages as evidence. Gaps are acknowledged as gaps.
- It does not produce a grade or summative evaluation of the instructor. It produces a professional development document in the tradition of lesson study (jugyō kenkyū) — the instructor as reflective practitioner.

---

## Output: Document T — Instructor Term Report

A single markdown document. Target length: 8–12 pages. Direct, specific, and evidence-grounded throughout. The instructor values accuracy over flattery — never hedge a finding with unnecessary qualifications and never soften a critique with praise padding.

### Section structure

#### T1. Course Arc and Thematic Coherence

- What was the intended course arc? (From syllabus/schedule)
- What arc is visible in the transcripts?
- Are the early and late sessions in the same intellectual conversation, or do they feel like separate courses?
- Is the conceptual through-line visible to a student who was paying attention?

#### T2. Opening Questions and the Hatsumon Function

For each transcript set (early/late):
- What forms did opening questions take?
- Were they experience-grounded, concept-grounded, or content-delivery openers?
- Did they create productive cognitive tension (hatsumon function), or were they primarily warm-up?
- Did the opening question connect to the session's central intellectual work?
- How did the opening-question practice change across the term?

#### T3. Discussion Structure and Instructor Moves

Analyze the instructor's pedagogical moves as observable across the transcript set. Distinguish:

- **Consistent moves** — what the instructor does reliably across the term. Name these precisely.
- **Developmental moves** — what changed from early to late term, and whether the change represents growth, drift, or strategic adaptation.
- **Missing moves** — what the lesson-planning framework called for (scope-challenging, matome, anticipated-thinking verification, neriage) that is systematically absent or underdeployed.

For each move identified, cite at least one specific transcript moment as evidence. Do not make claims without transcript grounding.

#### T4. Student Engagement — Quality and Distribution

- What is the distribution of participation across students? Does it change across the term?
- What is the *quality* of student analytical moves in early vs. late sessions? Use specific evidence.
- Are students, by late term, initiating conceptual moves themselves — or are they still primarily responding to instructor questions?
- What is the gap between the most and least analytically engaged students, and does it narrow or widen?

Note: In small seminars (≤10 students), individual patterns may be visible. Name them if they are pedagogically significant. Do not name students in ways that would embarrass or disadvantage them if shared; use neutral identifiers if needed.

#### T5. Instructor Pedagogy — Persistent Strengths and Specific Refinements

**Strengths:** Name 3–5 persistent pedagogical strengths with specific transcript evidence. These should be the moves that characterize the instructor's distinctive pedagogical identity — not generic good-teaching behaviors.

**Refinements:** Name 4–6 specific, actionable refinements. Each refinement should:
- Name the pattern (not just an instance)
- Cite transcript evidence
- Propose a specific alternative
- Indicate whether this is a high-stakes or low-stakes change

Do not produce generic feedback ("ask more follow-up questions"). Produce specific feedback ("the closing matome question appears in zero of 16 sessions reviewed; three minutes of protected time at the end of each session would recover this").

#### T6. Course-Level Research Question — What Did You Learn About Teaching?

Return to the instructor's implicit or explicit research question for the term. Based on transcript evidence:
- What can be said about the question now?
- What evidence supports any claim?
- What remains unknown and would require different data to answer?
- What new question does this term raise?

This section is the most important for professional development. It treats the instructor as a practitioner-researcher, not just a course deliverer.

#### T7. Carry-Forward Recommendations

5–8 specific, prioritized recommendations for the next offering of this course. Distinguish:
- **High-leverage structural changes** (course arc, assessment design, sequencing)
- **Session-level design changes** (opening questions, closing structure, activity types)
- **Infrastructure changes** (Canvas setup, question-submission systems, transcript/feedback loops)

Order by expected impact, not by how easy they are to implement.

#### T8. Honest Summary Observation

One to three paragraphs that synthesize the most important finding about this instructor's teaching — the thing that, if they understood it clearly, would improve the course most. This is not a compliment sandwich. It is a direct professional observation. It should be specific enough to be actionable and honest enough to be useful.

---

## Quality Standards for the Report

### Be genuinely specific
Every claim about pedagogy should be grounded in a specific transcript moment or a pattern visible across multiple sessions. "Students became more analytical over the term" is not a claim. "In the April 14–16 *Seven Up* sessions, students independently named hindsight bias, filmmakers' gendered assumptions about whose life matters, and social class as more predictive than individual institutions — conceptual moves that do not appear in January transcripts even when prompted" is a claim.

### Acknowledge transcript limitations
Auto-generated captions are unreliable. Garbled passages should be treated as missing data, not evidence. When a finding relies on a single clear transcript moment rather than a pattern, say so.

### Calibrate to the instructor's experience level
A first-year instructor needs different framing than a 40-year veteran. The veteran already knows the course content; they need the analysis to show them something they couldn't see from inside the session. Prioritize observations about patterns across time that are invisible in the moment.

### Use the lesson-planning vocabulary where relevant
The term feedback skill shares vocabulary with the lesson-planning workflow:
- **Hatsumon** — the driving question; evaluated in T2
- **Matome** — the closing consolidation; tracked in T3 and T5
- **Neriage** — structured comparison and synthesis of student ideas; tracked in T3
- **Kikan-shido** — observation during student work; tracked in T3
- **Scope-challenging** — explicit evaluation of research findings' limits; tracked in T3

These are not required in the output document (use English equivalents if the instructor prefers), but they orient the analysis.

### Do not flatten the course into an average
The goal is to track change, not describe a static state. The early-term and late-term patterns should be clearly distinguished. If the course ends stronger than it began, say so precisely. If particular sessions or units stand out — in either direction — name them.

---

## Formatting

- Markdown, using `##` for section headers matching the T1–T8 structure
- 8–12 pages
- No bullet lists as the primary mode of delivery within sections — write in prose with embedded specifics
- A table or structured list is appropriate only for carry-forward recommendations (T7)
- Avoid hedging phrases like "it seems," "perhaps," "one could argue." Make claims and ground them.

---

## Relationship to Other Workflow Skills

| Skill | Scope | When to Use |
|-------|-------|-------------|
| lesson-planning-workflow Phase 5 | Single session | Post-class reflection, within 48 hours of class |
| **term-feedback-workflow** | Full term | End of term, before next offering |
| (Future) cohort-feedback-workflow | Across multiple sections or instructors | Program-level analysis |

The term feedback skill draws on patterns that are only visible across many sessions. It is not a substitute for session-level analysis — it is a complement that sees what session-level analysis cannot.

---

## Prompt Template

The following prompt produces the Term Instructor Report when used with this skill. Fill in bracketed fields.

```
I want a term-level instructor feedback report for [COURSE NAME AND NUMBER], [TERM YEAR].

Instructor: [NAME]
Class size: [N students]
Meeting pattern: [e.g., twice weekly, 80 minutes]
First or repeat offering: [first / repeat; if repeat, how many prior offerings]

Course arc (from syllabus): [paste or summarize the course schedule/topics by unit]

Transcripts provided:
- Early term: [list session dates]
- Late term: [list session dates]
- Excluded (per convention): [first session, last session if presentations-only]

[Optional: Known context — unusual disruptions, mid-term changes, specific pedagogical goals the instructor was working on]

[Optional: Prior lesson plans if available from the lesson-planning-workflow]

Please produce Document T (Instructor Term Report) following the term-feedback-workflow skill. 
The report should be 8–12 pages, direct, evidence-grounded, and specific. 
The instructor values accuracy over flattery.
```

---

## Example Invocation

> I want a term-level instructor feedback report for ED 359: Growing Up in School, Winter 2026.
> 
> Instructor: Your Name. Class size: ~7 undergraduates and master's students. Meets Tuesdays and Thursdays, 80 minutes. Repeat offering.
> 
> Course arc: ecological/cultural frameworks → preschool documentaries (U.S., China, Japan) → number naming and literacy → migration/floating children → adolescent identity → educational biography presentations → *Seven Up* documentary and life-course development → final projects.
> 
> Early term transcripts: Jan 13, 15, 20, 22, 27, 29; Feb 3, 5
> Late term transcripts: Mar 19, 24, 26, 31; Apr 2, 7, 9, 14, 16
> Excluded: Jan 13 (first day, orientation), Apr 21 (final presentations only)
> 
> Please produce Document T following the term-feedback-workflow skill. The instructor values accuracy over flattery.
