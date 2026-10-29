#!/usr/bin/env python3
"""Make Second Reader literature notes and author notes from a Zotero RDF export.

An instructor exports a course collection from Zotero (Export Collection… →
Zotero RDF, with "Export Files"). This script reads that export and writes,
inside an Obsidian vault:

  Literature notes/<title>.md   one note per reading, named the way Second
                                Reader's import names it, carrying the reading's
                                citation key so it finds the student's own copy
                                in Zotero after they import the same RDF
  Authors/<First Last>.md       one note per lead author; each literature note
                                embeds its lead author's "About" section

Existing notes are never overwritten, so it is safe to run again after adding
readings. Author details come from an optional JSON file (--authors), keyed by
the author's name as "First Last":

  {"Hao-Ping Lee": {"position": "...", "bio": "...", "homepage": "...",
                    "openalex": "A5...", "sources": ["https://..."]}}

Figures can be added from an optional JSON file (--figures), keyed by citation
key: {"lee2025": [{"file": "lee2025 fig01.png", "caption": "...", "page": 3}]},
with the images already in Images/<citekey>/.

Usage:
  python3 make_literature_notes.py --rdf "path/to/Course.rdf" --vault "path/to/vault"
      [--authors authors.json] [--figures figures.json] [--template path]

Only the Python standard library is needed.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from urllib.parse import quote

NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "z": "http://www.zotero.org/namespaces/export#",
    "dcterms": "http://purl.org/dc/terms/",
    "bib": "http://purl.org/net/biblio#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "link": "http://purl.org/rss/1.0/modules/link/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "prism": "http://prismstandard.org/namespaces/1.2/basic/",
}
ABOUT = "{%s}about" % NS["rdf"]
RESOURCE = "{%s}resource" % NS["rdf"]
SKIP_TYPES = {"attachment", "note", "memo"}


# ---------------------------------------------------------------- reading RDF

def text(el, path):
    found = el.find(path, NS)
    return found.text.strip() if found is not None and found.text else ""


def people(el, role="bib:authors"):
    out = []
    for p in el.findall(f"{role}/rdf:Seq/rdf:li/foaf:Person", NS):
        out.append((text(p, "foaf:surname"), text(p, "foaf:givenName")))
    return out


def identifiers(el):
    ids = {}
    for ident in el.findall("dc:identifier", NS):
        if ident.text and ident.text.strip():
            kind, _, value = ident.text.strip().partition(" ")
            ids[kind.upper()] = value.strip()
        uri = ident.find("dcterms:URI/rdf:value", NS)
        if uri is not None and uri.text:
            ids["URL"] = uri.text.strip()
    return ids


def read_rdf(path):
    root = ET.parse(path).getroot()
    nodes = {n.get(ABOUT): n for n in root if n.get(ABOUT)}
    items = []
    for n in root:
        itype = text(n, "z:itemType")
        if not itype or itype in SKIP_TYPES:
            continue
        container = {}
        part = n.find("dcterms:isPartOf", NS)
        if part is not None and part.get(RESOURCE) in nodes:
            c = nodes[part.get(RESOURCE)]
            container = {"title": text(c, "dc:title"), "volume": text(c, "prism:volume"),
                         "issue": text(c, "prism:number"), **identifiers(c)}
        pub = n.find("dc:publisher/foaf:Organization/foaf:name", NS)
        ids = identifiers(n)
        extra = text(n, "dc:description")
        key = text(n, "z:citationKey")
        m = re.search(r"^Citation Key:\s*(\S+)", extra, re.M)
        if not key and m:
            key = m.group(1)
        items.append({
            "type": itype,
            "title": text(n, "dc:title"),
            "authors": people(n),
            "date": text(n, "dc:date"),
            "container": container.get("title", ""),
            "volume": container.get("volume", "") or text(n, "prism:volume"),
            "issue": container.get("issue", "") or text(n, "prism:number"),
            "pages": text(n, "bib:pages"),
            "doi": ids.get("DOI") or container.get("DOI", ""),
            "url": ids.get("URL", ""),
            "publisher": pub.text.strip() if pub is not None and pub.text else "",
            "citekey": key,
        })
    return items


# ---------------------------------------------------------------- formatting

def year_of(date):
    m = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", date or "")
    return m.group(1) if m else "n.d."


def fallback_key(it):
    sur = it["authors"][0][0] if it["authors"] else "anon"
    sur = unicodedata.normalize("NFKD", sur).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", sur) + year_of(it["date"])


def note_name(title):
    """Second Reader's import file-name rules (replaceIllegalChars)."""
    s = re.sub(r"\s*[*?]+\s*", " ", title).strip()
    return re.sub(r'\s*[:"<>|]+\s*', " - ", s).strip()


def initials(given):
    parts = re.split(r"(\s+|-)", given.strip())
    out = ""
    for p in parts:
        if p == "-":
            out = out.rstrip() + "-"
        elif p.strip():
            out += p[0] + ". "
    return out.strip()


def apa_authors(authors):
    names = [f"{s}, {initials(g)}" if g else s for s, g in authors]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) <= 20:
        return ", ".join(names[:-1]) + ", & " + names[-1]
    return ", ".join(names[:19]) + ", . . . " + names[-1]


def apa(it):
    a = apa_authors(it["authors"])
    y = year_of(it["date"])
    t = it["title"]
    doi = f"https://doi.org/{it['doi']}" if it["doi"] else it["url"]
    end = f" {doi}" if doi else ""
    if it["type"] == "journalArticle":
        src = f"*{it['container']}, {it['volume']}*" if it["volume"] else f"*{it['container']}*"
        iss = f"({it['issue']})" if it["issue"] else ""
        pg = f", {it['pages']}" if it["pages"] else ""
        return f"{a} ({y}). {t}. {src}{iss}{pg}.{end}"
    if it["type"] == "conferencePaper":
        pub = f" {it['publisher']}." if it["publisher"] else ""
        return f"{a} ({y}). {t}. In *{it['container']}*.{pub}{end}"
    if it["type"] == "preprint":
        m = re.search(r"arXiv\.(\d{4}\.\d{4,5})", it["doi"] or "")
        num = f" (arXiv:{m.group(1)})" if m else ""
        pub = f" {it['publisher']}." if it["publisher"] else ""
        return f"{a} ({y}). *{t}*{num}.{pub}{end}"
    pub = f" {it['publisher']}." if it["publisher"] else ""
    return f"{a} ({y}). *{t}*.{pub}{end}"


def full_name(person):
    s, g = person
    return f"{g} {s}".strip()


def file_safe(s):
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "-", s).strip()


def obsidian_param(s):
    out = quote(s, safe="-_.~!*'()")
    for c in "()'!*":
        out = out.replace(c, "%%%02X" % ord(c))
    return out


# ---------------------------------------------------------------- notes

def find_author(authors, person):
    """Details for a person: by "First Last", else by surname and first initial."""
    name = full_name(person)
    if name in authors:
        return authors[name]
    sur, given = person
    for k, v in authors.items():
        if k.split()[-1] == sur and given and k[0] == given[0]:
            return v
    return {}


def author_note(name, info):
    lines = ["---", f'name: "{name}"']
    if info.get("openalex"):
        lines.append(f"openalex: {info['openalex']}")
    lines += ["tags: [author]", "---", f"# {name}", "", "## About", "%% author-info start %%",
              f"%% Photo: save a photo in the Authors folder and embed it on the next line, e.g. ![[{name}.jpg|160]] %%"]
    if info.get("position"):
        lines.append(f"- **Position:** {info['position']}")
    if info.get("bio"):
        lines.append(f"- {info['bio']}")
    links = []
    if info.get("homepage"):
        links.append(f"[Homepage]({info['homepage']})")
    if info.get("openalex"):
        links.append(f"[OpenAlex profile](https://openalex.org/{info['openalex']})")
    if links:
        lines.append("- **Links:** " + " · ".join(links))
    if info.get("sources"):
        labels = [re.sub(r"^https?://(www\.)?", "", u).split("/")[0] for u in info["sources"]]
        lines.append("- **Sources:** " + " · ".join(f"[{lab}]({u})" for lab, u in zip(labels, info["sources"])))
    if not any(info.get(k) for k in ("position", "bio", "homepage", "openalex")):
        lines.append("*No details found yet.*")
    lines += ["%% author-info end %%", "", "## Readings in this vault", "",
              "```dataview", 'LIST FROM "Literature notes"', "WHERE contains(author, this.name)",
              "SORT year ASC", "```", "", "## Notes", "", ""]
    return "\n".join(lines)


def literature_note(it, template, lead, figures):
    key = it["citekey"]
    name = note_name(it["title"])
    authors = ", ".join(full_name(p) for p in it["authors"])
    open_pdf = f"obsidian://second-reader?open-pdf={obsidian_param(name)}"
    zotero = f"zotero://select/items/@{key}"
    title_yaml = it["title"].replace('"', '\\"')

    fm = "\n".join([
        "---", f'title: "{title_yaml}"', f"author: {authors}", f"year: {year_of(it['date'])}",
        f"citekey: {key}", f"zotero: {zotero}", "pdf: ", 'source-md: "[[]]"', "student: ", "course: ",
        "status: literature", "tags: [literature-note]", "date-read: ", "---", ""])

    body = template.split("\n---", 2)[-1] if template.startswith("---") else template
    body = body.lstrip("-\n")
    body = body.replace("{{title}}", it["title"])
    body = re.sub(r"> \*\*Zotero:\*\* .*",
                  f"> **Zotero:** [Open PDF]({open_pdf}) · [Open in Zotero]({zotero}) · "
                  f"**Cite:** [@{key}] · **Full text (md):** [[source-md]]", body)
    body = body.replace("{{bibliography}}", apa(it))
    body = re.sub(r"\{% persist \"annotations\" %\}[\s\S]*?\{% endpersist %\}",
                  "%% begin annotations %%\n%% end annotations %%", body)
    if lead:
        block = f"%% begin author-info %%\n![[{lead}#About]]\n%% end author-info %%"
        body = re.sub(r"(## Author information\n)\*Who wrote this\?[^\n]*\n\n- *\n",
                      lambda m: m.group(1) + block + "\n", body)
    if figures:
        figs = ["%% begin paper-figures %%"]
        for f in figures:
            page = f" (PDF p. {f['page']})" if f.get("page") else ""
            figs += [f"![[{f['file']}]]", f"*Caption from the paper:* {f['caption']}{page}", ""]
        figs[-1] = "%% end paper-figures %%"
        body = re.sub(r"(## Figures & images\n\*[^\n]*\*\n\n)!\[\[\]\]\n",
                      lambda m: m.group(1) + "\n".join(figs) + "\n", body)
    leftover = re.findall(r"\{\{.*?\}\}|\{%.*?%\}", body)
    if leftover:
        sys.exit(f"Template has fields this script doesn't fill: {sorted(set(leftover))}")
    return fm + "\n" + body.lstrip("\n"), name


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rdf", required=True)
    ap.add_argument("--vault", required=True)
    ap.add_argument("--authors", help="JSON file of author details")
    ap.add_argument("--figures", help="JSON file of figures by citation key")
    ap.add_argument("--template", help="literature-note template (default: the vault's)")
    args = ap.parse_args()

    vault = os.path.abspath(args.vault)
    tpath = args.template or os.path.join(vault, "Templates", "Literature Note Template - Zotero Import.md")
    with open(tpath, encoding="utf-8") as f:
        template = f.read()
    authors = json.load(open(args.authors, encoding="utf-8")) if args.authors else {}
    figures = json.load(open(args.figures, encoding="utf-8")) if args.figures else {}

    lit_dir = os.path.join(vault, "Literature notes")
    auth_dir = os.path.join(vault, "Authors")
    os.makedirs(lit_dir, exist_ok=True)
    os.makedirs(auth_dir, exist_ok=True)

    made, kept, made_a = [], [], []
    for it in read_rdf(args.rdf):
        if not it["citekey"]:
            it["citekey"] = fallback_key(it)
            print(f"note: no citation key in the RDF for '{it['title']}'; using {it['citekey']}")
        lead = file_safe(full_name(it["authors"][0])) if it["authors"] else ""
        if lead:
            ap_ = os.path.join(auth_dir, f"{lead}.md")
            if not os.path.exists(ap_):
                with open(ap_, "w", encoding="utf-8") as f:
                    f.write(author_note(lead, find_author(authors, it["authors"][0])))
                made_a.append(lead)
        text_, name = literature_note(it, template, lead, figures.get(it["citekey"], []))
        path = os.path.join(lit_dir, f"{name}.md")
        if os.path.exists(path):
            kept.append(name)
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_)
        made.append(name)

    print(f"Made {len(made)} literature note(s) and {len(made_a)} author note(s).")
    for n in made:
        print(f"  + {n}")
    if kept:
        print(f"Left {len(kept)} existing literature note(s) alone:")
        for n in kept:
            print(f"  = {n}")


if __name__ == "__main__":
    main()
