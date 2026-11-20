---
tags: [home]
title: Projects home
---

[➕ New project](obsidian://second-reader?new-project=1)

## Projects

```dataview
TABLE category AS "Category", status AS "Status", output-type AS "Output"
FROM "Projects"
WHERE type = "project"
SORT string(category) ASC, file.name ASC
```

Projects are sorted by the `category:` property of each project note. Change a project's category there; nothing has to move.

## Time on projects

```dataviewjs
// Totals from Projects/project-time-log.csv, written by ▶️ Start and 🛑 Stop in each project letter.
const path = "Projects/project-time-log.csv";
if (!(await app.vault.adapter.exists(path))) {
  dv.paragraph("*No timed sessions yet.*");
} else {
  const text = await app.vault.adapter.read(path);
  const parse = line => {
    const out = []; let f = "", q = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (q) { if (c === '"') { if (line[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
      else if (c === '"') q = true; else if (c === ",") { out.push(f); f = ""; } else f += c;
    }
    out.push(f); return out;
  };
  const lines = text.split(/\r?\n/).filter(l => l.trim());
  const head = parse(lines[0]);
  const col = name => head.indexOf(name);
  const byProject = new Map();
  for (const line of lines.slice(1)) {
    const r = parse(line);
    const project = r[col("project")];
    const p = byProject.get(project) || { project, category: r[col("category")], letter: r[col("letter")], sessions: 0, minutes: 0, last: "", open: false };
    if (r[col("minutes")] !== "") { p.sessions++; p.minutes += Number(r[col("minutes")]); }
    if (!r[col("end")] && !r[col("note")]) p.open = true;
    if (r[col("start")] > p.last) p.last = r[col("start")];
    p.letter = r[col("letter")];
    byProject.set(project, p);
  }
  const fmt = m => m < 60 ? `${m} min` : `${Math.floor(m / 60)} h${m % 60 ? " " + (m % 60) + " min" : ""}`;
  const rows = [...byProject.values()].sort((a, b) => b.last.localeCompare(a.last));
  dv.table(["Project", "Category", "Sessions", "Time", "Last worked"],
    rows.map(p => [dv.fileLink(p.letter, false, p.project), p.category, p.sessions,
      fmt(p.minutes) + (p.open ? " (running)" : ""), p.last.slice(0, 10)]));
}
```


*Each ▶️ Start and 🛑 Stop in a project letter adds a row to `Projects/project-time-log.csv`, which opens in a spreadsheet or R.*
