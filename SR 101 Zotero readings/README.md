# SR 101 Zotero readings

This folder holds the SR 101 readings in a form Zotero can import.

- `SR 101 readings.ris` has the reference for each reading and points to its PDF under `files/`.
- `files/` holds the PDFs. Only the ones whose licenses allow redistribution are included in the repository. See `SOURCES.md` at the top of the repository.
- `fetch_readings.py` downloads the rest to your own computer.

## Steps

1. Get the PDFs that aren't included. On a Mac, open Terminal in this folder and run:

   ```
   python3 fetch_readings.py
   ```

   It skips PDFs that are already here. If a site refuses the download, the script names the file and the place to save it; download that one in your browser.

2. In Zotero, make a new collection for the course (for example "SR 101"), select it, then choose **File → Import…** → **A file (BibTeX, RIS, Zotero RDF, etc.)** → pick `SR 101 readings.ris`. When asked about files, choose **Copy files to the Zotero storage folder**.

3. Check that each item has a PDF under it. If one doesn't, drag that PDF from `files/` onto the item.

4. In Obsidian, run **Second Reader: APA Zotero import** for each reading you want to start. Keep the titles Zotero shows: the syllabus finds your literature notes by title.
