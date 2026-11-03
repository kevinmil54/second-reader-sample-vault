<%*
const course = await tp.system.prompt("Course", "SR 101");
const offering = await tp.system.prompt("Offering", "Winter 2027");
const num = String(await tp.system.prompt("Meeting number (e.g. 3)", "")).padStart(2, "0");
const date = await tp.system.prompt("Date (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD"));
const topic = await tp.system.prompt("Topic", "");
const base = `Class ${num} - ${date}`;
await tp.file.rename(`${base} - Student`);
-%>
---
type: class-note
course: "<% course %>"
offering: <% offering %>
meeting: <% Number(num) %>
date: <% date %>
topic: "<% topic %>"
tags: [class-note, teaching]
---

# <% base %>: <% topic %>

Previous: [[]] · Next: [[]] · [[SR 101 - Course home|Course home]] · [[Syllabus - SR 101 Thinking With Machines - student copy|Syllabus]]

## Themes or goals
![[Syllabus - SR 101 Thinking With Machines - student copy#^w<% num %>-goal]]

## Questions to think about before class
![[Syllabus - SR 101 Thinking With Machines - student copy#^w<% num %>-questions]]

## Readings
![[Syllabus - SR 101 Thinking With Machines - student copy#^w<% num %>-readings]]

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

