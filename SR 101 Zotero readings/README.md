# SR 101 Zotero readings

This folder is a Zotero collection of the SR 101 readings, in the same form as a Zotero "Export Collection… → Zotero RDF" with files.

- `SR 101 - Thinking With Machines.rdf` has the reference for each reading and points to its PDF under `files/`. Importing it creates a Zotero collection with that name.
- `files/` holds the PDFs. Every reading was chosen because its license allows the PDF to be shared publicly (see `SOURCES.md`).
- `fetch_readings.py` downloads any PDF that's missing.

## If a PDF is missing

The PDFs should already be in `files/`. If one isn't, open Terminal in this folder and run:

```
python3 fetch_readings.py
```

It skips PDFs that are already here. If a site refuses the download, the script names the file and the place to save it; download that one in your browser and save it under that name.

## Importing into Zotero

1. In Zotero, choose **File → Import…** → **A file (BibTeX, RIS, Zotero RDF, etc.)** → pick `SR 101 - Thinking With Machines.rdf`.
2. When asked about files, choose **Copy files to the Zotero storage folder**.
3. Check that each item has a PDF under it. If one doesn't, drag that PDF from `files/` onto the item.

The literature notes in the vault are already made and carry each reading's citation key, so they find these items in your Zotero. Don't rename the items or change their citation keys.

## Giving the collection to other people

Run `python3 fetch_readings.py --zip`. It makes `SR 101 Zotero readings.zip` with the Zotero file and every PDF, ready to post on Canvas or anywhere else. People unzip it and follow "Importing into Zotero" above.

All the readings are openly licensed. Two of them (Kosmyna et al. and Doshi & Hauser) are licensed for noncommercial use only, so don't sell the package.
