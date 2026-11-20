---
name: place-notes-in-project-outline
description: Place permanent-note links under the points of a project note's Outline, using the user's own outline text. Use when asked to organize, attach or sort notes in a project note.
---

# Place notes in a project outline

A project note in the user's Obsidian vault has an `## Outline` of numbered points the user wrote, a holding list of permanent-note links (`## Notes I'm drawing on`, or `## Not placed yet`), and live Dataview lists under `## Source material`. This skill moves the links in the holding list under the outline points they support. The outline is the user's argument, so the user's words stay exactly as they are.

## Steps

1. Read the project note again immediately before editing. The user may have changed it while you were working. Work from that fresh text, not from an earlier read.
2. Copy the note to `.backup-<date>/` at the top of the vault before changing it.
3. Collect the candidate notes: the links in the holding list, plus any permanent note in `Permanent notes/` that links to the project note and is not yet in the outline. If the project has a `synthesis` property, the permanent notes listed in those synthesis notes are also candidates, but add them only if the user asked.
4. For each candidate, read its `title`, its Core idea and its Source link. Most permanent notes here are one-line claims with an empty Core idea, so the title usually carries the meaning.
5. Match each note to the outline point it supports, by meaning. Use the deepest point that fits. Put a note under one point unless it clearly supports two. If no point fits, leave the note in the holding list under `## Not placed yet`.
6. Edit the note:
   - Insert each note as an indented bullet directly under its point, one tab deeper than the point. Copy the link line exactly as it appears in the holding list, including any `|alias`.
   - Do not change, reword, renumber or reorder the user's points. Do not add points or write argument text.
   - Remove a link from the holding list only after it is in the outline. Before saving, check that the number of links now in the outline plus the number left in the holding list equals the number you started with. If it does not, do not save.
7. If the Outline is empty, offer to split the `## Central claim` into numbered points using the user's own sentences word for word. Do not do this without being asked.
8. Report in plain prose: where you put the notes, which placements are weak guesses, which outline points have no notes (the gaps), and which notes are left unplaced. Say that a note can be moved by cutting and pasting its line.

## Do not

- Do not edit the permanent notes themselves.
- Do not delete anything from the project note except links you have placed.
- Do not touch the frontmatter, the live Dataview queries, or any section other than the Outline and the holding list.
