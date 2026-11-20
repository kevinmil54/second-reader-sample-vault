"""Render APA references from CSL JSON with citeproc-py and a CSL style file."""
from __future__ import annotations

import html
import json
import re
import warnings

warnings.filterwarnings("ignore", message="The following arguments for Reference are unsupported")


def _fix_dates(e: dict) -> dict:
    e = json.loads(json.dumps(e))
    for k in ("issued", "accessed", "original-date"):
        if k in e and isinstance(e[k], dict) and "date-parts" in e[k]:
            e[k]["date-parts"] = [[int(x) for x in p if str(x).isdigit()] for p in e[k]["date-parts"]]
    return e


class Renderer:
    def __init__(self, style_path: str):
        try:
            from citeproc import CitationStylesStyle, CitationStylesBibliography, formatter, Citation, CitationItem
            from citeproc.source.json import CiteProcJSON
        except ImportError as exc:  # pragma: no cover
            raise SystemExit("citeproc-py is required: pip install citeproc-py") from exc
        self._mods = (CitationStylesBibliography, formatter, Citation, CitationItem, CiteProcJSON)
        self.style = CitationStylesStyle(style_path, validate=False)

    def apa(self, csl: dict) -> str:
        Bib, formatter, Citation, CitationItem, CiteProcJSON = self._mods
        e = _fix_dates(csl)
        src = CiteProcJSON([e])
        bib = Bib(self.style, src, formatter.html)
        bib.register(Citation([CitationItem(e["id"])]))
        s = str(bib.bibliography()[0])
        s = re.sub(r"</?(span|div)[^>]*>", "", s)
        s = re.sub(r"<i>(.*?)</i>", r"_\1_", s)
        s = re.sub(r"<b>(.*?)</b>", r"**\1**", s)
        s = html.unescape(s).strip()
        s = re.sub(
            r"(?<![\(\[])(https?://[^\s)]+?)(?=[.,;]?(\s|$))", lambda m: "[%s](%s)" % (m.group(1), m.group(1)), s
        )
        return s
