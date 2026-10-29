---
type: synthesis
topic: 
status: draft
created: {{date}}
---

# {{title}}

*A synthesis note gathers your permanent notes on one topic and states what you now think. Write it in your own words and keep it short enough to reread in two minutes.*

## The question
*What are you trying to understand? One or two sentences.*

## What I think right now
*Your current position, in a few short paragraphs or a numbered list of claims. Link each claim to the permanent notes that support it, like [[Permanent note title]].*

1. 
2. 

## Permanent notes on this topic
*Give this note a topic word in the `topic:` property above (for example `memory`). Add the same word as a tag to each permanent note you want to include. This list fills itself.*

```dataview
LIST
FROM "Permanent notes"
WHERE contains(file.tags, "#" + this.topic)
SORT file.name ASC
```

## Where the notes disagree or leave gaps
- 

## What I still need to read or think through
- 

## Where I will use this
*A class paper, the final project, a discussion. Link the project note if there is one: [[Project - ]]*
