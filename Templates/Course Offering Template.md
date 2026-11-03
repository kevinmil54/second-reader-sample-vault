<%*
// Sets up a new offering of a course: folders, this course home, and the
// course's "changes for next time" note. Make class notes with the
// Class Meeting templates.
const classesDir = "Classes";
const root = app.vault.getAbstractFileByPath(classesDir);
const existing = root ? root.children.filter(f => f.children).map(f => f.name).sort() : [];
const NEW = "New course…";
let courseFolder = await tp.system.suggester([...existing, NEW], [...existing, NEW], false, "Which course?");
if (!courseFolder) { new Notice("Cancelled"); return; }
if (courseFolder === NEW) courseFolder = (await tp.system.prompt("Course folder name, e.g. ED 336 - How to thrive in a world of intelligent machines", "")).trim();
const code = await tp.system.prompt("Short course code", courseFolder.split(" - ")[0]);
const course = await tp.system.prompt("Course name for notes", code);
const first = await tp.system.prompt("First class (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD"));
const firstDay = window.moment(first, "YYYY-MM-DD");
const mo = firstDay.month(), yr = firstDay.year();
const season = mo < 4 ? "Winter" : mo < 8 ? "Spring-Summer" : "Fall";
const offeringDefault = `${season} ${yr}`;
const offering = await tp.system.prompt("Offering", offeringDefault);
const n = Number(await tp.system.prompt("Number of class meetings", "14"));
const gap = Number(await tp.system.prompt("Days between meetings", "7"));
const syllabus = await tp.system.prompt("Syllabus note name", `Syllabus - ${code} ${offering}`);
const courseDir = `${classesDir}/${courseFolder}`;
const base = `${courseDir}/${offering}`;
for (const d of [courseDir, base, `${base}/Meeting notes`, `${base}/Planning`])
  if (!app.vault.getAbstractFileByPath(d)) await app.vault.createFolder(d);
const meetings = [...Array(n).keys()].map(i => {
  const m = firstDay.clone().add(i * gap, "days");
  return { week: i + 1, num: String(i + 1).padStart(2, "0"), iso: m.format("YYYY-MM-DD"), short: m.format("MMM D") };
});
const rows = meetings.map(m => `| ${m.week} | ${m.short} |  | [[Class ${m.num} - ${m.iso} - Student\\|Open]] |  |`).join("\n");
const home = `${code} ${offering} - Course home`;
const changes = `${courseDir}/${code} changes for next time.md`;
if (!app.vault.getAbstractFileByPath(changes)) {
  const weeks = meetings.map(m => `### Week ${m.week} (${m.short})\n- [ ] \n`).join("\n");
  await app.vault.create(changes, `---
type: note
created: ${tp.date.now("YYYY-MM-DD")}
topics: [teaching-practice]
course: "${course}"
---

# ${code} changes for next time

Changes to make the next time I teach this course. Add items as they come up; check them off when they're in the new syllabus or planning notes.

This offering: [[${home}]]

## Whole course
- [ ] 

## Syllabus and assignments
- [ ] 

## Readings to add, drop, or replace
- [ ] 

## By week

${weeks}`);
}
await tp.file.move(`${base}/${home}`);
-%>
---
tags: [teaching, class-note]
type: course-home
course: "<% course %>"
offering: <% offering %>
---

# <% course %>

<% offering %> · *days, time and room* · Instructor: *your name*

Start here: [[<% syllabus %>|Syllabus]]

Each class has its own note. It shows the goals, the questions to think about before class, and the readings for that week. It also has space for your own notes and for ideas you want to turn into permanent notes.

## Schedule

| Week | Date | Topic | Class note | Assignments |
|---|---|---|---|---|
<% rows %>

## Other course material

- [[<% syllabus %>#Important Dates|Important dates]]
- [[<% syllabus %>#Course Policies|Course policies]]
