# Writing a Strong Introduction & Title (45-minute session)

Quarto Reveal.js deck for **Session 7 – Writing a Strong Introduction & Title**.

- Workshop: *Workshop on AI in Health Research* (NAMS, MGIMS Sevagram)
- When: Day 2, 24 November 2026, 10:30–11:15 (45 min)
- Presenter: Dr Rahul Narang, Dean and Professor & Head, Microbiology, AIIMS Bibinagar
- Methods: "Spot the Problem" and "Title Makeover"

## Timing plan

| Min | Block |
|---|---|
| 0–3 | Hook: read first, written last |
| 3–12 | Anatomy of an Introduction (funnel, CARS, objective, what does not belong) |
| 12–22 | Activity: Spot the Problem |
| 22–27 | Citing in the Introduction |
| 27–32 | Evaluating AI-generated text (naive prompt, reference check, planted fake) |
| 32–42 | Activity: Title Makeover (5 weak titles and a running-example makeover) |
| 42–45 | Take-home and checklist |

## Files

| File | Purpose |
|---|---|
| `index.qmd` / `index.html` | Deck source and self-contained deck (press `S` for speaker view) |
| `Introduction_Title_Session7.pdf` | PDF export (no speaker notes; tabs print as separate pages) |
| `handout.qmd` → `handout.pdf`, `handout.docx` | 2-page handout: flawed Introduction, 5 weak titles, checklist. No answers |
| `ai_demo/intro_prompt_and_output.md` | Exact prompt and raw, unedited AI output |
| `style.css`, `_extensions/` | House style and tabset plugin |

## Render

```bash
quarto render index.qmd
quarto render handout.qmd --to typst   # PDF
quarto render handout.qmd --to docx
```

## What is synthetic

- The running example (312 urinary *E. coli* isolates, Telangana) is synthetic.
- The flawed Introduction, its rewrite, all weak and fixed titles, and the 42-word trial title are written for teaching. Author names in the flawed text are placeholders.
- **Planted fake reference** (slide "Plant one fake, then catch it"): Narayanan & Deshpande, *J Glob Antimicrob Resist* 2023;33:211-9. It is invented, labelled in red, and a PubMed title search found no match.
- The AI demo is **real**: one call to a small Claude model (Haiku), no tools, on 23 Nov 2026. All five references it gave exist in PubMed. Three do not fully support the sentence they are attached to. Support was judged from abstracts, not full texts.

## Verified and not verified

- Verified (fetched): ICMJE Section V (AI use by authors; AI use by reviewers); STROBE item 1a (cross-sectional checklist PDF); CONSORT 2025 item 1a (published checklist table, PMC11996237); the five AI references in PubMed.
- Not verified: Swales' CARS model was confirmed only from secondary guides (the 1990 book was not opened); no ICMR AMRSN report was checked, so none is cited; the "300–500 words" range is a teaching guide, not a rule; journal word limits vary.
