"""Check citations against Crossref (and DataCite for arXiv/Zenodo-style DOIs). Needs network access.
Responses are cached in <course>/.coursenotes/cache so a rerun is instant and works offline."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from .match import _pages, title_sim
from .zotero import norm


class Fetcher:
    def __init__(self, cache_dir: str, mailto: str = "", offline: bool = False, pause: float = 0.12):
        self.cache_dir = cache_dir
        self.ua = "coursenotes/0.1" + (" (mailto:%s)" % mailto if mailto else "")
        self.offline = offline
        self.pause = pause
        self.failures = 0
        self.last_error = ""
        os.makedirs(cache_dir, exist_ok=True)

    def _curl(self, url: str):
        import shutil, subprocess
        exe = shutil.which("curl")
        if not exe:
            return None
        try:
            r = subprocess.run([exe, "-sS", "-L", "-m", "25", "-w", "\n%{http_code}", "-A", self.ua,
                                "-H", "Accept: application/json", url], capture_output=True, text=True, timeout=40)
        except Exception as e:
            self.last_error += " | curl: %s" % e
            return None
        body, _, code = r.stdout.rpartition("\n")
        if code == "404":
            return {"_status": 404}
        if code != "200":
            self.last_error += " | curl: HTTP %s %s" % (code, r.stderr.strip()[:100])
            return None
        try:
            time.sleep(self.pause)
            return json.loads(body)
        except ValueError:
            return None

    def get(self, url: str):
        p = os.path.join(self.cache_dir, hashlib.sha1(url.encode()).hexdigest() + ".json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        if self.offline:
            return None
        data = None
        try:
            req = urllib.request.Request(url, headers={"User-Agent": self.ua, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            time.sleep(self.pause)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data = {"_status": 404}
            else:
                self.failures += 1
                self.last_error = "HTTP %s from %s" % (e.code, url.split("/")[2])
                return None
        except Exception as e:
            # Python on macOS often lacks root certificates (CERTIFICATE_VERIFY_FAILED); curl uses the system store.
            self.last_error = "%s: %s" % (type(e).__name__, e)
            data = self._curl(url)
            if data is None:
                self.failures += 1
                return None
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        return data


def _crossref_rec(msg: dict) -> dict:
    years = set()
    for k in ("issued", "published-print", "published-online", "published"):
        dp = (msg.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            years.add(str(dp[0][0]))
    return {
        "source": "Crossref", "doi": msg.get("DOI", ""), "title": (msg.get("title") or [""])[0],
        "container": (msg.get("container-title") or [""])[0], "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""), "pages": msg.get("page", "") or msg.get("article-number", ""),
        "years": years, "families": [a.get("family", "") or a.get("name", "") for a in msg.get("author", [])],
    }


def _datacite_rec(attrs: dict) -> dict:
    return {
        "source": "DataCite", "doi": attrs.get("doi", ""), "title": ((attrs.get("titles") or [{}])[0]).get("title", ""),
        "container": "", "volume": "", "issue": "", "pages": "",
        "years": {str(attrs.get("publicationYear", ""))},
        "families": [c.get("familyName", "") or c.get("name", "") for c in attrs.get("creators", [])],
    }


def lookup_doi(fetcher: Fetcher, doi: str):
    q = urllib.parse.quote(doi, safe="/:()")
    d = fetcher.get("https://api.crossref.org/works/" + q)
    if d is None:
        return None, "lookup failed (offline or blocked)"
    if "message" in d:
        return _crossref_rec(d["message"]), ""
    d = fetcher.get("https://api.datacite.org/dois/" + q)
    if d and "data" in d:
        return _datacite_rec(d["data"]["attributes"]), ""
    return None, "DOI not found in Crossref or DataCite"


def search_title(fetcher: Fetcher, reading):
    q = urllib.parse.quote("%s %s" % (reading.title, reading.author))
    d = fetcher.get("https://api.crossref.org/works?query.bibliographic=%s&rows=3" % q)
    if not d or "message" not in d:
        return None, 0.0
    best, bs = None, 0.0
    for msg in d["message"].get("items", []):
        rec = _crossref_rec(msg)
        s = title_sim(reading.title, rec["title"])
        if s > bs:
            best, bs = rec, s
    return best, bs


def compare(fields: dict, rec: dict, label: str) -> list:
    """fields: year, volume, issue, pages, article, title, author (all strings, may be empty)."""
    out = []
    if fields.get("year") and rec["years"] and fields["year"] not in rec["years"]:
        out.append("%s year %s, %s %s" % (label, fields["year"], rec["source"], "/".join(sorted(rec["years"]))))
    if fields.get("volume") and rec["volume"] and fields["volume"] != rec["volume"]:
        out.append("%s volume %s, %s %s" % (label, fields["volume"], rec["source"], rec["volume"]))
    if fields.get("issue") and rec["issue"] and fields["issue"] != rec["issue"]:
        out.append("%s issue %s, %s %s" % (label, fields["issue"], rec["source"], rec["issue"]))
    p = fields.get("pages") or fields.get("article")
    if p and rec["pages"] and _pages(p) != _pages(rec["pages"]):
        out.append("%s pages %s, %s %s" % (label, p, rec["source"], rec["pages"]))
    if fields.get("title") and rec["title"] and title_sim(fields["title"], rec["title"]) < 0.8:
        out.append("%s title “%s”, %s “%s”" % (label, fields["title"][:60], rec["source"], rec["title"][:60]))
    if fields.get("author") and rec["families"] and norm(fields["author"].split(",")[0]) != norm(rec["families"][0]):
        out.append("%s first author %s, %s %s" % (label, fields["author"], rec["source"], rec["families"][0]))
    return out


def verify_all(matches, fetcher: Fetcher):
    rows = []
    for m in matches:
        r = m.reading
        syl = {"year": r.year, "volume": r.volume, "issue": r.issue, "pages": r.pages, "article": r.article,
               "title": r.title, "author": r.author}
        doi = r.doi or (m.item.doi if m.item else "")
        if doi:
            rec, err = lookup_doi(fetcher, doi)
            if rec is None:
                rows.append((r.id, "no-record", err, doi))
                continue
            issues = compare(syl, rec, "syllabus")
            if m.item is not None:
                it = m.item
                zf = {"year": it.year, "volume": it.field("volume"), "issue": it.field("issue"),
                      "pages": it.field("pages"), "title": it.title}
                issues += compare(zf, rec, "Zotero")
            rows.append((r.id, "mismatch" if issues else "ok", "; ".join(issues), doi))
        elif r.title:
            rec, s = search_title(fetcher, r)
            if rec is None:
                rows.append((r.id, "no-doi", "no DOI in the syllabus; search failed or found nothing", ""))
            elif s >= 0.85:
                issues = compare(syl, rec, "syllabus")
                rows.append((r.id, "found-doi", "likely DOI %s (title match %.2f)%s" % (rec["doi"], s, "; " + "; ".join(issues) if issues else ""), rec["doi"]))
            else:
                rows.append((r.id, "no-doi", "no confident match in Crossref (best title match %.2f): a book, report, web page, or a citation error" % s, ""))
        else:
            rows.append((r.id, "no-doi", "could not read a title from the syllabus line", ""))
    return rows
