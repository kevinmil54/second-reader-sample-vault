---
type: map
created: 2026-02-17
name: class-agenda-pdf
description: "Use when producing a student-facing class agenda/handout as a PDF. Generates a clean, concise 1-2 page PDF using Python reportlab with specific typography that students have responded well to. Covers any course. Input: lesson plan or session structure with segment titles, times, and discussion questions. Output: a PDF handout."
---

# Class Agenda PDF Skill

## Purpose

Generate a concise, well-formatted PDF agenda that students receive before or at the start of class. This is a *thinking tool* — the questions tell students what to prepare for and what to think about, not just what topics will be covered.

## Design Principles

1. **Questions are the backbone.** Every segment has at least one discussion question. If a segment doesn't have a question, it probably doesn't belong on the student agenda.

2. **Context is minimal.** One to two sentences of setup per segment — just enough to orient, not enough to summarize. Students have done the reading; the agenda tells them what we'll *do* with it.

3. **No instructor notes on the handout.** No "likely patterns," no "points to surface," no facilitation cues, no anticipated student responses. Those belong in the lesson plan, not the student agenda.

4. **End with what's next.** Include readings and a bridging question for the next session, separated by a horizontal rule.

5. **Prefer one page.** Two pages maximum. If it's longer, cut context, not questions.

## Layout and Typography

**Page setup:**
- Page size: US Letter (8.5 × 11 inches)
- Top margin: 0.7 inches
- Bottom margin: 0.6 inches
- Left/right margins: 0.8 inches

**Style specifications:**

| Element | Font | Size | Leading | Alignment | Other |
|---------|------|------|---------|-----------|-------|
| Title | Helvetica-Bold | 14pt | 18pt | Center | spaceAfter=2 |
| Subtitle (date/theme) | Helvetica | 10pt | 13pt | Center | textColor=#444444, spaceAfter=4 |
| Section heading | Helvetica-Bold | 11pt | 14pt | Left | spaceBefore=10, spaceAfter=4, textColor=#1a1a1a |
| Body text | Times-Roman | 10.5pt | 14pt | Left | spaceAfter=4 |
| Discussion questions | Times-Italic | 10.5pt | 14pt | Left | leftIndent=18, spaceAfter=4 |
| Concept bullets | Times-Roman | 10.5pt | 14pt | Left | leftIndent=18, spaceAfter=2 |
| Readings/next session | Times-Roman | 10pt | 13pt | Left | leftIndent=18 |
| Essential question | Times-Italic | 10.5pt | 14pt | Left | spaceAfter=6 |

**Horizontal rules:** HRFlowable, width="100%", thickness=0.5, color=#999999

## Document Structure

1. **Title** — Course name (centered, Helvetica-Bold 14pt)
2. **Subtitle** — Session theme, week number, and/or date (centered, Helvetica 10pt, gray)
3. **Horizontal rule**
4. **Essential question for the week** (if applicable) — Bold label ("Essential question for the week:"), followed by the question in regular weight
5. **Segments** — Each segment is:
   - Section heading: `"N. Title (XX min)"` in Helvetica-Bold 11pt
   - Brief context: 1–2 sentences in Times-Roman 10.5pt
   - Discussion question(s): Times-Italic 10.5pt, indented 18pt
   - Key concepts as bullets (if applicable): Times-Roman 10.5pt, indented 18pt
6. **Horizontal rule**
7. **"For [next session]:"** — Readings with bridging question, in slightly smaller type (10pt)

## Python Template

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.colors import HexColor

output_path = "/mnt/user-data/outputs/[filename].pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    topMargin=0.7*inch,
    bottomMargin=0.6*inch,
    leftMargin=0.8*inch,
    rightMargin=0.8*inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=14, leading=18,
    alignment=TA_CENTER, spaceAfter=2,
)
subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontName='Helvetica', fontSize=10, leading=13,
    alignment=TA_CENTER, spaceAfter=4, textColor=HexColor('#444444'),
)
section_style = ParagraphStyle(
    'Section', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=11, leading=14,
    spaceBefore=10, spaceAfter=4, textColor=HexColor('#1a1a1a'),
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=10.5, leading=14, spaceAfter=4,
)
question_style = ParagraphStyle(
    'Question', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=10.5, leading=14,
    leftIndent=18, spaceAfter=4,
)
bullet_style = ParagraphStyle(
    'Bullet', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=10.5, leading=14,
    leftIndent=18, spaceAfter=2,
)
reading_style = ParagraphStyle(
    'Reading', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=10, leading=13,
    leftIndent=18, spaceAfter=2,
)
essential_q_style = ParagraphStyle(
    'EssentialQ', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=10.5, leading=14, spaceAfter=6,
)

story = []

# --- Header ---
story.append(Paragraph("[Course Number] — [Course Name]", title_style))
story.append(Paragraph("[Week/Session info]: [Session Title]", subtitle_style))
story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#999999'), spaceAfter=8))

# --- Essential question (optional) ---
story.append(Paragraph(
    "<b>Essential question:</b> [The driving question for the session or week]",
    body_style
))

# --- Segments ---
story.append(Paragraph("1. Opening Question (10 min)", section_style))
story.append(Paragraph(
    "\u201c[The opening question, in quotes]\u201d",
    question_style
))

story.append(Paragraph("2. [Segment Title] (XX min)", section_style))
story.append(Paragraph(
    "[1-2 sentences of context]",
    body_style
))
story.append(Paragraph(
    "[Discussion question in italic]",
    question_style
))
story.append(Paragraph(
    "\u2022 [Key concept or term, if needed]",
    bullet_style
))

# ... additional segments ...

story.append(Paragraph("N. Closing Reflection (10 min)", section_style))
story.append(Paragraph(
    "What did you learn today that is new to you, important for you, "
    "and/or worth remembering?",
    question_style
))

# --- Next session ---
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#999999'), spaceAfter=6))
story.append(Paragraph("For [next session]", section_style))
story.append(Paragraph("[Reading 1 citation]", reading_style))
story.append(Paragraph("[Reading 2 citation]", reading_style))
story.append(Paragraph(
    "[Bridging question for next session]",
    question_style
))

doc.build(story)
print(f"Created: {output_path}")
```

## Checklist Before Generating

- [ ] Total segment times add to class duration
- [ ] Every segment has at least one discussion question
- [ ] No instructor notes, facilitation cues, or anticipated responses leaked onto handout
- [ ] Fits on 1–2 pages (prefer 1)
- [ ] Readings for next session included with bridging question
- [ ] Pacing tags (🟢🟡🔴) do NOT appear
- [ ] Unicode characters used for em dashes (\u2014), quotes (\u201c \u201d), and bullets (\u2022)
