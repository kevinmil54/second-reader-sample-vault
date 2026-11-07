*This guide covers two cases. If you downloaded the SR 101 starter vault from GitHub, the vault and the course's Zotero collection come together in one download. Its folders, templates, plugins and import format are already set up, so in Part 4 you can skip "Vault folders" and steps a–e. If you are setting up your own vault from scratch, follow every step. The import command in the starter vault is "Second Reader: APA Zotero import".*

# Setting Up Your Second Reader Note System

This gets your computer ready to take literature notes the Second Reader way:
import a paper from Zotero into a structured note, then read it in Zotero
with your note open right beside it — typing your own notes and highlighting
as you go. One click syncs your highlights into the note as quotes with page
numbers (without touching anything you've typed), and one checkbox promotes
your best ideas into standalone permanent notes. It's a one-time setup
(30–45 minutes) — after that, each new paper takes seconds to turn into a
note.

**Already set up from an earlier version?** Don't redo this setup — follow
**[UPDATING.md](https://github.com/kevinmil54/second-reader-obsidian-promote/blob/main/UPDATING.md)** instead.

Works on **Mac or Windows**. Steps are marked where they differ.

---

## How the pieces fit together

Every paper you read becomes a **Literature note** — your own notes on that
source, plus whatever Second Reader adds. From there, ideas worth keeping on
their own move through three more note types, each with its own top-level
folder in your vault:

- **Permanent notes** — one idea per note, in your own words, built to stand
  alone years from now. You create these by checking a box in a literature
  note.
- **Synthesis notes** — gather your Permanent notes on one topic (e.g.
  "College students are reading less than they once did") and state what
  you now think, short enough to reread in two minutes.
- **Project notes** — the argument-and-evidence framework for something
  you're actually writing (a paper, a talk) — pulls from your Permanent
  notes so you start from a structure instead of a blank page.

```
Literature note → Permanent notes → Synthesis note
                                  ↘ Project note
```

**Topics tie these together.** Each literature note and permanent note has
a `topics:` property, a list of one or two words for what it is about (for
example `ai-and-thinking`). Obsidian suggests the words you have already
used, so pick one when it fits and type a new word when none does. A
permanent note starts with the topics of the literature note it came from,
and you can change them. A synthesis note names one topic in its own
`topic:` property, and a list of the permanent notes on that topic that
the synthesis note does not link to yet fills itself. A note leaves the list
when you link it in your own writing.

A Permanent note's **Connections** section is where you link it to the
Synthesis and Project notes that draw on it. You add those links by hand as
your vault grows.

---

## 1. Get a good markdown editor

Your notes are plain text files in a format called **Markdown** (`# heading`,
`**bold**`, `[[links]]`). Obsidian (step 2) *is* a markdown editor and will
be where you do almost all your writing — but it's worth having a
lightweight general-purpose one too, for quickly opening a `.md` file
without launching Obsidian.

**Recommended: [Zettlr](https://www.zettlr.com/)** — free, open-source, and
identical on Mac and Windows. Unlike a general code editor, it's built
specifically for academic Markdown writing (citations, footnotes, live
preview), which fits this note-taking system well.

- **Mac:** Download the `.dmg` → open it → drag **Zettlr** to Applications.
- **Windows:** Download the installer → run it → accept the defaults.

**If you work with R or Quarto:** use **[Positron](https://positron.posit.co/)**
instead (or alongside Zettlr) — Posit's IDE built for R, Python, and Quarto
(`.qmd`) documents. Same install pattern on both platforms: download →
run the installer → open.

**Avoid TextEdit (Mac) and WordPad (Windows) for this** unless you switch
them to plain-text mode — both default to rich text and will quietly corrupt
a `.md` file with hidden formatting. Plain Notepad on Windows is fine in a
pinch; on Mac, use TextEdit's **Format → Make Plain Text** first.

---

## 2. Install Obsidian

1. Go to **[obsidian.md](https://obsidian.md/)** and click **Download** — it
   detects your OS automatically.
2. **Mac:** open the downloaded `.dmg`, drag **Obsidian** into Applications,
   launch it.
   **Windows:** run the downloaded installer, launch Obsidian when it
   finishes.
3. On first launch, open or create a vault (a vault is just a folder of
   notes).
   - **If you have the SR 101 starter vault:** download it from the link
     you were given, or from the GitHub page with the green **Code** button →
     **Download ZIP**. Unzip it somewhere that isn't inside another vault.
     The unzipped folder is named after the version you downloaded, such as
     `second-reader-sample-vault-1.1` or `second-reader-sample-vault-main`;
     you can rename it. In Obsidian choose
     **Open folder as vault** and pick that folder itself, not the folder
     that contains it. When Obsidian asks whether you trust the author,
     choose **Trust author and enable plugins**.
   - **If you're starting from scratch:** choose **Create a new vault**.

---

## 3. Install Zotero

Zotero is where your papers live; it's what feeds Obsidian the metadata
(title, authors, citation key) for each note.

1. Go to **[zotero.org/download](https://www.zotero.org/download/)** and
   download **Zotero 7** for your OS.
2. **Mac:** open the `.dmg`, drag Zotero to Applications.
   **Windows:** run the installer.
3. Launch Zotero. Create a free account at zotero.org when prompted, and
   sign in (Zotero → Settings → Sync) — this backs up your library and lets
   you use Zotero on more than one device. Not required, but you'll want it.
4. **Turn on the setting that lets Obsidian talk to Zotero:** Zotero →
   Settings → **Advanced** → check **"Allow other applications to
   communicate with Zotero."** Zotero must be running (in the background is
   fine) whenever you import a note in Obsidian.
5. **Install the Better BibTeX plugin.** This is what generates the stable
   citation key (like `smith2023learning`) and the formatted APA reference
   the templates use — without it, those fields come out blank.
   - Download the latest `.xpi` from
     **[the Better BibTeX releases page](https://github.com/retorquere/zotero-better-bibtex/releases/latest)**
     (the file named `zotero-better-bibtex-X.X.X.xpi`).
   - In Zotero: **Tools → Plugins** → gear icon (top right) → **"Install
     Plugin From File..."** → select the downloaded `.xpi`.
   - Restart Zotero.

### 3a. Install the Zotero Connector (browser extension)

This is what saves an article into Zotero straight from your browser.

1. Go to **[zotero.org/download](https://www.zotero.org/download/)** and
   scroll to **"Zotero Connector."** It detects your browser (Chrome,
   Firefox, Edge, Safari) and gives you the right install button.
2. Click it, then confirm the install in your browser's extension store.
3. **To use it:** open an article's webpage (or its PDF), click the Zotero
   icon that appears in your browser's toolbar. It saves the citation info —
   and the PDF, when available — into whichever collection is currently
   selected in the Zotero app. Zotero must be open for this to work.

### 3b. Add the class readings to Zotero

The class readings come as a Zotero collection: a `.rdf` file with a
`files` folder of PDFs next to it. Importing it puts every reading, with its
PDF, into your own Zotero library in one step. **Install Better BibTeX
(step 3, item 5) before doing this**, so each reading gets the same citation
key the literature notes expect.

1. Find the collection.
   - **Starter vault from GitHub:** it's already in the vault, in the
     `Second Reader Sample Readings (Zotero)` folder (`Second Reader Sample
     Readings (Zotero).rdf` and `files`). There's nothing else to download.
   - **A course that posts its readings on Canvas:** download the readings
     file (a `.zip`) and unzip it (**Mac:** double-click it; **Windows:**
     right-click → **Extract All…**). You'll get a folder containing a
     `.rdf` file and a `files` folder.
2. In Zotero: **File → Import…** → choose **"A file (BibTeX, RIS, Zotero
   RDF, etc.)"** → **Next** → select the `.rdf` file. Keep it where it is,
   with the `files` folder beside it; Zotero looks for the PDFs there.
3. On the options screen:
   - Leave **"Place imported collections and items into new collection"**
     checked, so the readings arrive in their own collection.
   - Under **File Handling**, choose **"Copy files to the Zotero storage
     folder."**
4. Click **Next**, then **Finish**. The readings appear in a new collection
   in your library, each with its PDF. Check that each item has a PDF under
   it.

Don't rename the items or change their citation keys in Zotero. The
literature notes find each reading by its citation key.

When your instructor adds readings later, they'll post another file.
Import it the same way.

---

## 4. Set up Obsidian for the Second Reader note system

### Vault folders

If you're using the starter vault, these folders are already there, along
with everything in steps a–e, so you can skip ahead to step f. If you're setting up your own
vault, create each of these at the top level of your vault (in Obsidian's
file explorer, right-click the vault's root → **New folder**, once per
name). It's often easier to start from the starter vault, rename it, and
delete the sample course.

| Folder | What it holds |
|---|---|
| `Classes` | One folder per course, with the syllabus, a course home note, and a `Meeting notes` folder with one note per class |
| `Literature notes` | One note per reading, made by the import command |
| `Authors` | One note per author, with a short bio, links and, if you like, a photo; literature notes embed these |
| `Permanent notes` | Your own ideas, one idea per note, made from literature notes |
| `Synthesis notes` | Notes that pull several permanent notes together on one topic |
| `Projects` | Notes for something you're writing, such as a paper or talk |
| `Inbox` | New and unsorted notes until you file them |
| `Images` | Figures from the papers, images from your Zotero highlights, and screenshots |
| `Templates` | The literature note, permanent note, synthesis note, project and class meeting templates |
| `Uploads` | Zips made by the syllabus's "Package my Week N" links, ready to hand in |

Then set `Images` as the attachment folder: Settings → **Files and links** →
**Default location for new attachments** → **In the folder specified below**
→ `Images`.

Everything below (the plugin's defaults, the import format, the templates'
Connections section) assumes these folders exist with these exact names:
plain spaces, no underscores or abbreviations.

### a. Turn on community plugins
Settings (gear icon) → **Community plugins** → **Turn on community
plugins** (you'll see a one-time warning about third-party code — this is
expected).

### b. Install "Second Reader"
One plugin does everything: imports papers from Zotero, syncs your
highlights, and promotes permanent-note candidates. You **don't** need the
separate "Zotero Integration" community plugin; Second Reader includes it.

In the SR 101 starter vault, Second Reader is already installed and
enabled. In any other vault:

1. Settings → Community plugins → **Browse** → search **"Second Reader"**
   → **Install** → **Enable**.
2. **If you have the "Zotero Integration" plugin from another class, turn
   it off** (Settings → Community plugins). Otherwise you'll see two sets
   of look-alike commands. Second Reader reminds you with a message until
   you do.
3. If you installed Second Reader earlier through BRAT, open BRAT's
   settings and remove `kevinmil54/second-reader-obsidian-promote` from
   its list of beta plugins, leaving Second Reader installed. Obsidian then
   updates it from the community directory, and your settings carry over.

### c. Get the two templates into your vault
Your instructor will give you two files — **`Literature Note Template -
Zotero Import.md`** and **`Permanent Note Template.md`** — or you can get
them from
**[the class repo's Templates folder](https://github.com/kevinmil54/second-reader-obsidian-promote/tree/main/Templates)**
(open each file there and use the download button). Put both into the
`Templates` folder you created above.

Your instructor may also give you a **Synthesis Note Template** and a
**Project Template** (they're in the starter vault). Put them in
`Templates` too. The lists of notes they build for you need the
**Dataview** community plugin (Settings → Community plugins → Browse →
"Dataview" → Install → Enable); without it, those lists show as code.

### d. Check the promote settings
Settings → **Second Reader** → **Promote candidates** (at the top). It
already defaults to `Templates/Permanent Note Template.md` for **Template
path** and `Permanent notes` for **New note folder** — check both match
where you put things, and adjust if you used different folder names.

### e. Check the import format
Second Reader comes with this import format already set up, with the
reference in APA 7th edition. Look under **Zotero import & highlight sync**
→ **Import Formats** on the same Settings page and check it matches the
list below. If you have no import format (for example after deleting it),
add one with these settings:
- **Name:** **"Literature Note"** — this name matters (see the note below).
- **Template:** the path to `Templates/Literature Note Template - Zotero
  Import.md`
- **Output path template:** `Literature notes/{{title}}.md` — this names
  each note after the reading's title, which is how the class syllabus finds
  your notes. (If you set this up earlier with `{{citekey}}`, Second Reader
  offers to fix it for you — see [UPDATING.md](https://github.com/kevinmil54/second-reader-obsidian-promote/blob/main/UPDATING.md).)
- **Bibliography Style:** search **"APA"** → choose **American Psychological
  Association 7th edition**

**Important:** once you save this, Obsidian gets a *new* command named after
it — **"Second Reader: Literature Note."** That's the command you'll use to
create every literature note. (The command always takes the format's name,
so if you named your format something else — or upgraded from an earlier
version with a differently named format — look for "Second Reader:" followed
by that name.)

### f. (Optional, recommended) Auto-open imported notes
Same Settings page → toggle **"Open the created or updated note(s) after
import"** on, so each new literature note opens automatically.

### g. Know where the sync button is
You'll use this every time you read, so it's worth finding now. There are
three ways to sync your Zotero highlights into a note — use whichever you
like:

1. **The highlighter button at the top of your literature note (easiest).**
   When a literature note is open, a small **highlighter-pen icon** appears
   in the row of icons at the **top-right corner of the note**, next to the
   `⋮` (more options) button. Hover over it and it says **"Sync Zotero
   highlights into this note."** It only shows up in literature notes made
   by the import command, so if you don't see it, you're probably looking at
   a different note.
2. **The highlighter button in the ribbon.** The ribbon is the thin vertical
   strip of icons along the **far-left edge** of the Obsidian window. The
   same highlighter-pen icon is in there — hover over the icons to find the
   one that says "Sync Zotero highlights into this note."
   - Don't see a strip of icons at all? Turn it on: Settings →
     **Appearance** → **Show ribbon**.
   - Too many icons to spot it? Drag the highlighter to the top of the
     strip, or right-click the ribbon to hide icons you don't use.
3. **A keyboard shortcut (optional).** Settings → **Hotkeys** → search
   **"Sync highlights"** → click `+` → press a shortcut you'll remember
   (e.g. `Cmd/Ctrl + Shift + S`). The command is also in the Command
   Palette as **"Second Reader: Sync highlights into current note."**

---

## Reading a paper: notes and highlights together

Once setup is done, this is the whole routine per paper.

### Before you start reading

1. **Make sure the article is in your Zotero.** Class readings already are,
   from step 3b. For anything else, click the Zotero Connector button on the
   article's webpage (best — pulls in full metadata), or drag the PDF
   straight into the Zotero app window. If you dragged in a bare PDF and
   the title or authors are blank, right-click the item → **"Retrieve
   Metadata for PDF."**
2. **Create the literature note.** In Obsidian: Command Palette →
   **"Second Reader: Literature Note"** (the command named after your import
   format from step 4e). Search for the article by title or author and
   select it. Obsidian creates the note, pre-filled with title, authors,
   year, an **Open PDF** link, the Zotero link, and the full APA reference.
   Make every class reading's note this way, and don't rename the note, so
   the syllabus can find it. In the starter vault, every class reading
   already has its literature note; open it from the syllabus instead.
3. **Open the paper** with the **Open PDF** link at the top of the note, or
   with the **open pdf** link next to that reading in the class syllabus
   (see [Using the class syllabus](#using-the-class-syllabus)).

### While you read

4. **Put the paper and the note side by side.** Open the PDF in **Zotero's
   own reader** (the **Open PDF** link from step 3 opens it there, or
   double-click the PDF in Zotero) on one half of your screen, and your
   literature note in Obsidian on the other.
   - **Mac:** hover over a window's green button → **Tile Window to Left of
     Screen**, then click the other window to fill the right side.
   - **Windows:** press `Win + ←` in one window, then pick the other window
     to fill the right side.
5. **Type and highlight in whatever rhythm suits you.** Highlight passages
   worth keeping in Zotero, and add a comment to a highlight when you have
   a reaction (click the highlight, then type in its comment box). At the
   same time, type your own notes into the literature note — "Summary (in my
   own words)," "Key ideas," questions as they occur to you.
   Highlight in **Zotero's** reader, not Preview or Adobe — Zotero's reader
   is what records the real (printed) page number for each highlight.
   - **Keeping a figure or table:** use the **select-area** tool in Zotero's
     reader to draw a box around it. When you sync, the image comes into
     "Quotes worth keeping" with its page number, like a highlight.
6. **Sync whenever you like** — after each section, or only at the end.
   Click the **highlighter-pen icon at the top-right of your literature
   note** (or use the ribbon icon or your shortcut — see step 4g). Every
   highlight and comment made since your last sync appears under **"Quotes
   worth keeping,"** each with its page number. Nothing you've typed is
   touched — it's safe to sync in the middle of a sentence.
   - Edit, trim, or react to imported quotes freely; syncing again won't
     undo your edits or duplicate quotes.
   - You can move a quote into another section (say, next to the idea it
     supports) — it won't be re-added to the Quotes section.
   - Each quote ends with a code like `^nb-ABCD1234`. Leave it: it's how
     sync knows the quote is already in your note, and it lets you link to
     that exact quote from a permanent note.

### Promoting ideas

7. When an idea is worth its own standalone note, write its title in your
   own words under **"Permanent note candidates."** Want to add more before
   promoting it? Press **Enter, then Tab** right after the title to write an
   indented line or two — that carries over into the new note too.
8. **Check its box** — a new permanent note is created automatically, built
   from the Permanent Note Template, and that line becomes a link to it.
9. **Coming back to the paper later?** Keep highlighting in Zotero and sync
   again — new highlights are added and everything else stays as you left
   it.
10. When you finish a literature note, fill in its `topics:` property. When
   three or four permanent notes share a topic, gather them into a
   **Synthesis note** (in your `Synthesis notes` folder) that says what you
   now think about it. With Second Reader 2.11 or later the note is created
   for you when a topic reaches four permanent notes, with a list of the
   permanent notes you have not used yet. To make one yourself, put the topic in
   the synthesis note's `topic:` property. Use **Project notes** (in `Projects`) when you're actually
   writing something and want to pull together the Permanent notes that
   support it. Link back to a Permanent note's **Connections** section as
   you build these.

---

## Using the class syllabus

The syllabus is an Obsidian note. In the starter vault it's already in
`Classes/SR 101 example/Winter 2027`, with a course home note and a meeting note
for each class. For another course, your instructor gives you the syllabus
(for example on Canvas); put it in that course's folder under `Classes`. Each reading in it has two
links:

> Zotero: **open pdf** · Literature note: **[[Title of the reading]]**

**The literature-note link shows where you are with each reading** by its
color:

| Link looks like | Meaning |
|---|---|
| Dimmed (Obsidian's "not created yet" style) | You haven't made the literature note yet |
| Normal link color | You've made the note but haven't written in it yet |
| **Yellow** | You've synced Zotero highlights into it, but haven't typed anything yet |
| **Green** | You've written your own notes in it |

Click the link to open the note (or to create it, if it's dimmed — but use
the import command from step 2 above instead, so the note gets filled in).

**"open pdf" opens your own copy of the reading** in Zotero's PDF reader.
It works once you've made that reading's literature note; if you haven't, a
message tells you which command to run. (Zotero needs to be open.)

### Handing in a week's literature notes

Under each week's heading in the syllabus there is a link, **Package my
Week N literature notes for upload**. Click it and Second Reader:

1. finds the literature notes you have worked on for that week's readings
   (one file per reading). Notes that are still blank, and readings you
   haven't made a note for, are skipped and listed in the message;
2. puts them in a zip named like `SR 101 Week 01 literature notes - Your Name.zip`
   in the `Uploads` folder of your vault;
3. shows the zip in Finder (Explorer on Windows), ready to hand in (for
   example on Canvas).

The first time, it asks for your name; you can change it later under
Settings → Second Reader → "Your name". Clicking the link again replaces
that week's zip with a fresh one. You can also run **"Second Reader: Package
a week's literature notes for upload"** with the syllabus open and pick the
week.

---

## Getting updates later

The plugin improves from time to time. Obsidian updates it like any other
community plugin: Settings → Community plugins → **Check for updates**, or
turn on automatic updates there.

If your literature-note template is too old to bring in highlights, Second
Reader offers to update it for you (it asks when Obsidian starts, and again
if you try to sync). You can also run **"Second Reader: Update
literature-note template"** from the Command Palette at any time. It only
changes the "Quotes worth keeping" section and saves a backup of your old
template first. For any other template change, re-download it from
**[the class repo](https://github.com/kevinmil54/second-reader-obsidian-promote/tree/main/Templates)**
and replace your copy.

A newer copy of the starter vault on GitHub won't replace yours
automatically. If you want something from it, such as an updated syllabus,
download the new copy somewhere else and copy over only the files you need.
Don't copy over your literature notes or permanent notes, or you'll lose
what you wrote.

### Upgrading to Second Reader 2

If you set things up earlier this term (with "Second Reader: Promote
Candidates" plus the separate "Zotero Integration" plugin), follow the
step-by-step instructions in **[UPDATING.md](https://github.com/kevinmil54/second-reader-obsidian-promote/blob/main/UPDATING.md)**.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Second Reader: Literature Note" doesn't appear in the Command Palette | Plugin isn't enabled, the import format isn't set up yet (step 4e), or Obsidian needs a full restart (not just a reload). If you upgraded, look for "Second Reader: …" — the old "Zotero Integration: …" names are gone. |
| An import made an empty note titled with just the citekey (e.g. `smith2023learning`) | That came from the old generic "Import notes" command, which ignores your template (Second Reader 2.0.1 and later no longer have it). Delete the empty note and use the command named after your import format ("Second Reader: Literature Note"). |
| Every Zotero command appears twice | The old "Zotero Integration" plugin is still on — turn it off in Settings → Community plugins. |
| Import or sync fails / "could not connect to Zotero" / "is Zotero running?" | Zotero desktop must be running. Check Zotero → Settings → Advanced → "Allow other applications to communicate with Zotero" is checked. |
| Sync says "No new highlights" but you just highlighted | The highlights were made in another PDF app (Preview, Adobe) — make them in **Zotero's** PDF reader. Also check that the note you have open is the literature note for that paper. |
| "open pdf" in the syllabus says you haven't made the literature note yet, but you have | The note's name doesn't match the syllabus link. If it's named by citation key (like `cai2009`), run **"Second Reader: Name literature notes by title"**; if you renamed it, rename it back to the title shown in the syllabus link. |
| "open pdf" says it couldn't find a PDF | Make sure Zotero is open, and that the reading has its PDF attached in your Zotero library (re-import the class readings from the vault's `Second Reader Sample Readings (Zotero)` folder, or from Canvas, if it's missing). |
| A syllabus link stays dimmed after you made the note | The note's name has to match the link exactly. If your notes are named by citation key (like `cai2009`), run **"Second Reader: Name literature notes by title"** — it renames them and fixes your import format. Otherwise rename the note to the title shown in the link. |
| A syllabus link is green but you haven't written anything | Anything typed in the note body counts — check for a stray word or line. Filling in the top section (your name, course, date read) doesn't count. |
| Readings import into Zotero without PDFs | When importing the class readings file, choose **"Copy files to the Zotero storage folder"**, and import the `.rdf` from where it sits, with its `files` folder next to it. In the starter vault that's the `Second Reader Sample Readings (Zotero)` folder. |
| Sync says the note "has no citekey in its frontmatter" | Sync only works in a literature note created by the import command, which records the paper's citekey at the top of the note. Don't delete the `citekey:` line. |
| Quotes show the PDF's sheet number instead of the printed page | The PDF's page numbering is missing or wrong. In Zotero's reader, right-click a page in the thumbnails sidebar → **Rename Page…** to set the correct number; future syncs will use it (quotes already synced keep their old number — edit them by hand). |
| A quote I deleted from the note came back after syncing | Syncing adds any highlight that isn't in the note yet. To remove a quote for good, delete the highlight in Zotero too. |
| A highlight you deleted in Zotero is still in the note | Syncing only *adds* quotes; it never removes them. Delete the quote in Obsidian by hand. |
| Citation key or reference comes out blank, or shows `{{citekey}}` literally | Better BibTeX isn't installed, or Zotero wasn't restarted after installing it. |
| Import errors on a paper with no publication year | Fixed as of the current template — if you're on an older copy, update to the latest from [the class repo](https://github.com/kevinmil54/second-reader-obsidian-promote/tree/main/Templates). |
| Checking a candidate box just crosses out the text — no new note appears | The "Second Reader" plugin isn't enabled, the note's frontmatter is missing `tags: [literature-note]`, or the heading isn't exactly `## Permanent note candidates`. |
| Reference style isn't APA | You likely set the "Citation Style" (used for inline citations) instead of the **Import Format's own "Bibliography Style"** field — these are two separate settings in the plugin. |
