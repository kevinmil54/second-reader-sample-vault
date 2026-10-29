#!/usr/bin/env python3
"""Download the SR 101 readings into files/ so Zotero can import them with
"SR 101 readings.ris".

PDFs whose licenses allow redistribution may already be here; this script
skips any file that exists. The others are downloaded only to your computer
and are kept out of the repository by .gitignore.

Usage (from this folder):
    python3 fetch_readings.py
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
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
            print(f"  {r['path']}  <-  {r['urls'][0]}\n      ({r['title']})")
        sys.exit(1)
    print("\nAll readings are in files/. Import 'SR 101 readings.ris' into Zotero.")


if __name__ == "__main__":
    main()
