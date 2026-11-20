"""Built-in note templates. Placeholders look like {{name}}. Point [notes] template / [classes] template
in the config at your own files to replace them."""

LITERATURE_NOTE = """---
tags: [literature-note]
title: "{{title_yaml}}"
author: {{authors}}
year: {{year}}
citekey: {{citekey}}
zotero: {{zotero_uri}}
source-md: "[[]]"
student: 
course: {{course_yaml}}
status: literature
date-read: 
---

# {{title}}

> **Zotero:** [Open in Zotero]({{zotero_uri}}) · **Cite:** [@{{citekey}}] · **Full text (md):** [[source-md]]

**Reference (APA):** {{reference}}

## Why I'm reading this

- 

## Summary (in my own words)

- 
- 

## Key ideas/findings/arguments

*Selective - core ideas and findings. If you're copying sentences, stop and write in your own words.*

- 
- 

## How this connects to other sources

*Does this confirm, contradict, or complicate other things you've read? Name the notes.*

- 

## Open questions this raises

- 

## Questions for class discussion

- 

## Quotes worth keeping

*Your Zotero highlights and comments arrive below, with page numbers, each time you click the highlighter-pen icon at the top-right of this note. Edit or trim them freely. Add your own quotes too — if possible, include a page number.*

%% begin annotations %%
%% end annotations %%

> "..." (p. )

## Figures & images

*Screenshots, diagrams, or tables worth keeping. Embed with `![[filename]]`, and caption each one in your own words — why does it matter?*

![[]]

## Permanent note candidates

*Write your own permanent note titles in your own words. These should be "nuggets" — ideas that are interesting to you and/or that you might use in your own work. Checking the box promotes it: a new permanent note gets created automatically and this line becomes a link to it, carrying over any tags you've added above (`literature-note` itself doesn't carry over — the new note is tagged `permanent-note` instead). Want to say more before you promote it? Press Enter then Tab right after the title to add an indented line or two — that carries over into the new note's Core idea too.*

- [ ] 
- [ ] 

## Related notes

- [[]]
"""

# For readings that are not in Zotero (web essays, videos, lectures) but have a URL.
WEB_NOTE = """---
tags: [literature-note]
title: "{{title_yaml}}"
author: {{authors}}
year: {{year}}
source-type: {{source_type}}
url: {{url}}
source-md: "[[]]"
student: 
course: {{course_yaml}}
status: literature
date-read: 
---

# {{title}}

> **Source:** [{{url}}]({{url}})

**Reference (APA):** {{reference}}

## Why I'm reading this

- 

## Summary (in my own words)

- 
- 

## Key ideas/findings/arguments

- 
- 

## How this connects to other sources

- 

## Questions for class discussion

- 

## Quotes worth keeping

> "..." (p. )

## Permanent note candidates

- [ ] 
- [ ] 

## Related notes

- [[]]
"""

STUDENT_CLASS_NOTE = """---
type: class-note
course: "{{course}}"
offering: {{offering}}
meeting: {{meeting}}
date: {{date}}
topic: "{{topic_yaml}}"
tags: [class-note, teaching]
---

# Class {{nn}} - {{date}}: {{topic}}

Previous: {{prev}} · Next: {{next}}{{extra_links}}

## Themes or goals
![[{{syllabus}}#^{{block}}-goal]]

## Questions to think about before class
![[{{syllabus}}#^{{block}}-questions]]

## Readings
![[{{syllabus}}#^{{block}}-readings]]

## Your notes
*Write here before and during class. Put `?` on anything you want to ask about.*



## Questions I still have
- 

## Permanent note candidates
*Write ideas from today in your own words, as the title of a note you might want to keep. Checking the box creates a permanent note and turns the line into a link to it. To say more first, press Enter then Tab after the title and add an indented line or two; that goes into the new note's Core idea.*

- [ ] 
- [ ] 

## Links
- Slides: 
- Class summary: 
- Assignment due: 

## What did I learn today?
*Two or three sentences before you leave.*

"""


def fill(template: str, values: dict) -> str:
    import re

    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), m.group(0))), template)
