---
name: new-project
description: Make a new project in the user's Obsidian vault. Asks for a title, then makes a folder in Projects, a project note from the project template, and a project letter from the letter template. Use when asked to start, create or set up a new project.
---

# New project

A project in your vault is a folder in `Projects/` with two notes in it: the project note (outline, notes it draws on) and the project letter (a dated log written to the second reader, whose "Permanent note candidates" the Second Reader plugin promotes into permanent notes). The plugin has the same command, "New project (folder, project note and letter)", and the two should give the same result. The Engelbart cul-de-sac project is the model for both notes.

## Steps

1. Ask for the project title if it was not given, and the output type (talk, article, substack-post, book-chapter, grant, course, personal, paper, other). Ask both in one question. Ask nothing else.
2. Make the project name from the title: replace `\ / : * ? " < > | # ^ [ ]` with spaces, collapse repeated spaces, and strip trailing dots and spaces. The same name is used for the folder, the project note, the `project:` property and the title line.
3. Look in `Projects/` for a folder with that name, ignoring upper and lower case. If there is one, stop and say so. Do not overwrite or merge.
4. Make the folder `Projects/<name>/`.
5. Make the project note `Projects/<name>/<name>.md` from `Templates/Project Template.md`, or from `Templates/Substack Project Template.md` when the type is substack-post (the Substack one has no title line; its title is in the `title:` property, set `project:` to the name and leave `status: draft`, and put the letter link on the line after the properties). Both templates are written for Templater, so fill them in by hand:
   - `project:` is the name, `output-type:` is the type chosen, `status:` is `Active`, `created:` is today's date (YYYY-MM-DD, local time).
   - The title line is `# <name>`.
   - Add `topics: [<name>]` on the line after `tags:`.
   - Add a blank line and `Letter to the second reader: [[<name> - letter]]` under the title line, with the template's blank line after it.
   - Leave everything else as the template has it, including the Dataview blocks. No `undefined` code may remain.
6. Make the letter `Projects/<name>/<name> - letter.md` from `Templates/Project Letter Template.md`. Replace `{{date}}` with today's date and `{{project}}` and `{{topics}}` with the name. If either template is missing, say so and stop.
7. If the name could be misread as something other than text in YAML (it starts with `- ? : , [ ] { } # & * ! | > ' " % @` or a backtick, is yes, no, true, false or null, or is only a number), put it in double quotes in `project:`. In `topics:`, leave out commas, brackets, braces and quotes.
8. Do not change either template or any other project. Say in one or two sentences what was made and where.

## Notes

- The letter's `topics:` carries over to each permanent note promoted from it, which is how a project's notes come to share a topic.
- A new project note has no outline yet. Do not write one.
