"""
Render a class agenda markdown file (format from the lesson-planning skill, Phase 3)
to a three-column PDF (time | segment | details) with WeasyPrint.

Usage: python agenda_md_to_pdf.py agenda.md output.pdf
Needs: pip install weasyprint --break-system-packages
"""
import html, re, sys
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

ACCENT, LIGHT_BG, MID_BG = "#00274C", "#eef3f7", "#c8d8e8"

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s

def parse(md):
    head, reading, rows, footer = [], [], [], {"lines": []}
    body, foot = md.split("\n---\n", 1) if "\n---\n" in md else (md, "")
    for line in foot.strip().splitlines():
        m = re.match(r"(closing|lookahead|note):\s*(.*)", line)
        if m: footer[m.group(1)] = m.group(2)
        elif line.startswith("- "): footer["lines"].append(line[2:])
    blocks = re.split(r"\n\s*\n", body.strip())
    for b in blocks:
        lines = b.splitlines()
        if lines[0].startswith("# ") or lines[0].startswith("> "):
            for l in lines:
                if l.startswith("# "): head.append(("h1", l[2:]))
                elif l.startswith("## "): head.append(("h2", l[3:]))
                elif l.startswith("### "): head.append(("h3", l[4:]))
                elif l.startswith(">"): reading.append(l.lstrip("> ").rstrip())
            continue
        if lines[0].startswith("## ") and len(lines) == 1:
            rows.append({"type": "section", "title": lines[0][3:]}); continue
        m = re.match(r"(\d{1,2}:\d{2}[–-]\d{1,2}:\d{2}) · (.*)", lines[0])
        if not m: continue
        det = ""
        for l in lines[1:]:
            if l.startswith("- "): det += f'<span class="plain">{inline(l[2:])}</span>'
            elif l.startswith("*") and l.endswith("*") and not l.startswith("**"): det += f"<em>{inline(l[1:-1])}</em>"
            else: det += f'<span class="plain">{inline(l)}</span>'
        rows.append({"type": "row", "time": m.group(1), "title": inline(m.group(2)), "det": det})
    return head, reading, rows, footer

def build(md):
    head, reading, rows, footer = parse(md)
    hh = "".join(f"<{t}>{inline(x)}</{t}>" for t, x in head)
    rd = "<br>".join(inline(x) for x in reading)
    trs = ""
    for r in rows:
        if r["type"] == "section":
            trs += f'<tr class="section-row"><td colspan="3">{inline(r["title"])}</td></tr>'
        else:
            trs += f'<tr><td class="time">{r["time"]}</td><td class="title">{r["title"]}</td><td class="det">{r["det"]}</td></tr>'
    la = "".join(f'<div class="lr">&rarr; {inline(x)}</div>' for x in footer["lines"])
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Noto Sans","DejaVu Sans",sans-serif;font-size:9pt;color:#1a1a1a;padding:10mm 14mm 8mm 14mm}}
.hd{{border-bottom:2.5px solid {ACCENT};padding-bottom:5px;margin-bottom:8px}}
.hd h1{{font-size:12pt;font-weight:700;color:{ACCENT}}} .hd h2{{font-size:9pt;font-weight:600;color:#333;margin-top:2px}}
.hd h3{{font-size:9.5pt;font-weight:400;font-style:italic;color:{ACCENT};margin-top:2px}}
.rb{{background:{LIGHT_BG};border-left:3px solid {ACCENT};padding:5px 8px;margin-bottom:9px;font-size:8pt;color:#333;line-height:1.45}}
table{{width:100%;border-collapse:collapse;margin-bottom:9px}} col.t{{width:12%}} col.s{{width:22%}} col.d{{width:66%}}
thead th{{background:{ACCENT};color:#fff;font-size:8pt;padding:4px 6px;text-align:left;text-transform:uppercase;letter-spacing:.05em}}
tbody tr:nth-child(odd){{background:#fff}} tbody tr:nth-child(even){{background:{LIGHT_BG}}}
tr.section-row td{{background:{MID_BG};color:{ACCENT};font-weight:700;font-size:8pt;padding:3px 6px;text-transform:uppercase;letter-spacing:.06em}}
tbody td{{padding:3.5px 6px;vertical-align:top;font-size:8.2pt;line-height:1.38}}
td.time{{color:#444;font-weight:600;white-space:nowrap}} td.title{{font-weight:700}}
td.det em{{font-style:italic;color:#003366;display:block;margin-bottom:2px}} td.det .plain{{display:block;margin-bottom:2px}}
tr{{page-break-inside:avoid}}
.ft{{border-top:1.5px solid {ACCENT};padding-top:7px;display:flex;gap:16px}} .fl{{flex:0 0 40%}} .fr{{flex:1}}
.lab{{font-size:7.5pt;font-weight:700;color:{ACCENT};text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px}}
.cq{{font-size:9pt;font-style:italic;font-weight:600;line-height:1.4}} .br{{font-size:8.5pt;font-style:italic;color:#333;margin-bottom:5px;line-height:1.4}} .lr{{font-size:8pt;color:#444;margin-bottom:2px}}
</style></head><body>
<div class="hd">{hh}</div>
<div class="rb">{rd}</div>
<table><colgroup><col class="t"><col class="s"><col class="d"></colgroup>
<thead><tr><th>Time</th><th>Segment</th><th>Details</th></tr></thead><tbody>{trs}</tbody></table>
<div class="ft"><div class="fl"><div class="lab">Closing reflection</div><div class="cq">{inline(footer.get("closing",""))}</div></div>
<div class="fr"><div class="lab">{inline(footer.get("lookahead",""))}</div><div class="br">{inline(footer.get("note",""))}</div>{la}</div></div>
</body></html>"""

if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    fc = FontConfiguration()
    HTML(string=build(open(src, encoding="utf-8").read())).write_pdf(
        out, stylesheets=[CSS(string="@page{size:letter;margin:0}", font_config=fc)], font_config=fc)
    print("wrote", out)
