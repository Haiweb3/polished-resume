---
name: polished-resume
description: Generate polished resumes by turning raw candidate materials, old resumes, or structured profile data into a clean HTML resume and exporting it to PDF. Use when a user asks to create, rewrite, polish, or redesign a resume/CV, especially when visual quality matters more than editable Word output. This skill is appropriate for one-page or concise multi-section resumes, HTML-based resume templates, and HTML-to-PDF export workflows.
---

# Polished Resume

Build resumes with a stable pipeline:

1. Normalize source material into structured resume data.
2. Rewrite content into concise, results-oriented resume copy.
3. Render HTML from a fixed template.
4. Export the HTML to PDF.

## Workflow

### 1. Gather the source material

Accept any of these inputs:

- a filled markdown intake sheet
- an old resume
- scattered notes about experience, projects, education, and skills

Prefer the markdown intake format in `references/intake-template.md` for new work. If the user gives unstructured material, normalize it into the schema in `references/schema.md` before rendering.

### 2. Build the resume spec

Create a clean intermediate JSON object before touching the template.

- Use `references/schema.md` for the target structure.
- Keep only resume-ready content in the final spec.
- Drop low-signal filler, repeated phrases, and vague self-evaluation.
- Prefer measurable impact, scope, ownership, and technical depth.

### 3. Rewrite for resume quality

Use `references/writing-rules.md`.

Key rules:

- Start bullets with strong verbs.
- Prefer outcome and impact over task lists.
- Keep wording concrete.
- Compress aggressively to protect layout quality.
- When the page gets crowded, cut low-value detail instead of shrinking typography too far.

### 4. Render the HTML

Use the provided assets:

- `assets/template.html`
- `assets/base.css`

Write the normalized JSON spec to a file, then run:

```bash
python3 scripts/render_resume.py input.json output.html
```

The renderer:

- injects structured data into the template
- escapes unsafe HTML
- formats lists and section blocks
- supports the first-pass fixed layout used by this skill

### 5. Export to PDF

Use the bundled exporter:

```bash
node scripts/export_pdf.js output.html output.pdf
```

The exporter opens the local HTML file in headless Chrome or Chromium and prints it to PDF. If Chrome is installed in a non-standard location, set `CHROME_PATH` first.

### 6. Validate the result

After export:

- check page count
- confirm section hierarchy reads cleanly
- confirm no clipping, overlaps, or orphaned headings
- if needed, tighten copy and re-render

Use the `pdf` skill if you need deeper rendering review.

## Default section strategy

The default template is optimized for concise technical resumes. Use this order unless the user's material clearly demands a different order:

1. Header
2. Education
3. Skills
4. Projects
5. Experience
6. Awards

If the candidate is experienced, move `Experience` above `Projects`. If the candidate is student-heavy, keep `Projects` early.

## Input guidance

### Preferred input

Ask for a markdown intake sheet based on `references/intake-template.md` when the user is starting from scratch.

### Acceptable fallback inputs

- plain text old resume
- copied LinkedIn-style profile
- project notes and experience bullets

Normalize all of them into the schema before rendering.

## References

Read only what you need:

- `references/schema.md`
- `references/writing-rules.md`
- `references/template-notes.md`
- `references/intake-template.md`

## Scripts and assets

- `scripts/render_resume.py`: render HTML from structured JSON
- `scripts/export_pdf.js`: print local HTML to PDF with Chrome or Chromium
- `assets/template.html`: fixed HTML shell
- `assets/base.css`: typography and layout rules
- `assets/sample_resume.json`: minimal example input

## Guardrails

- Do not generate Word-first resumes in this skill.
- Do not treat the HTML template as the source of truth; the JSON spec is the source of truth.
- Favor layout stability over exhaustive detail.
- Keep the first version visually polished and conservative rather than flashy.
