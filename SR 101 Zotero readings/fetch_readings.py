#!/usr/bin/env python3
"""Download the SR 101 readings into files/, where the Zotero file
"SR 101 - Thinking With Machines.rdf" expects them, and optionally zip the
folder so you can hand it to someone.

PDFs whose licenses allow redistribution may already be here; this script
skips any file that exists. The others are downloaded only to your computer
and are kept out of the repository by .gitignore.

Usage (from this folder):
    python3 fetch_readings.py            download what's missing
    python3 fetch_readings.py --zip      then make "SR 101 Zotero readings.zip"
"""
import json
import os
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
RDF = "SR 101 - Thinking With Machines.rdf"
ZIP_NAME = "SR 101 Zotero readings.zip"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) SecondReaderSample/1.0"


def is_pdf(path):
    with open(path, "rb") as f:
        return f.read(5) == b"%PDF-"


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    tmp = dest + ".part"
    with open(tmp, "wb") as f:
        f.write(data)
    if not is_pdf(tmp):
        os.remove(tmp)
        raise ValueError("response was not a PDF (the site may require a browser)")
    os.replace(tmp, dest)


def make_zip(readings):
    out = os.path.join(HERE, ZIP_NAME)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(HERE, RDF), f"SR 101 Zotero readings/{RDF}")
        for r in readings:
            p = os.path.join(HERE, r["path"])
            if os.path.exists(p):
                z.write(p, f"SR 101 Zotero readings/{r['path']}")
    print(f"\nMade {ZIP_NAME}. It contains every PDF you have here, including ones whose")
    print("licenses don't allow redistribution, so share it with your own students, not publicly.")


def main():
    with open(os.path.join(HERE, "readings.json"), encoding="utf-8") as f:
        readings = json.load(f)
    failed = []
    for r in readings:
        dest = os.path.join(HERE, r["path"])
        if os.path.exists(dest) and is_pdf(dest):
            print(f"have  {r['path']}")
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        for url in r["urls"]:
            try:
                fetch(url, dest)
                print(f"got   {r['path']}")
                break
            except Exception as e:  # noqa: BLE001
                print(f"      {url}: {e}")
        else:
            failed.append(r)
    if failed:
        print("\nDownload these by hand in a browser and save them under the path shown:")
        for r in failed:
            print(f"  {r['path']}\n      <- {r['urls'][0]}")
    else:
        print(f"\nAll readings are in files/. Import '{RDF}' into Zotero.")
    if "--zip" in sys.argv:
        make_zip(readings)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
