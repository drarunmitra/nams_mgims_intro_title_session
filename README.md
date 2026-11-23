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
| 22–26 | Citing in the Introduction |
| 26–33 | Evaluating AI-generated text (naive prompt, reference check, nine-run summary, planted fake, using AI safely) |
| 33–42 | Activity: Title Makeover (5 weak titles and a running-example makeover) |
| 42–45 | Take-home and checklist |

## Files

| File | Purpose |
|---|---|
| `index.qmd` / `index.html` | Deck source and self-contained deck (press `S` for speaker view) |
| `Introduction_Title_Session7.pdf` | PDF export (no speaker notes; tabs print as separate pages) |
| `facilitator_guide.html`, `Facilitator_Guide_Session7.pdf` | Facilitator guide: prep checklist, minute-by-minute run of show, answer keys for both activities, how to present the AI demo, what to cut, likely questions, neighbouring sessions, what is verified |
| `handout.qmd` → `handout.pdf`, `handout.docx` | 2-page handout: flawed Introduction, 5 weak titles, checklist. No answers |
| `ai_demo/intro_prompt_and_output.md` | Exact prompt and raw, unedited AI output |
| `style.css`, `_extensions/` | House style and tabset plugin |

## Render

```bash
quarto render index.qmd
quarto render handout.qmd --to typst   # PDF
quarto render handout.qmd --to docx
```

## Revision (23 Nov 2026): literature review
- `docs/literature_review.md` maps each slide claim to a source and a status. Detail: `docs/lit_A_intro_structure.md`, `docs/lit_B_titles_ai.md`.
- Added: ICMJE / STROBE / CONSORT 2025 anchors for the Introduction; published paragraph and length guides (they disagree); real, verified citations in the rewrite; a nine-run AI summary slide; a "Using AI for the Introduction, safely" slide; title-evidence aside. Removed an unsupported claim about CARS.
- Slide count: 34 (including section dividers). Overflow check: every slide checked at 1280x720 with all fragments shown.

## What is synthetic

- The running example (312 urinary *E. coli* isolates, Telangana) is synthetic.
- The flawed Introduction, its rewrite, all weak and fixed titles, and the 42-word trial title are written for teaching. Author names in the flawed text are placeholders. The gap statements in the rewrite are illustrative; its four citations are real.
- **Planted fake reference** (slide "Plant one fake, then catch it"): Narayanan & Deshpande, *J Glob Antimicrob Resist* 2023;33:211-9. It is invented, labelled in red, and a PubMed title search found no match.
- The AI demo is **real**: the same naive prompt, 9 fresh calls (6 Haiku, 3 Opus) on 23 Nov 2026, no tools, raw outputs in `ai_demo/`. `ai_demo/check_refs.py` and `ref_check.csv` check that references exist. 43 of 43 journal references exist in PubMed; 2 cite an ICMR 2022 report I could not open. Support for the claim was judged by title for the "exceeds half" sentence only. Each call was told to answer from memory, so later runs add "verify" notes.

## Verified and not verified

See `docs/literature_review.md`. Not verified: Swales 1990/2004 (secondary sources only), Annesley 2010 and Hartley 2007 text, any ICMR report newer than 2024, full texts of the AI references.
