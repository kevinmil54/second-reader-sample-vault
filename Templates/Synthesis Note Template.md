---
type: synthesis
topic: 
status: draft
created: {{date}}
updated: {{date}}
tags: [synthesis]
---

# {{title}}

*A synthesis note gathers what you know on one topic, built from your permanent notes. Write it in your own words. Every claim links to the permanent notes behind it. Keep it short enough to reread in a few minutes.*

## The question
*What are you trying to understand? One or two sentences.*



## Where I stand now
*Your current position as a short numbered list of claims. End each claim with links to the permanent notes that support it, like ([[Permanent note title]]).*

1. 
2. 
3. 

## Permanent notes not yet used
*Permanent notes with your topic word that this note does not link to yet. Link one in a claim above and it leaves this list. The list fills itself.*

```dataview
LIST WITHOUT ID link(file.path, default(title, file.name))
FROM "Permanent notes"
WHERE contains(topics, this.topic) AND !contains(this.file.outlinks, file.link)
SORT file.name ASC
```

## Where the notes agree and disagree
*Which claims are well supported across sources? Which pull against each other? Name the notes.*

- Agree: 
- Disagree: 

## Gaps
*What is missing: evidence, a population, a counterexample, a source you haven't read.*

- 

## Still to read or think through

- [ ] 

## How my thinking has changed
*One dated line each time your position above shifts, with the reason.*

- {{date}}: first draft

## Used in
*Fills itself from the `synthesis:` property on project notes.*

```dataview
LIST
FROM ""
WHERE type = "project" AND contains(synthesis, this.file.link)
```
