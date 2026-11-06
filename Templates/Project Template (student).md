---
type: project
project: 
output-type: paper
status: Active
deadline: 
synthesis: []
draft: ""
created: {{date}}
tags: [project]
---

# {{title}}

*A project note plans one paper, presentation or other piece of work. It draws on your synthesis and permanent notes and points to your draft.*

*Fill in `project:` above with a short word, for example `final-project`. Add the same line, `project: final-project`, to the properties of every note you want collected here. In `synthesis:` list links to your synthesis notes. In `draft:` put a link to your draft note. Links in properties need quotes, like "[[Note title]]".*

## What this is for

- What you are making, and for whom:
- Due:
- What you want the reader or audience to take away:

## Central claim
*One or two sentences. Revise it as your argument firms up.*



## Argument skeleton
*One row per move in your argument. "Supported by" links to permanent notes. "In the draft" is the section where the move appears.*

| Move | What I say | Supported by | In the draft |
|---|---|---|---|
| 1 | | [[]] | |
| 2 | | [[]] | |
| 3 | | [[]] | |

## Draft
*Your draft is linked in the `draft:` property. Other notes in this project appear below.*

```dataview
TABLE type AS "Type", status AS "Status"
FROM ""
WHERE project = this.project AND file.name != this.file.name
SORT type ASC, file.name ASC
```

## Source material

Permanent notes linked from this note, or that link to it:

```dataview
LIST
FROM "Permanent notes"
WHERE contains(file.outlinks, this.file.link) OR contains(this.file.outlinks, file.link)
SORT file.name ASC
```

Synthesis notes (from the `synthesis:` property):

```dataview
LIST
FROM ""
WHERE type = "synthesis" AND contains(this.synthesis, file.link)
```

## Gaps in the material
*Claims in the skeleton that have no permanent note behind them yet.*

- 

## To verify

- 

## Tasks

- [ ] 
