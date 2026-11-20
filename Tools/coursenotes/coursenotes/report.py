from __future__ import annotations

import os
import time
from typing import List


def cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def table(headers: List[str], rows: List[list]) -> str:
    if not rows:
        return "_none_\n"
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(cell(c) for c in r) + " |")
    return "\n".join(out) + "\n"


def write_report(cfg, name: str, body: str) -> str:
    os.makedirs(cfg.reports_dir, exist_ok=True)
    path = os.path.join(cfg.reports_dir, "Report - %s.md" % name)
    head = "---\ntags: [coursenotes-report]\ngenerated: %s\n---\n\n" % time.strftime("%Y-%m-%d %H:%M")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + body)
    return path
