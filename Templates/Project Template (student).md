---
type: project
project: 
output-type: paper
status: Active
synthesis: []
draft: ""
created: {{date}}
tags: [project]
---

# {{title}}

%% project: a short word, the same on every note you want collected here, for example final-project. synthesis: links to your synthesis notes. draft: a link to your draft note. Links in properties need quotes, like "[[Note title]]". %%

## Notes



## Draft

Other notes in this project:

```dataview
TABLE type AS "Type", status AS "Status"
FROM ""
WHERE project = this.project AND file.name != this.file.name
SORT type ASC, file.name ASC
```

## Source material

Permanent notes that link to this note but are not linked here yet:

```dataview
LIST WITHOUT ID link(file.path, default(title, file.name))
FROM "Permanent notes"
WHERE contains(file.outlinks, this.file.link) AND !contains(this.file.outlinks, file.link)
SORT file.name ASC
```

Synthesis notes (from the `synthesis` property):

```dataview
LIST
FROM ""
WHERE type = "synthesis" AND contains(this.synthesis, file.link)
```
