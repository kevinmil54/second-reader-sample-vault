import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from coursenotes.parse import parse_syllabus
from coursenotes.config import DEFAULT_WEEK_HEADING
from coursenotes.zotero import Item, Library, norm_doi
from coursenotes.match import match_all, title_sim
from coursenotes.notes import safe_filename
from coursenotes.link import apply_edits, plan_links

SYL = """# Syllabus

#### Week 1 (Sept 2): Intro
1. Smith, J. (2020). Learning well. _Journal of Things_, 5(2), 1-10. https://doi.org/10.1000/abc
2. Jones, K. (2019). Thinking fast: A study of speed. _Minds_, 3, 4-9.

#### Week 2 (Sept 9): Next
1. Nobody, X. (2001). A paper not in Zotero. _Nothing_, 1, 1-2.
"""


class FakeIndex:
    def note_for_item(self, key): return None
    def note_for_url(self, url): return None
    def resolve_name(self, name): return None


def toy_lib():
    lib = Library()
    for key, title, year, doi, auth in [
            ("AAAA1111", "Learning well", "2020", "10.1000/abc", "Smith"),
            ("BBBB2222", "Thinking fast: A study of speed", "2019", "", "Jones")]:
        it = Item(key, "journalArticle", {"title": title, "date": year, "DOI": doi}, [("author", auth, "X")])
        lib.items[key] = it
    lib._build_indexes()
    return lib


class Tests(unittest.TestCase):
    def test_parse(self):
        s = parse_syllabus(SYL, DEFAULT_WEEK_HEADING)
        self.assertEqual(len(s.weeks), 2)
        self.assertEqual(len(s.readings), 3)
        r = s.readings[0]
        self.assertEqual((r.author, r.year, r.doi), ("Smith", "2019" if False else "2020", "10.1000/abc"))

    def test_doi(self):
        self.assertEqual(norm_doi("https://doi.org/10.1000/ABC"), "10.1000/abc")

    def test_filename(self):
        self.assertNotIn(":", safe_filename("A: b/c"))

    def test_title_sim(self):
        self.assertGreater(title_sim("Learning well", "Learning well!"), 0.9)

    def test_match(self):
        s = parse_syllabus(SYL, DEFAULT_WEEK_HEADING)
        ms = match_all(s.readings, toy_lib(), [])
        self.assertEqual([m.item.key if m.item else None for m in ms], ["AAAA1111", "BBBB2222", None])

    def test_link_idempotent(self):
        s = parse_syllabus(SYL, DEFAULT_WEEK_HEADING)
        lib = toy_lib()
        ms = match_all(s.readings, lib, [])
        e = plan_links(s, ms, lib, FakeIndex(), {})
        new = apply_edits(s.lines, e)
        self.assertEqual(sum("Zotero:" in l for l in new), 2)
        s2 = parse_syllabus("\n".join(new), DEFAULT_WEEK_HEADING)
        ms2 = match_all(s2.readings, lib, [])
        self.assertEqual(plan_links(s2, ms2, lib, FakeIndex(), {}), [])


if __name__ == "__main__":
    unittest.main()
