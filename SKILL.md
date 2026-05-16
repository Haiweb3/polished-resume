---
name: polished-resume
description: Generate polished resumes by turning raw candidate materials, old resumes, or structured profile data into a clean HTML resume and exporting it to PDF. Supports 5 visual templates (technical / modern / classic / compact / creative) and 5 industry presets (tech / design / business / academic / marketing). Use when a user asks to create, rewrite, polish, or redesign a resume/CV, especially when visual quality matters more than editable Word output.
---

# Polished Resume

Build resumes with a stable pipeline:

1. Normalize source material into structured resume data.
2. Rewrite content into concise, results-oriented resume copy.
3. Choose a template and industry preset.
4. Render HTML and export to PDF.

## Workflow

### 1. Gather the source material

Accept any of these inputs:

- a filled markdown intake sheet (`references/intake-template.md`)
- an old resume
- scattered notes about experience, projects, education, and skills

Normalize unstructured material into the schema in `references/schema.md` before rendering.

### 2. Pick template and industry

Two independent axes; combine freely.

**Template** (`meta.template`): visual look.

- `technical` — Times serif, blue section headers, dense (default)
- `modern` — sans-serif, minimal, lots of whitespace
- `classic` — Garamond/Georgia serif, B&W, formal
- `compact` — small font, dense, for senior multi-page content
- `creative` — colored hero band, pill section titles

**Industry** (`meta.industry`): skill categories and section order.

- `tech` — languages / frameworks / databases / infrastructure / tools (default)
- `design` — software / specialties / output / methodology / tools
- `business` — tools / methodologies / domains / languages / certifications
- `academic` — research_areas / methods / tools / publications / languages
- `marketing` — channels / content / analytics / platforms / tools

If the user does not state a preference, infer from the role they're applying for and confirm before rendering.

### 3. Build the resume spec

Create a clean intermediate JSON before touching the template.

- Use `references/schema.md` for the target structure.
- Make `meta.template` and `meta.industry` explicit even if defaulted.
- Drop low-signal filler, repeated phrases, and vague self-evaluation.
- Prefer measurable impact, scope, ownership, and technical depth.

### 4. Rewrite for resume quality

Use `references/writing-rules.md`.

Key rules:

- Start bullets with strong verbs.
- Prefer outcome and impact over task lists.
- Keep wording concrete.
- Compress aggressively to protect layout quality.
- When the page gets crowded, cut low-value detail instead of shrinking typography.

### 5. Render the HTML

```bash
python3 scripts/render_resume.py input.json output.html
```

The renderer:

- inlines the chosen template's CSS into one self-contained HTML file
- escapes unsafe HTML
- drops empty sections
- warns (does not fail) on unknown template / industry / language and falls back to defaults

### 6. Export to PDF

```bash
node scripts/export_pdf.js output.html output.pdf
```

The exporter opens the local HTML in headless Chrome and prints to PDF. Set `CHROME_PATH` for non-standard Chrome locations.

### 7. Validate the result

After export:

- check page count
- confirm section hierarchy reads cleanly
- confirm no clipping, overlaps, or orphaned headings
- if needed, tighten copy and re-render

Use the `pdf` skill for deeper rendering review.

## Default section strategy

Each industry has its own default section order. Override the order by changing the data, not the renderer:

- Student / early career: keep `Projects` before `Experience`.
- Mid / senior: keep `Experience` before `Projects` (already the default for `business`, `academic`, `marketing`).

## Industry-specific guidance

- **tech**: emphasize architecture decisions, system constraints, and measurable performance.
- **design**: link to portfolio in `basic.website`; emphasize shipped surfaces and design system contributions.
- **business**: emphasize business outcomes (GMV, conversion, ARR), team scope, and stakeholder management.
- **academic**: highlight publications, advisors, and funding; English is the typical default.
- **marketing**: emphasize channel breadth, campaign outcomes (ROI, GMV, reach), and platform fluency.

## References

Read only what you need:

- `references/schema.md`
- `references/writing-rules.md`
- `references/template-notes.md`
- `references/intake-template.md`

## Scripts and assets

- `scripts/render_resume.py`: render HTML from structured JSON
- `scripts/export_pdf.js`: print HTML to PDF with headless Chrome
- `assets/templates/<name>/template.html` + `style.css`: visual templates
- `assets/sample_resume.json`: minimal tech example
- `assets/samples/<industry>.json`: realistic per-industry examples

## Guardrails

- Do not generate Word-first resumes in this skill.
- Do not treat the HTML template as the source of truth; the JSON spec is.
- Favor layout stability over exhaustive detail.
- Keep the first version visually conservative rather than flashy.
- Never put real personal contact info (phone, email) in committed samples; use placeholder data.
