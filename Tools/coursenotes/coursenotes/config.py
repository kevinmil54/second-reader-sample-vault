"""Configuration (course.toml). Uses tomllib when available, else a small built-in reader."""
from __future__ import annotations

import os
import re

try:  # Python 3.11+
    import tomllib as _tomllib
except ImportError:  # pragma: no cover
    try:
        import tomli as _tomllib  # type: ignore
    except ImportError:
        _tomllib = None


def _parse_value(s: str):
    s = s.strip()
    if s.startswith('"'):
        m = re.match(r'"((?:[^"\\]|\\.)*)"\s*(?:#.*)?$', s)
        if not m:
            raise ValueError("bad string value: " + s)
        return m.group(1).replace('\\"', '"').replace("\\\\", "\\").replace("\\n", "\n")
    if s.startswith("'"):
        m = re.match(r"'([^']*)'\s*(?:#.*)?$", s)
        if not m:
            raise ValueError("bad string value: " + s)
        return m.group(1)
    if s.startswith("["):
        inner = s[1 : s.rindex("]")]
        found = re.findall(r'"((?:[^"\\]|\\.)*)"|\'([^\']*)\'', inner)
        return [a or b for a, b in found]
    s = re.sub(r"\s+#.*$", "", s)
    if s in ("true", "false"):
        return s == "true"
    try:
        return int(s)
    except ValueError:
        return s


def _mini_toml(text: str) -> dict:
    data: dict = {}
    cur = data
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"\[([\w.\-]+)\]$", line)
        if m:
            cur = data
            for part in m.group(1).split("."):
                cur = cur.setdefault(part, {})
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            cur[k.strip()] = _parse_value(v)
    return data


def read_toml(path: str) -> dict:
    with open(path, "rb") as fh:
        raw = fh.read()
    if _tomllib is not None:
        return _tomllib.loads(raw.decode("utf-8"))
    return _mini_toml(raw.decode("utf-8"))


DEFAULT_WEEK_HEADING = r"^#{2,6}\s*Week\s+(\d+)\s*(?:\(([^)]*)\))?\s*[:\-–—]?\s*(.*?)\s*$"

DEFAULTS = {
    "course": {"literature_dir": "Literature notes"},
    "zotero": {
        "data_dir": "~/Zotero",
        "csl_json": "My Library.json",
        "csl_style": "styles/apa.csl",
        "sqlite": "zotero.sqlite",
        "link_style": "key",
    },
    "syllabus": {"week_heading": DEFAULT_WEEK_HEADING},
    "classes": {"name_format": "Class {nn} - {date} - Student"},
}


class Config:
    def __init__(self, data: dict, path: str):
        self.data = data
        self.path = os.path.abspath(path)
        self.base = os.path.dirname(self.path)

    # -- generic access -------------------------------------------------
    def get(self, section: str, key: str, default=None):
        v = self.data.get(section, {}).get(key)
        if v is None or v == "":
            v = DEFAULTS.get(section, {}).get(key, default)
        return default if v is None else v

    def _abs(self, p: str, base: str) -> str:
        p = os.path.expanduser(p)
        return p if os.path.isabs(p) else os.path.join(base, p)

    # -- locations --------------------------------------------------------
    @property
    def vault_root(self) -> str:
        r = self.get("vault", "root", "")
        return os.path.abspath(self._abs(r, self.base)) if r else self.base

    @property
    def syllabus(self) -> str:
        s = self.get("course", "syllabus", "")
        if not s:
            raise SystemExit("config: [course] syllabus is required")
        return self._abs(s, self.vault_root)

    @property
    def course_dir(self) -> str:
        return os.path.dirname(self.syllabus)

    @property
    def literature_dir(self) -> str:
        return self._abs(self.get("course", "literature_dir", "Literature notes"), self.vault_root)

    @property
    def classes_dir(self) -> str:
        return self._abs(self.get("course", "classes_dir", "") or "Meeting notes", self.course_dir)

    @property
    def reports_dir(self) -> str:
        return self._abs(self.get("course", "reports_dir", "") or "Tool reports", self.course_dir)

    @property
    def state_dir(self) -> str:
        return os.path.join(self.course_dir, ".coursenotes")

    @property
    def zotero_dir(self) -> str:
        return os.path.expanduser(self.get("zotero", "data_dir", "~/Zotero"))

    def zpath(self, key: str, default: str = "") -> str:
        p = self.get("zotero", key, default)
        return self._abs(p, self.zotero_dir) if p else ""

    @property
    def collections(self) -> list:
        c = self.data.get("zotero", {}).get("collections", [])
        return [c] if isinstance(c, str) else list(c)


def load_config(path: str) -> Config:
    if not os.path.exists(path):
        raise SystemExit("config file not found: %s (run `coursenotes init`)" % path)
    return Config(read_toml(path), path)
